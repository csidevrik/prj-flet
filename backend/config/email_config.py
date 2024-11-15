from dataclasses import dataclass
from typing import Optional, Dict, Any
import json
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

@dataclass
class EmailConfig:
    smtp_server: str
    smtp_port: int
    email: str
    password: str
    imap_server: Optional[str] = None
    imap_port: int = 993
    
    def __post_init__(self):
        """Validación después de la inicialización"""
        if not self.smtp_server:
            raise ValueError("El servidor SMTP es requerido")
        if not isinstance(self.smtp_port, int) or self.smtp_port <= 0:
            raise ValueError("Puerto SMTP inválido")
        if not self.email or '@' not in self.email:
            raise ValueError("Correo electrónico inválido")
        if not self.password:
            raise ValueError("La contraseña es requerida")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la configuración a un diccionario.
        No incluye la contraseña por seguridad.
        """
        return {
            'smtp_server': self.smtp_server,
            'smtp_port': self.smtp_port,
            'email': self.email,
            'imap_server': self.imap_server,
            'imap_port': self.imap_port
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], password: str) -> 'EmailConfig':
        """
        Crea una instancia de EmailConfig desde un diccionario
        
        Args:
            data: Diccionario con la configuración
            password: Contraseña del correo (se pasa por separado por seguridad)
            
        Returns:
            EmailConfig: Nueva instancia de configuración
            
        Raises:
            ValueError: Si faltan datos requeridos o son inválidos
        """
        try:
            return cls(
                smtp_server=data['smtp_server'],
                smtp_port=int(data['smtp_port']),
                email=data['email'],
                password=password,
                imap_server=data.get('imap_server'),
                imap_port=data.get('imap_port', 993)
            )
        except (KeyError, ValueError) as e:
            logger.error(f"Error creando configuración desde diccionario: {str(e)}")
            raise ValueError(f"Datos de configuración inválidos: {str(e)}")

    def validate(self) -> bool:
        """
        Valida que la configuración sea correcta
        
        Returns:
            bool: True si la configuración es válida
        """
        try:
            self.__post_init__()
            return True
        except ValueError:
            return False
    
    def clone(self, **changes) -> 'EmailConfig':
        """
        Crea una copia de la configuración con cambios opcionales
        
        Args:
            **changes: Cambios a aplicar a la copia
            
        Returns:
            EmailConfig: Nueva instancia con los cambios aplicados
        """
        data = self.to_dict()
        data.update(changes)
        return self.from_dict(data, changes.get('password', self.password))
    
    def __str__(self) -> str:
        """Representación en string sin mostrar la contraseña"""
        return (
            f"EmailConfig(smtp_server='{self.smtp_server}', "
            f"smtp_port={self.smtp_port}, "
            f"email='{self.email}', "
            f"imap_server='{self.imap_server}', "
            f"imap_port={self.imap_port})"
        )
    
    def get_connection_string(self) -> str:
        """
        Obtiene la cadena de conexión (sin contraseña)
        
        Returns:
            str: Cadena de conexión formateada
        """
        return f"smtp://{self.email}@{self.smtp_server}:{self.smtp_port}"