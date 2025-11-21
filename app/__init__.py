from flask import Flask, session, has_request_context
from datetime import datetime
from .routes import main

LANGUAGES = {
    "tr": {
        "nav_dashboard": "Gösterge Paneli",
        "nav_add_workout": "Şablon Oluştur",
        "nav_history": "Antrenman Geçmişi",
        "nav_profile": "Profil",
        "nav_logout": "Çıkış Yap",
        "language_label": "Dil",
        "dashboard_title": "Gösterge Paneli",
        "dashboard_subtitle": "Genel antrenman özetin",
        "dashboard_total_workouts": "Toplam Antrenman",
        "dashboard_total_volume": "Toplam Hacim (kg)",
        "dashboard_last_workout": "Son Antrenman Tarihi",
        "dashboard_muscle_table_title": "Kas Grubu Başına Ortalama Hacim ve Ağırlık",
        "dashboard_no_data": "Henüz antrenman verisi bulunmuyor.",
        "dashboard_chart_title": "Kas Grubu Ortalama Hacim Bar Grafiği",
        "table_muscle_group": "Kas Grubu",
        "table_avg_volume": "Ortalama Hacim (kg)",
        "table_avg_weight": "Ortalama Ağırlık (kg)",
        "table_date": "Tarih",
        "table_type": "Tür",
        "table_duration": "Süre (dk)",
        "table_notes": "Notlar",
        "table_exercise": "Hareket",
        "table_muscle": "Kas",
        "table_sets": "Set",
        "table_reps": "Tekrar",
        "table_weight": "Ağırlık (kg)",
        "add_workout_templates_title": "Workout Şablonları",
        "add_workout_templates_desc": "Kayıtlı workout şablonların",
        "add_workout_add_today": "Bugüne Ekle",
        "add_workout_no_templates": "Henüz bir şablon oluşturmadın.",
        "add_workout_form_title": "Yeni Workout Şablonu Oluştur",
        "add_workout_template_name": "Şablon Adı",
        "add_workout_template_placeholder": "Örn: Push Günü",
        "add_workout_workout_type": "Antrenman Türü",
        "add_workout_exercises_title": "Hareketler",
        "add_workout_add_exercise_btn": "+ Hareket Ekle",
        "add_workout_submit_btn": "Şablonu Oluştur",
        "add_workout_placeholder_exercise": "Örn: Bench Press",
        "add_workout_placeholder_muscle": "Örn: Göğüs",
        "add_workout_placeholder_weight": "Kg",
        "workout_type_push": "Push (İtme)",
        "workout_type_pull": "Pull (Çekme)",
        "workout_type_legs": "Bacak",
        "workout_type_upper": "Üst Vücut",
        "workout_type_lower": "Alt Vücut",
        "workout_type_full": "Tüm Vücut",
        "workout_type_other": "Diğer",
        "workout_type_custom": "Özel",
        "workouts_title": "Antrenmanlar",
        "exercises_title": "Egzersizler",
        "exercises_selected_date": "Tarih",
        "exercises_summary_title": "Kas Grubu Özeti",
        "workout_detail_title": "Antrenman Detayları",
        "workout_detail_day_suffix": "Günü",
        "workout_detail_info_date": "Tarih",
        "workout_detail_info_note": "Not",
        "workout_detail_exercises_title": "Hareketler",
        "login_subtitle": "Giriş yap",
        "login_email_label": "E-posta",
        "login_email_placeholder": "ornek@mail.com",
        "login_password_label": "Şifre",
        "login_password_placeholder": "Şifre",
        "login_button": "Giriş Yap",
    },
    "en": {
        "nav_dashboard": "Dashboard",
        "nav_add_workout": "Add Workout",
        "nav_history": "Workout History",
        "nav_profile": "Profile",
        "nav_logout": "Logout",
        "language_label": "Language",
        "dashboard_title": "Dashboard",
        "dashboard_subtitle": "Your overall workout summary",
        "dashboard_total_workouts": "Total Workouts",
        "dashboard_total_volume": "Total Volume (kg)",
        "dashboard_last_workout": "Last Workout Date",
        "dashboard_muscle_table_title": "Average Volume and Weight per Muscle Group",
        "dashboard_no_data": "No workout data found yet.",
        "dashboard_chart_title": "Muscle Group Average Volume Bar Chart",
        "table_muscle_group": "Muscle Group",
        "table_avg_volume": "Average Volume (kg)",
        "table_avg_weight": "Average Weight (kg)",
        "table_date": "Date",
        "table_type": "Type",
        "table_duration": "Duration (min)",
        "table_notes": "Notes",
        "table_exercise": "Exercise",
        "table_muscle": "Muscle",
        "table_sets": "Sets",
        "table_reps": "Reps",
        "table_weight": "Weight (kg)",
        "add_workout_templates_title": "Workout Templates",
        "add_workout_templates_desc": "Your saved workout templates",
        "add_workout_add_today": "Add Today",
        "add_workout_no_templates": "You have not created a template yet.",
        "add_workout_form_title": "Create a New Workout Template",
        "add_workout_template_name": "Template Name",
        "add_workout_template_placeholder": "Ex: Push Day",
        "add_workout_workout_type": "Workout Type",
        "add_workout_exercises_title": "Exercises",
        "add_workout_add_exercise_btn": "+ Add Exercise",
        "add_workout_submit_btn": "Create Template",
        "add_workout_placeholder_exercise": "Ex: Bench Press",
        "add_workout_placeholder_muscle": "Ex: Chest",
        "add_workout_placeholder_weight": "Kg",
        "workout_type_push": "Push",
        "workout_type_pull": "Pull",
        "workout_type_legs": "Legs",
        "workout_type_upper": "Upper",
        "workout_type_lower": "Lower",
        "workout_type_full": "Full Body",
        "workout_type_other": "Other",
        "workout_type_custom": "Custom",
        "workouts_title": "Workouts",
        "exercises_title": "Exercises",
        "exercises_selected_date": "Date",
        "exercises_summary_title": "Muscle Group Summary",
        "workout_detail_title": "Workout Details",
        "workout_detail_day_suffix": "Day",
        "workout_detail_info_date": "Date",
        "workout_detail_info_note": "Note",
        "workout_detail_exercises_title": "Exercises",
        "login_subtitle": "Sign in",
        "login_email_label": "Email",
        "login_email_placeholder": "example@mail.com",
        "login_password_label": "Password",
        "login_password_placeholder": "Password",
        "login_button": "Sign In",
    },
}

LANGUAGE_NAMES = {"tr": "Türkçe", "en": "English"}

def datetime_format(value, format=None):
    if value is None:
        return ""
    lang = "tr"
    if has_request_context():
        lang = session.get("language", "tr")
    default_format = "%d/%m/%Y" if lang == "tr" else "%b %d, %Y"
    fmt = format or default_format
    return datetime.strptime(value, "%Y-%m-%d").strftime(fmt)


def create_app():
    app = Flask(__name__)

    # SESSION için GEREKLİ
    app.secret_key = "fitanalytics_secret_key"

    
    app.config["LANGUAGES"] = LANGUAGES
    app.config["LANGUAGE_NAMES"] = LANGUAGE_NAMES

    app.register_blueprint(main)
    app.jinja_env.filters["datetime_format"] = datetime_format
    app.jinja_env.filters["format_date"] = datetime_format

    @app.context_processor
    def inject_translations():
        language_code = session.get("language", "tr")
        translations = app.config["LANGUAGES"].get(language_code, app.config["LANGUAGES"]["tr"])
        return {
            "t": translations,
            "current_language": language_code,
            "language_names": app.config["LANGUAGE_NAMES"],
        }

    return app
