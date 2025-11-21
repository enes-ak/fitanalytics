from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from .database import get_connection

main = Blueprint('main', __name__)

@main.route("/login", methods=["GET", "POST"])
def login():
    # ... mevcut login kodun burada dursun ...
    ...

@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))

@main.route("/")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("main.login"))

    # Şimdilik placeholder değerler, sonra DB'den çekeceğiz
    stats = {
        "total_workouts": 3,
        "total_volume": 5550,
        "last_workout_date": "2025-01-14"
    }

    return render_template(
        "dashboard.html",
        total_workouts=stats["total_workouts"],
        total_volume=stats["total_volume"],
        last_workout_date=stats["last_workout_date"],
    )
