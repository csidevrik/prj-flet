import math
import flet as ft
from utils.gradients import gradient

# Colors
PRIMARY_COLOR   = "#18684d"
SECONDARY_COLOR = "#222222"
ACCENT_GREEN    = "#00e8b2"
ACCENT_YELLOW   = "#f3ae35"

# Window
APP_TITLE     = "PAYMENTS"
WINDOW_WIDTH  = 600
WINDOW_HEIGHT = 600

# Divider limits
LIMIT_VD1_MAX = 200
LIMIT_VD1_MIN = 100
LIMIT_VD2_MAX = 200
LIMIT_VD2_MIN = 100

# Gradient
GRADIENT = ft.LinearGradient(
    begin=ft.Alignment(-1, -1),
    end=ft.Alignment(0.8, 1),
    colors=gradient("Kye Meh"),
    rotation=math.pi / 4.6,
)
