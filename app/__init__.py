from flask import Flask, session
from datetime import datetime, date
from .routes import main


def create_app():
    app = Flask(__name__)
    app.secret_key = "fitanalytics_secret_key"

    # ============================================================
    # INTERNATIONALIZATION LAYER
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
    # GLOBAL TEMPLATE CONTEXT
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
    # UNIFIED DATE FILTERS
    # ============================================================
    def _parse_date_value(value):
        """Coerce different incoming date representations into a datetime."""
        if not value:
            return None

        if isinstance(value, datetime):
            return value

        if isinstance(value, date):
            return datetime(value.year, value.month, value.day)

        if isinstance(value, str):
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d.%m.%Y", "%d-%m-%Y"):
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue

        return None

    @app.template_filter("format_date")
    def format_date(value):
        """Render any stored date as Gün-Ay-Yıl (DD.MM.YYYY)."""
        dt = _parse_date_value(value)
        if not dt:
            return value if value else "-"
        return dt.strftime("%d.%m.%Y")

    @app.template_filter("datetime_format")
    def datetime_format(value):
        """Human readable Gün Ay Yıl format (e.g. 24 Mart 2025)."""
        dt = _parse_date_value(value)
        if not dt:
            return value if value else "-"

        # İngilizce ay isimleri gelmesin diye locale bağımlılığını çözüyoruz
        months_tr = {
            1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran",
            7: "Temmuz", 8: "Ağustos", 9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"
        }

        month_name = months_tr.get(dt.month, str(dt.month))
        return f"{dt.day} {month_name} {dt.year}"

    # ============================================================
    # BLUEPRINT REGISTRATION
    # ============================================================
    app.register_blueprint(main)

    return app
