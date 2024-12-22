import flet as ft

def main(page: ft.Page):
    page.title = "Generador de Banners ASCII Aruba"
    page.padding = 20
    page.spacing = 20
    page.theme = ft.Theme(color_scheme_seed=ft.colors.BLUE)
    
    def generate_banner():
        aruba_logo = """\
000000 0000      00    00   000   000000    00009   000000000  000    00   000
000000000000    a00    000000a    000000  00000000  a0000000   000    0000000 
00   00   000   a00    000000     000     00    009    000     000    000000  
00   00   000   a00    000b000a   000     00000000     000     000    00aa0000
00   00   000    00    00   000   a0a      a00000      00a      00    00   000"""

        def pad_right(text: str, length: int) -> str:
            return text.ljust(length)

        banner = f"""{aruba_logo}
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
     .~?5GB######BBPJ~:         | AG |   HOSTNAME: {pad_right(hostname_field.value, 20)}|
 .~?5GB#BBBG5??5GB###BG5J~:     | {pad_right(agency_number.value, 2)} |   AGENCY: {pad_right(agency_field.value, 20)}|
JGB#BBBBBBBP7:  .~?5GB#B#BB?    |____| \tLOCATION: {pad_right(location_field.value, 20)}|
GBBBB5~^!JPB##G57.  .~JBBBBP    +====+=====================================|
GBBBB5?~.  :!JY7^  .  :BBBBP    |          model: {pad_right(model_field.value, 20)}|
GBBBB!:!PP?~    ^?55. :BBBBP    |    serial-number: {pad_right(serial_field.value, 20)}|
GBBBB~  Y###J  !###P. :BBBBP    |                                          |
GBBBB7  YBB#J  7BBBP  ~BBBBP    |                                          |
P#BBBBPJPBBBJ  !BBBGJ5BBBB#5    |                                          |
^!YGB###BBBB5::JBBBB###BG57:    |                                          |
   .^7YGB#BBBBBBBB#BG5?~.       |                                          |
       .^7YGB##BG5?~.           |                                          |
        [MANAGED BY OCTABA]      |                                          |
==============================================================================""" 
        
        preview.value = banner
        page.update()

    # Estilo común para los campos de texto
    field_border = ft.InputBorder.UNDERLINE
    field_radius = 8
    field_bgcolor = ft.colors.WHITE
    field_height = 45

    # Campos del formulario con estilo mejorado
    hostname_field = ft.TextField(
        label="Hostname",
        value="MKT_45_12ABRIL",
        border=field_border,
        bgcolor=field_bgcolor,
        height=field_height,
        border_radius=field_radius,
        on_change=lambda _: generate_banner()
    )

    agency_number = ft.TextField(
        label="Número de Agencia",
        value="45",
        width=150,
        border=field_border,
        bgcolor=field_bgcolor,
        height=field_height,
        border_radius=field_radius,
        on_change=lambda _: generate_banner()
    )

    agency_field = ft.TextField(
        label="Agency",
        value="AG_45_12ABRIL",
        border=field_border,
        bgcolor=field_bgcolor,
        height=field_height,
        border_radius=field_radius,
        on_change=lambda _: generate_banner()
    )

    location_field = ft.TextField(
        label="Location",
        value="MERCADO 12 DE ABRIL",
        border=field_border,
        bgcolor=field_bgcolor,
        height=field_height,
        border_radius=field_radius,
        on_change=lambda _: generate_banner()
    )

    model_field = ft.TextField(
        label="Model",
        value="2011L",
        border=field_border,
        bgcolor=field_bgcolor,
        height=field_height,
        border_radius=field_radius,
        on_change=lambda _: generate_banner()
    )

    serial_field = ft.TextField(
        label="Serial Number",
        value="3D6D02A0BB33",
        border=field_border,
        bgcolor=field_bgcolor,
        height=field_height,
        border_radius=field_radius,
        on_change=lambda _: generate_banner()
    )

    # Card para el formulario
    form_card = ft.Card(
        content=ft.Container(
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text("Información del Dispositivo", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Column(
                                col={"sm": 6, "md": 4},
                                controls=[agency_number],
                            ),
                            ft.Column(
                                col={"sm": 6, "md": 4},
                                controls=[hostname_field],
                            ),
                            ft.Column(
                                col={"sm": 6, "md": 4},
                                controls=[agency_field],
                            ),
                        ],
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Column(
                                col={"sm": 6, "md": 4},
                                controls=[location_field],
                            ),
                            ft.Column(
                                col={"sm": 6, "md": 4},
                                controls=[model_field],
                            ),
                            ft.Column(
                                col={"sm": 6, "md": 4},
                                controls=[serial_field],
                            ),
                        ],
                    ),
                ],
                spacing=20,
            ),
        )
    )

    # Preview con estilo mejorado
    preview = ft.TextField(
        read_only=True,
        multiline=True,
        min_lines=20,
        max_lines=20,
        border=field_border,
        bgcolor=field_bgcolor,
        border_radius=field_radius
    )

    def copy_to_clipboard(_):
        page.set_clipboard(preview.value)
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("¡Banner copiado al portapapeles!"),
                action="OK"
            )
        )

    # Botón estilizado
    copy_button = ft.ElevatedButton(
        "Copiar al portapapeles",
        icon=ft.icons.COPY,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=copy_to_clipboard
    )

    # Preview card
    preview_card = ft.Card(
        content=ft.Container(
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text("Vista Previa del Banner", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    preview,
                    copy_button,
                ],
                spacing=20,
            ),
        )
    )

    # Contenedor principal
    main_column = ft.Column(
        controls=[
            ft.Container(
                content=ft.Text(
                    "Generador de Banners ASCII Aruba",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLUE,
                ),
                padding=ft.padding.only(bottom=20),
            ),
            form_card,
            preview_card,
        ],
        spacing=20,
    )

    page.add(main_column)
    generate_banner()

ft.app(target=main)