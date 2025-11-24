# app/services/template_services.py
from app.database import get_connection


# ------------------------------------------------------------
# CREATE TEMPLATE
# ------------------------------------------------------------
def create_workout_template(user_id: int, name: str, workout_type: str) -> int:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO workout_templates (user_id, template_name, workout_type)
        VALUES (?, ?, ?)
    """, (user_id, name, workout_type))

    template_id = cur.lastrowid
    conn.commit()
    conn.close()
    return template_id


# ------------------------------------------------------------
# ADD MULTIPLE EXERCISES TO TEMPLATE
# ------------------------------------------------------------
def add_exercises_to_template(template_id, exercise_ids, sets, reps, weights):
    conn = get_connection()
    cur = conn.cursor()

    for i in range(len(exercise_ids)):
        cur.execute("""
            INSERT INTO template_exercises
            (template_id, exercise_lib_id, default_sets,
             default_reps, default_weight)
            VALUES (?, ?, ?, ?, ?)
        """, (
            template_id,
            exercise_ids[i],
            sets[i] or None,
            reps[i] or None,
            weights[i] or None
        ))

    conn.commit()
    conn.close()


# ------------------------------------------------------------
# GET TEMPLATE HEADER
# ------------------------------------------------------------
def get_template_header(template_id: int, user_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT template_id, template_name, workout_type
        FROM workout_templates
        WHERE template_id = ? AND user_id = ?
    """, (template_id, user_id))

    row = cur.fetchone()
    conn.close()
    return row


# ------------------------------------------------------------
# GET TEMPLATE EXERCISES
# ------------------------------------------------------------
def get_template_exercises(template_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT template_exercise_id, exercise_lib_id,
               exercise_name, muscle_id,
               default_sets, default_reps, default_weight
        FROM template_exercises
        WHERE template_id = ?
        ORDER BY template_exercise_id ASC
    """, (template_id,))

    rows = cur.fetchall()
    conn.close()
    return rows


# ------------------------------------------------------------
# DELETE TEMPLATE
# ------------------------------------------------------------
def delete_template_by_id(template_id: int, user_id: int):
    conn = get_connection()
    cur = conn.cursor()

    # güvenlik: template kullanıcının mı?
    cur.execute("""
        SELECT template_id
        FROM workout_templates
        WHERE template_id = ? AND user_id = ?
    """, (template_id, user_id))

    if not cur.fetchone():
        conn.close()
        return False

    # exercises → cascade
    cur.execute("DELETE FROM template_exercises WHERE template_id = ?", (template_id,))
    cur.execute("DELETE FROM workout_templates WHERE template_id = ?", (template_id,))

    conn.commit()
    conn.close()
    return True
