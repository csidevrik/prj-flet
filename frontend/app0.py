import flet as ft
import pandas as pd
from typing import List, Dict

class LocalesApp:
    def __init__(self):
        self.df = None
        self.load_data()
        
    def load_data(self):
        # Aquí cargaríamos el archivo Excel, por ahora usamos los datos como lista
        data = []
        # Agregamos algunos registros de ejemplo desde tus datos
        data.append({
            "nombre_local": "FARMASOL",
            "propietario": "PILLCO MOROCHO JIMMY FRANCISCO",
            "ruc": "0104842992",
            "direccion": "S. Bolivar 5-52 y H. Miguel",
            "email": "jimmypillco2781@gmail.com",
            "telefono": "0987280532",
            "valor": 0.00
        })
        self.df = pd.DataFrame(data)

    def main_page(self, page: ft.Page):
        page.title = "Gestión de Locales"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20

        # Barra de búsqueda
        search_field = ft.TextField(
            label="Buscar local",
            width=300,
            prefix_icon=ft.icons.SEARCH,
        )

        # Lista de locales
        locales_list = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
        )

        def update_list(e=None):
            locales_list.controls.clear()
            search_term = search_field.value.lower() if search_field.value else ""
            
            for _, row in self.df.iterrows():
                if search_term in row['nombre_local'].lower():
                    local_card = ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.ListTile(
                                        leading=ft.Icon(ft.icons.STORE),
                                        title=ft.Text(row['nombre_local'], size=16, weight=ft.FontWeight.BOLD),
                                        subtitle=ft.Text(row['direccion']),
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.Text(f"Tel: {row['telefono']}", size=12),
                                            ft.Text(f"Valor: ${row['valor']:.2f}", size=12),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ),
                                ],
                            ),
                            padding=10,
                        )
                    )
                    locales_list.controls.append(local_card)
            
            page.update()

        # Estadísticas
        stats_row = ft.Row(
            controls=[
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Total Locales", size=14),
                                ft.Text(str(len(self.df)), size=20, weight=ft.FontWeight.BOLD),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=15,
                    ),
                ),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Total Ventas", size=14),
                                ft.Text(f"${self.df['valor'].sum():.2f}", size=20, weight=ft.FontWeight.BOLD),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=15,
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )

        search_field.on_change = update_list

        # Construir la página
        page.add(
            ft.Text("Gestión de Locales Comerciales", size=24, weight=ft.FontWeight.BOLD),
            search_field,
            stats_row,
            locales_list,
        )
        
        update_list()

def main():
    app = LocalesApp()
    ft.app(target=app.main_page)

if __name__ == "__main__":
    main()