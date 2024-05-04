import flet as ft


class UI(ft.UserControl):
    def __init__(self, page):
        super().__init__(expand= True)

        self.color_teal = "teal"

        self.mode_switch = ft.Switch(
            value=True,
            thumb_color = "black",
            # thumb_icon  = {
            #     ft.MaterialState.DEFAULT: ft.icons.LIGHT_MODE,
            #     ft.MaterialState.SELECTED: ft.icons.DARK_MODE
            # }
        )

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
            bgcolor = self.color_teal,
            content=ft.Column(
                controls=[
                    ft.Container(
                        border_radius=7,
                        padding=ft.padding.only(right=200),
                        alignment=ft.alignment.top_left,
                        content= ft.Container(

                        )
                    )
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
    page.theme_mode         = ft.ThemeMode.DARK
    page.add(UI(page))

ft.app(main)