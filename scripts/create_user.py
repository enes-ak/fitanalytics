import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "fitanalytics.db"

def create_user(name, email, raw_password):
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database bulunamadı: {DB_PATH}")

    password_hash = generate_password_hash(raw_password)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO users (name, email, password_hash)
        VALUES (?, ?, ?)
        """,
        (name, email, password_hash)
    )

    conn.commit()
    conn.close()

    print(f"Kullanıcı oluşturuldu: {email}")


if __name__ == "__main__":
    create_user("enes", "enes@example.com", "1234")
