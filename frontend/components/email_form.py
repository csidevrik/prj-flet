import flet as ft
from typing import List, Optional
import os
from backend.services.email_service import EmailService
from backend.utils.validators import validate_email

class EmailForm(ft.UserControl):
    def __init__(self, email_service: EmailService):
        super().__init__()
        self.email_service = email_service
        self.selected_files: List[dict] = []
    
    def build(self):
        # Crear el selector de archivos
        self.pick_files_dialog = ft.FilePicker(
            on_result=self.on_file_picked
        )
        
        # Asegurarse de que el FilePicker esté disponible en la página
        self.page.overlay.append(self.pick_files_dialog)
        
        # Campo para correos destinatarios
        self.emails_input = ft.TextField(
            label="Para",
            multiline=True,
            min_lines=2,
            max_lines=5,
            helper_text="Ingrese los correos separados por comas",
            prefix_icon=ft.icons.EMAIL,
            border_color=ft.colors.BLUE_400,
            focused_border_color=ft.colors.BLUE,
            hint_text="ejemplo@dominio.com, ejemplo2@dominio.com"
        )
        
        # Campo para el asunto
        self.subject_input = ft.TextField(
            label="Asunto",
            value="Notificación de Póliza",
            prefix_icon=ft.icons.SUBJECT,
            border_color=ft.colors.BLUE_400,
            focused_border_color=ft.colors.BLUE
        )
        
        # Campo para el mensaje
        self.message_input = ft.TextField(
            label="Mensaje",
            multiline=True,
            min_lines=5,
            max_lines=10,
            prefix_icon=ft.icons.MESSAGE,
            border_color=ft.colors.BLUE_400,
            focused_border_color=ft.colors.BLUE
        )
        
        # Lista de archivos adjuntos
        self.files_column = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            height=150
        )
        
        # Contenedor para la lista de archivos
        self.files_container = ft.Container(
            content=self.files_column,
            border=ft.border.all(1, ft.colors.BLUE_200),
            border_radius=5,
            padding=10,
            visible=False
        )
        
        # Barra de estado
        self.status_bar = ft.Text(
            color=ft.colors.BLUE_GREY_400,
            size=12,
            visible=False
        )
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "Nuevo Correo",
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.colors.BLUE
                                    ),
                                    self.emails_input,
                                    self.subject_input,
                                    self.message_input,
                                    ft.Row(
                                        controls=[
                                            ft.ElevatedButton(
                                                "Adjuntar PDF",
                                                icon=ft.icons.ATTACH_FILE,
                                                on_click=lambda _: self.pick_files_dialog.pick_files(
                                                    allow_multiple=True,
                                                    file_type=ft.FilePickerFileType.CUSTOM,
                                                    allowed_extensions=["pdf"]
                                                )
                                            ),
                                            ft.Text(
                                                "Máximo 25MB por archivo",
                                                color=ft.colors.BLUE_GREY_400,
                                                size=12,
                                                italic=True
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    ),
                                    self.files_container,
                                    self.status_bar,
                                    ft.Row(
                                        controls=[
                                            ft.ElevatedButton(
                                                "Enviar",
                                                icon=ft.icons.SEND,
                                                on_click=self.send_email,
                                                bgcolor=ft.colors.BLUE,
                                                color=ft.colors.WHITE
                                            ),
                                            ft.OutlinedButton(
                                                "Limpiar",
                                                icon=ft.icons.CLEAR,
                                                on_click=self.clear_form
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.END
                                    )
                                ],
                                spacing=20
                            ),
                            padding=20
                        )
                    )
                ]
            ),
            padding=20
        )
        
    def validate_form(self) -> tuple[bool, str]:
        """Valida el formulario antes de enviar"""
        if not self.emails_input.value:
            return False, "Por favor ingrese al menos un correo destinatario"
            
        # Validar correos
        emails = [e.strip() for e in self.emails_input.value.split(",")]
        for email in emails:
            if not validate_email(email):
                return False, f"El correo '{email}' no es válido"
        
        if not self.subject_input.value:
            return False, "Por favor ingrese un asunto"
            
        if not self.message_input.value:
            return False, "Por favor ingrese un mensaje"
            
        return True, ""
    
    def on_file_picked(self, e: ft.FilePickerResultEvent):
        """Maneja la selección de archivos"""
        if e.files:
            for file in e.files:
                # Validar tamaño del archivo (máximo 25MB)
                file_size_mb = os.path.getsize(file.path) / (1024 * 1024)
                if file_size_mb > 25:
                    self.show_error(f"El archivo {file.name} excede el límite de 25MB")
                    continue
                
                file_info = {
                    'name': file.name,
                    'path': file.path,
                    'size': file_size_mb
                }
                self.selected_files.append(file_info)
                self.files_column.controls.append(
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.DESCRIPTION, color=ft.colors.BLUE),
                            ft.Text(
                                f"{file.name} ({self.format_size(file_size_mb)})",
                                expand=True,
                                color=ft.colors.BLUE_GREY_800
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_color=ft.colors.RED_400,
                                icon_size=16,
                                tooltip="Eliminar archivo",
                                on_click=lambda x, f=file_info: self.remove_file(f)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                )
            
            self.files_container.visible = True
            self.update_status()
            self.update()
    
    def remove_file(self, file_info: dict):
        """Elimina un archivo de la lista"""
        self.selected_files.remove(file_info)
        self.files_column.controls = [
            control for control in self.files_column.controls 
            if control.controls[1].value.split(" (")[0] != file_info['name']
        ]
        
        if not self.selected_files:
            self.files_container.visible = False
            
        self.update_status()
        self.update()
    
    def format_size(self, size_mb: float) -> str:
        """Formatea el tamaño del archivo"""
        return f"{size_mb:.1f}MB"
    
    def update_status(self):
        """Actualiza la barra de estado"""
        total_size = sum(file['size'] for file in self.selected_files)
        self.status_bar.value = (
            f"Archivos adjuntos: {len(self.selected_files)} "
            f"(Total: {self.format_size(total_size)})"
        )
        self.status_bar.visible = bool(self.selected_files)
    
    def send_email(self, e):
        """Envía el correo electrónico"""
        # Validar formulario
        is_valid, error_message = self.validate_form()
        if not is_valid:
            self.show_error(error_message)
            return
        
        # Obtener destinatarios
        to_emails = [email.strip() for email in self.emails_input.value.split(",")]
        
        # Obtener rutas de archivos adjuntos
        attachments = [f['path'] for f in self.selected_files]
        
        # Mostrar indicador de progreso
        self.show_progress("Enviando correo...")
        
        # Enviar correo
        success, message = self.email_service.send_email(
            to_emails=to_emails,
            subject=self.subject_input.value,
            body=self.message_input.value,
            attachments=attachments
        )
        
        # Ocultar indicador de progreso
        self.hide_progress()
        
        if success:
            self.show_success("Correo enviado exitosamente")
            self.clear_form(None)
        else:
            self.show_error(f"Error al enviar el correo: {message}")
    
    def clear_form(self, e):
        """Limpia el formulario"""
        self.emails_input.value = ""
        self.subject_input.value = "Notificación de Póliza"
        self.message_input.value = ""
        self.selected_files.clear()
        self.files_column.controls.clear()
        self.files_container.visible = False
        self.status_bar.visible = False
        self.update()
    
    def show_error(self, message: str):
        """Muestra un mensaje de error"""
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
    
    def show_success(self, message: str):
        """Muestra un mensaje de éxito"""
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(message),
                bgcolor=ft.colors.GREEN_400
            )
        )
    
    def show_progress(self, message: str):
        """Muestra un diálogo de progreso"""
        self.progress_dialog = ft.AlertDialog(
            content=ft.Column(
                controls=[
                    ft.ProgressRing(),
                    ft.Text(message)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        self.page.dialog = self.progress_dialog
        self.progress_dialog.open = True
        self.page.update()
    
    def hide_progress(self):
        """Oculta el diálogo de progreso"""
        if hasattr(self, 'progress_dialog'):
            self.progress_dialog.open = False
            self.page.update()