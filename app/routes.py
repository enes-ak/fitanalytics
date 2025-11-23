# app/routes.py

from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, jsonify, current_app
)
from werkzeug.security import check_password_hash
from .database import get_connection
from scripts.utils.datetime import get_today_date
from scripts.utils.normalization import normalize_text

main = Blueprint("main", __name__)


# ============================================================
# API: EXERCISE AUTOCOMPLETE
# ============================================================
@main.route("/api/search_exercises")
def api_search_exercises():
    """
    Unified autocomplete:
    Kullanıcı 'tri' yazdı → hareketlerde arar.
    Kullanıcı 'chest' yazdı → muscle_aliases → tüm ilgili hareketleri döner.
    Sonuç: muscle_code altında gruplanmiş exercise listesi (canonical).
    """
    raw_q = request.args.get("q", "")
    q = normalize_text(raw_q)
    if len(q) < 2:
        return jsonify([])

    conn = get_connection()
    cur = conn.cursor()

    # ---- A) Kullanıcı kas adı yazmış olabilir → muscle_aliases lookup
    cur.execute(
        """
        SELECT m.muscle_id, m.code, m.name_en, m.name_tr
        FROM muscle_aliases ma
        JOIN muscles m ON ma.muscle_id = m.muscle_id
        WHERE lower(ma.alias_text) LIKE ?
        """,
        (f"%{q}%",),
    )
    muscle_alias_rows = cur.fetchall()
    muscle_ids = [r["muscle_id"] for r in muscle_alias_rows]

    # ---- B) Kullanıcı hareket adı yazmış olabilir → exercise_library lookup
    cur.execute(
        """
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
        """,
        (f"%{q}%", f"%{q}%"),
    )
    name_matches = cur.fetchall()

    # ---- C) Eğer kas bulunduysa → o kasa ait TÜM hareketler
    muscle_group_rows = []
    if muscle_ids:
        placeholders = ",".join(["?"] * len(muscle_ids))
        cur.execute(
            f"""
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
            """,
            muscle_ids,
        )
        muscle_group_rows = cur.fetchall()

    conn.close()

    # ---- D) Sonuçları birleştir (priority: muscle_match → 0, text_match → 1)
    combined = {}

    def absorb(rows, priority):
        for r in rows:
            ex_id = r["exercise_lib_id"]
            if ex_id not in combined or priority < combined[ex_id]["priority"]:
                combined[ex_id] = {
                    "exercise_lib_id": ex_id,
                    "slug": r["slug"],
                    "name_en": r["name_en"],
                    "name_tr": r["name_tr"],
                    "equipment": r["equipment"],
                    "difficulty": r["difficulty"],
                    "muscle_id": r["muscle_id"],
                    "muscle_code": r["muscle_code"],
                    "muscle_name_en": r["muscle_name_en"],
                    "muscle_name_tr": r["muscle_name_tr"],
                    "priority": priority,
                }

    absorb(muscle_group_rows, 0)
    absorb(name_matches, 1)

    # ---- E) Kas koduna göre grupla
    grouped = {}
    for r in combined.values():
        code = r["muscle_code"]
        if code not in grouped:
            grouped[code] = {
                "muscle_code": code,
                "muscle_name_en": r["muscle_name_en"],
                "muscle_name_tr": r["muscle_name_tr"],
                "exercises": []
            }
        grouped[code]["exercises"].append({
            "exercise_lib_id": r["exercise_lib_id"],
            "slug": r["slug"],
            "name_en": r["name_en"],
            "name_tr": r["name_tr"],
            "equipment": r["equipment"],
            "difficulty": r["difficulty"],
        })

    # alfabetik sırala
    for bucket in grouped.values():
        bucket["exercises"].sort(key=lambda x: x["name_en"])

    return jsonify(list(grouped.values()))


# ============================================================
# LOGIN / LOGOUT
# ============================================================
@main.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))

    error = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT user_id, name, password_hash FROM users WHERE email = ?",
            (email,),
        )
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["user_id"]
            session["user_name"] = user["name"]
            return redirect(url_for("main.dashboard"))
        else:
            translations = current_app.config["LANGUAGES"][
                session.get("language", "tr")
            ]
            error = translations["login_error_invalid"]

    return render_template("login.html", error=error)


@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))


# ============================================================
# LANGUAGE SWITCHER
# ============================================================
@main.route("/set-language", methods=["POST"])
def set_language():
    selected = request.form.get("language", "tr")
    if selected not in current_app.config["LANGUAGES"]:
        selected = "tr"

    session["language"] = selected
    return redirect(request.referrer or url_for("main.dashboard"))


# ============================================================
# DASHBOARD
# ============================================================
@main.route("/")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]
    conn = get_connection()
    cur = conn.cursor()

    # -----------------------------------------------------
    # A) TOPLAM WORKOUT SAYISI
    # -----------------------------------------------------
    cur.execute("SELECT COUNT(*) FROM workouts WHERE user_id = ?", (user_id,))
    total_workouts = cur.fetchone()[0]

    # -----------------------------------------------------
    # B) TOPLAM VOLUME
    # -----------------------------------------------------
    cur.execute("""
        SELECT SUM(e.sets * e.reps * e.weight_kg)
        FROM exercises e
        JOIN workouts w ON w.workout_id = e.workout_id
        WHERE w.user_id = ?
    """, (user_id,))
    total_volume = cur.fetchone()[0] or 0

    # -----------------------------------------------------
    # C) KAS BAZLI İSTATİSTİKLER (YENİ ŞEMA)
    # -----------------------------------------------------
    cur.execute("""
        SELECT 
            m.name_tr AS muscle_name,
            AVG(e.sets * e.reps * e.weight_kg) AS avg_volume,
            AVG(e.weight_kg) AS avg_weight
        FROM exercises e
        JOIN muscles m ON m.muscle_id = e.muscle_id
        JOIN workouts w ON w.workout_id = e.workout_id
        WHERE w.user_id = ?
        GROUP BY m.muscle_id
        ORDER BY avg_volume DESC
    """, (user_id,))

    raw_stats = cur.fetchall()

    # JSON için dönüştür
    muscle_stats = [
        {
            "muscle": row["muscle_name"],
            "avg_volume": float(row["avg_volume"] or 0),
            "avg_weight": float(row["avg_weight"] or 0),
        }
        for row in raw_stats
    ]

    muscle_labels = [row["muscle_name"] for row in raw_stats]
    muscle_volumes = [float(row["avg_volume"] or 0) for row in raw_stats]

    # -----------------------------------------------------
    # D) SON WORKOUT TARİHİ
    # -----------------------------------------------------
    cur.execute("""
        SELECT workout_date
        FROM workouts
        WHERE user_id = ?
        ORDER BY workout_date DESC
        LIMIT 1
    """, (user_id,))
    last_row = cur.fetchone()
    last_date = last_row["workout_date"] if last_row else None

    conn.close()

    return render_template(
        "dashboard.html",
        total_workouts=total_workouts,
        total_volume=total_volume,
        muscle_stats=muscle_stats,
        muscle_labels=muscle_labels,
        muscle_volumes=muscle_volumes,
        last_workout_date=last_date
    )


# ============================================================
# WORKOUT HISTORY (DATE LIST)
# ============================================================
@main.route("/history")
def history():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]

    conn = get_connection()
    cur = conn.cursor()

    # tarihler
    cur.execute(
        """
        SELECT DISTINCT workout_date
        FROM workouts
        WHERE user_id = ?
        ORDER BY workout_date DESC
        """,
        (user_id,),
    )
    dates = [r["workout_date"] for r in cur.fetchall()]

    selected = request.args.get("date", dates[0] if dates else None)

    exercises = []
    summary = []

    if selected:
        cur.execute(
            """
            SELECT e.exercise_name, m.name_tr AS muscle, e.sets, e.reps, e.weight_kg
            FROM exercises e
            JOIN muscles m ON m.muscle_id = e.muscle_id
            JOIN workouts w ON w.workout_id = e.workout_id
            WHERE w.user_id = ? AND w.workout_date = ?
            """,
            (user_id, selected),
        )
        exercises = cur.fetchall()

        cur.execute(
            """
            SELECT m.name_tr AS muscle,
                   AVG(e.sets * e.reps * e.weight_kg) AS avg_volume,
                   AVG(e.weight_kg) AS avg_weight
            FROM exercises e
            JOIN muscles m ON e.muscle_id = m.muscle_id
            JOIN workouts w ON w.workout_id = e.workout_id
            WHERE w.user_id = ? AND w.workout_date = ?
            GROUP BY m.muscle_id
            """,
            (user_id, selected),
        )
        summary = cur.fetchall()

    conn.close()

    return render_template(
        "history.html",
        dates=dates,
        selected_date=selected,
        exercises=exercises,
        summary=summary,
    )


# ============================================================
# TEMPLATE LIST
# ============================================================
@main.route("/my-templates")
def my_templates():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            wt.template_id,
            wt.template_name,
            wt.workout_type,
            COUNT(te.template_exercise_id) AS count_ex,
            COALESCE(SUM(te.default_sets * te.default_reps * te.default_weight), 0) AS volume
        FROM workout_templates wt
        LEFT JOIN template_exercises te ON te.template_id = wt.template_id
        WHERE wt.user_id = ?
        GROUP BY wt.template_id
        ORDER BY wt.template_name ASC
        """,
        (user_id,),
    )
    templates = cur.fetchall()
    conn.close()

    return render_template("templates.html", templates=templates)


# ============================================================
# TEMPLATE DETAIL
# ============================================================
@main.route("/template/<int:template_id>")
def template_detail(template_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT template_id, template_name, workout_type FROM workout_templates WHERE template_id = ? AND user_id = ?",
        (template_id, session["user_id"]),
    )
    template = cur.fetchone()

    if not template:
        conn.close()
        return "Template not found", 404

    cur.execute(
        """
        SELECT
            te.exercise_name,
            m.name_tr AS muscle,
            te.default_sets,
            te.default_reps,
            te.default_weight
        FROM template_exercises te
        JOIN muscles m ON m.muscle_id = te.muscle_id
        WHERE te.template_id = ?
        """,
        (template_id,),
    )
    ex_list = cur.fetchall()

    conn.close()

    return render_template("template_detail.html", template=template, exercises=ex_list)


# ============================================================
# CREATE TEMPLATE
# ============================================================
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

        # template kaydet
        cur.execute(
            """
            INSERT INTO workout_templates (user_id, template_name, workout_type)
            VALUES (?, ?, ?)
            """,
            (user_id, name, workout_type),
        )
        tpl_id = cur.lastrowid

        # hareketler
        exercise_ids = request.form.getlist("exercise_lib_id")
        sets_list = request.form.getlist("sets")
        reps_list = request.form.getlist("reps")
        weight_list = request.form.getlist("weight")

        for ex_lib_id, sets, reps, weight in zip(
            exercise_ids, sets_list, reps_list, weight_list
        ):
            if not ex_lib_id:
                continue

            # exercise_library → doğru muscle_id
            cur.execute(
                "SELECT muscle_id, name_en FROM exercise_library WHERE exercise_lib_id = ?",
                (ex_lib_id,),
            )
            row = cur.fetchone()
            if not row:
                continue

            muscle_id = row["muscle_id"]
            exercise_name = row["name_en"]

            cur.execute(
                """
                INSERT INTO template_exercises
                    (template_id, exercise_lib_id, exercise_name, muscle_id, default_sets, default_reps, default_weight)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (tpl_id, ex_lib_id, exercise_name, muscle_id, sets or None, reps or None, weight or None),
            )

        conn.commit()
        conn.close()
        return redirect(url_for("main.my_templates"))

    return render_template("add_template.html")


# ============================================================
# USE TEMPLATE → CREATE WORKOUT TODAY
# ============================================================
@main.route("/use-template/<int:template_id>")
def use_template(template_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]
    
    today = get_today_date()
    conn = get_connection()
    cur = conn.cursor()

    # template info
    cur.execute(
        "SELECT template_name, workout_type FROM workout_templates WHERE template_id = ? AND user_id = ?",
        (template_id, user_id),
    )
    tpl = cur.fetchone()
    if not tpl:
        conn.close()
        return "Template not found", 404

    tpl_name, workout_type = tpl

    # workout oluştur
    cur.execute(
        """
        INSERT INTO workouts (user_id, workout_date, workout_type, notes)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, today, workout_type, f"From template: {tpl_name}"),
    )
    workout_id = cur.lastrowid

    # hareketler → exercises tablosuna
    cur.execute(
        """
        SELECT exercise_lib_id, exercise_name, muscle_id,
               default_sets, default_reps, default_weight
        FROM template_exercises
        WHERE template_id = ?
        """,
        (template_id,),
    )

    for r in cur.fetchall():
        cur.execute(
            """
            INSERT INTO exercises
                (workout_id, exercise_lib_id, exercise_name, muscle_id, sets, reps, weight_kg)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                workout_id,
                r["exercise_lib_id"],
                r["exercise_name"],
                r["muscle_id"],
                r["default_sets"],
                r["default_reps"],
                r["default_weight"],
            ),
        )

    conn.commit()
    conn.close()

    return redirect(url_for("main.workout_detail", workout_id=workout_id))


# ============================================================
# WORKOUT DETAIL
# ============================================================
@main.route("/workout/<int:workout_id>")
def workout_detail(workout_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT workout_id, workout_date, workout_type, notes FROM workouts WHERE workout_id = ?",
        (workout_id,),
    )
    workout = cur.fetchone()

    cur.execute(
        """
        SELECT e.exercise_id,
               e.exercise_name,
               m.name_tr AS muscle,
               e.sets, e.reps, e.weight_kg
        FROM exercises e
        JOIN muscles m ON m.muscle_id = e.muscle_id
        WHERE e.workout_id = ?
        ORDER BY e.exercise_id ASC
        """,
        (workout_id,),
    )
    items = cur.fetchall()

    conn.close()

    return render_template("workout_detail.html", workout=workout, exercises=items)


# ============================================================
# DELETE EXERCISE
# ============================================================
@main.route("/exercise/<int:exercise_id>/delete", methods=["POST"])
def delete_exercise(exercise_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT workout_id FROM exercises WHERE exercise_id = ?", (exercise_id,))
    r = cur.fetchone()
    if not r:
        conn.close()
        return "Not found", 404

    workout_id = r["workout_id"]

    cur.execute("DELETE FROM exercises WHERE exercise_id = ?", (exercise_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("main.workout_detail", workout_id=workout_id))


# ============================================================
# EDIT EXERCISE
# ============================================================
@main.route("/exercise/<int:exercise_id>/edit", methods=["POST"])
def edit_exercise(exercise_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    sets = request.form.get("sets")
    reps = request.form.get("reps")
    weight = request.form.get("weight")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT workout_id FROM exercises WHERE exercise_id = ?", (exercise_id,))
    r = cur.fetchone()

    if not r:
        conn.close()
        return "Not found", 404

    workout_id = r["workout_id"]

    cur.execute(
        """
        UPDATE exercises
        SET sets = ?, reps = ?, weight_kg = ?
        WHERE exercise_id = ?
        """,
        (sets, reps, weight, exercise_id),
    )

    conn.commit()
    conn.close()

    return redirect(url_for("main.workout_detail", workout_id=workout_id))


@main.route("/template/<int:template_id>/delete", methods=["POST"])
def delete_template(template_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]

    conn = get_connection()
    cur = conn.cursor()

    # Template gerçekten sana mı ait?
    cur.execute(
        "SELECT template_id FROM workout_templates WHERE template_id = ? AND user_id = ?",
        (template_id, user_id),
    )
    row = cur.fetchone()

    if not row:
        conn.close()
        return "Not found", 404

    # Önce bağlı hareketler silinir
    cur.execute("DELETE FROM template_exercises WHERE template_id = ?", (template_id,))
    # Sonra template silinir
    cur.execute("DELETE FROM workout_templates WHERE template_id = ?", (template_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("main.my_templates"))
