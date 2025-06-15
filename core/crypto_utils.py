# crypto_utils.py
# Verschlüsselung, Key-Derivation, Secure-Helpers

import os
from base64 import urlsafe_b64encode, urlsafe_b64decode
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def _derive_key(password: str, salt: bytes, iterations: int = 100_000) -> bytes:
    """Derive a 32-byte key from the password and salt using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt(data: str, password: str) -> str:
    """Encrypt data with a password using PBKDF2 and AES-GCM."""
    salt = os.urandom(16)
    key = _derive_key(password, salt)
    iv = os.urandom(12)
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()
    ciphertext = encryptor.update(data.encode()) + encryptor.finalize()
    return urlsafe_b64encode(
        salt + iv + encryptor.tag + ciphertext
    ).decode()

def decrypt(token: str, password: str) -> str:
    """Decrypt data with a password using PBKDF2 and AES-GCM."""
    decoded = urlsafe_b64decode(token)
    salt, iv, tag, ciphertext = decoded[:16], decoded[16:28], decoded[28:44], decoded[44:]
    key = _derive_key(password, salt)
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()
    return (decryptor.update(ciphertext) + decryptor.finalize()).decode()

