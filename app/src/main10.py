import flet as ft

def main(page: ft.Page):
    page.title = "Generador de Banners ASCII Aruba"
    page.padding = 20
    page.spacing = 20
    page.theme = ft.Theme(color_scheme_seed=ft.colors.BLUE)

    # Template exacto del banner
    BANNER_TEMPLATE = """\
000000 0000      00    00   000   000000    00009   000000000  000    00   000
000000000000    a00    000000a    000000  00000000  a0000000   000    0000000 
00   00   000   a00    000000     000     00    009    000     000    000000  
00   00   000   a00    000b000a   000     00000000     000     000    00aa0000
00   00   000    00    00   000   a0a      a00000      00a      00    00   000
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
     .~?5GB######BBPJ~:         | AG |   HOSTNAME: {hostname:<20}|
 .~?5GB#BBBG5??5GB###BG5J~:     | {agency_num} |   AGENCY: {agency:<20}|
JGB#BBBBBBBP7:  .~?5GB#B#BB?    |____| LOCATION: {location:<20}|
GBBBB5~^!JPB##G57.  .~JBBBBP    +============================================|
GBBBB5?~.  :!JY7^  .  :BBBBP    |          model: {model:<25}|
GBBBB!:!PP?~    ^?55. :BBBBP    |    serial-number: {serial:<25}|
GBBBB~  Y###J  !###P. :BBBBP    |                                            |
GBBBB7  YBB#J  7BBBP  ~BBBBP    |                                            |
P#BBBBPJPBBBJ  !BBBGJ5BBBB#5    |                                            |
^!YGB###BBBB5::JBBBB###BG57:    |                                            |
   .^7YGB#BBBBBBBB#BG5?~.       |                                            |
       .^7YGB##BG5?~.           |                                            |
        [MANAGED BY OCTABA]      |                                            |
============================================================================"""

    # Campo de vista previa principal
    preview = ft.TextField(
        read_only=True,
        multiline=True,
        min_lines=20,
        max_lines=20,
        border=ft.InputBorder.NONE,
        bgcolor=ft.colors.WHITE,
        border_radius=8,
        text_style=ft.TextStyle(
            size=6,
            weight=ft.FontWeight.BOLD,
        ),
    )

    # Campo de minimapa
    minimap_preview = ft.TextField(
        read_only=True,
        multiline=True,
        min_lines=10,
        max_lines=10,
        border=ft.InputBorder.NONE,
        bgcolor=ft.colors.GREY_50,
        border_radius=8,
        text_style=ft.TextStyle(
            size=4,
            weight=ft.FontWeight.BOLD,
        ),
    )

    def align_text(alignment):
        """Alinea el texto según la alineación especificada"""
        lines = preview.value.split('\n')
        max_width = max(len(line) for line in lines)
        
        aligned_lines = []
        for line in lines:
            if alignment == "center":
                padding = (max_width - len(line)) // 2
                aligned_lines.append(" " * padding + line)
            elif alignment == "right":
                aligned_lines.append(" " * (max_width - len(line)) + line)
            else:  # left alignment
                aligned_lines.append(line)
        
        preview.value = '\n'.join(aligned_lines)
        generate_preview(None)  # Actualizar minimapa
        page.update()

    def update_spacing(e):
        """Actualiza el espaciado del banner"""
        try:
            spacing = int(e.control.value)
            if spacing < 0:
                spacing = 0
                e.control.value = "0"
            elif spacing > 50:
                spacing = 50
                e.control.value = "50"
                
            lines = preview.value.split('\n')
            spaced_lines = [" " * spacing + line for line in lines]
            preview.value = '\n'.join(spaced_lines)
            generate_preview(None)  # Actualizar minimapa
            page.update()
        except ValueError:
            e.control.value = "0"
            page.update()

    def generate_banner():
        """Genera el banner principal"""
        banner = BANNER_TEMPLATE.format(
            hostname=hostname_field.value,
            agency_num=agency_number.value,
            agency=agency_field.value,
            location=location_field.value,
            model=model_field.value,
            serial=serial_field.value
        )
        preview.value = banner
        generate_preview(None)
        page.update()

    def generate_preview(_):
        """Genera la vista previa en el minimapa"""
        minimap_preview.value = preview.value
        page.update()

    def validate_length(e):
        """Validar la longitud de los campos"""
        text_field = e.control
        max_lengths = {
            "hostname": 20,
            "agency": 20,
            "location": 20,
            "agency_number": 2,
            "model": 25,
            "serial": 25
        }
        
        if len(text_field.value) > max_lengths.get(text_field.data, 20):
            text_field.value = text_field.value[:max_lengths.get(text_field.data, 20)]
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text(f"Máximo {max_lengths.get(text_field.data, 20)} caracteres permitidos"))
            )
        generate_banner()

    # Estilo común para los campos
    field_style = {
        "border": ft.InputBorder.UNDERLINE,
        "bgcolor": ft.colors.WHITE,
        "height": 45,
        "border_radius": 8,
    }

    # Campos del formulario
    hostname_field = ft.TextField(
        label="Hostname",
        value="MKT_45_12ABRIL",
        on_change=validate_length,
        data="hostname",
        **field_style
    )

    agency_number = ft.TextField(
        label="Número de Agencia",
        value="45",
        width=150,
        on_change=validate_length,
        data="agency_number",
        **field_style
    )

    agency_field = ft.TextField(
        label="Agency",
        value="AG_45_12ABRIL",
        on_change=validate_length,
        data="agency",
        **field_style
    )

    location_field = ft.TextField(
        label="Location",
        value="MERCADO 12 DE ABRIL",
        on_change=validate_length,
        data="location",
        **field_style
    )

    model_field = ft.TextField(
        label="Model",
        value="2011L",
        on_change=validate_length,
        data="model",
        **field_style
    )

    serial_field = ft.TextField(
        label="Serial Number",
        value="3D6D02A0BB33",
        on_change=validate_length,
        data="serial",
        **field_style
    )

    def copy_to_clipboard(_):
        """Copia el banner al portapapeles"""
        page.set_clipboard(preview.value)
        page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("¡Banner copiado al portapapeles!"),
                action="OK"
            )
        )

    # Controles de alineación
    alignment_controls = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.icons.FORMAT_ALIGN_LEFT,
                on_click=lambda _: align_text("left"),
                tooltip="Alinear a la izquierda",
                icon_color=ft.colors.BLUE,
            ),
            ft.IconButton(
                icon=ft.icons.FORMAT_ALIGN_CENTER,
                on_click=lambda _: align_text("center"),
                tooltip="Centrar",
                icon_color=ft.colors.BLUE,
            ),
            ft.IconButton(
                icon=ft.icons.FORMAT_ALIGN_RIGHT,
                on_click=lambda _: align_text("right"),
                tooltip="Alinear a la derecha",
                icon_color=ft.colors.BLUE,
            ),
            ft.VerticalDivider(width=1),
            ft.TextField(
                label="Espaciado",
                width=100,
                value="0",
                text_align=ft.TextAlign.RIGHT,
                keyboard_type=ft.KeyboardType.NUMBER,
                on_change=update_spacing,
                suffix_text="px",
                **field_style
            ),
        ],
        spacing=10,
    )

    # Botones principales
    main_buttons = ft.Row(
        controls=[
            ft.ElevatedButton(
                "Generar Vista Previa",
                icon=ft.icons.PREVIEW,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
                on_click=generate_preview
            ),
            ft.ElevatedButton(
                "Copiar al portapapeles",
                icon=ft.icons.COPY,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
                on_click=copy_to_clipboard
            ),
        ],
        spacing=10
    )

    # Card del formulario
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

    # Card de la vista previa
    preview_card = ft.Card(
        content=ft.Container(
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text("Vista Previa del Banner", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    preview,
                    ft.Row(
                        controls=[
                            alignment_controls,
                            ft.VerticalDivider(width=1),
                            main_buttons,
                        ],
                        spacing=10,
                    ),
                ],
                spacing=20,
            ),
        )
    )

    # Card del minimapa
    minimap_card = ft.Card(
        content=ft.Container(
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text("Vista Previa en Miniatura", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    minimap_preview,
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
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[preview_card],
                        col={"sm": 12, "md": 8}
                    ),
                    ft.Column(
                        controls=[minimap_card],
                        col={"sm": 12, "md": 4}
                    ),
                ],
                spacing=20,
            ),
        ],
        spacing=20,
    )

    page.add(main_column)
    generate_banner()  # Generar banner inicial

ft.app(target=main)