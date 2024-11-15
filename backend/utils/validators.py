import re
from typing import List

def validate_email(email: str) -> bool:
    """Valida el formato de un correo electrónico"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_file_size(file_path: str, max_size_mb: int = 25) -> bool:
    """Valida el tamaño de un archivo"""
    try:
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        return size_mb <= max_size_mb
    except:
        return False