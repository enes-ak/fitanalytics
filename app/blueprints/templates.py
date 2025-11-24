# app/blueprints/templates.py

from flask import render_template, request, redirect, url_for, session
from . import main
from app.database import get_connection
from app.utils.datetime import today_db

# Service katmanı
from app.services.workout_services import create_workout_from_template
from app.services.template_services import (
    create_workout_template,
    get_template_header,
    get_template_exercises,
    add_exercises_to_template,
    delete_template_by_id
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

    templates = cur.fetchall()
    conn.close()

    return render_template("templates.html", templates=templates)


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

    return render_template("add_template.html")


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
