import flet as ft
import logging
from backend.services.email_service import EmailService
from backend.services.storage_service import StorageService
from backend.config.email_config import EmailConfig

logger = logging.getLogger(__name__)

class SettingsView(ft.UserControl):
    def __init__(self, email_service: EmailService):
        super().__init__()
        self.email_service = email_service
        self.storage_service = StorageService()
        
    def build(self):
        # Campos de configuración
        self.server_input = ft.TextField(
            label="Servidor SMTP",
            value=self.email_service.config.smtp_server if self.email_service.config else "",
            helper_text="Ejemplo: mail.emov.gob.ec",
            prefix_icon=ft.icons.DNS,
            width=400
        )
        
        self.port_input = ft.TextField(
            label="Puerto SMTP",
            value=str(self.email_service.config.smtp_port if self.email_service.config else "465"),
            helper_text="Puerto SMTPS (normalmente 465)",
            prefix_icon=ft.icons.NUMBERS,
            width=400
        )
        
        self.email_input = ft.TextField(
            label="Correo electrónico",
            value=self.email_service.config.email if self.email_service.config else "",
            helper_text="Ejemplo: usuario@emov.gob.ec",
            prefix_icon=ft.icons.EMAIL,
            width=400
        )
        
        self.password_input = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.icons.LOCK,
            width=400
        )
        
        # Indicador de estado
        self.status_row = ft.Row(
            controls=[
                ft.ProgressRing(width=16, height=16, visible=False),
                ft.Text("", size=14)
            ],
            visible=False
        )
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Encabezado con botón de regreso
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                icon_color=ft.colors.BLUE,
                                tooltip="Volver",
                                on_click=self.go_back
                            ),
                            ft.Text(
                                "Configuración",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.BLUE
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START
                    ),
                    ft.Divider(),
                    
                    # Sección de configuración de correo
                    ft.Text(
                        "Configuración de Correo",
                        size=16,
                        weight=ft.FontWeight.BOLD
                    ),
                    self.server_input,
                    self.port_input,
                    self.email_input,
                    self.password_input,
                    
                    # Estado y mensajes
                    self.status_row,
                    
                    # Botones de acción
                    ft.Row(
                        controls=[
                            ft.FilledTonalButton(
                                "Probar Conexión",
                                icon=ft.icons.NETWORK_CHECK,
                                on_click=self.test_connection
                            ),
                            ft.FilledButton(
                                "Guardar Cambios",
                                icon=ft.icons.SAVE,
                                on_click=self.save_settings
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                spacing=20
            ),
            padding=30
        )
    
    def show_status(self, message: str, is_error: bool = False, show_progress: bool = False):
        """Muestra un mensaje de estado"""
        self.status_row.controls[0].visible = show_progress
        self.status_row.controls[1].value = message
        self.status_row.controls[1].color = "red" if is_error else "green"
        self.status_row.visible = True
        self.update()
    
    def validate_inputs(self) -> tuple[bool, str]:
        """Valida los campos de entrada"""
        if not self.server_input.value:
            return False, "Por favor ingrese el servidor SMTP"
        if not self.email_input.value:
            return False, "Por favor ingrese el correo electrónico"
        if not self.password_input.value and not self.email_service.config:
            return False, "Por favor ingrese la contraseña"
        try:
            port = int(self.port_input.value)
            if port <= 0 or port > 65535:
                return False, "Puerto inválido"
        except ValueError:
            return False, "El puerto debe ser un número"
        return True, ""
    
    async def test_connection(self, e):
        """Prueba la conexión con el servidor"""
        is_valid, error_message = self.validate_inputs()
        if not is_valid:
            self.show_status(error_message, is_error=True)
            return
            
        self.show_status("Probando conexión...", show_progress=True)
        
        try:
            # Crear configuración de prueba
            config = EmailConfig(
                smtp_server=self.server_input.value,
                smtp_port=int(self.port_input.value),
                email=self.email_input.value,
                password=self.password_input.value or self.email_service.config.password
            )
            
            # Probar conexión
            success, message = self.email_service.test_connection(config)
            
            if success:
                self.show_status("✓ Conexión exitosa", is_error=False)
            else:
                self.show_status(f"✗ Error: {message}", is_error=True)
                
        except Exception as e:
            logger.error(f"Error probando conexión: {str(e)}")
            self.show_status(f"✗ Error: {str(e)}", is_error=True)
    
    async def save_settings(self, e):
        """Guarda la configuración"""
        is_valid, error_message = self.validate_inputs()
        if not is_valid:
            self.show_status(error_message, is_error=True)
            return
        
        # Deshabilitar botones mientras se guarda
        for control in self.content.controls[-1].controls[-1].controls:
            control.disabled = True
        self.update()
        
        try:
            self.show_status("Guardando configuración...", show_progress=True)
            
            # Crear nueva configuración
            config = EmailConfig(
                smtp_server=self.server_input.value,
                smtp_port=int(self.port_input.value),
                email=self.email_input.value,
                # Si no hay nueva contraseña, mantener la anterior
                password=self.password_input.value or self.email_service.config.password if self.email_service.config else self.password_input.value
            )
            
            # Probar conexión antes de guardar
            success, message = self.email_service.test_connection(config)
            
            if success:
                # Guardar configuración
                if self.storage_service.save_config(config):
                    # Actualizar la configuración en el servicio de email
                    self.email_service.config = config
                    self.email_service.is_connected = True
                    
                    self.show_status("✓ Configuración guardada exitosamente")
                    
                    # Usar ft.ProgressBar en lugar de sleep
                    self.show_success_and_return()
                else:
                    self.show_status("Error guardando configuración", is_error=True)
            else:
                self.show_status(f"Error de conexión: {message}", is_error=True)
                
        except Exception as e:
            logger.error(f"Error guardando configuración: {str(e)}")
            self.show_status(f"Error: {str(e)}", is_error=True)
        finally:
            # Rehabilitar botones
            for control in self.content.controls[-1].controls[-1].controls:
                control.disabled = False
            self.update()
    
    def show_success_and_return(self):
        """Muestra mensaje de éxito y regresa a la vista principal"""
        def return_to_main(e):
            self.snack_bar.open = False
            self.page.update()
            self.go_back(None)
        
        # Crear Snackbar
        self.snack_bar = ft.SnackBar(
            content=ft.Text("Configuración guardada exitosamente"),
            action="OK",
            action_color=ft.colors.WHITE,
            bgcolor=ft.colors.GREEN_400
        )
        
        # Mostrar Snackbar
        self.page.show_snack_bar(self.snack_bar)
        
        # Programar el retorno después de 2 segundos
        self.page.after(2, return_to_main)
    
    def show_success_message(self, message: str):
        """Muestra un mensaje de éxito"""
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.colors.GREEN_400
            )
        )
    
    def go_back(self, e):
        """Regresa a la vista principal"""
        self.page.go("/")
    
    def show_error(self, message: str):
        """Muestra un diálogo de error"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()
            
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("Cerrar", on_click=close_dialog)
            ]
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()