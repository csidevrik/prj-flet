import flet as ft
import logging
from backend.services.email_service import EmailService
from backend.services.storage_service import StorageService
from .views import MainView, SettingsView

logger = logging.getLogger(__name__)

class EmailClientApp:
    def __init__(self):
        self.email_service = EmailService()
        self.storage_service = StorageService()
        
    def main(self, page: ft.Page):
        page.title = "Cliente de Correo"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window_width = 1000
        page.window_height = 800
        page.window_min_width = 800
        page.window_min_height = 600
        
        def route_change(route):
            page.views.clear()
            
            if page.route == "/settings":
                page.views.append(
                    ft.View(
                        route="/settings",
                        controls=[SettingsView(self.email_service)]
                    )
                )
            else:
                page.views.append(
                    ft.View(
                        route="/",
                        controls=[MainView(self.email_service)]
                    )
                )
            
            page.update()
        
        def view_pop(view):
            page.views.pop()
            page.go(page.views[-1].route)
        
        page.on_route_change = route_change
        page.on_view_pop = view_pop
        
        # Cargar configuración guardada
        saved_config = self.storage_service.load_config()
        if saved_config:
            success, message = self.email_service.connect(saved_config)
            if success:
                logger.info("Conexión automática establecida")
            else:
                logger.error(f"Error en conexión automática: {message}")
        
        # Iniciar en la vista principal
        page.go("/")

    def show_error(self, message: str):
        """Muestra un mensaje de error al usuario"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()
            
        dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("Cerrar", on_click=close_dialog)
            ]
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()