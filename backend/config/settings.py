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

# Configuraciones generales
APP_NAME = "Email Client"
CONFIG_DIR = Path.home() / ".email_client"
CONFIG_FILE = CONFIG_DIR / "config.json"