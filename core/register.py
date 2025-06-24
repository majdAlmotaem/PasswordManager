# register.py
# Handles user registration logic (extended)

import sqlite3
from core.auth import hash_password

def register_user( username, email,  password, password2, db_path='data/vault.db'):
    """Register a new user with extended info. Returns (True, None) if successful, else (False, error_message)."""
    if password != password2:
        return False, "Passwords do not match."
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id FROM user WHERE username=?', (username,))
    if c.fetchone():
        conn.close()
        return False, "Username already exists."
    c.execute('SELECT id FROM user WHERE email=?', (email,))
    if c.fetchone():
        conn.close()
        return False, "Email already registered."
    hashed = hash_password(password)
    c.execute('INSERT INTO user ( username, email, master_password) VALUES ( ?, ?, ?)',
              (username, email,  hashed))
    conn.commit()
    conn.close()
    return True, None
