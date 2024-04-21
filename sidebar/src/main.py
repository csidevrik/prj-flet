from flet import *

class App(UserControl):
    def __init__(self, pg:Page):
        super().__init__()

        self.pg = pg
        self.init_helper()

    def init_helper(self):
        self.pg.add(
            Container(
                expand=True,
                bgcolor="#2C2C2C",
                content=Row(
                    spacing=0,
                    controls=[
                        Container(
                            bgcolor="#E68745",
                            # expand=True,
                            width=80,
                        ), #sidebar
                        Container(
                            bgcolor="#E05C4A",
                            # expand=True
                        ), #main screen
                    ]
                )
            )
        )
app(target=App)