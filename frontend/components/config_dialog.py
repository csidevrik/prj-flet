import flet as ft
from typing import Callable, Optional
import logging
from backend.services.email_service import EmailService
from backend.services.storage_service import StorageService
from backend.config.email_config import EmailConfig

logger = logging.getLogger(__name__)

class ConfigDialog(ft.UserControl):
    def __init__(self, email_service: EmailService, on_close: Callable[[bool], None]):
        """
        Inicializa el diálogo de configuración.
        
        Args:
            email_service: Servicio de email para la conexión
            on_close: Callback que se ejecuta al cerrar el diálogo
        """
        super().__init__()
        self.email_service = email_service
        self.storage_service = StorageService()
        self.on_close = on_close
        self.is_testing = False
        
    def build(self):
        # Campos de entrada
        self.server_input = ft.TextField(
            label="Servidor SMTP",
            value=self.email_service.config.smtp_server if self.email_service.config else "",
            helper_text="Ejemplo: mail.emov.gob.ec",
            prefix_icon=ft.icons.DNS,
            border_color=ft.colors.BLUE_400,
            focused_border_color=ft.colors.BLUE,
            width=400
        )
        
        self.email_input = ft.TextField(
            label="Correo electrónico",
            value=self.email_service.config.email if self.email_service.config else "",
            helper_text="Ejemplo: usuario@emov.gob.ec",
            prefix_icon=ft.icons.EMAIL,
            border_color=ft.colors.BLUE_400,
            focused_border_color=ft.colors.BLUE,
            width=400
        )
        
        self.password_input = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.icons.LOCK,
            border_color=ft.colors.BLUE_400,
            focused_border_color=ft.colors.BLUE,
            width=400
        )
        
        # Configuración avanzada (inicialmente oculta)
        self.port_input = ft.TextField(
            label="Puerto SMTP",
            value=str(self.email_service.config.smtp_port if self.email_service.config else "465"),
            helper_text="Puerto SMTPS (normalmente 465)",
            prefix_icon=ft.icons.NUMBERS,
            border_color=ft.colors.BLUE_400,
            focused_border_color=ft.colors.BLUE,
            width=400
        )
        
        # Indicador de estado
        self.status_row = ft.Row(
            controls=[
                ft.ProgressRing(visible=False, width=16, height=16),
                ft.Text("", color="green")
            ],
            visible=False
        )
        
        # Botón para mostrar/ocultar configuración avanzada
        self.advanced_button = ft.TextButton(
            "Mostrar configuración avanzada",
            icon=ft.icons.ARROW_DROP_DOWN,
            on_click=self.toggle_advanced
        )
        
        # Contenedor de configuración avanzada
        self.advanced_container = ft.Container(
            content=ft.Column(
                controls=[
                    self.port_input,
                    ft.Row(
                        controls=[
                            ft.Text("Conexión segura:", size=14),
                            ft.Switch(value=True, active_color=ft.colors.BLUE)
                        ]
                    )
                ]
            ),
            visible=False
        )
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Encabezado
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.SETTINGS, color=ft.colors.BLUE),
                            ft.Text(
                                "Configuración de Correo",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.BLUE
                            )
                        ]
                    ),
                    ft.Divider(),
                    
                    # Campos principales
                    self.server_input,
                    self.email_input,
                    self.password_input,
                    
                    # Sección avanzada
                    self.advanced_button,
                    self.advanced_container,
                    
                    # Estado y mensajes
                    self.status_row,
                    
                    ft.Divider(),
                    
                    # Botones de acción
                    ft.Row(
                        controls=[
                            ft.FilledButton(
                                "Probar conexión",
                                icon=ft.icons.NETWORK_CHECK,
                                on_click=self.test_connection
                            ),
                            ft.FilledButton(
                                "Guardar",
                                icon=ft.icons.SAVE,
                                bgcolor=ft.colors.BLUE,
                                on_click=self.save_clicked
                            ),
                            ft.OutlinedButton(
                                "Cancelar",
                                icon=ft.icons.CANCEL,
                                on_click=self.cancel_clicked
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END
                    )
                ],
                tight=True,
                spacing=20
            ),
            padding=30,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            width=500
        )
    
    def toggle_advanced(self, e):
        """Muestra u oculta la configuración avanzada"""
        self.advanced_container.visible = not self.advanced_container.visible
        self.advanced_button.icon = (
            ft.icons.ARROW_DROP_UP if self.advanced_container.visible 
            else ft.icons.ARROW_DROP_DOWN
        )
        self.advanced_button.text = (
            "Ocultar configuración avanzada" if self.advanced_container.visible
            else "Mostrar configuración avanzada"
        )
        self.update()
    
    def show_status(self, message: str, is_error: bool = False):
        """Muestra un mensaje de estado"""
        self.status_row.controls[1].value = message
        self.status_row.controls[1].color = "red" if is_error else "green"
        self.status_row.visible = True
        self.status_row.controls[0].visible = False
        self.update()
    
    def show_progress(self, message: str = "Conectando..."):
        """Muestra el indicador de progreso"""
        self.status_row.controls[1].value = message
        self.status_row.controls[1].color = ft.colors.BLUE
        self.status_row.visible = True
        self.status_row.controls[0].visible = True
        self.update()
    
    def validate_inputs(self) -> tuple[bool, str]:
        """Valida los campos de entrada"""
        if not self.server_input.value:
            return False, "Por favor ingrese el servidor SMTP"
        if not self.email_input.value:
            return False, "Por favor ingrese el correo electrónico"
        if not self.password_input.value:
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
        if self.is_testing:
            return
            
        # Validar campos
        is_valid, error_message = self.validate_inputs()
        if not is_valid:
            self.show_status(error_message, is_error=True)
            return
        
        self.is_testing = True
        self.show_progress("Probando conexión...")
        
        try:
            # Crear configuración temporal
            config = EmailConfig(
                smtp_server=self.server_input.value,
                smtp_port=int(self.port_input.value),
                email=self.email_input.value,
                password=self.password_input.value
            )
            
            # Intentar conexión
            success, message = self.email_service.connect(config)
            
            if success:
                self.show_status("Conexión exitosa")
            else:
                self.show_status(f"Error de conexión: {message}", is_error=True)
                
        except Exception as e:
            logger.error(f"Error probando conexión: {str(e)}")
            self.show_status(f"Error: {str(e)}", is_error=True)
        
        finally:
            self.is_testing = False
    
    def save_clicked(self, e):
        """Guarda la configuración"""
        # Validar campos
        is_valid, error_message = self.validate_inputs()
        if not is_valid:
            self.show_status(error_message, is_error=True)
            return
        
        self.show_progress("Guardando configuración...")
        
        try:
            # Crear configuración
            config = EmailConfig(
                smtp_server=self.server_input.value,
                smtp_port=int(self.port_input.value),
                email=self.email_input.value,
                password=self.password_input.value
            )
            
            # Probar conexión antes de guardar
            success, message = self.email_service.connect(config)
            
            if success:
                # Guardar configuración
                if self.storage_service.save_config(config):
                    logger.info("Configuración guardada exitosamente")
                    self.on_close(True)
                else:
                    self.show_status("Error guardando configuración", is_error=True)
            else:
                self.show_status(f"Error de conexión: {message}", is_error=True)
                
        except Exception as e:
            logger.error(f"Error guardando configuración: {str(e)}")
            self.show_status(f"Error: {str(e)}", is_error=True)
    
    def cancel_clicked(self, e):
        """Cierra el diálogo sin guardar"""
        self.on_close(False)
    
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