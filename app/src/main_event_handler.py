import flet as ft

class WindowEventHandler:
    def __init__(self, page: ft.Page):
        self.page = page

    async def button_exit(self, e):
        await self.page.window_destroy_async()
        await self.page.update_async()

    async def button_maximize(self, e):
        self.page.window.height = 1080
        self.page.window.width = 1920
        await self.page.update_async()

    async def button_minimize(self, e):
        self.page.window_minimized = True
        await self.page.update_async()
