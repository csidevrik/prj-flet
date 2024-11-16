from cryptography.fernet import Fernet
import base64
import os
from pathlib import Path
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class SecurityManager:
    _instance = None
    _key: Optional[bytes] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SecurityManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._key is None:
            self._key = self._get_or_create_key()
    
    def _get_or_create_key(self) -> bytes:
        """
        Obtiene o crea una clave de encriptación
        
        Returns:
            bytes: Clave de encriptación
        """
        try:
            key_file = Path.home() / ".email_client" / "secret.key"
            key_file.parent.mkdir(parents=True, exist_ok=True)
            
            if key_file.exists():
                logger.debug("Cargando clave existente")
                with open(key_file, "rb") as f:
                    return f.read()
            else:
                logger.info("Generando nueva clave")
                key = Fernet.generate_key()
                with open(key_file, "wb") as f:
                    f.write(key)
                return key
                
        except Exception as e:
            logger.error(f"Error manejando clave de encriptación: {str(e)}")
            raise
    
    def encrypt(self, data: str) -> str:
        """
        Encripta datos sensibles
        
        Args:
            data: String a encriptar
            
        Returns:
            str: Datos encriptados en formato base64
        """
        try:
            f = Fernet(self._key)
            encrypted_data = f.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            logger.error(f"Error encriptando datos: {str(e)}")
            raise
    
    def decrypt(self, encrypted_data: str) -> str:
        """
        Desencripta datos sensibles
        
        Args:
            encrypted_data: Datos encriptados en formato base64
            
        Returns:
            str: Datos desencriptados
        """
        try:
            f = Fernet(self._key)
            decrypted_data = f.decrypt(base64.urlsafe_b64decode(encrypted_data))
            return decrypted_data.decode()
        except Exception as e:
            logger.error(f"Error desencriptando datos: {str(e)}")
            raise

# Instancia global del administrador de seguridad
_security_manager = SecurityManager()

def encrypt_data(data: str) -> str:
    """
    Función de utilidad para encriptar datos
    
    Args:
        data: String a encriptar
        
    Returns:
        str: Datos encriptados
    """
    return _security_manager.encrypt(data)

def decrypt_data(encrypted_data: str) -> str:
    """
    Función de utilidad para desencriptar datos
    
    Args:
        encrypted_data: Datos encriptados
        
    Returns:
        str: Datos desencriptados
    """
    return _security_manager.decrypt(encrypted_data)

def generate_random_key(length: int = 32) -> str:
    """
    Genera una clave aleatoria
    
    Args:
        length: Longitud de la clave
        
    Returns:
        str: Clave aleatoria en formato base64
    """
    return base64.urlsafe_b64encode(os.urandom(length)).decode()

def hash_password(password: str) -> str:
    """
    Crea un hash seguro de una contraseña
    
    Args:
        password: Contraseña a hashear
        
    Returns:
        str: Hash de la contraseña
    """
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(password.encode())
    return f"{base64.b64encode(salt).decode()}:{base64.b64encode(key).decode()}"

def verify_password(password: str, hash_str: str) -> bool:
    """
    Verifica una contraseña contra su hash
    
    Args:
        password: Contraseña a verificar
        hash_str: Hash almacenado
        
    Returns:
        bool: True si la contraseña coincide
    """
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.exceptions import InvalidKey
    
    try:
        salt_str, key_str = hash_str.split(":")
        salt = base64.b64decode(salt_str)
        stored_key = base64.b64decode(key_str)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        kdf.verify(password.encode(), stored_key)
        return True
    except (InvalidKey, Exception):
        return False