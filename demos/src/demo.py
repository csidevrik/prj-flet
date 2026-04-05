import flet as ft

name = "Draggable VerticalDivider"

def main(page: ft.Page):
    page.window.width = 1920
    page.window.height = 1080
    page.title = "facturet"
    page.bgcolor = "#263238"

    def move_vertical_divider(e: ft.DragUpdateEvent):
        dx = e.local_delta.x if e.local_delta else 0
        width = c.width or 300
        if (dx > 0 and width < 800) or (dx < 0 and width > 400):
            c.width = width + dx
        c.update()

    def show_draggable_cursor(e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.RESIZE_LEFT_RIGHT
        e.control.update()

    c = ft.Container(
        bgcolor=ft.Colors.ORANGE_300,
        alignment=ft.Alignment(0.5, 0.5),
        width=300,
        # expand=1,
    )

    fila= ft.Row(
        controls=[
            c,
            ft.GestureDetector(
                content=ft.VerticalDivider(),
                drag_interval=10,
                on_pan_update=move_vertical_divider,
                on_hover=show_draggable_cursor,
            ),
            ft.Container(
                bgcolor= "#263238",
                alignment=ft.Alignment(0.5, 0.5),
                expand=1,
            ),
        ],
        spacing=0,
        width=1920,
        height=1080,
    )




    page.add(fila)
    pass


ft.run(main)