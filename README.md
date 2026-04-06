prj-flet
----------

Este repo trata de recopilar todos los trabajos que hago con flet y python

**Index**
1. [Instalacion en linux](#id1)
2. [En fedora](#id2)
3. [Migracion a Flet 0.80+](#id3)

## Instalacion en linux <a name="id1"></a>
Hoy domingo me di cuenta que al tratar de usar flet con este ejemplo 

https://flet.dev/docs/controls/searchbar/

Esto no me corria ni en windows ni en linux, luego averiguando me di cuenta que podia ser la version de flet, y es que para windows y linux se usa el mismo comando  que es el siguiente:

```terminal
    python -m pip install --upgrade flet
```
### En fedora <a name="id2"></a>
En fedora tuve problemillas que surgieron pero voy a comentar la manera en la que se resolvi[o].

Primero he tratado con instalar mpvlibs, en fedora trate de utilizar la ultima version de la libreria.

```bash
    sudo dnf install mpv-libs-0.35.1-2.fc37.x86_64 
```

Lamentablemente con esta libreria que en escencia es la mas actualizada, nada pues toco googlear and i find a foro talking about the versions of the librarie mpv then i uninstall the version mpv-libs-0.35 por la libreria mpv-libs-0.34 pues con esta ya no tuvimos problemas al menos en linux fedora 37.

```bash
    sudo dnf install mpv-libs-0.34.1-11.fc37.x86_64
```

## Migracion a Flet 0.80+ <a name="id3"></a>

A partir de la version 0.80, Flet elimino varias APIs asincronas y renombro metodos. Los cambios aplicados en `app/src/` son:

| Deprecated | Reemplazo |
|------------|-----------|
| `ft.app(target=fn)` | `ft.run(fn)` |
| `ft.alignment.center` / `ft.alignment.top_left` / etc. | `ft.Alignment(x, y)` |
| `await page.update_async()` | `page.update()` |
| `await control.update_async()` | `control.update()` |
| `await page.window_destroy_async()` | `await page.window.close()` |
| `page.window_minimized = True` | `page.window.minimized = True` |
| `ft.icons.XXX` | `ft.Icons.XXX` |
| `ft.colors.XXX` | `ft.Colors.XXX` |
| `ft.border.only(...)` | `ft.Border.only(...)` |
| `ft.ElevatedButton(` | `ft.Button(` |
| `ft.FilePicker(on_result=fn)` | `ft.FilePicker()` + `.on_result = fn` |
| `ft.FilePickerResultEvent` (eliminado) | quitar type hint o usar sin anotación |
| `ElevatedButton(text="...")` | `Button("...")` (texto posicional) |
| `e.delta_x` en DragUpdateEvent | `e.delta.dx` |
| `animate_offset=ft.Animation.curve` | `animate_offset=True` |

**Referencia de coordenadas para `ft.Alignment(x, y)`:**

| Posicion | x | y |
|----------|---|---|
| center | 0 | 0 |
| top_left | -1 | -1 |
| top_center | 0 | -1 |
| top_right | 1 | -1 |
| center_left | -1 | 0 |
| center_right | 1 | 0 |
| bottom_left | -1 | 1 |
| bottom_center | 0 | 1 |
| bottom_right | 1 | 1 |

**Archivos modificados:** `main.py`, `main1.py`, `main3.py`, `main6.py`, `main7.py`, `main8.py`, `main9.py`, `main10.py`, `main11.py`, `main12.py`, `ui/loader.py`, `ui/event_handler.py`, `ui/components.py`, `ui/utils.py`
