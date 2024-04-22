from flet import *

class App(UserControl):
    def __init__(self, pg:Page):
        super().__init__()

        self.pg = pg
        self.pg.window_title_bar_buttons_hidden = True
        self.pg.window_title_bar_hidden = True
        self.init_helper()

    def init_helper(self):
        self.pg.add(
            Container(
                expand=True, padding=1,
                bgcolor="#2C2C2C",
                border_radius=15,
                content=Row(
                    spacing=0,
                    controls=[
                        Container(
                            bgcolor="#006262",
                            # expand=True,
                            width=80,
                            content=Row(
                                spacing=0,
                                controls=[
                                    Column(
                                        expand=True,
                                        controls=[
                                            Container(bgcolor="#006262",
                                                      expand=True,)
                                        ]
                                    ),
                                    Column(
                                        expand=True,
                                        controls=[
                                            Container(bgcolor="red",
                                                      width=3,height=10,)
                                        ]
                                    )
                                ]
                            )
                        ), #sidebar
                        Container(
                            bgcolor="#fdfcff",
                            expand=True,
                            padding=0,
                            margin=0,
                        ), #main screen
                    ],
                    vertical_alignment=10,
                )
            )
        )
app(target=App)