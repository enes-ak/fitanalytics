# app/services/template_services.py
from app.database import get_connection

PLAN_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS active_weekly_plan (
    plan_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    plan_slot   INTEGER NOT NULL,
    template_id INTEGER NOT NULL,
    UNIQUE(user_id, plan_slot),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (template_id) REFERENCES workout_templates(template_id)
)
"""


def ensure_plan_table(conn):
    conn.execute(PLAN_TABLE_SQL)


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
        lib_id = exercise_ids[i]

        # Boş satırı atla
        if not lib_id or str(lib_id).strip() == "":
            continue

        cur.execute("""
            SELECT name_tr AS exercise_name, muscle_id
            FROM exercise_library
            WHERE exercise_lib_id = ?
        """, (lib_id,))

        row = cur.fetchone()
        if row is None:
            # Hatalı ID gelmişse de atla
            continue

        exercise_name = row["exercise_name"]
        muscle_id = row["muscle_id"]

        cur.execute("""
            INSERT INTO template_exercises
            (template_id, exercise_lib_id, exercise_name, muscle_id,
             default_sets, default_reps, default_weight)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            template_id,
            lib_id,
            exercise_name,
            muscle_id,
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
        SELECT te.template_exercise_id, te.exercise_lib_id,
               te.exercise_name, te.muscle_id,
               m.name_tr AS muscle_name,
               te.default_sets, te.default_reps, te.default_weight
        FROM template_exercises te
        LEFT JOIN muscles m ON m.muscle_id = te.muscle_id
        WHERE te.template_id = ?
        ORDER BY te.template_exercise_id ASC
    """, (template_id,))

    rows = cur.fetchall()
    conn.close()
    return rows


# ------------------------------------------------------------
# ACTIVE WEEKLY PLAN HELPERS
# ------------------------------------------------------------
def get_active_plan(user_id: int):
    conn = get_connection()
    ensure_plan_table(conn)
    cur = conn.cursor()

    cur.execute("""
        SELECT awp.plan_slot, wt.template_id, wt.template_name, wt.workout_type
        FROM active_weekly_plan awp
        JOIN workout_templates wt ON wt.template_id = awp.template_id
        WHERE awp.user_id = ?
        ORDER BY awp.plan_slot ASC
    """, (user_id,))

    rows = cur.fetchall()
    conn.close()
    return rows


def save_active_plan(user_id: int, template_ids):
    conn = get_connection()
    ensure_plan_table(conn)
    cur = conn.cursor()

    cur.execute("DELETE FROM active_weekly_plan WHERE user_id = ?", (user_id,))

    slot = 1
    for template_id in template_ids:
        cur.execute(
            """
            INSERT INTO active_weekly_plan (user_id, plan_slot, template_id)
            VALUES (?, ?, ?)
            """,
            (user_id, slot, template_id),
        )
        slot += 1

    conn.commit()
    conn.close()


def get_plan_muscle_stats(user_id: int):
    conn = get_connection()
    ensure_plan_table(conn)
    cur = conn.cursor()

    cur.execute("""
        SELECT m.name_tr AS muscle_name,
               SUM(
                   COALESCE(te.default_sets, 0) *
                   COALESCE(te.default_reps, 0) *
                   COALESCE(te.default_weight, 0)
               ) AS total_volume
        FROM active_weekly_plan awp
        JOIN template_exercises te ON te.template_id = awp.template_id
        JOIN muscles m ON m.muscle_id = te.muscle_id
        WHERE awp.user_id = ?
        GROUP BY m.muscle_id
        ORDER BY total_volume DESC
    """, (user_id,))

    stats = [
        {
            "muscle": row["muscle_name"],
            "total_volume": float(row["total_volume"] or 0),
        }
        for row in cur.fetchall()
    ]

    conn.close()
    return stats


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
