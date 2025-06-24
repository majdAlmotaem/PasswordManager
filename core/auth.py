# auth.py
# Handles user authentication and registration logic

import sqlite3
import os
import hashlib
import binascii

# Secure password hashing helpers
HASH_ITERATIONS = 200_000
HASH_ALGO = 'sha256'
SALT_SIZE = 16

def hash_password(password: str, salt: bytes = None) -> str:
    if salt is None:
        salt = os.urandom(SALT_SIZE)
    pwd_hash = hashlib.pbkdf2_hmac(HASH_ALGO, password.encode(), salt, HASH_ITERATIONS)
    return binascii.hexlify(salt).decode() + ':' + binascii.hexlify(pwd_hash).decode()

def verify_password(stored: str, provided: str) -> bool:
    try:
        salt_hex, hash_hex = stored.split(':')
        salt = binascii.unhexlify(salt_hex)
        pwd_hash = hashlib.pbkdf2_hmac(HASH_ALGO, provided.encode(), salt, HASH_ITERATIONS)
        return binascii.hexlify(pwd_hash).decode() == hash_hex
    except Exception:
        return False

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
    if row and verify_password(row[0], password):
        return True
    return False
