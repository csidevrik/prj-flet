import flet as ft

def main(page: ft.Page):
    page.title = "Generador de Banners ASCII Aruba"
    page.padding = 20
    page.spacing = 20
    page.theme = ft.Theme(color_scheme_seed=ft.colors.BLUE)

    # Campo de previsualización
    preview = ft.TextField(
        read_only=True,
        multiline=True,
        min_lines=20,
        max_lines=20,
        border=ft.InputBorder.UNDERLINE,
        bgcolor=ft.colors.WHITE,
        border_radius=8
    )

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

        # Construir el banner inicial
        banner = f"""{aruba_logo}
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
     .~?5GB######BBPJ~:         | AG |   HOSTNAME: {hostname_field.value}
 .~?5GB#BBBG5??5GB###BG5J~:     | {agency_number.value} |   AGENCY: {agency_field.value}
JGB#BBBBBBBP7:  .~?5GB#B#BB?    |____| \tLOCATION: {location_field.value}
GBBBB5~^!JPB##G57.  .~JBBBBP    +====+=======================================
GBBBB5?~.  :!JY7^  .  :BBBBP    |          model: {model_field.value}
GBBBB!:!PP?~    ^?55. :BBBBP    |    serial-number: {serial_field.value}
GBBBB~  Y###J  !###P. :BBBBP    |
GBBBB7  YBB#J  7BBBP  ~BBBBP    |
P#BBBBPJPBBBJ  !BBBGJ5BBBB#5    |
^!YGB###BBBB5::JBBBB###BG57:    |
   .^7YGB#BBBBBBBB#BG5?~.       |
       .^7YGB##BG5?~.           |
        [MANAGED BY OCTABA]      |
==============================================================================""" 
        
        preview.value = banner
        page.update()

    def align_banner():
        """
        Realinear el banner manualmente según el formato exacto
        """
        SEPARATOR_LENGTH = 70

        def pad_exact(text, target_length):
            return text + " " * (target_length - len(text))

        # Formato específico para cada línea de información
        hostname_line = f"| {pad_exact('.~?5GB######BBPJ~:', 40)}| AG | {pad_exact('HOSTNAME: ' + hostname_field.value, 20)}|"
        agency_line = f"| {pad_exact('.~?5GB#BBBG5??5GB###BG5J~:', 40)}| {agency_number.value} | {pad_exact('AGENCY: ' + agency_field.value, 20)}|"
        location_line = f"|{pad_exact('JGB#BBBBBBBP7:  .~?5GB#B#BB?', 40)}|____| {pad_exact('LOCATION: ' + location_field.value, 30)}|"
        model_line = f"|{pad_exact('GBBBB5?~.  :!JY7^  .  :BBBBP', 40)}       {pad_exact('model: ' + model_field.value, 25)}|"
        serial_line = f"|{pad_exact('GBBBB!:!PP?~    ^?55. :BBBBP', 40)}    {pad_exact('serial-number: ' + serial_field.value, 35)}|"

        # Líneas del logo que siempre están fijas
        fixed_logo = [
            "GBBBB~ Y###J !###P. :BBBBP",
            "GBBBB7 YBB#J 7BBBP ~BBBBP",
            "P#BBBBPJPBBBJ !BBBGJ5BBBB#5",
            "^!YGB###BBBB5::JBBBB###BG57:",
            "   .^7YGB#BBBBBBBB#BG5?~.",
            "       .^7YGB##BG5?~.",
            "        [MANAGED BY OCTABA]"
        ]

        # Construir las líneas fijas con padding correcto
        fixed_lines = [f"|{pad_exact(line, 67)}|" for line in fixed_logo]

        # Juntar todo el banner
        aruba_logo = """\
000000 0000      00    00   000   000000    00009   000000000  000    00   000
000000000000    a00    000000a    000000  00000000  a0000000   000    0000000 
00   00   000   a00    000000     000     00    009    000     000    000000  
00   00   000   a00    000b000a   000     00000000     000     000    00aa0000
00   00   000    00    00   000   a0a      a00000      00a      00    00   000"""

        aligned_banner = [
            aruba_logo,
            ":" * SEPARATOR_LENGTH,
            hostname_line,
            agency_line,
            location_line,
            "+" + "=" * (SEPARATOR_LENGTH - 2) + "+",
            model_line,
            serial_line,
            *fixed_lines,
            "=" * SEPARATOR_LENGTH
        ]

        preview.value = "\n".join(aligned_banner)
        page.update()

    def validate_length(e):
        """Validar la longitud de los campos para evitar que se rompa el formato"""
        text_field = e.control
        max_lengths = {
            "hostname": 20,
            "agency": 20,
            "location": 20,
            "agency_number": 2,
            "model": 15,
            "serial": 25
        }
        
        if len(text_field.value) > max_lengths.get(text_field.data, 20):
            text_field.value = text_field.value[:max_lengths.get(text_field.data, 20)]
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text(f"Máximo {max_lengths.get(text_field.data, 20)} caracteres permitidos"))
            )
        generate_banner()

    # Estilo común para los campos
    field_border = ft.InputBorder.UNDERLINE
    field_radius = 8
    field_bgcolor = ft.colors.WHITE
    field_height = 45

    # Campos del formulario
    hostname_field = ft.TextField(
        label="Hostname",
        value="MKT_44_10AGOSTO",
        border=field_border,
        bgcolor=field_bgcolor,
        height=field_height,
        border_radius=field_radius,
        on_change=validate_length,
        data="hostname"
    )

    agency_number = ft.TextField(
        label="Número de Agencia",
        value="44",
        width=150,
        border=field_border,
        bgcolor=field_bgcolor,
        height=field_height,
        border_radius=field_radius,
        on_change=validate_length,
        data="agency_number"
    )

    agency_field = ft.TextField(
        label="Agency",
        value="AG_44_10AGOSTO",
        border=field_border,
        bgcolor=field_bgcolor,
        height=field_height,
        border_radius=field_radius,
        on_change=validate_length,
        data="agency"
    )

    location_field = ft.TextField(
        label="Location",
        value="MERCADO 10 DE AGOSTO",
        border=field_border,
        bgcolor=field_bgcolor,
        height=field_height,
        border_radius=field_radius,
        on_change=validate_length,
        data="location"
    )

    model_field = ft.TextField(
        label="Model",
        value="2011L",
        border=field_border,
        bgcolor=field_bgcolor,
        height=field_height,
        border_radius=field_radius,
        on_change=validate_length,
        data="model"
    )

    serial_field = ft.TextField(
        label="Serial Number",
        value="3D6D02A0BB33",
        border=field_border,
        bgcolor=field_bgcolor,
        height=field_height,
        border_radius=field_radius,
        on_change=validate_length,
        data="serial"
    )

    def copy_to_clipboard(_):
        page.set_clipboard(preview.value)
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("¡Banner copiado al portapapeles!"),
                action="OK"
            )
        )

    # Botones
    copy_button = ft.ElevatedButton(
        "Copiar al portapapeles",
        icon=ft.icons.COPY,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=copy_to_clipboard
    )

    align_button = ft.ElevatedButton(
        "Alinear Banner",
        icon=ft.icons.FORMAT_ALIGN_CENTER,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=lambda _: align_banner()
    )

    # Fila de botones
    buttons_row = ft.Row(
        controls=[
            align_button,
            copy_button,
        ],
        spacing=10
    )

    # Cards
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

    preview_card = ft.Card(
        content=ft.Container(
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text("Vista Previa del Banner", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    preview,
                    buttons_row,
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
    generate_banner()  # Generar banner inicial

ft.app(target=main)