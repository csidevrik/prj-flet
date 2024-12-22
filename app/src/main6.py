import flet as ft

def main(page: ft.Page):
    page.title = "Generador de Banners ASCII Aruba"
    page.padding = 20
    page.spacing = 20

    def generate_banner():
        # Logo ARUBA en ASCII
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

    # Campos del formulario
    hostname_field = ft.TextField(
        label="Hostname",
        value="MKT_45_12ABRIL",
        on_change=lambda _: generate_banner()
    )

    agency_number = ft.TextField(
        label="Número de Agencia",
        value="45",
        width=100,
        on_change=lambda _: generate_banner()
    )

    agency_field = ft.TextField(
        label="Agency",
        value="AG_45_12ABRIL",
        on_change=lambda _: generate_banner()
    )

    location_field = ft.TextField(
        label="Location",
        value="MERCADO 12 DE ABRIL",
        on_change=lambda _: generate_banner()
    )

    model_field = ft.TextField(
        label="Model",
        value="2011L",
        on_change=lambda _: generate_banner()
    )

    serial_field = ft.TextField(
        label="Serial Number",
        value="3D6D02A0BB33",
        on_change=lambda _: generate_banner()
    )

    # Campo de previsualización simplificado
    preview = ft.TextField(
        read_only=True,
        multiline=True,
        min_lines=20,
        max_lines=20
    )

    def copy_to_clipboard(_):
        page.set_clipboard(preview.value)
        page.show_snack_bar(
            ft.SnackBar(content=ft.Text("¡Banner copiado al portapapeles!"))
        )

    copy_button = ft.ElevatedButton(
        "Copiar al portapapeles",
        icon=ft.icons.COPY,
        on_click=copy_to_clipboard
    )

    # Layout del formulario
    form_row1 = ft.Row(
        controls=[
            agency_number,
            hostname_field,
            agency_field,
        ],
        wrap=True,
    )

    form_row2 = ft.Row(
        controls=[
            location_field,
            model_field,
            serial_field,
        ],
        wrap=True,
    )

    # Contenedor principal
    container = ft.Column(
        controls=[
            ft.Text("Generador de Banners ASCII Aruba", size=24),
            form_row1,
            form_row2,
            copy_button,
            preview,
        ],
        spacing=20,
    )

    page.add(container)
    generate_banner()  # Generar banner inicial

ft.app(target=main)