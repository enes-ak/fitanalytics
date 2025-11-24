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
            "nav_dashboard": "Ana Sayfa",
            "nav_history": "Spor Kayıtları",
            "nav_logout": "Çıkış",
            "nav_profile": "Profil",
            "login_error_invalid": "E-posta veya şifre hatalı.",
            "login_version_label": "Sürüm v0.1",
            "login_info_title": "Akıllı Fitness Takibi",
            "login_info_description": "Antrenmanlarını tek panelde topla, kas gruplarını analiz et, ilerlemeni gör.",
            "login_info_features": "Hazır Programlar • Hedef takibi • Anlık analiz",
            "login_subtitle": "Hesabına giriş yap ve son antrenmanını kaydet.",
            "login_email_label": "E-posta",
            "login_email_placeholder": "user@example.com",
            "login_password_label": "Şifre",
            "login_password_placeholder": "••••••••",
            "login_button": "Giriş Yap",
        },
        "en": {
            "language_label": "Language",
            "nav_dashboard": "Dashboard",
            "nav_history": "Exercise Logs",
            "nav_logout": "Logout",
            "nav_profile": "Profile",
            "login_error_invalid": "Invalid email or password.",
            "login_version_label": "Version v0.1",
            "login_info_title": "Smarter Workout Tracking",
            "login_info_description": "Collect every session in one dashboard, analyze muscles, stay consistent.",
            "login_info_features": "Programs • Goal tracking • Instant insights",
            "login_subtitle": "Sign in to log your latest workout.",
            "login_email_label": "E-mail",
            "login_email_placeholder": "user@example.com",
            "login_password_label": "Password",
            "login_password_placeholder": "Enter your password",
            "login_button": "Sign In",
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
