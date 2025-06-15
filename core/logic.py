# logic.py
# Fachlogik: Validierung, Passwort-Speicherung

def validate_password(password):
    """Validate password strength. Returns True if valid, else False."""
    if not isinstance(password, str) or len(password) < 8:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in '!@#$%^&*()-_=+[{]}|;:,<.>/?' for c in password)
    return has_upper and has_lower and has_digit and has_special

def save_password(service, username, password, notes='', db_path='data/vault.db'):
    """Encrypt and save a password entry to the database."""
    from . import crypto_utils, db
    encrypted_password = crypto_utils.encrypt(password, password)  # For demo: use password as key
    db.add_entry(service, username, encrypted_password, notes, db_path)