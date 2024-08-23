import flet as ft
import asyncio
from main_window_config import setup_window
from main_event_handler import WindowEventHandler
from main_ui_components import create_appbar, create_main_layout
from main_loader import Loader

async def main(page: ft.Page):
    # Inicializar el loader
    loader = Loader(page)

    # Mostrar el loader
    await loader.show_loader()

    # Simular un tiempo de carga (puedes usar esta parte para cargar recursos, etc.)
    await asyncio.sleep(2)  # Simula un retraso de 2 segundos

    # Configurar la ventana principal
    setup_window(page)

    # Inicializar el manejador de eventos
    event_handler = WindowEventHandler(page)

    # Configurar la UI principal
    page.appbar = create_appbar(event_handler)
    page.add(create_main_layout())

    # Ocultar el loader
    await loader.hide_loader()

    # Agregar más elementos o configuraciones si es necesario

# Ejecutar la aplicación
ft.app(target=main, assets_dir="assets")
