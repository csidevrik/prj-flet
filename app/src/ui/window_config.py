import flet as ft

def setup_window(page: ft.Page):
    page.window.height = 600
    page.window.width = 600
    page.window.resizable = True
    # page.window_movable = True
    page.title = "PAYMENTS"
    # page.window_title_bar_hidden = True+      
    # page.window_title_bar_buttons_hidden = True
    page.padding = 0
    # page.background_color = GRADIENT
