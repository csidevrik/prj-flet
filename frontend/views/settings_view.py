import flet as ft
from backend.services.email_service import EmailService
from backend.services.storage_service import StorageService

class SettingsView(ft.UserControl):
    def __init__(self, email_service: EmailService):
        super().__init__()
        self.email_service = email_service
        self.storage_service = StorageService()
        
    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                on_click=self.go_back
                            ),
                            ft.Text("Configuración", size=24, weight="bold")
                        ]
                    ),
                    ft.Divider(),
                    self._build_email_settings(),
                ],
                spacing=20
            ),
            padding=20
        )
    
    def _build_email_settings(self):
        return ft.Column(
            controls=[
                ft.Text("Configuración de Correo", size=16, weight="bold"),
                ft.TextField(
                    label="Servidor SMTP",
                    value=self.email_service.config.smtp_server if self.email_service.config else "",
                    on_change=self.on_settings_change
                ),
                ft.TextField(
                    label="Puerto SMTP",
                    value=str(self.email_service.config.smtp_port if self.email_service.config else "465"),
                    on_change=self.on_settings_change
                ),
                ft.TextField(
                    label="Correo electrónico",
                    value=self.email_service.config.email if self.email_service.config else "",
                    on_change=self.on_settings_change
                ),
                ft.TextField(
                    label="Contraseña",
                    password=True,
                    can_reveal_password=True,
                    on_change=self.on_settings_change
                ),
                ft.ElevatedButton(
                    "Guardar cambios",
                    on_click=self.save_settings
                )
            ],
            spacing=10
        )
    
    def go_back(self, e):
        self.page.go("/")
    
    def on_settings_change(self, e):
        # Implementar lógica de validación en tiempo real
        pass
    
    def save_settings(self, e):
        # Implementar lógica para guardar configuración
        pass