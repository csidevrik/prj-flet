## prj-flet

Este repo trata de recopilar todos los trabajos que hago con flet y python

**Index**

1. [Instalacion en linux](#id1)
2. [En fedora](#id2)
3. [Migracion a Flet 0.80+](#migracion-flet-080)

---

## Instalacion en linux

Hoy domingo me di cuenta que al tratar de usar flet con este ejemplo

https://flet.dev/docs/controls/searchbar/

Esto no me corria ni en windows ni en linux, luego averiguando me di cuenta que podia ser la version de flet, y es que para windows y linux se usa el mismo comando que es el siguiente:

```
    python -m pip install --upgrade flet
```

### En fedora

En fedora tuve problemillas que surgieron pero voy a comentar la manera en la que se resolvi\[o\].

Primero he tratado con instalar mpvlibs, en fedora trate de utilizar la ultima version de la libreria.

```
    sudo dnf install mpv-libs-0.35.1-2.fc37.x86_64 
```

Lamentablemente con esta libreria que en escencia es la mas actualizada, nada pues toco googlear and i find a foro talking about the versions of the librarie mpv then i uninstall the version mpv-libs-0.35 por la libreria mpv-libs-0.34 pues con esta ya no tuvimos problemas al menos en linux fedora 37.

```
    sudo dnf install mpv-libs-0.34.1-11.fc37.x86_64
```


## Migracion a Flet 0.80+

Al actualizar a Flet 0.80, la API cambio de manera significativa. A continuacion se describen los cambios aplicados en `app/src/main.py` para que el proyecto funcione correctamente con la nueva version.

### Resumen de cambios

#### 1. Punto de entrada: `ft.app()` → `ft.run()`

`ft.app()` fue deprecado. Ahora el argumento `target` es posicional:

```python
# Antes
ft.app(target=main, assets_dir="assets")

# Despues
ft.run(main, assets_dir="assets")
```

#### 2. Funcion `main`: ya no necesita ser `async`

En Flet 0.80+ la funcion principal puede ser sincrona si no usa `await` internamente:

```python
# Antes
async def main(page: ft.Page):

# Despues
def main(page: ft.Page):
```

#### 3. Alineacion: `ft.alignment.top_left` → `ft.Alignment(-1, -1)`

Las constantes del modulo `ft.alignment` fueron eliminadas. Ahora se usa la clase `ft.Alignment` directamente con valores numericos:

```python
# Antes
begin=ft.alignment.top_left

# Despues
begin=ft.Alignment(-1, -1)
```

#### 4. Borde: `ft.border.only()` → `ft.Border.only()`

```python
# Antes
border=ft.border.only(left=ft.BorderSide(1, "green"))

# Despues
border=ft.Border.only(left=ft.BorderSide(1, "green"))
```

#### 5. Boton: `ft.ElevatedButton` → `ft.Button`

`ElevatedButton` fue deprecado. El nuevo `ft.Button` no acepta `text` ni `icon` directamente; se usa `content`:

```python
# Antes
ft.ElevatedButton(
    text="Open Directory",
    icon=ft.Icons.FOLDER_OPEN,
    on_click=...,
)

# Despues
ft.Button(
    content=ft.Row(
        controls=[ft.Icon(ft.Icons.FOLDER_OPEN), ft.Text("Open Directory")],
        tight=True,
    ),
    on_click=...,
)
```

#### 6. FilePicker: `on_result` ya no va en el constructor

```python
# Antes
get_directory_dialog = ft.FilePicker(on_result=get_directory_result)

# Despues
get_directory_dialog = ft.FilePicker()
get_directory_dialog.on_result = get_directory_result
```

#### 7. Tipo de evento `FilePickerResultEvent` eliminado

```python
# Antes
def get_directory_result(e: ft.FilePickerResultEvent):

# Despues
def get_directory_result(e):
```

#### 8. Evento de arrastre: `e.delta_x` → `e.local_delta.x`

El objeto `DragUpdateEvent` cambio su estructura. El delta horizontal ahora es `e.local_delta.x`:

```python
# Antes
left01.width += e.delta_x

# Despues
dx = e.local_delta.x
left01.width += dx
```

#### 9. `update()` ya no es awaitable

En Flet 0.80+, tanto `control.update()` como `page.update()` son metodos sincronos:

```python
# Antes
await left01.update()
await page.update()

# Despues
left01.update()
page.update()
```

#### 10. Control de ventana: nueva API `page.window`

```python
# Antes
await page.window_destroy_async()
page.window_minimized = True

# Despues
page.window.destroy()
page.window.minimized = True
```

### Tabla resumen

| Antes (< 0.80)                        | Despues (0.80+)                   |
| ------------------------------------- | --------------------------------- |
| `ft.alignment.top_left`             | `ft.Alignment(-1, -1)`          |
| `ft.border.only()`                  | `ft.Border.only()`              |
| `ft.app(target=main)`               | `ft.run(main)`                  |
| `async def main(page)`              | `def main(page)`                |
| `ft.ElevatedButton(text=...)`       | `ft.Button(content=...)`        |
| `FilePicker(on_result=fn)`          | asignar `picker.on_result = fn` |
| `ft.FilePickerResultEvent`          | eliminado                         |
| `e.delta_x` en DragUpdateEvent      | `e.local_delta.x`               |
| `await control.update()`            | `control.update()`              |
| `await page.window_destroy_async()` | `page.window.destroy()`         |
| `page.window_minimized`             | `page.window.minimized`         |

---

## Por que `page.window.destroy()` requiere `async`/`await`

Al hacer click en el boton de cerrar, si no se usa `async` y `await`, Python lanza este warning y la ventana no se cierra:

```
RuntimeWarning: coroutine 'Window.destroy' was never awaited
```

### Explicacion

En Flet, `page.window.destroy()` esta implementado como una **coroutine** (funcion `async`) porque internamente necesita comunicarse con la capa nativa de Flutter a traves de un canal I/O, lo cual puede tomar tiempo.

Cuando llamas una funcion `async` sin `await`, Python solo **crea** el objeto coroutine pero **nunca lo ejecuta**:

```python
# MAL — solo crea la coroutine, NO la ejecuta. La ventana no se cierra.
def button_exit(e):
    page.window.destroy()
```

```python
# BIEN — ejecuta la coroutine y espera que termine. La ventana se cierra.
async def button_exit(e):
    await page.window.destroy()
```

> **Regla:** para usar `await` dentro de una funcion, esa funcion tambien debe ser `async`.

### Por que otros handlers no necesitan `async`

Los handlers que solo modifican propiedades locales (sin I/O) son sincronos y no necesitan `await`:

```python
def button_maximize(e):
    page.window.height = 1080   # solo asigna un valor local
    page.window.width = 1920
    page.update()               # update() es sincrono en Flet 0.80+

def button_minimize(e):
    page.window.minimized = True
    page.update()
```

Solo `destroy()` (y metodos similares que comunican con la capa nativa) requieren `async`/`await`.

---
