# scripts/init_db.py

import sqlite3
from pathlib import Path

# Projenin ana dizinini bul
BASE_DIR = Path(__file__).resolve().parent.parent

# Veritabanı dosyasının yolu
DB_PATH = BASE_DIR / "db" / "fitanalytics.db"

# Şema dosyasının yolu
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"

def init_db():
    print(f"Veritabanı oluştuluyor: {DB_PATH}")

    # db klasörü yoksa oluştur
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # SQLite veritabanına bağlan (yoksa oluşturur)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Şema dosyasını oku
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    # Şema SQL'ini çalıştır (tabloları oluştur)
    cur.executescript(schema_sql)

    conn.commit()
    conn.close()

    print("Veritabanı başarıyla oluşturuldu.")

if __name__ == "__main__":
    init_db()
