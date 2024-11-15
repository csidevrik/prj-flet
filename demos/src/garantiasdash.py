import flet as ft
from datetime import datetime, timedelta
import sqlite3
from dateutil.relativedelta import relativedelta

class GarantiasDashboard:
    def __init__(self):
        self.conn = sqlite3.connect('garantias.db')
        self.cursor = self.conn.cursor()
    
    def get_stats(self):
        # Obtener estadísticas generales
        garantias_activas = self.cursor.execute("""
            SELECT COUNT(*), SUM(monto_original)
            FROM garantia 
            WHERE estado = 'VIGENTE'
        """).fetchone()
        
        # Garantías próximas a vencer (próximos 30 días)
        fecha_limite = datetime.now() + timedelta(days=30)
        proximas_vencer = self.cursor.execute("""
            SELECT COUNT(*)
            FROM garantia 
            WHERE fecha_vencimiento <= ? 
            AND estado = 'VIGENTE'
        """, (fecha_limite.date(),)).fetchone()
        
        return {
            'total_garantias': garantias_activas[0],
            'monto_total': garantias_activas[1],
            'proximas_vencer': proximas_vencer[0]
        }
    
    def get_garantias_por_vencer(self):
        # Obtener lista de garantías próximas a vencer
        self.cursor.execute("""
            SELECT g.numero_garantia, c.razon_social, g.fecha_vencimiento, 
                   g.monto_original, JULIANDAY(g.fecha_vencimiento) - JULIANDAY('now') as dias
            FROM garantia g
            JOIN contrato ct ON g.contrato_id = ct.contrato_id
            JOIN contratista c ON ct.contratista_id = c.contratista_id
            WHERE g.estado = 'VIGENTE'
            AND g.fecha_vencimiento <= date('now', '+30 days')
            ORDER BY g.fecha_vencimiento
        """)
        return self.cursor.fetchall()

def main(page: ft.Page):
    page.title = "Dashboard de Garantías"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    # Inicializar dashboard
    dashboard = GarantiasDashboard()
    stats = dashboard.get_stats()
    
    # Función para formatear montos
    def format_money(amount):
        if amount is None:
            return "S/. 0.00"
        return f"S/. {amount:,.2f}"
    
    # Componentes del dashboard
    header = ft.Container(
        content=ft.Text("Dashboard de Control de Garantías", size=30, weight=ft.FontWeight.BOLD),
        margin=ft.margin.only(bottom=20)
    )
    
    # Tarjetas de resumen
    stats_row = ft.Row(
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("Garantías Activas", size=20),
                    ft.Text(str(stats['total_garantias']), size=30, weight=ft.FontWeight.BOLD),
                ]),
                bgcolor=ft.colors.BLUE_100,
                padding=20,
                border_radius=10,
                expand=True
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Monto Total Garantizado", size=20),
                    ft.Text(format_money(stats['monto_total']), size=30, weight=ft.FontWeight.BOLD),
                ]),
                bgcolor=ft.colors.GREEN_100,
                padding=20,
                border_radius=10,
                expand=True
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Próximas a Vencer", size=20),
                    ft.Text(str(stats['proximas_vencer']), size=30, weight=ft.FontWeight.BOLD),
                ]),
                bgcolor=ft.colors.RED_100 if stats['proximas_vencer'] > 0 else ft.colors.GREY_100,
                padding=20,
                border_radius=10,
                expand=True
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
    
    # Tabla de garantías por vencer
    garantias_vencer = dashboard.get_garantias_por_vencer()
    tabla_garantias = ft.DataTable(
        heading_row_height=70,
        heading_row_color=ft.colors.BLUE_GREY_100,
        data_row_max_height=100,
        columns=[
            ft.DataColumn(ft.Text("N° Garantía")),
            ft.DataColumn(ft.Text("Contratista")),
            ft.DataColumn(ft.Text("Vencimiento")),
            ft.DataColumn(ft.Text("Monto")),
            ft.DataColumn(ft.Text("Días Restantes")),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(g[0])),
                    ft.DataCell(ft.Text(g[1])),
                    ft.DataCell(ft.Text(g[2])),
                    ft.DataCell(ft.Text(format_money(g[3]))),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(f"{int(g[4])} días"),
                            bgcolor=ft.colors.RED_100 if g[4] < 15 else ft.colors.YELLOW_100,
                            padding=5,
                            border_radius=5
                        )
                    ),
                ]
            ) for g in garantias_vencer
        ],
    )
    
    tabla_container = ft.Container(
        content=ft.Column([
            ft.Text("Garantías Próximas a Vencer", size=20, weight=ft.FontWeight.BOLD),
            tabla_garantias
        ]),
        margin=ft.margin.only(top=20)
    )
    
    # Barra de filtros
    filtros = ft.Row([
        ft.TextField(label="Buscar contratista", width=300),
        ft.Dropdown(
            label="Estado",
            width=200,
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("Vigentes"),
                ft.dropdown.Option("Por vencer"),
                ft.dropdown.Option("Vencidas"),
            ]
        ),
        ft.IconButton(
            icon=ft.icons.REFRESH,
            tooltip="Actualizar datos",
            on_click=lambda _: page.update()
        )
    ])
    
    # Agregar todos los componentes a la página
    page.add(
        header,
        stats_row,
        ft.Divider(height=20, color=ft.colors.BLUE_GREY_100),
        filtros,
        tabla_container
    )
    
    page.update()

if __name__ == '__main__':
    ft.app(target=main)