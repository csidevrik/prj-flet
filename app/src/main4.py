import flet as ft

def main(page: ft.Page):
    def on_section_click(e):
        # Update the main content area based on the button clicked
        if e.control.text == "Settings":
            main_content.controls = [ft.Text("Settings Content")]
        elif e.control.text == "Accounts":
            main_content.controls = [ft.Text("Accounts Content")]
        main_content.update()

    sidebar = ft.Column(
        [
            ft.TextButton("Settings", on_click=on_section_click),
            ft.TextButton("Accounts", on_click=on_section_click),
            # Add more buttons for other sections...
        ],
        width=200,
        # bgcolor=ft.colors.BLUE_GREY_500
    )

    main_content = ft.Container(
        content=ft.Text("Default Content"),
        expand=True,
        padding=10,
    )

    page.add(ft.Row([sidebar, main_content], expand=True))

ft.app(target=main)
