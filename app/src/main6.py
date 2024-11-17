import flet as ft
import os
from flet import (
    Column, 
    Container, 
    IconButton, 
    Page, 
    Row, 
    Text, 
    TextField,
    FilePicker,
    FilePickerResultEvent,
    TextButton,
    icons,
)

class EmailClient:
    def __init__(self):
        self.selected_files = []
        
    def main(self, page: Page):
        page.title = "Cliente de Correo"
        page.padding = 0
        
        # Creamos el selector de archivos PDF
        self.pick_files_dialog = FilePicker(
            on_result=self.on_file_picked
        )
        page.overlay.append(self.pick_files_dialog)
        
        # Campo para correos destinatarios
        self.emails_input = TextField(
            label="Correos destinatarios",
            multiline=True,
            min_lines=2,
            max_lines=5,
            helper_text="Ingrese los correos separados por comas"
        )
        
        # Campo para el asunto
        self.subject_input = TextField(
            label="Asunto",
            value="Notificación de Póliza"
        )
        
        # Campo para el mensaje
        self.message_input = TextField(
            label="Mensaje",
            multiline=True,
            min_lines=5,
            max_lines=10
        )
        
        # Lista de archivos seleccionados
        self.files_list = Column(spacing=10)
        
        # Contenido principal
        main_content = Container(
            content=Column(
                controls=[
                    Text("Nuevo Correo", size=24, weight="bold"),
                    self.emails_input,
                    self.subject_input,
                    self.message_input,
                    Container(
                        content=Row(
                            controls=[
                                TextButton(
                                    "Adjuntar PDF",
                                    icon=icons.ATTACH_FILE,
                                    on_click=lambda _: self.pick_files_dialog.pick_files(
                                        allow_multiple=True,
                                        file_type=ft.FilePickerFileType.CUSTOM,
                                        allowed_extensions=["pdf"]
                                    )
                                )
                            ]
                        )
                    ),
                    self.files_list,
                    TextButton(
                        "Enviar",
                        icon=icons.SEND,
                        on_click=self.send_email
                    )
                ],
                spacing=20,
                scroll=ft.ScrollMode.AUTO
            ),
            padding=20,
            expand=True
        )
        
        # Menú lateral
        sidebar = Container(
            content=Column(
                controls=[
                    Container(
                        content=IconButton(
                            icon=icons.MAIL_OUTLINE,
                            icon_color="blue",
                            icon_size=24,
                            tooltip="Nuevo correo"
                        ),
                        margin=10
                    ),
                    Container(
                        content=IconButton(
                            icon=icons.INBOX,
                            icon_size=24,
                            tooltip="Bandeja de entrada"
                        ),
                        margin=10
                    ),
                    Container(
                        content=IconButton(
                            icon=icons.SEND,
                            icon_size=24,
                            tooltip="Enviados"
                        ),
                        margin=10
                    ),
                    Container(
                        content=IconButton(
                            icon=icons.DELETE,
                            icon_size=24,
                            tooltip="Papelera"
                        ),
                        margin=10
                    ),
                ]
            ),
            bgcolor=ft.colors.BLUE_GREY_50,
            width=60,
            height=page.height
        )
        
        # Layout principal
        page.add(
            Row(
                controls=[
                    sidebar,
                    ft.VerticalDivider(width=1),
                    main_content
                ],
                spacing=0,
                expand=True
            )
        )
    
    def on_file_picked(self, e: FilePickerResultEvent):
        if e.files:
            for file in e.files:
                self.selected_files.append(file)
                self.files_list.controls.append(
                    Row(
                        controls=[
                            Text(file.name),
                            IconButton(
                                icon=icons.DELETE,
                                icon_size=16,
                                on_click=lambda file=file: self.remove_file(file)
                            )
                        ]
                    )
                )
            self.files_list.update()
    
    def remove_file(self, file):
        self.selected_files.remove(file)
        for control in self.files_list.controls:
            if control.controls[0].value == file.name:
                self.files_list.controls.remove(control)
                break
        self.files_list.update()
    
    def send_email(self, e):
        # Aquí implementarías la lógica de envío de correo
        print("Enviando correo...")
        print(f"Destinatarios: {self.emails_input.value}")
        print(f"Asunto: {self.subject_input.value}")
        print(f"Mensaje: {self.message_input.value}")
        print(f"Archivos adjuntos: {[f.name for f in self.selected_files]}")

def main():
    app = EmailClient()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()