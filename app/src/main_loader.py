import flet as ft
import asyncio

class Loader:
    def __init__(self, page: ft.Page):
        self.page = page
        self.loader_container = None

    async def show_loader(self):
        # Crear un contenedor que simule un loader
        self.loader_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.ProgressRing(),
                    ft.Text("Cargando la aplicación...", color="white"),
                ],
                alignment="center",
                horizontal_alignment="center",
            ),
            bgcolor="#18684d",  # Color de fondo del loader
            alignment=ft.alignment.center,
            expand=True
        )

        # Agregar el loader a la página y actualizar
        self.page.add(self.loader_container)
        await self.page.update_async()

    async def hide_loader(self):
        # Remover el loader de la página y actualizar
        self.page.controls.remove(self.loader_container)
        await self.page.update_async()
