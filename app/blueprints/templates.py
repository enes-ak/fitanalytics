# app/blueprints/templates.py

from flask import render_template, request, redirect, url_for, session
from . import main
from app.database import get_connection
from app.utils.datetime import today_db
from app.data.popular_templates import POPULAR_TEMPLATES

# Service katmanı
from app.services.workout_services import create_workout_from_template
from app.services.template_services import (
    create_workout_template,
    get_template_header,
    get_template_exercises,
    add_exercises_to_template,
    delete_template_by_id,
    get_active_plan,
    save_active_plan,
    get_plan_muscle_stats,
)

# -------------------------------------------------------------
# TEMPLATE LIST
# -------------------------------------------------------------
@main.route("/my-templates")
def my_templates():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT wt.template_id, wt.template_name, wt.workout_type,
               COUNT(te.template_exercise_id) AS count_ex,
               COALESCE(SUM(te.default_sets * te.default_reps * te.default_weight), 0) AS volume
        FROM workout_templates wt
        LEFT JOIN template_exercises te ON te.template_id = wt.template_id
        WHERE wt.user_id = ?
        GROUP BY wt.template_id
        ORDER BY wt.template_name ASC
    """, (user_id,))

    template_rows = cur.fetchall()
    conn.close()

    templates = [dict(row) for row in template_rows]
    active_plan = [dict(row) for row in get_active_plan(user_id)]
    plan_stats = get_plan_muscle_stats(user_id)

    return render_template(
        "templates.html",
        templates=templates,
        active_plan=active_plan,
        plan_stats=plan_stats,
    )


# -------------------------------------------------------------
# TEMPLATE DETAIL
# -------------------------------------------------------------
@main.route("/template/<int:template_id>")
def template_detail(template_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]

    template = get_template_header(template_id, user_id)
    if not template:
        return "Template not found", 404

    exercises = get_template_exercises(template_id)

    return render_template(
        "template_detail.html",
        template=template,
        exercises=exercises
    )


# -------------------------------------------------------------
# ADD TEMPLATE
# -------------------------------------------------------------
@main.route("/add-template", methods=["GET", "POST"])
def add_template():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    if request.method == "POST":
        user_id = session["user_id"]
        name = request.form.get("template_name")
        workout_type = request.form.get("workout_type")

        # Template oluştur
        tpl_id = create_workout_template(user_id, name, workout_type)

        # Exercise listelerini topla
        exercise_ids = request.form.getlist("exercise_lib_id")
        sets = request.form.getlist("sets")
        reps = request.form.getlist("reps")
        weights = request.form.getlist("weight")

        # Template içine exercises ekle
        add_exercises_to_template(
            tpl_id,
            exercise_ids=exercise_ids,
            sets=sets,
            reps=reps,
            weights=weights
        )

        return redirect(url_for("main.my_templates"))

    return render_template("add_template.html", popular_templates=POPULAR_TEMPLATES)


# -------------------------------------------------------------
# ADD TEMPLATE FROM PRESET
# -------------------------------------------------------------
@main.route("/add-template/preset", methods=["POST"])
def add_template_from_preset():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    slug = request.form.get("preset_slug")
    preset = next((tpl for tpl in POPULAR_TEMPLATES if tpl["slug"] == slug), None)
    if not preset:
        return redirect(url_for("main.add_template"))

    user_id = session["user_id"]
    custom_name = request.form.get("custom_name") or preset["name"]

    template_id = create_workout_template(user_id, custom_name, preset["workout_type"])

    exercise_ids = [str(ex["exercise_lib_id"]) for ex in preset["exercises"]]
    sets = [str(ex.get("sets") or "") for ex in preset["exercises"]]
    reps = [str(ex.get("reps") or "") for ex in preset["exercises"]]
    weights = [str(ex.get("weight") or "") for ex in preset["exercises"]]

    add_exercises_to_template(
        template_id,
        exercise_ids=exercise_ids,
        sets=sets,
        reps=reps,
        weights=weights,
    )

    return redirect(url_for("main.template_detail", template_id=template_id))


# -------------------------------------------------------------
# UPDATE ACTIVE WEEKLY PLAN
# -------------------------------------------------------------
@main.route("/my-templates/active-plan", methods=["POST"])
def update_active_plan():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]
    template_ids = []
    for raw in request.form.getlist("plan_template_id[]"):
        raw = (raw or "").strip()
        if raw.isdigit():
            template_ids.append(int(raw))

    save_active_plan(user_id, template_ids)
    return redirect(url_for("main.my_templates"))


# -------------------------------------------------------------
# USE TEMPLATE — STEP 1 (check duplicate workout on same day)
# -------------------------------------------------------------
@main.route("/use-template/<int:template_id>")
def use_template(template_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]
    today = today_db()

    tpl = get_template_header(template_id, user_id)
    if not tpl:
        return "Template not found", 404

    tpl_name = tpl["template_name"]
    workout_type = tpl["workout_type"]

    # Check if today's workout already exists
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT workout_id
        FROM workouts
        WHERE user_id = ? AND workout_date = ?
    """, (user_id, today))

    existing = cur.fetchone()
    conn.close()

    if existing:
        # Çakışma var → kullanıcıya sor
        return render_template(
            "confirm_repeat_workout.html",
            template_id=template_id,
            template_name=tpl_name,
            workout_type=workout_type,
            date=today
        )

    # Çakışma yok → direkt oluştur
    return create_workout_from_template(
        user_id,
        template_id,
        tpl_name,
        workout_type,
        today
    )


# -------------------------------------------------------------
# USE TEMPLATE — STEP 2 (user confirms overwrite)
# -------------------------------------------------------------
@main.route("/confirm-use-template", methods=["POST"])
def confirm_use_template():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]

    template_id = int(request.form.get("template_id"))
    tpl_name = request.form.get("template_name")
    workout_type = request.form.get("workout_type")
    date = request.form.get("date")

    return create_workout_from_template(
        user_id,
        template_id,
        tpl_name,
        workout_type,
        date
    )


# -------------------------------------------------------------
# DELETE TEMPLATE
# -------------------------------------------------------------
@main.route("/template/<int:template_id>/delete", methods=["POST"])
def delete_template(template_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    delete_template_by_id(
        template_id=template_id,
        user_id=session["user_id"]
    )

    return redirect(url_for("main.my_templates"))
