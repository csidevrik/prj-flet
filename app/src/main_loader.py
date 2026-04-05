import flet as ft

class Loader:
    def __init__(self, page: ft.Page):
        self.page = page
        self.loader_container = None

    def show_loader(self):
        self.loader_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.ProgressRing(),
                    ft.Text("Cargando la aplicación...", color="white"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#18684d",
            alignment=ft.Alignment(0.5, 0.5),
            expand=True
        )
        self.page.add(self.loader_container)

    def hide_loader(self):
        if self.loader_container:
            self.page.remove(self.loader_container)
