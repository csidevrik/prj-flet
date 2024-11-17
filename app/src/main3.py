import math
import flet as ft
from li.gradients import gradient

# VARIABLES
LIMIT_VD1_MAX = 200
LIMIT_VD1_MIN = 100
LIMIT_VD2_MAX = 200
LIMIT_VD2_MIN = 100

COLOR1 = "#18684d"
COLOR2 = "#222222"
COLORR = "#00e8b2"
COLORQ = "#f3ae35"

GRADIENT = ft.LinearGradient(
    begin=ft.alignment.top_left,
    end=ft.Alignment(0.8, 1),
    colors=gradient("Kye Meh"),
    rotation=math.pi / 4.6,
)

class MyApp:
    def __init__(self):
        self.page = None
        self.left01 = None
        self.left02 = None

    async def button_exit(self, e):
        self.page.window.destroy()
        self.page.update()

    async def button_maximize(self, e):
        self.page.window.height = 1080
        self.page.window.width = 1920
        self.page.update()

    async def button_minimize(self, e):
        self.page.window.minimized = True
        self.page.update()

    async def move_vertical_divider1(self, e: ft.DragUpdateEvent):
        if (e.delta_x > 0 and self.left01.width < LIMIT_VD1_MAX) or (e.delta_x < 0 and self.left01.width > LIMIT_VD1_MIN):
            self.left01.width += e.delta_x
        self.left01.update()

    async def move_vertical_divider2(self, e: ft.DragUpdateEvent):
        if (e.delta_x > 0 and self.left02.width < LIMIT_VD2_MAX) or (e.delta_x < 0 and self.left02.width > LIMIT_VD2_MIN):
            self.left02.width += e.delta_x
            self.left02.update()

    async def show_draggable_cursor(self, e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        e.control.update()

    def create_appbar(self):
        return ft.AppBar(
            leading=ft.Icon(ft.icons.WEB),
            title=ft.Text("PAYMENTS"),
            center_title=False,
            bgcolor=COLOR1,
            actions=[
                ft.IconButton(ft.icons.MINIMIZE_SHARP, icon_color=COLOR2, on_click=self.button_minimize),
                ft.IconButton(ft.icons.MAXIMIZE_ROUNDED, icon_color=COLOR2, on_click=self.button_maximize),
                ft.IconButton(ft.icons.EXIT_TO_APP, icon_color=COLOR2, on_click=self.button_exit),
            ],
        )

    def create_container(self, content, width, bgcolor, gradient=None, border=None, alignment=None):
        return ft.Container(
            content,
            bgcolor=bgcolor,
            gradient=gradient,
            border=border,
            alignment=alignment,
            width=width,
        )

    async def main(self, page: ft.Page):
        self.page = page
        page.window.height = 600
        page.window.width = 600
        page.window.resizable = True
        page.title = "PAYMENTS"
        page.padding = 0
        page.appbar = self.create_appbar()

        inputSearch = ft.TextField(
            hint_text="SEARCH",
            text_align=ft.TextAlign.CENTER,
            border=ft.InputBorder.UNDERLINE,
            filled=True,
            bgcolor=COLOR1,            
        )

        colu = ft.Column(
            controls=[inputSearch],
            animate_offset=ft.Animation.curve,
        )

        self.left01 = self.create_container(
            colu,
            100,
            COLOR1,
            GRADIENT,
            ft.border.only(left=ft.BorderSide(1, "green")),
            ft.alignment.center_right,
        )

        self.left02 = self.create_container(
            None,
            100,
            COLOR1,
        )

        right01 = self.create_container(
            None,
            None,
            COLOR1,
            alignment=ft.alignment.center,
        )

        gestureDetector1 = ft.GestureDetector(
            content=ft.VerticalDivider(),
            drag_interval=10,
            on_pan_update=self.move_vertical_divider1,
            on_hover=self.show_draggable_cursor,
        )

        gestureDetector2 = ft.GestureDetector(
            content=ft.VerticalDivider(),
            drag_interval=10,
            on_pan_update=self.move_vertical_divider2,
            on_hover=self.show_draggable_cursor,
        )

        row = ft.Row(
            expand=True,
            controls=[
                self.left01,
                gestureDetector1,
                self.left02,
                gestureDetector2,
                right01,
            ]
        )

        container = ft.Container(
            row,
            width=1920,
            height=1080,
            bgcolor=COLOR1,
            expand=True,
        )

        page.add(container)

    def run(self):
        ft.app(target=self.main, assets_dir="assets")

if __name__ == "__main__":
    app = MyApp()
    app.run()
