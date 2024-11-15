import flet as ft
from ..components import EmailForm, Sidebar
from backend.services.email_service import EmailService

class MainView(ft.UserControl):
    def __init__(self, email_service: EmailService):
        super().__init__()
        self.email_service = email_service
        
    def build(self):
        # Componentes principales
        self.email_form = EmailForm(self.email_service)
        self.sidebar = Sidebar(on_config_click=self.show_settings)
        
        # Estado de conexión
        self.connection_status = ft.Text(
            value="No conectado",
            color="red",
            size=12
        )
        
        # Contenedor principal con padding
        main_content = ft.Container(
            content=ft.Column(
                controls=[
                    self.connection_status,
                    self.email_form
                ],
                expand=True,
                spacing=20,
            ),
            padding=20
        )
        
        return ft.Row(
            controls=[
                self.sidebar,
                ft.VerticalDivider(width=1),
                main_content
            ],
            expand=True
        )
    
    def show_settings(self, e):
        self.page.go("/settings")
    
    def update_connection_status(self):
        is_connected = self.email_service.is_connected
        self.connection_status.value = (
            f"Conectado como {self.email_service.config.email}"
            if is_connected else "No conectado"
        )
        self.connection_status.color = "green" if is_connected else "red"
        self.connection_status.update()