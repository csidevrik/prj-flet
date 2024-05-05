from flet import *



def main(page: Page):
    COLOR_0="#019689"
    COLOR_1="#00a3c2"
    
    container = Container(
        width=500,
        height=128,
        bgcolor=COLOR_0,
        border_radius=35,
        content=stack(
            controls = [
                page_1,
                page_2,
                
            ]
        )
    )


app(target=main, view=WEB_BROWSER)

