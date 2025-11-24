# app/blueprints/templates.py
from flask import render_template, request, redirect, url_for, session
from . import main
from app.database import get_connection
from app.utils.datetime import today_db
from app.services.workout_services import create_workout_from_template


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
# ADD TEMPLATE  (Layout içinde ihtiyaç var → endpoint geri geldi)
# -------------------------------------------------------------
@main.route("/add-template", methods=["GET", "POST"])
def add_template():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    if request.method == "POST":
        user_id = session["user_id"]
        name = request.form.get("template_name")
        workout_type = request.form.get("workout_type")

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO workout_templates (user_id, template_name, workout_type)
            VALUES (?, ?, ?)
        """, (user_id, name, workout_type))
        tpl_id = cur.lastrowid

        ex_ids = request.form.getlist("exercise_lib_id")
        sets = request.form.getlist("sets")
        reps = request.form.getlist("reps")
        weight = request.form.getlist("weight")

        for exid, s, r, w in zip(ex_ids, sets, reps, weight):
            if not exid:
                continue

            cur.execute("SELECT muscle_id, name_en FROM exercise_library WHERE exercise_lib_id = ?", (exid,))
            row = cur.fetchone()
            if not row:
                continue

            cur.execute("""
                INSERT INTO template_exercises
                (template_id, exercise_lib_id, exercise_name, muscle_id, default_sets, default_reps, default_weight)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (tpl_id, exid, row["name_en"], row["muscle_id"], s or None, r or None, w or None))

        conn.commit()
        conn.close()

        return redirect(url_for("main.my_templates"))

    return render_template("add_template.html")


# -------------------------------------------------------------
# TEMPLATE DETAIL
# -------------------------------------------------------------
@main.route("/template/<int:template_id>")
def template_detail(template_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT template_id, template_name, workout_type
        FROM workout_templates
        WHERE template_id = ? AND user_id = ?
    """, (template_id, session["user_id"]))
    template = cur.fetchone()

    if not template:
        conn.close()
        return "Template not found", 404

    cur.execute("""
        SELECT te.exercise_name, m.name_tr AS muscle,
               te.default_sets, te.default_reps, te.default_weight
        FROM template_exercises te
        JOIN muscles m ON m.muscle_id = te.muscle_id
        WHERE te.template_id = ?
    """, (template_id,))
    exercises = cur.fetchall()

    conn.close()

    return render_template("template_detail.html", template=template, exercises=exercises)


# -------------------------------------------------------------
# USE TEMPLATE — FIRST CHECK (if workout exists)
# -------------------------------------------------------------
@main.route("/use-template/<int:template_id>")
def use_template(template_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]
    today = today_db()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT template_name, workout_type
        FROM workout_templates
        WHERE template_id = ? AND user_id = ?
    """, (template_id, user_id))
    tpl = cur.fetchone()
    if not tpl:
        conn.close()
        return "Template not found", 404

    tpl_name, workout_type = tpl

    # BU GÜNDE VAR MI?
    cur.execute("SELECT workout_id FROM workouts WHERE user_id = ? AND workout_date = ?", (user_id, today))
    existing = cur.fetchone()
    conn.close()

    if existing:
        # doğrulama ekranı
        return render_template(
            "confirm_repeat_workout.html",
            template_id=template_id,
            template_name=tpl_name,
            workout_type=workout_type,
            date=today
        )

    # hiç yok → direk oluştur
    return create_workout_from_template(user_id, template_id, tpl_name, workout_type, today)


# -------------------------------------------------------------
# CONFIRM ADD SECOND WORKOUT (POST)
# -------------------------------------------------------------
@main.route("/confirm-use-template", methods=["POST"])
def confirm_use_template():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    # Tüm alanları güvenli şekilde al
    template_id = request.form.get("template_id")
    tpl_name = request.form.get("template_name")
    workout_type = request.form.get("workout_type")
    date = request.form.get("date")

    # Eksik parametre varsa güvenli fallback
    if not template_id or not workout_type or not date:
        return "Missing template data", 400

    # INT cast burada artık güvenli
    template_id = int(template_id)

    return create_workout_from_template(
        session["user_id"],
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

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT template_id
        FROM workout_templates
        WHERE template_id = ? AND user_id = ?
    """, (template_id, session["user_id"]))
    if not cur.fetchone():
        conn.close()
        return "Not found", 404

    cur.execute("DELETE FROM template_exercises WHERE template_id = ?", (template_id,))
    cur.execute("DELETE FROM workout_templates WHERE template_id = ?", (template_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("main.my_templates"))
