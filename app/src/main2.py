import flet as ft
from li.gradients import gradient
import math

class UI(ft.UserControl):
    def __init__(self, page):
        super().__init__(expand=True)
        self.page = page

        GRADIENT=ft.LinearGradient(
            begin=ft.alignment.bottom_center,
            end=ft.Alignment(0.8,1),
            colors = gradient("Quepal"),
            rotation=math.pi/4.6,
        )
        self.color_container = GRADIENT
        self.color_items = ft.colors.BLUE_GREY_500
        self.color_selec_items = ft.colors.DEEP_ORANGE
        self.color_icons_light = ft.colors.BLACK
        self.color_icons_dark  = ft.colors.WHITE

        self.animation_style = ft.animation.Animation(400,ft.AnimationCurve.EASE_IN_TO_LINEAR)

        self.bt_home = ft.Container(
            width=70,
            height=70,
            bgcolor=self.color_container,
            border_radius=10,
            alignment=ft.alignment.center,
            content=ft.IconButton(icon=ft.icons.HOME,
                                  icon_color=self.color_icons_dark,
                                  on_click=self.bar_icons
                                  )
        )

        self.frame_title = ft.Container(
            expand=True,
            height=60,
            bgcolor=self.color_container,
            border_radius= 10,
            alignment=ft.alignment.center,
            content=ft.Text("Flet App",size=30)
        )

        self.navigation = ft.Container(
            bgcolor=self.color_container,
            animate_size=self.animation_style,
            width=200,
            border_radius=10,
            padding=20,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            spacing=10,
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                            
                        )
                    )
                ]
            )
        )

        self.page.add(ft.Column(
            expand=True,
            controls=[
                ft.Row(
                    controls=[
                        self.bt_home,
                        self.frame_title,
                    ]
                )
            ]
        ))

    def bar_icons(self, e):
        
        pass

ft.app(target=UI)