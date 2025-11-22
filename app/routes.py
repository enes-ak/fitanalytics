from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    current_app,
)
from werkzeug.security import check_password_hash
from .database import get_connection

main = Blueprint("main", __name__)

# Hangi workout_type'lara izin veriyoruz
ALLOWED_WORKOUT_TYPES = {"push", "pull", "legs", "upper", "lower", "full", "other"}

# Hazır (default) şablonlar – hem create-template sayfasında, hem route'ta kullanacağız
DEFAULT_TEMPLATES = {
    "Push Day (Beginner)": {
        "workout_type": "push",
        "exercises": [
            ("Bench Press", "Chest", 3, 10, 20),
            ("Incline Dumbbell Press", "Chest", 3, 12, 12),
            ("Shoulder Press", "Shoulders", 3, 10, 10),
            ("Lateral Raise", "Shoulders", 3, 15, 6),
            ("Triceps Pushdown", "Triceps", 3, 12, 15),
        ],
    },
    "Pull Day (Beginner)": {
        "workout_type": "pull",
        "exercises": [
            ("Lat Pulldown", "Back", 3, 12, 35),
            ("Seated Row", "Back", 3, 12, 40),
            ("Face Pull", "Rear Delts", 3, 15, 12),
            ("Barbell Curl", "Biceps", 3, 10, 20),
        ],
    },
    "Legs Day (Beginner)": {
        "workout_type": "legs",
        "exercises": [
            ("Squat", "Legs", 3, 10, 60),
            ("Leg Press", "Legs", 3, 12, 100),
            ("Leg Extension", "Legs", 3, 15, 30),
            ("Leg Curl", "Hamstrings", 3, 12, 30),
            ("Calf Raise", "Calves", 4, 15, 25),
        ],
    },
}


# ------------------------------
# AUTH
# ------------------------------
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
            """
            SELECT user_id, name, password_hash
            FROM users
            WHERE email = ?;
        """,
            (email,),
        )
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["user_id"]
            session["user_name"] = user["name"]

            next_url = request.args.get("next") or url_for("main.dashboard")
            return redirect(next_url)

        translations = current_app.config["LANGUAGES"].get(
            session.get("language", "tr"),
            current_app.config["LANGUAGES"]["tr"],
        )
        error = translations.get("login_error_invalid", "E-posta veya şifre hatalı.")

    return render_template("login.html", error=error)


@main.route("/set-language", methods=["POST"])
def set_language():
    selected_language = request.form.get("language", "tr")
    available_languages = current_app.config.get("LANGUAGES", {})

    if selected_language not in available_languages:
        selected_language = "tr"

    session["language"] = selected_language
    next_url = request.form.get("next") or request.referrer or url_for("main.dashboard")
    return redirect(next_url)


@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))


# ------------------------------
# DASHBOARD
# ------------------------------
@main.route("/")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = get_connection()
    cur = conn.cursor()
    user_id = session["user_id"]

    # 1) Toplam workout sayısı
    cur.execute(
        """
        SELECT COUNT(*)
        FROM workouts
        WHERE user_id = ?;
    """,
        (user_id,),
    )
    total_workouts = cur.fetchone()[0]

    # 2) Toplam volume
    cur.execute(
        """
        SELECT SUM(e.sets * e.reps * e.weight_kg)
        FROM exercises e
        JOIN workouts w ON e.workout_id = w.workout_id
        WHERE w.user_id = ?;
    """,
        (user_id,),
    )
    total_volume = cur.fetchone()[0] or 0

    # 3) Kas bazlı ortalama volume + ağırlık
    cur.execute(
        """
        SELECT
            e.target_muscle,
            AVG(e.sets * e.reps * e.weight_kg) AS avg_muscle_volume,
            AVG(e.weight_kg) AS avg_weight_per_muscle
        FROM exercises e
        JOIN workouts w ON e.workout_id = w.workout_id
        WHERE w.user_id = ?
        GROUP BY e.target_muscle
        ORDER BY avg_muscle_volume DESC;
    """,
        (user_id,),
    )

    muscle_volumes_rows = cur.fetchall()
    muscles = [row[0] for row in muscle_volumes_rows]
    avg_volumes = [row[1] for row in muscle_volumes_rows]
    avg_weights = [row[2] for row in muscle_volumes_rows]

    # 4) Son workout tarihi
    cur.execute(
        """
        SELECT workout_date
        FROM workouts
        WHERE user_id = ?
        ORDER BY workout_date DESC
        LIMIT 1;
    """,
        (user_id,),
    )
    row = cur.fetchone()
    workout_date = row["workout_date"] if row else None

    conn.close()

    return render_template(
        "dashboard.html",
        total_workouts=total_workouts,
        total_volume=total_volume,
        muscle_volumes=muscle_volumes_rows,
        workout_date=workout_date,
        muscles=muscles,
        avg_volumes=avg_volumes,
        avg_weights=avg_weights,
    )


# ------------------------------
# ESKİ /workouts → ARTIK GEÇMİŞ SAYFASINA GÖNDERİYORUZ
# ------------------------------
@main.route("/workouts")
def workouts():
    if "user_id" not in session:
        return redirect(url_for("main.login"))
    # Artık ana "geçmiş" sayfası /exercises
    return redirect(url_for("main.exercises"))


# ------------------------------
# WORKOUT HISTORY (TARİH BAZLI)
# ------------------------------
@main.route("/exercises")
def exercises():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = get_connection()
    cur = conn.cursor()
    user_id = session["user_id"]

    # Soldaki tarih listesi
    cur.execute(
        """
        SELECT DISTINCT workout_date
        FROM workouts
        WHERE user_id = ?
        ORDER BY workout_date DESC;
    """,
        (user_id,),
    )
    workout_dates = [row["workout_date"] for row in cur.fetchall()]

    selected_workout_date = request.args.get(
        "date", workout_dates[0] if workout_dates else None
    )

    exercises = []
    muscle_summary = []

    if selected_workout_date:
        # Seçilen tarihin hareketleri
        cur.execute(
            """
            SELECT
                e.exercise_name,
                e.target_muscle,
                e.sets,
                e.reps,
                e.weight_kg
            FROM exercises e
            JOIN workouts w ON e.workout_id = w.workout_id
            WHERE w.user_id = ?
              AND w.workout_date = ?
            ORDER BY e.exercise_name ASC;
        """,
            (user_id, selected_workout_date),
        )
        exercises = cur.fetchall()

        # Kas bazlı özet
        cur.execute(
            """
            SELECT
                e.target_muscle,
                AVG(e.sets * e.reps * e.weight_kg) AS avg_volume,
                AVG(e.weight_kg) AS avg_weight
            FROM exercises e
            JOIN workouts w ON e.workout_id = w.workout_id
            WHERE w.user_id = ?
              AND w.workout_date = ?
            GROUP BY e.target_muscle
            ORDER BY avg_volume DESC;
        """,
            (user_id, selected_workout_date),
        )
        muscle_summary = cur.fetchall()

    conn.close()

    return render_template(
        "exercises.html",
        workout_dates=workout_dates,
        exercises=exercises,
        selected_workout_date=selected_workout_date,
        muscle_summary=muscle_summary,
    )


# ------------------------------
# YENİ ŞABLON OLUŞTUR SAYFASI
# (solda hazır şablonlar, sağda manuel oluşturma formu)
# ------------------------------
@main.route("/add-workout", methods=["GET", "POST"])
def add_workout():
    """
    Bu sayfa artık:
      - Solda DEFAULT_TEMPLATES (hazır push/pull/legs)
      - Sağda manuel "yeni şablon oluştur" formu
    """
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]
    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        template_name = request.form.get("template_name")
        workout_type = request.form.get("workout_type")

        if not template_name:
            conn.close()
            return redirect(url_for("main.add_workout"))

        if workout_type not in ALLOWED_WORKOUT_TYPES:
            workout_type = "other"

        # 1) Yeni template kaydet
        cur.execute(
            """
            INSERT INTO workout_templates (user_id, template_name, workout_type)
            VALUES (?, ?, ?);
        """,
            (user_id, template_name, workout_type),
        )
        template_id = cur.lastrowid

        # 2) Formdan gelen hareketler
        exercise_names = request.form.getlist("exercise_name")
        muscles = request.form.getlist("muscle")
        sets_list = request.form.getlist("sets")
        reps_list = request.form.getlist("reps")
        weight_list = request.form.getlist("weight")

        for name, muscle, sets, reps, weight in zip(
            exercise_names, muscles, sets_list, reps_list, weight_list
        ):
            if not name:
                continue
            cur.execute(
                """
                INSERT INTO template_exercises
                    (template_id, exercise_name, target_muscle, default_sets, default_reps, default_weight)
                VALUES (?, ?, ?, ?, ?, ?);
            """,
                (template_id, muscle and name, muscle, sets or None, reps or None, weight or None),
            )

        conn.commit()
        conn.close()

        # Yeni şablon → "Benim Şablonlarım" sayfasına
        return redirect(url_for("main.my_templates"))

    # GET: sayfayı render et
    conn.close()
    return render_template("add_workout.html", default_templates=DEFAULT_TEMPLATES)


# ------------------------------
# BENİM ŞABLONLARIM SAYFASI
# ------------------------------
@main.route("/my-templates")
def my_templates():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]
    conn = get_connection()
    cur = conn.cursor()

    # Şablonlar + basic analiz (exercise sayısı + toplam volume)
    cur.execute(
        """
        SELECT
            wt.template_id,
            wt.template_name,
            wt.workout_type,
            COUNT(te.template_exercise_id) AS exercise_count,
            COALESCE(
                SUM(te.default_sets * te.default_reps * te.default_weight),
                0
            ) AS total_volume
        FROM workout_templates wt
        LEFT JOIN template_exercises te
          ON wt.template_id = te.template_id
        WHERE wt.user_id = ?
        GROUP BY wt.template_id, wt.template_name, wt.workout_type
        ORDER BY wt.template_name ASC;
    """,
        (user_id,),
    )

    templates = cur.fetchall()
    conn.close()

    return render_template("my_templates.html", templates=templates)


# ------------------------------
# HAZIR ŞABLONU BENİM ŞABLONLARIMA KOPYALA
# (DEFAULT_TEMPLATES → workout_templates + template_exercises)
# ------------------------------
@main.route("/default-templates/use/<string:template_name>", methods=["POST"])
def use_default_template(template_name):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    if template_name not in DEFAULT_TEMPLATES:
        return "Template bulunamadı", 404

    tpl = DEFAULT_TEMPLATES[template_name]
    workout_type = tpl["workout_type"]
    exercises = tpl["exercises"]

    user_id = session["user_id"]
    conn = get_connection()
    cur = conn.cursor()

    # 1) Yeni template kaydet
    cur.execute(
        """
        INSERT INTO workout_templates (user_id, template_name, workout_type)
        VALUES (?, ?, ?);
    """,
        (user_id, template_name, workout_type),
    )
    template_id = cur.lastrowid

    # 2) Egzersizleri kaydet
    for name, muscle, sets, reps, weight in exercises:
        cur.execute(
            """
            INSERT INTO template_exercises
                (template_id, exercise_name, target_muscle, default_sets, default_reps, default_weight)
            VALUES (?, ?, ?, ?, ?, ?);
        """,
            (template_id, name, muscle, sets, reps, weight),
        )

    conn.commit()
    conn.close()

    return redirect(url_for("main.my_templates"))


# ------------------------------
# ŞABLONDAN BUGÜNE WORKOUT OLUŞTUR
# ------------------------------
@main.route("/use-template/<int:template_id>")
def use_template(template_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]
    conn = get_connection()
    cur = conn.cursor()

    # Template bilgisi
    cur.execute(
        """
        SELECT template_name, workout_type
        FROM workout_templates
        WHERE template_id = ? AND user_id = ?;
    """,
        (template_id, user_id),
    )
    template = cur.fetchone()

    if not template:
        conn.close()
        return "Template bulunamadı", 404

    template_name, workout_type = template
    normalized_workout_type = (
        workout_type if workout_type in ALLOWED_WORKOUT_TYPES else "other"
    )

    # Bugün aynı tipten workout var mı?
    cur.execute(
        """
        SELECT workout_id
        FROM workouts
        WHERE user_id = ?
          AND workout_type = ?
          AND workout_date = DATE('now');
    """,
        (user_id, normalized_workout_type),
    )
    existing = cur.fetchone()

    if existing:
        conn.close()
        return render_template(
            "confirm_repeat_workout.html",
            template_id=template_id,
            workout_type=normalized_workout_type,
            template_name=template_name,
        )

    # Yoksa direkt oluştur
    cur.execute(
        """
        INSERT INTO workouts (user_id, workout_date, workout_type, notes)
        VALUES (?, DATE('now'), ?, ?);
    """,
        (user_id, normalized_workout_type, f"From template: {template_name}"),
    )
    new_workout_id = cur.lastrowid

    # Template egzersizleri
    cur.execute(
        """
        SELECT exercise_name, target_muscle, default_sets, default_reps, default_weight
        FROM template_exercises
        WHERE template_id = ?;
    """,
        (template_id,),
    )
    template_exercises = cur.fetchall()

    for name, muscle, sets, reps, weight in template_exercises:
        cur.execute(
            """
            INSERT INTO exercises
                (workout_id, exercise_name, target_muscle, sets, reps, weight_kg)
            VALUES (?, ?, ?, ?, ?, ?);
        """,
            (new_workout_id, name, muscle, sets, reps, weight),
        )

    conn.commit()
    conn.close()

    return redirect(url_for("main.workout_detail", workout_id=new_workout_id))


@main.route("/confirm-use-template/<int:template_id>", methods=["POST"])
def confirm_use_template(template_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]
    conn = get_connection()
    cur = conn.cursor()

    # Template bilgisi
    cur.execute(
        """
        SELECT template_name, workout_type
        FROM workout_templates
        WHERE template_id = ? AND user_id = ?;
    """,
        (template_id, user_id),
    )
    template = cur.fetchone()

    if not template:
        conn.close()
        return "Template bulunamadı", 404

    template_name, workout_type = template

    # Workout oluştur
    cur.execute(
        """
        INSERT INTO workouts (user_id, workout_date, workout_type, notes)
        VALUES (?, DATE('now'), ?, ?);
    """,
        (user_id, workout_type, f"From template: {template_name}"),
    )
    new_workout_id = cur.lastrowid

    # Template egzersizleri
    cur.execute(
        """
        SELECT exercise_name, target_muscle, default_sets, default_reps, default_weight
        FROM template_exercises
        WHERE template_id = ?;
    """,
        (template_id,),
    )
    template_exercises = cur.fetchall()

    for name, muscle, sets, reps, weight in template_exercises:
        cur.execute(
            """
            INSERT INTO exercises
                (workout_id, exercise_name, target_muscle, sets, reps, weight_kg)
            VALUES (?, ?, ?, ?, ?, ?);
        """,
            (new_workout_id, name, muscle, sets, reps, weight),
        )

    conn.commit()
    conn.close()

    return redirect(url_for("main.workout_detail", workout_id=new_workout_id))


# ------------------------------
# WORKOUT DETAYI + EXERCISE EDIT/DELETE
# ------------------------------
@main.route("/workout/<int:workout_id>")
def workout_detail(workout_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT workout_id, workout_date, workout_type, notes
        FROM workouts
        WHERE workout_id = ?;
    """,
        (workout_id,),
    )
    workout_row = cur.fetchone()

    if not workout_row:
        conn.close()
        return "Workout not found", 404

    workout = {
        "workout_id": workout_row["workout_id"],
        "workout_date": workout_row["workout_date"],
        "workout_type": workout_row["workout_type"],
        "notes": workout_row["notes"],
    }

    cur.execute(
        """
        SELECT exercise_id, exercise_name, target_muscle, sets, reps, weight_kg
        FROM exercises
        WHERE workout_id = ?;
    """,
        (workout_id,),
    )
    exercises = cur.fetchall()

    conn.close()

    return render_template("workout_detail.html", workout=workout, exercises=exercises)


@main.route("/exercise/<int:exercise_id>/delete", methods=["POST"])
def delete_exercise(exercise_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT workout_id FROM exercises WHERE exercise_id = ?;",
        (exercise_id,),
    )
    row = cur.fetchone()

    if not row:
        conn.close()
        return "Exercise not found", 404

    workout_id = row["workout_id"]

    cur.execute("DELETE FROM exercises WHERE exercise_id = ?;", (exercise_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("main.workout_detail", workout_id=workout_id))


@main.route("/exercise/<int:exercise_id>/edit", methods=["POST"])
def edit_exercise(exercise_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    sets = request.form.get("sets")
    reps = request.form.get("reps")
    weight = request.form.get("weight_kg")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT workout_id FROM exercises WHERE exercise_id = ?;",
        (exercise_id,),
    )
    row = cur.fetchone()

    if not row:
        conn.close()
        return "Exercise not found", 404

    workout_id = row["workout_id"]

    cur.execute(
        """
        UPDATE exercises
        SET sets = ?, reps = ?, weight_kg = ?
        WHERE exercise_id = ?;
    """,
        (sets, reps, weight, exercise_id),
    )

    conn.commit()
    conn.close()

    return redirect(url_for("main.workout_detail", workout_id=workout_id))


@main.route("/template/<int:template_id>")
def template_detail(template_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = get_connection()
    cur = conn.cursor()

    # Template info
    cur.execute("""
        SELECT template_id, template_name, workout_type
        FROM workout_templates
        WHERE template_id = ? AND user_id = ?;
    """, (template_id, session["user_id"]))
    template = cur.fetchone()

    if not template:
        conn.close()
        return "Template bulunamadı", 404

    # Exercises
    cur.execute("""
        SELECT exercise_name, target_muscle, default_sets, default_reps, default_weight
        FROM template_exercises
        WHERE template_id = ?;
    """, (template_id,))
    exercises = cur.fetchall()

    conn.close()

    return render_template(
        "template_detail.html",
        template=template,
        exercises=exercises
    )