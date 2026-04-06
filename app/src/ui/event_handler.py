import flet as ft

class WindowEventHandler:
    def __init__(self, page: ft.Page):
        self.page = page

    async def button_exit(self, e):
        await self.page.window.close()

    async def button_maximize(self, e):
        self.page.window.height = 1080
        self.page.window.width = 1920
        self.page.update()

    async def button_minimize(self, e):
        self.page.window.minimized = True
        self.page.update()
