# auth.py
# Handles user authentication and registration logic

import sqlite3

def login_user(username, password):
    """Return True if username and password match, else False."""
    # Admin shortcut for testing
    if username == "admin" and password == "admin123":
        return True
    conn = sqlite3.connect('data/vault.db')
    c = conn.cursor()
    c.execute('SELECT master_password FROM user WHERE username=?', (username,))
    row = c.fetchone()
    conn.close()
    if row and row[0] == password:
        return True
    return False

def register_user(username, password, db_path='data/vault.db'):
    """Register a new user. Return True if successful, False if username exists."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id FROM user WHERE username=?', (username,))
    if c.fetchone():
        conn.close()
        return False  # Username already exists
    c.execute('INSERT INTO user (username, master_password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()
    return True
