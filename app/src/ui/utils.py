import flet as ft
import math
from li.gradients import gradient

PRIMARY_COLOR = "#18684d"
ICON_COLOR = "#222222"

GRADIENT = ft.LinearGradient(
    # begin=ft.alignment.top_left ,
    # end=ft.Alignment(0.8, 1),
    colors=gradient("Dance To Forget"),
    rotation=math.pi / 3,
)

def get_primary_gradient():
    return GRADIENT
