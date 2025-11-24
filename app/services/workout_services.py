from app.database import get_connection
from flask import redirect, url_for

def create_workout_from_template(user_id, template_id, tpl_name, workout_type, date):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO workouts (user_id, workout_date, workout_type, notes)
        VALUES (?, ?, ?, ?)
    """, (user_id, date, workout_type, f"From template: {tpl_name}"))

    workout_id = cur.lastrowid

    cur.execute("""
        SELECT exercise_lib_id, exercise_name, muscle_id,
               default_sets, default_reps, default_weight
        FROM template_exercises
        WHERE template_id = ?
    """, (template_id,))

    for r in cur.fetchall():
        cur.execute("""
            INSERT INTO exercises
            (workout_id, exercise_lib_id, exercise_name, muscle_id, sets, reps, weight_kg)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            workout_id,
            r["exercise_lib_id"],
            r["exercise_name"],
            r["muscle_id"],
            r["default_sets"],
            r["default_reps"],
            r["default_weight"]
        ))

    conn.commit()
    conn.close()

    return redirect(url_for("main.workout_detail", workout_id=workout_id))
