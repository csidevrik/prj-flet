# import flet as ft

# def main(page: ft.Page):
#     def on_section_click(e):
#         # Update the main content area based on the button clicked
#         if e.control.text == "Settings":
#             main_content.controls = [ft.Text("Settings Content")]
#         elif e.control.text == "Accounts":
#             main_content.controls = [ft.Text("Accounts Content")]
#         main_content.update()

#     sidebar = ft.Column(
#         [
#             ft.TextButton("Settings", on_click=on_section_click),
#             ft.TextButton("Accounts", on_click=on_section_click),
#             # Add more buttons for other sections...
#         ],
#         width=200,
#         # bgcolor=ft.colors.BLUE_GREY_500
#     )

#     main_content = ft.Container(
#         content=ft.Text("Default Content"),
#         expand=True,
#         padding=10,
#     )

#     page.add(ft.Row([sidebar, main_content], expand=True))

# ft.app(target=main)



# '''''''''
# import flet as ft
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
# def main(page: ft.Page):
#     page.title = "Interfaz de aplicación"
#     page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
#     page.scroll = "adaptive"

#     # Primera columna (Menú principal) con color de fondo usando Container
#     menu_principal = ft.Container(
#         content=ft.Column(
#             [
#                 ft.Text("Menú 1"),
#                 ft.Text("Menú 2"),
#                 ft.Text("Menú 3"),
#             ],
#             width=200,
#             height=page.height
#         ),
#         bgcolor="lightgray"
#     )

#     # Segunda columna (Submenús)
#     submenu = ft.Container(
#         content=ft.Column(
#             [
#                 ft.Text("Submenú A"),
#                 ft.Text("Submenú B"),
#                 ft.Text("Submenú C"),
#             ],
#             width=200,
#             height=page.height
#         ),
#         bgcolor="lightgreen"
#     )

#     # Última columna (Área de trabajo)
#     area_trabajo = ft.Container(
#         content=ft.Text("Área de trabajo"),
#         expand=True,
#         bgcolor="white"
#     )

#     # Layout principal
#     layout = ft.Row(
#         [
#             menu_principal,
#             submenu,
#             area_trabajo
#         ],
#         expand=True
#     )

#     page.add(layout)

# ft.app(target=main)

import flet as ft

def main(page: ft.Page):
    page.title = "Página con fondo de gradiente"
    
    # Crear un gradiente lineal
    gradient = ft.LinearGradient(
        begin=ft.alignment.top_left,
        end=ft.alignment.bottom_right,
        colors=["#FF5733", "#C70039", "#900C3F"]
    )
    
    # Container con el gradiente
    background_container = ft.Container(
        content=ft.Text("Contenido de la página", color="white"),
        expand=True,
        gradient=gradient
    )
    
    # Agregar el contenedor a la página
    page.add(background_container)

ft.app(target=main)
