prj-flet
----------

Este repo trata de recopilar todos los trabajos que hago con flet y python

**Index**
1. [Instalacion en linux](#id1)
2. [En fedora](#id2)

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

