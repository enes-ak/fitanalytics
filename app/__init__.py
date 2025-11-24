from flask import Flask, session
from datetime import datetime
from app.blueprints import main as main_blueprint


def create_app():
    app = Flask(__name__)
    app.secret_key = "fitanalytics_secret_key"

    # ============================================================
    # LANGUAGES (TR / EN)
    # ============================================================
    app.config["LANGUAGES"] = {
        "tr": {
            "language_label": "Dil",
            "nav_dashboard": "Dashboard",
            "nav_history": "Geçmiş",
            "nav_logout": "Çıkış",
            "nav_profile": "Profil",
            "login_error_invalid": "E-posta veya şifre hatalı.",
        },
        "en": {
            "language_label": "Language",
            "nav_dashboard": "Dashboard",
            "nav_history": "History",
            "nav_logout": "Logout",
            "nav_profile": "Profile",
            "login_error_invalid": "Invalid email or password.",
        },
    }

    app.config["language_names"] = {
        "tr": "Türkçe",
        "en": "English",
    }

    # ============================================================
    # JINJA GLOBAL CONTEXT
    # ============================================================
    @app.context_processor
    def inject_globals():
        lang = session.get("language", "tr")
        translations = app.config["LANGUAGES"].get(lang, app.config["LANGUAGES"]["tr"])
        return {
            "current_language": lang,
            "t": translations,
            "language_names": app.config["language_names"],
        }

    # ============================================================
    # JINJA FILTERS
    # ============================================================
    @app.template_filter("format_date")
    def format_date(value):
        if not value:
            return "-"
        try:
            dt = datetime.strptime(value, "%Y-%m-%d")
            return dt.strftime("%d/%m/%Y")
        except Exception:
            return value

    @app.template_filter("datetime_format")
    def datetime_format(value):
        if not value:
            return "-"
        try:
            dt = datetime.strptime(value, "%Y-%m-%d")
            return dt.strftime("%d/%m/%Y")
        except Exception:
            return value

    # ============================================================
    # REGISTER BLUEPRINTS
    # ============================================================
    # Artık routes.py yok; tüm route’lar blueprints içinde
    app.register_blueprint(main_blueprint)

    return app
