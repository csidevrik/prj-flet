from cryptography.fernet import Fernet
import base64
import os
from typing import Union

def get_or_create_key() -> bytes:
    """Obtiene o crea una clave de encriptación"""
    key_file = os.path.join(os.path.expanduser("~"), ".email_client", "secret.key")
    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        os.makedirs(os.path.dirname(key_file), exist_ok=True)
        with open(key_file, "wb") as f:
            f.write(key)
        return key

def encrypt_data(data: str) -> str:
    """Encripta datos sensibles"""
    try:
        key = get_or_create_key()
        f = Fernet(key)
        return base64.urlsafe_b64encode(f.encrypt(data.encode())).decode()
    except Exception:
        return ""

def decrypt_data(encrypted_data: str) -> str:
    """Desencripta datos sensibles"""
    try:
        key = get_or_create_key()
        f = Fernet(key)
        return f.decrypt(base64.urlsafe_b64decode(encrypted_data)).decode()
    except Exception:
        return ""