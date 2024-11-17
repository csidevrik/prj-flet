import flet as ft
from typing import List, Dict
import json
from datetime import datetime

class FinancialExpertSystem:
    def __init__(self):
        self.rules_base = {
            "ingresos": self.analizar_ingresos,
            "gastos": self.analizar_gastos,
            "balance": self.calcular_balance,
            "proyecciones": self.calcular_proyecciones
        }
        self.data = {}
    
    def analizar_ingresos(self, datos: Dict) -> Dict:
        total = sum(datos.values())
        promedio = total / len(datos)
        return {
            "total": total,
            "promedio": promedio,
            "tendencia": "positiva" if total > promedio else "negativa"
        }
    
    def analizar_gastos(self, datos: Dict) -> Dict:
        total = sum(datos.values())
        categorias = list(datos.keys())
        return {
            "total": total,
            "categoria_mayor": max(datos, key=datos.get),
            "categorias": categorias
        }
    
    def calcular_balance(self, ingresos: float, gastos: float) -> Dict:
        balance = ingresos - gastos
        return {
            "balance": balance,
            "estado": "positivo" if balance > 0 else "negativo",
            "porcentaje_gastos": (gastos/ingresos) * 100 if ingresos > 0 else 0
        }
    
    def calcular_proyecciones(self, historico: List[float]) -> Dict:
        promedio = sum(historico) / len(historico)
        tendencia = historico[-1] - historico[0]
        return {
            "proyeccion": promedio + tendencia,
            "confianza": "alta" if len(historico) > 6 else "media"
        }

class FinancialApp:
    def __init__(self):
        self.expert_system = FinancialExpertSystem()
        
    def main(self, page: ft.Page):
        page.title = "Sistema Experto Financiero"
        page.theme_mode = "light"
        page.padding = 20

        # Componentes de la interfaz
        self.ingresos_field = ft.TextField(
            label="Ingresos mensuales",
            keyboard_type="number",
            width=300
        )
        
        self.gastos_field = ft.TextField(
            label="Gastos mensuales",
            keyboard_type="number",
            width=300
        )
        
        self.resultado_text = ft.Text(
            size=16,
            color="black"
        )
        
        def analizar_clicked(e):
            try:
                ingresos = float(self.ingresos_field.value)
                gastos = float(self.gastos_field.value)
                
                # Análisis con el sistema experto
                balance = self.expert_system.calcular_balance(ingresos, gastos)
                
                # Mostrar resultados
                resultado = f"""
                Balance: ${balance['balance']:.2f}
                Estado: {balance['estado']}
                Porcentaje de gastos: {balance['porcentaje_gastos']:.1f}%
                
                Recomendaciones:
                """
                
                if balance['porcentaje_gastos'] > 80:
                    resultado += "\n- Alerta: Los gastos son muy elevados respecto a los ingresos"
                if balance['estado'] == "negativo":
                    resultado += "\n- Se recomienda revisar gastos no esenciales"
                if balance['porcentaje_gastos'] < 50:
                    resultado += "\n- Considere inversiones o ahorro del excedente"
                
                self.resultado_text.value = resultado
                page.update()
                
            except ValueError:
                self.resultado_text.value = "Por favor ingrese valores numéricos válidos"
                page.update()

        analizar_btn = ft.ElevatedButton(
            text="Analizar",
            on_click=analizar_clicked,
            style=ft.ButtonStyle(
                color="white",
                bgcolor=ft.colors.BLUE_600,
            )
        )

        # Layout
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Sistema Experto Financiero", size=24, weight="bold"),
                    ft.Divider(),
                    self.ingresos_field,
                    self.gastos_field,
                    analizar_btn,
                    ft.Divider(),
                    self.resultado_text
                ]),
                padding=20,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=ft.colors.BLACK12
                )
            )
        )

def main():
    app = FinancialApp()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()