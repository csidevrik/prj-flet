import flet as ft
from typing import List, Callable, Optional, Dict

class FileList(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.files: List[Dict] = []  # Cambiado a List[Dict]
        self.on_delete: Optional[Callable] = None
        
    def build(self):
        self.files_column = ft.Column(spacing=10)
        return self.files_column
    
    def add_file(self, file: Dict):
        """
        Agrega un archivo a la lista
        
        Args:
            file: Diccionario con información del archivo {name, path, size}
        """
        file_row = ft.Row(
            controls=[
                ft.Icon(ft.icons.DESCRIPTION, color=ft.colors.BLUE),
                ft.Text(
                    f"{file['name']} ({self.format_size(file['size'])})",
                    expand=True
                ),
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    icon_size=16,
                    on_click=lambda e, f=file: self.remove_file(f)
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        self.files.append(file)
        self.files_column.controls.append(file_row)
        self.update()
    
    def remove_file(self, file: Dict):
        """
        Elimina un archivo de la lista
        
        Args:
            file: Diccionario con información del archivo
        """
        self.files.remove(file)
        self.files_column.controls = [
            control for control in self.files_column.controls 
            if control.controls[1].value.split(" (")[0] != file['name']
        ]
        if self.on_delete:
            self.on_delete(file)
        self.update()
    
    def clear(self):
        """Limpia la lista de archivos"""
        self.files.clear()
        self.files_column.controls.clear()
        self.update()
    
    def format_size(self, size_mb: float) -> str:
        """
        Formatea el tamaño del archivo
        
        Args:
            size_mb: Tamaño en megabytes
            
        Returns:
            str: Tamaño formateado (ej: "1.5 MB")
        """
        return f"{size_mb:.1f}MB"
    
    @property
    def total_size(self) -> float:
        """
        Calcula el tamaño total de todos los archivos
        
        Returns:
            float: Tamaño total en megabytes
        """
        return sum(file['size'] for file in self.files)
    
    @property
    def file_count(self) -> int:
        """
        Obtiene el número total de archivos
        
        Returns:
            int: Número de archivos en la lista
        """
        return len(self.files)
    
    def get_file_paths(self) -> List[str]:
        """
        Obtiene la lista de rutas de los archivos
        
        Returns:
            List[str]: Lista de rutas de archivos
        """
        return [file['path'] for file in self.files]
    
    def set_on_delete(self, callback: Callable):
        """
        Establece el callback para cuando se elimina un archivo
        
        Args:
            callback: Función a llamar cuando se elimina un archivo
        """
        self.on_delete = callback
    
    def is_empty(self) -> bool:
        """
        Verifica si la lista está vacía
        
        Returns:
            bool: True si no hay archivos, False en caso contrario
        """
        return len(self.files) == 0