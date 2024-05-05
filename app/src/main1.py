import flet as ft


class UI(ft.UserControl):
    def __init__(self, page):
        super().__init__(expand= True)
        self.COLOR_0="#019689"
        self.COLOR_1="#00a3c2"

        self.color_teal = self.COLOR_1

        self.mode_switch = ft.Switch(
            value=True,
            thumb_color = "black",
        )

        self.initial_container_1 = ft.Container(
            bgcolor= self.color_teal,
            border_radius=20,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text("Dia"),
                    ft.Container(
                        border_radius=20, 
                    )
                ]
            )
        )
        
        self.initial_container_2 = ft.Container(
            bgcolor= self.color_teal,
            border_radius=20,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text("Noche"),
                    ft.Container(
                        border_radius=20, 
                    )
                ]
            )
        )

        self.container_1 = ft.Container(content=self.initial_container_1)
        self.container_2 = ft.Container(content=self.initial_container_2)

        self.navigation_container = ft.Container(
            col = 1,
            bgcolor = self.color_teal,
            border_radius=5,
            content=ft.Column(
                controls=[
                    ft.Container(
                        expand=True,
                        content=ft.NavigationRail(
                            bgcolor=self.color_teal,
                            expand=True,
                            selected_index=0,
                            destinations=[
                                ft.NavigationDestination(
                                    icon=ft.icons.HOME,
                                ),
                                ft.NavigationDestination(
                                    icon=ft.icons.LOCATION_ON_OUTLINED,
                                ),
                                ft.NavigationDestination(
                                    icon=ft.icons.CALENDAR_MONTH_SHARP,
                                ),
                                ft.NavigationDestination(
                                    icon=ft.icons.SETTINGS,
                                ),

                            ]
                            
                        )
                    ),
                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            expand = True,
                            alignment=ft.MainAxisAlignment.END,
                            controls = [
                                ft.IconButton(
                                    icon=ft.icons.OUTPUT,
                                ),
                                self.mode_switch
                            ]
                        )                        
                    )
                ]
            )
        )

        self.frame2 = ft.Container(
            col = 6,
            # bgcolor = self.color_teal,
            content=ft.Column(
                controls=[
                    ft.Container(
                        border_radius=7,
                        padding=ft.padding.only(right=200),
                        alignment=ft.alignment.top_left,
                        content= ft.Container(
                            bgcolor=self.color_teal,
                            border_radius=20,
                            content=ft.Row(
                                controls=[
                                    ft.IconButton(icon = ft.icons.SEARCH),
                                    ft.TextField(
                                        hint_text="Search for something",
                                        border = ft.InputBorder.NONE,
                                        border_radius=14)
                                ]
                            )
                        )
                    ),
                    self.container_1,
                    self.container_2
                ]

            )
        )

        self.frame3 = ft.Container(
            col = 5,
            bgcolor = self.color_teal,
            content=ft.Column(
                
            )
        )


        self.container = ft.ResponsiveRow(
            controls=[
                self.navigation_container,
                self.frame2,
                self.frame3
            ]
        )

    def build(self):
        return self.container

def main(page: ft.Page):
    page.window_min_height  = 820
    page.window_min_width   = 530
    page.theme = ft.Theme(font_family="Consolas")
    page.theme_mode         = ft.ThemeMode.DARK
    page.add(UI(page))

ft.app(main)