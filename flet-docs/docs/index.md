|# Welcome to prj-flet documentation

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.   
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.
``

## Compartiendo el codigo
Primero creamos los contenedores de la ventana
* Crea el siguiente codigo
  
```shell
    fila= ft.Row(
        controls=[
            c,
            ft.GestureDetector(
                content=ft.VerticalDivider(),
                drag_interval=10,
                on_pan_update=move_vertical_divider,
                on_hover=show_draggable_cursor,
            ),
            ft.Container(
                bgcolor= "#263238",
                alignment=ft.alignment.center,
                expand=1,
            ),
        ],
        spacing=0,
        width=1920,
        height=1080,
    )
```

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
