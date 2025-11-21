from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from werkzeug.security import check_password_hash
from .database import get_connection

ALLOWED_WORKOUT_TYPES = {"push", "pull", "legs", "upper", "lower", "full", "other"}

main = Blueprint('main', __name__)

@main.route("/login", methods=["GET", "POST"])
def login():
    # ... mevcut login kodun burada dursun ...
    ...


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

@main.route("/")
def dashboard():
    # Giriş yapılmamışsa login'e gönder
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = get_connection()
    cur = conn.cursor()

    user_id = session["user_id"]

    # 1) Toplam workout sayısı
    cur.execute("""
        SELECT COUNT(*) 
        FROM workouts 
        WHERE user_id = ?;
    """, (user_id,))
    total_workouts = cur.fetchone()[0]

    # 2) Toplam volume (sets * reps * weight_kg)
    cur.execute("""
        SELECT SUM(sets * reps * weight_kg)
        FROM exercises
        WHERE workout_id IN (
            SELECT workout_id FROM workouts WHERE user_id = ?
        );
    """, (user_id,))
    total_volume = cur.fetchone()[0]
    if total_volume is None:
        total_volume = 0


    # 3) Toplam volume - Kasa göre (sets * reps * weight_kg)
    cur.execute("""
        SELECT e.target_muscle, 
                AVG(e.sets * e.reps * e.weight_kg) AS avg_muscle_volume,
                AVG(e.weight_kg) AS avg_weight_per_muscle
        FROM exercises e
        JOIN workouts w ON e.workout_id = w.workout_id
        WHERE w.user_id = ?
        GROUP BY e.target_muscle 
        ORDER BY avg_muscle_volume DESC;
    """, (user_id,))
    muscle_volumes = cur.fetchall() 
    muscles = [row[0] for row in muscle_volumes]
    avg_volumes = [row[1] for row in muscle_volumes]
    avg_weights = [row[2] for row in muscle_volumes]

    if muscle_volumes is None:
        muscle_volumes = 0
    

    # 4) Son workout tarihi
    cur.execute("""
        SELECT workout_date
        FROM workouts
        WHERE user_id = ?
        ORDER BY workout_date DESC
        LIMIT 1;
    """, (user_id,))
    row = cur.fetchone()
    workout_date = row["workout_date"] if row else None

    conn.close()

    return render_template(
        "dashboard.html",
        total_workouts=total_workouts,
        total_volume=total_volume,
        muscle_volumes=muscle_volumes,
        workout_date=workout_date,
        muscles=muscles,
        avg_volumes=avg_volumes,
        avg_weights=avg_weights
    )


@main.route("/workouts")
def workouts():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = get_connection()
    cur = conn.cursor()

    user_id = session["user_id"]

    cur.execute("""
        SELECT workout_id, workout_date, workout_type, duration_min, notes
        FROM workouts
        WHERE user_id = ?
        ORDER BY workout_date DESC;
    """, (user_id,))

    all_workouts = [
        {
            "workout_id": row["workout_id"],
            "workout_date": row["workout_date"],
            "workout_type": row["workout_type"],
            "duration_min": row["duration_min"],
            "notes": row["notes"],
        }
        for row in cur.fetchall()
    ]
    conn.close()

    return render_template("workouts.html", workouts=all_workouts)


@main.route("/exercises")
def exercises():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = get_connection()
    cur = conn.cursor()
    user_id = session["user_id"]

    # Sol taraftaki tarih listesi
    cur.execute("""
        SELECT DISTINCT workout_date
        FROM workouts
        WHERE user_id = ?
        ORDER BY workout_date DESC;
    """, (user_id,))
    workout_dates = [row["workout_date"] for row in cur.fetchall()]

    # Seçilen tarih (GET parametresi)
    selected_workout_date = request.args.get("date", workout_dates[0] if workout_dates else None)

    # Seçilen tarihin exercise'ları
    cur.execute("""
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
    """, (user_id, selected_workout_date))

    exercises = cur.fetchall()
    
    # --- Seçilen güne ait kas grubu özet istatistikleri ---
    cur.execute("""
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
    """, (user_id, selected_workout_date))

    muscle_summary = cur.fetchall()
    
    conn.close()

    return render_template(
        "exercises.html",
        workout_dates=workout_dates,
        exercises=exercises,
        selected_workout_date=selected_workout_date,
        muscle_summary=muscle_summary
    )
@main.route("/add-workout", methods=["GET", "POST"])
def add_workout():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = get_connection()
    cur = conn.cursor()
    user_id = session["user_id"]

    # --- TEMPLATE LISTESINI CEK ---
    cur.execute("""
        SELECT template_id, template_name, workout_type
        FROM workout_templates
        WHERE user_id = ?
        ORDER BY template_name ASC;
    """, (user_id,))
    templates = cur.fetchall()

    # --- TEMPLATE OLUSTURMA ---
    if request.method == "POST":
        template_name = request.form.get("template_name")
        workout_type = request.form.get("workout_type")
        if workout_type not in ALLOWED_WORKOUT_TYPES:
            workout_type = "other"

        # Yeni template'i kaydet
        cur.execute("""
            INSERT INTO workout_templates (user_id, template_name, workout_type)
            VALUES (?, ?, ?);
        """, (user_id, template_name, workout_type))

        template_id = cur.lastrowid

        # Exercise'ları al
        exercise_names = request.form.getlist("exercise_name")
        muscles = request.form.getlist("muscle")
        sets_list = request.form.getlist("sets")
        reps_list = request.form.getlist("reps")
        weight_list = request.form.getlist("weight")

        # Her exercise'ı kaydet
        for name, muscle, sets, reps, weight in zip(exercise_names, muscles, sets_list, reps_list, weight_list):
            cur.execute("""
                INSERT INTO template_exercises (template_id, exercise_name, target_muscle, default_sets, default_reps, default_weight)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (template_id, name, muscle, sets, reps, weight))

        conn.commit()
        conn.close()

        return redirect(url_for("main.add_workout"))

    conn.close()
    return render_template("add_workout.html", templates=templates)


@main.route("/use-template/<int:template_id>")
def use_template(template_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]
    conn = get_connection()
    cur = conn.cursor()

    # Template bilgisi çek
    cur.execute("""
        SELECT template_name, workout_type
        FROM workout_templates
        WHERE template_id = ? AND user_id = ?;
    """, (template_id, user_id))
    template = cur.fetchone()

    if not template:
        conn.close()
        return "Template bulunamadı", 404

    template_name, workout_type = template
    normalized_workout_type = workout_type if workout_type in ALLOWED_WORKOUT_TYPES else "other"

    # 1) Yeni workout oluştur (bugünün tarihi ile)
    cur.execute("""
        INSERT INTO workouts (user_id, workout_date, workout_type, duration_min, notes)
        VALUES (?, DATE('now'), ?, NULL, ?);
    """, (user_id, normalized_workout_type, f"From template: {template_name}"))

    new_workout_id = cur.lastrowid

    # 2) Template egzersizlerini çek
    cur.execute("""
        SELECT exercise_name, target_muscle, default_sets, default_reps, default_weight
        FROM template_exercises
        WHERE template_id = ?;
    """, (template_id,))
    template_exercises = cur.fetchall()

    # 3) Egzersizleri yeni workout'a ekle
    for name, muscle, sets, reps, weight in template_exercises:
        cur.execute("""
            INSERT INTO exercises (workout_id, exercise_name, target_muscle, sets, reps, weight_kg)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (new_workout_id, name, muscle, sets, reps, weight))

    conn.commit()
    conn.close()

    # Yeni workout detay sayfasına yönlendir
    return redirect(url_for("main.workout_detail", workout_id=new_workout_id))


@main.route("/workout/<int:workout_id>")
def workout_detail(workout_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = get_connection()
    cur = conn.cursor()

    # Workout bilgisi
    cur.execute("""
        SELECT workout_id, workout_date, workout_type, notes
        FROM workouts
        WHERE workout_id = ?;
    """, (workout_id,))
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

    # Exercise listesi
    cur.execute("""
        SELECT exercise_name, target_muscle, sets, reps, weight_kg
        FROM exercises
        WHERE workout_id = ?;
    """, (workout_id,))
    exercises = cur.fetchall()

    conn.close()

    return render_template(
        "workout_detail.html",
        workout=workout,
        exercises=exercises
    )
