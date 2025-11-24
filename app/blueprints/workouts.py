from flask import render_template, request, redirect, url_for, session
from . import main
from app.database import get_connection


@main.route("/")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]

    conn = get_connection()
    cur = conn.cursor()

    # Toplam workout sayısı
    cur.execute("SELECT COUNT(*) FROM workouts WHERE user_id = ?", (user_id,))
    total_workouts = cur.fetchone()[0]

    # Toplam volume
    cur.execute("""
        SELECT SUM(e.sets * e.reps * e.weight_kg)
        FROM exercises e
        JOIN workouts w ON w.workout_id = e.workout_id
        WHERE w.user_id = ?
    """, (user_id,))
    total_volume = cur.fetchone()[0] or 0

    # Kas bazlı istatistik
    cur.execute("""
        SELECT m.name_tr AS muscle_name,
               AVG(e.sets * e.reps * e.weight_kg) AS avg_volume,
               AVG(e.weight_kg) AS avg_weight
        FROM exercises e
        JOIN muscles m ON m.muscle_id = e.muscle_id
        JOIN workouts w ON w.workout_id = e.workout_id
        WHERE w.user_id = ?
        GROUP BY m.muscle_id
        ORDER BY avg_volume DESC
    """, (user_id,))
    rows = cur.fetchall()

    muscle_stats = [{
        "muscle": r["muscle_name"],
        "avg_volume": float(r["avg_volume"] or 0),
        "avg_weight": float(r["avg_weight"] or 0)
    } for r in rows]

    muscle_labels = [r["muscle_name"] for r in rows]
    muscle_volumes = [float(r["avg_volume"] or 0) for r in rows]

    # Son workout tarihi
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


@main.route("/history")
def history():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    user_id = session["user_id"]
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT workout_date
        FROM workouts
        WHERE user_id = ?
        ORDER BY workout_date DESC
    """, (user_id,))
    dates = [r["workout_date"] for r in cur.fetchall()]

    selected = request.args.get("date", dates[0] if dates else None)

    exercises = []
    summary = []

    if selected:
        cur.execute("""
            SELECT e.exercise_name, m.name_tr AS muscle,
                   e.sets, e.reps, e.weight_kg
            FROM exercises e
            JOIN muscles m ON m.muscle_id = e.muscle_id
            JOIN workouts w ON w.workout_id = e.workout_id
            WHERE w.user_id = ? AND w.workout_date = ?
        """, (user_id, selected))
        exercises = cur.fetchall()

        cur.execute("""
            SELECT m.name_tr AS muscle,
                   AVG(e.sets * e.reps * e.weight_kg) AS avg_volume,
                   AVG(e.weight_kg) AS avg_weight
            FROM exercises e
            JOIN muscles m ON e.muscle_id = m.muscle_id
            JOIN workouts w ON w.workout_id = e.workout_id
            WHERE w.user_id = ? AND w.workout_date = ?
            GROUP BY m.muscle_id
        """, (user_id, selected))
        summary = cur.fetchall()

    conn.close()

    return render_template(
        "history.html",
        dates=dates,
        selected_date=selected,
        exercises=exercises,
        summary=summary
    )


@main.route("/workout/<int:workout_id>")
def workout_detail(workout_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT workout_id, workout_date, workout_type, notes
        FROM workouts
        WHERE workout_id = ?
    """, (workout_id,))
    workout = cur.fetchone()

    cur.execute("""
        SELECT e.exercise_id, e.exercise_name, m.name_tr AS muscle,
               e.sets, e.reps, e.weight_kg
        FROM exercises e
        JOIN muscles m ON m.muscle_id = e.muscle_id
        WHERE workout_id = ?
        ORDER BY exercise_id ASC
    """, (workout_id,))
    exercises = cur.fetchall()

    conn.close()

    return render_template("workout_detail.html", workout=workout, exercises=exercises)


@main.route("/exercise/<int:exercise_id>/delete", methods=["POST"])
def delete_exercise(exercise_id):
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT workout_id FROM exercises WHERE exercise_id = ?", (exercise_id,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return "Not found", 404

    workout_id = row["workout_id"]

    cur.execute("DELETE FROM exercises WHERE exercise_id = ?", (exercise_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("main.workout_detail", workout_id=workout_id))


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
    row = cur.fetchone()

    if not row:
        conn.close()
        return "Not found", 404

    workout_id = row["workout_id"]

    cur.execute("""
        UPDATE exercises
        SET sets = ?, reps = ?, weight_kg = ?
        WHERE exercise_id = ?
    """, (sets, reps, weight, exercise_id))

    conn.commit()
    conn.close()

    return redirect(url_for("main.workout_detail", workout_id=workout_id))
