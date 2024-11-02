import flet as ft
from ui.utils import GRADIENT

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
def panel_submenu():
    return ft.Container

def panel_menu():
    return ft.Container(
        # expand=True,
        gradient=GRADIENT,
        border_radius=3,
        width=160,
    )

def create_main_layout():
    # Suponiendo que aquí creas una fila principal con algunos elementos
    return ft.Row(
        expand=True,
        controls=[
            panel_menu(),
        ],
    )
    # return row
    # pass

