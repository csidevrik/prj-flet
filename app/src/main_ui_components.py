import flet as ft

def create_appbar(event_handler):
    return ft.AppBar(
        leading=ft.Icon(ft.icons.WEB),
        title=ft.Text("PAYMENTS"),
        center_title=False,
        bgcolor="#18684d",  # Usar color primario
        actions=[
            ft.IconButton(ft.icons.MINIMIZE_SHARP, icon_color="#222222", on_click=event_handler.button_minimize),
            ft.IconButton(ft.icons.MAXIMIZE_ROUNDED, icon_color="#222222", on_click=event_handler.button_maximize),
            ft.IconButton(ft.icons.EXIT_TO_APP, icon_color="#222222", on_click=event_handler.button_exit),
        ],
    )

def create_main_layout():
    # Suponiendo que aquí creas una fila principal con algunos elementos
    row = ft.Row(
        controls=[
            ft.Text("Hola, mundo!"),
            ft.ElevatedButton(text="Click me"),
        ],
        alignment="center",
        vertical_alignment="center",
        expand=True
    )
    return row
    pass
