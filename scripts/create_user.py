from werkzeug.security import generate_password_hash
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "fitanalytics.db"

name = "enes"
email = "enes@example.com"
raw_password = "1234"

password_hash = generate_password_hash(raw_password)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
    INSERT INTO users (name, email, password_hash)
    VALUES (?, ?, ?)
""", (name, email, password_hash))

conn.commit()
conn.close()

print(f"{name} Kullanıcı oluşturuldu!")
