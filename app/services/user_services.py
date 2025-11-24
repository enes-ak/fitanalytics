# app/services/user_services.py

from app.database import get_connection

def get_user_by_email(email: str):
    """Email ile kullanıcıyı döner."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id, name, email, password_hash
        FROM users
        WHERE email = ?
    """, (email,))

    user = cur.fetchone()
    conn.close()
    return user


def get_user_by_id(user_id: int):
    """ID ile kullanıcıyı döner."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id, name, email
        FROM users
        WHERE user_id = ?
    """, (user_id,))

    user = cur.fetchone()
    conn.close()
    return user
