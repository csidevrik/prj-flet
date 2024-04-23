# Suponiendo que tienes una forma de acceder a la posición del mouse y la posición de la ventana
mouse_position_initial = None
window_position_initial = None
dragging = False

async def on_appbar_click(e):
    global mouse_position_initial, window_position_initial, dragging
    mouse_position_initial = e.mouse_position # Obtén la posición del mouse
    window_position_initial = page.window_position # Obtén la posición de la ventana
    dragging = True

async def on_mouse_move(e):
    global dragging
    if dragging:
        # Calcular la diferencia en la posición del mouse
        delta_x = e.mouse_position.x - mouse_position_initial.x
        delta_y = e.mouse_position.y - mouse_position_initial.y
        # Actualizar la posición de la ventana
        page.window_position = (window_position_initial.x + delta_x, window_position_initial.y + delta_y)
        await page.update_async()

async def on_mouse_up(e):
    global dragging
    dragging = False

# Asegúrate de conectar estos controladores de eventos a los eventos correspondientes
# Por ejemplo, podrías tener algo como esto (esto es pseudo-código y dependerá de cómo `flet` maneje los eventos):
appbar.on_click = on_appbar_click
page.on_mouse_move = on_mouse_move
page.on_mouse_up = on_mouse_up

