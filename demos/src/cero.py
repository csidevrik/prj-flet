# import flet as ft
# import time

# def main(page: ft.Page):
#     page.title = "Loader Example"
#     page.padding = 20
#     page.bgcolor = "#1b1e34"  # Fondo oscuro similar al de tu ejemplo

#     # Texto que indica el estado de la carga
#     status_text = ft.Text("Checking for updates", color="white", size=20)
    
#     # Barra de progreso
#     progress_bar = ft.ProgressBar(width=600, color="#6ef2ac")  # Color y ancho ajustados

#     # Texto para mostrar el porcentaje
#     percent_text = ft.Text("0% complete", color="#6ef2ac", size=20)

#     # Botón de cancelar
#     cancel_button = ft.TextButton("CANCEL CHECK", on_click=lambda _: page.exit())

#     def update_progress(e):
#         # Simula el progreso
#         for i in range(0, 101, 1):
#             progress_bar.value = i / 100
#             percent_text.value = f"{i}% complete"
#             page.update()
#             # ft.time.sleep(0.1)  # Controla la velocidad de actualización
#             # asyncio.sleep(2)
#             time.sleep(0.3)

#     page.add(status_text, progress_bar, percent_text, cancel_button)
#     update_progress(None)

# ft.app(target=main)
# //////////////////////////

import flet as ft

def main(page: ft.Page):
    page.title = "Lenovo Vantage - Style Interface"
    page.bgcolor = "#f8f9fc"  # Color de fondo claro similar
    page.padding = 20

    # Barra lateral de navegación
    sidebar_items = [
        ft.IconButton(icon=ft.icons.HOME, tooltip="Home"),
        ft.IconButton(icon=ft.icons.SETTINGS, tooltip="Settings"),
        ft.IconButton(icon=ft.icons.DOWNLOAD, tooltip="Downloads"),
        ft.IconButton(icon=ft.icons.POWER, tooltip="Power"),
        ft.IconButton(icon=ft.icons.SHIELD, tooltip="Security"),
        ft.IconButton(icon=ft.icons.HELP, tooltip="Help"),
        ft.IconButton(icon=ft.icons.SHOPPING_CART, tooltip="Shop")
    ]
    sidebar = ft.Column(sidebar_items, spacing=15)

    # Contenido principal
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Quick scan"),
            ft.Tab(text="Manual tests")
        ]
    )
    
    progress_info = ft.Container(
        content=ft.Text("Scanning: Storage (5/14)", size=16, color="#333"),
        bgcolor="#ffffff",
        padding=10,
        border_radius=5
    )
    progress_bar = ft.ProgressBar(value=0.33, color="#0d6efd", width=400)

    runtime_info = ft.Text("Runtime: 24 sec", size=14, color="#666")
    estimated_time = ft.Text("Estimated time: 18 min", size=14, color="#666")

    summary_results = ft.Container(
        content=ft.Column([progress_info, progress_bar, runtime_info, estimated_time], spacing=5),
        bgcolor="#f1f3f6",
        border_radius=10,
        padding=15
    )

    # Botón de cancelar
    cancel_button = ft.TextButton(
        "Cancel",
        # bgcolor="#dc3545",  # Color rojo similar al botón de la imagen
        # color="#ffffff",
        on_click=lambda _: print("Scan cancelled")
    )

    page.add(
        ft.Row([sidebar, ft.VerticalDivider( width=1, color="blue" ), ft.Column([tabs, cancel_button, summary_results], spacing=20)])
    )

ft.app(target=main)
