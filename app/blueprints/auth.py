# app/blueprints/auth.py

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session,
    current_app
)
from werkzeug.security import check_password_hash

from . import main

# Service katmanı
from app.services.user_services import get_user_by_email


@main.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))

    error = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Service kullanımı
        user = get_user_by_email(email)

        # Kullanıcı bulundu + şifre doğru mu?
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["user_id"]
            session["user_name"] = user["name"]
            return redirect(url_for("main.dashboard"))
        else:
            translations = current_app.config["LANGUAGES"][session.get("language", "tr")]
            error = translations["login_error_invalid"]

    return render_template("login.html", error=error)


@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))


@main.route("/set-language", methods=["POST"])
def set_language():
    selected = request.form.get("language", "tr")
    if selected not in current_app.config["LANGUAGES"]:
        selected = "tr"
    session["language"] = selected
    return redirect(request.referrer or url_for("main.dashboard"))
