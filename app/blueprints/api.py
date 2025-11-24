from flask import request, jsonify
from . import main
from app.database import get_connection
from app.utils.normalization import normalize_text

@main.route("/api/search_exercises")
def api_search_exercises():
    raw_q = request.args.get("q", "")
    q = normalize_text(raw_q)

    if len(q) < 2:
        return jsonify([])

    conn = get_connection()
    cur = conn.cursor()

    # --- A: Kas alias eşleşmesi
    cur.execute("""
        SELECT m.muscle_id, m.code, m.name_en, m.name_tr
        FROM muscle_aliases ma
        JOIN muscles m ON ma.muscle_id = m.muscle_id
        WHERE lower(ma.alias_text) LIKE ?
    """, (f"%{q}%",))
    alias_rows = cur.fetchall()
    muscle_ids = [r["muscle_id"] for r in alias_rows]

    # --- B: Hareket adı eşleşmesi
    cur.execute("""
        SELECT
            el.exercise_lib_id,
            el.slug,
            el.name_en,
            el.name_tr,
            el.equipment,
            el.difficulty,
            m.muscle_id,
            m.code AS muscle_code,
            m.name_en AS muscle_name_en,
            m.name_tr AS muscle_name_tr
        FROM exercise_library el
        JOIN muscles m ON el.muscle_id = m.muscle_id
        WHERE lower(el.name_en) LIKE ?
           OR lower(el.name_tr) LIKE ?
    """, (f"%{q}%", f"%{q}%"))
    name_rows = cur.fetchall()

    # --- C: Kas bulunduysa → tüm hareketleri getir
    muscle_rows = []
    if muscle_ids:
        placeholders = ",".join(["?"] * len(muscle_ids))
        cur.execute(f"""
            SELECT
                el.exercise_lib_id,
                el.slug,
                el.name_en,
                el.name_tr,
                el.equipment,
                el.difficulty,
                m.muscle_id,
                m.code AS muscle_code,
                m.name_en AS muscle_name_en,
                m.name_tr AS muscle_name_tr
            FROM exercise_library el
            JOIN muscles m ON el.muscle_id = m.muscle_id
            WHERE el.muscle_id IN ({placeholders})
        """, muscle_ids)
        muscle_rows = cur.fetchall()

    conn.close()

    combined = {}

    def absorb(rows, priority):
        for r in rows:
            eid = r["exercise_lib_id"]
            if eid not in combined or priority < combined[eid]["priority"]:
                combined[eid] = {
                    "exercise_lib_id": eid,
                    "slug": r["slug"],
                    "name_en": r["name_en"],
                    "name_tr": r["name_tr"],
                    "equipment": r["equipment"],
                    "difficulty": r["difficulty"],
                    "muscle_id": r["muscle_id"],
                    "muscle_code": r["muscle_code"],
                    "muscle_name_en": r["muscle_name_en"],
                    "muscle_name_tr": r["muscle_name_tr"],
                    "priority": priority
                }

    absorb(muscle_rows, 0)
    absorb(name_rows, 1)

    grouped = {}

    for r in combined.values():
        mc = r["muscle_code"]
        if mc not in grouped:
            grouped[mc] = {
                "muscle_code": mc,
                "muscle_name_en": r["muscle_name_en"],
                "muscle_name_tr": r["muscle_name_tr"],
                "exercises": []
            }
        grouped[mc]["exercises"].append({
            "exercise_lib_id": r["exercise_lib_id"],
            "slug": r["slug"],
            "name_en": r["name_en"],
            "name_tr": r["name_tr"],
            "equipment": r["equipment"],
            "difficulty": r["difficulty"]
        })

    for bucket in grouped.values():
        bucket["exercises"].sort(key=lambda x: x["name_en"])

    return jsonify(list(grouped.values()))
