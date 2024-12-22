import flet as ft

def main(page: ft.Page):
    page.title = "Generador de Banners ASCII Aruba"
    page.padding = 20
    page.spacing = 20
    page.theme = ft.Theme(color_scheme_seed=ft.colors.BLUE)
    
    def generate_banner():
        # Constantes para alineación
        SEPARATOR_LENGTH = 70  # Longitud de la línea de ':'
        CONTENT_LENGTH = 67    # Longitud efectiva del contenido (considerando los bordes '|')

        def pad_line(left_content, right_content=""):
            """
            Alinea una línea del banner con el ancho correcto
            """
            if right_content:
                # Calcula el espacio necesario entre el contenido izquierdo y derecho
                available_space = CONTENT_LENGTH - len(left_content) - len(right_content)
                return f"{left_content}{' ' * available_space}{right_content}"
            else:
                # Solo contenido izquierdo, alinear a la longitud total
                return f"{left_content}{' ' * (CONTENT_LENGTH - len(left_content))}"

        # Logo ARUBA en ASCII
        aruba_logo = """\
000000 0000      00    00   000   000000    00009   000000000  000    00   000
000000000000    a00    000000a    000000  00000000  a0000000   000    0000000 
00   00   000   a00    000000     000     00    009    000     000    000000  
00   00   000   a00    000b000a   000     00000000     000     000    00aa0000
00   00   000    00    00   000   a0a      a00000      00a      00    00   000"""

        # Separador con longitud exacta
        separator = ":" * SEPARATOR_LENGTH

        # Construir el banner con alineación precisa
        banner_lines = [
            aruba_logo,
            separator,
            f"|{pad_line('     .~?5GB######BBPJ~:', f'| AG |   HOSTNAME: {hostname_field.value}')}|",
            f"|{pad_line(' .~?5GB#BBBG5??5GB###BG5J~:', f'| {agency_number.value} |   AGENCY: {agency_field.value}')}|",
            f"|{pad_line('JGB#BBBBBBBP7:  .~?5GB#B#BB?', f'|____| \tLOCATION: {location_field.value}')}|",
            f"|{pad_line('GBBBB5~^!JPB##G57.  .~JBBBBP', '+====+=======================================')}|",
            f"|{pad_line('GBBBB5?~.  :!JY7^  .  :BBBBP', f'          model: {model_field.value}')}|",
            f"|{pad_line('GBBBB!:!PP?~    ^?55. :BBBBP', f'    serial-number: {serial_field.value}')}|",
            f"|{pad_line('GBBBB~  Y###J  !###P. :BBBBP')}|",
            f"|{pad_line('GBBBB7  YBB#J  7BBBP  ~BBBBP')}|",
            f"|{pad_line('P#BBBBPJPBBBJ  !BBBGJ5BBBB#5')}|",
            f"|{pad_line('^!YGB###BBBB5::JBBBB###BG57:')}|",
            f"|{pad_line('   .^7YGB#BBBBBBBB#BG5?~.')}|",
            f"|{pad_line('       .^7YGB##BG5?~.')}|",
            f"|{pad_line('        [MANAGED BY OCTABA]')}|",
            "=" * SEPARATOR_LENGTH
        ]

        preview.value = "\n".join(banner_lines)
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

    # Estilo común para los campos de texto
    field_border = ft.InputBorder.UNDERLINE
    field_radius = 8
    field_bgcolor = ft.colors.WHITE
    field_height = 45

    # Campos del formulario con estilo mejorado y validación
    hostname_field = ft.TextField(
        label="Hostname",
        value="MKT_45_12ABRIL",
        border=field_border,
        bgcolor=field_bgcolor,
        height=field_height,
        border_radius=field_radius,
        on_change=validate_length,
        data="hostname"
    )

    agency_number = ft.TextField(
        label="Número de Agencia",
        value="45",
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
        value="AG_45_12ABRIL",
        border=field_border,
        bgcolor=field_bgcolor,
        height=field_height,
        border_radius=field_radius,
        on_change=validate_length,
        data="agency"
    )

    location_field = ft.TextField(
        label="Location",
        value="MERCADO 12 DE ABRIL",
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

    # Campo de previsualización
    preview = ft.TextField(
        read_only=True,
        multiline=True,
        min_lines=20,
        max_lines=20,
        border=field_border,
        bgcolor=field_bgcolor,
        border_radius=field_radius,
    )

    def copy_to_clipboard(_):
        page.set_clipboard(preview.value)
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("¡Banner copiado al portapapeles!"),
                action="OK"
            )
        )

    # Botón para copiar
    copy_button = ft.ElevatedButton(
        "Copiar al portapapeles",
        icon=ft.icons.COPY,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=copy_to_clipboard
    )

    # Card de previsualización
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
    generate_banner()  # Generar banner inicial

ft.app(target=main)