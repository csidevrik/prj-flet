import logging
import os
from pathlib import Path

def setup_logging():
    """Configura el sistema de logging"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "app.log"),
            logging.StreamHandler()
        ]
    )

# Configuraciones generales de la aplicación
APP_NAME = "Email Client"
CONFIG_DIR = Path.home() / ".email_client"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Configuraciones de correo
DEFAULT_SMTP_PORT = 465
MAX_ATTACHMENT_SIZE_MB = 10
TIMEOUT_SECONDS = 30

# Configuraciones de archivos
ALLOWED_EXTENSIONS = ['pdf']
TEMP_DIR = CONFIG_DIR / "temp"
BACKUP_DIR = CONFIG_DIR / "backups"
MAX_BACKUPS = 5

# Mensajes de error comunes
ERROR_MESSAGES = {
    'auth_error': "Error de autenticación: Usuario o contraseña incorrectos",
    'connection_error': "Error de conexión: No se puede conectar al servidor",
    'timeout_error': "Error: Tiempo de espera agotado",
    'attachment_size': "Error: El archivo excede el tamaño máximo permitido",
    'invalid_email': "Error: Dirección de correo inválida",
    'no_connection': "Error: No hay conexión establecida"
}