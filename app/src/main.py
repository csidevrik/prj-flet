from flet import *

def main(page:Page):
    #CREATE FAKE DATTA
    page.add(
        Column([
            Text("Search",size=12,weight="bold")
        ])
    )

flet.app(target=main)