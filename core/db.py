# db.py
# DB-Handling (CRUD via SQLite)

import sqlite3

def initialize_db(db_path='data/vault.db'):
    """Initialize the SQLite database and create the user and vault tables if they don't exist."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # User table for username and master password
    c.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT UNIQUE,
            master_password TEXT NOT NULL
        )
    ''')
    # Vault table for saved passwords
    c.execute('''
        CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            service TEXT NOT NULL,
            password TEXT NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES user(id)
        )
    ''')
    conn.commit()
    conn.close()

def add_entry(user_id, service, password, notes='', db_path='data/vault.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO vault (user_id, service, password, notes) VALUES (?, ?, ?, ?)',
              (user_id, service, password, notes))
    conn.commit()
    conn.close()

def get_entries(user_id, db_path='data/vault.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id, service, password, notes, created_at FROM vault WHERE user_id=?', (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def update_entry(entry_id, user_id, service, password, notes='', db_path='data/vault.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        UPDATE vault SET service=?, password=?, notes=? WHERE id=? AND user_id=?
    ''', (service, password, notes, entry_id, user_id))
    conn.commit()
    conn.close()

def delete_entry(entry_id, user_id, db_path='data/vault.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('DELETE FROM vault WHERE id=? AND user_id=?', (entry_id, user_id))
    conn.commit()
    conn.close()

def get_user_id(username, db_path='data/vault.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id FROM user WHERE username=?', (username,))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0]
    return None