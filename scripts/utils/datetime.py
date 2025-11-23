from datetime import datetime
import pytz

# Uygulamanın resmi zaman dilimi
APP_TZ = pytz.timezone("Europe/Istanbul")


def get_today_date():
    """Uygulamada kullanılacak resmi tarih formatı."""
    return datetime.now(APP_TZ).strftime("%d/%m/%Y")


def get_now_timestamp():
    """ISO timestamp döner (log, audit trail vs. için ideal)."""
    return datetime.now(APP_TZ).strftime("%d-%m-%Y %H:%M:%S")