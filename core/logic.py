# logic.py
# Fachlogik: Validierung, Passwort-Speicherung

def validate_password(password):
    """Validate password strength. Returns a dict with rule checks and overall validity."""
    rules = {
        'length': len(password) >= 8,
        'uppercase': any(c.isupper() for c in password),
        'lowercase': any(c.islower() for c in password),
        'digit': any(c.isdigit() for c in password),
        'special': any(c in '!@#$%^&*()-_=+[{]}|;:,<.>/?' for c in password)
    }
    rules['valid'] = all(rules.values())
    return rules

def save_password(user_id, service, password, notes, master_password, db_path='data/vault.db'):
    from . import crypto_utils, db
    encrypted_password = crypto_utils.encrypt(password, master_password)
    db.add_entry(user_id, service, encrypted_password, notes, db_path)