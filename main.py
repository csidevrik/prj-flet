import flet as ft
from frontend.app import EmailClientApp
import logging
from backend.config.settings import setup_logging

def main():
    # Configurar logging
    setup_logging()
    logging.info("Iniciando aplicacion...")
    
    # Iniciar la aplicación
    app = EmailClientApp()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()