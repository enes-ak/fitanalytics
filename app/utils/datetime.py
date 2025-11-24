# app/utils/datetime.py
from datetime import datetime
import pytz

APP_TZ = pytz.timezone("Europe/Istanbul")

# --- Sistem Formatları ---
DB_DATE_FMT = "%Y-%m-%d"       # Veritabanı standardı
UI_DATE_FMT = "%d/%m/%Y"       # Kullanıcıya gösterilecek format
ISO_TS_FMT = "%Y-%m-%d %H:%M:%S"  # Loglar için timestamp


def now_ist():
    return datetime.now(APP_TZ)


def today_db():
    """DB için bugünün tarihini (YYYY-MM-DD) verir."""
    return now_ist().strftime(DB_DATE_FMT)


def today_ui():
    """UI için bugünün tarihini (dd.mm.yyyy) verir."""
    return now_ist().strftime(UI_DATE_FMT)


def iso_timestamp():
    """Log, audit, export vb için timestamp."""
    return now_ist().strftime(ISO_TS_FMT)


def parse_db_date(value: str):
    """DB tarihini datetime objesine çevirir."""
    return datetime.strptime(value, DB_DATE_FMT)
