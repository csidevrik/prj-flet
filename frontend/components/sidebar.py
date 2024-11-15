import flet as ft
from typing import Callable

class Sidebar(ft.UserControl):
    def __init__(self, on_config_click: Callable):
        super().__init__()
        self.on_config_click = on_config_click
        
    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.IconButton(
                            icon=ft.icons.MAIL_OUTLINE,
                            icon_color="blue",
                            icon_size=24,
                            tooltip="Nuevo correo",
                            on_click=self._on_new_mail
                        ),
                        margin=10
                    ),
                    ft.Container(
                        content=ft.IconButton(
                            icon=ft.icons.SETTINGS,
                            icon_size=24,
                            tooltip="Configuración",
                            on_click=self.on_config_click
                        ),
                        margin=10
                    ),
                    ft.Container(
                        content=ft.IconButton(
                            icon=ft.icons.HELP_OUTLINE,
                            icon_size=24,
                            tooltip="Ayuda",
                            on_click=self._on_help
                        ),
                        margin=10
                    ),
                ]
            ),
            bgcolor=ft.colors.BLUE_GREY_50,
            width=60,
            border=ft.border.all(1, ft.colors.BLUE_GREY_200)
        )
    
    def _on_new_mail(self, e):
        # Implementar lógica para nuevo correo
        pass
    
    def _on_help(self, e):
        # Implementar lógica para ayuda
        pass