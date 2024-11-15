import json
import keyring
import logging
import os
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
from ..config.email_config import EmailConfig
from ..utils.security import encrypt_data, decrypt_data

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self):
        """Inicializa el servicio de almacenamiento"""
        self.config_dir = Path.home() / ".email_client"
        self.config_file = self.config_dir / "config.json"
        self.temp_dir = self.config_dir / "temp"
        self.logs_dir = self.config_dir / "logs"
        self.setup_directories()

    def setup_directories(self) -> None:
        """Crea las carpetas necesarias para la aplicación"""
        try:
            # Crear directorios si no existen
            self.config_dir.mkdir(parents=True, exist_ok=True)
            self.temp_dir.mkdir(exist_ok=True)
            self.logs_dir.mkdir(exist_ok=True)

            # Limpiar archivos temporales antiguos
            self.cleanup_temp_files()
            
            logger.info("Directorios de la aplicación configurados correctamente")
        except Exception as e:
            logger.error(f"Error configurando directorios: {str(e)}")
            raise

    def save_config(self, config: EmailConfig) -> bool:
        """
        Guarda la configuración de manera segura
        
        Args:
            config: Objeto EmailConfig con la configuración a guardar
            
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        try:
            # Preparar datos para guardar
            config_data = {
                'smtp_server': config.smtp_server,
                'smtp_port': config.smtp_port,
                'email': config.email,
                'imap_server': config.imap_server,
                'imap_port': config.imap_port,
                'last_updated': datetime.now().isoformat()
            }

            # Guardar datos no sensibles en archivo
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4)

            # Guardar contraseña de forma segura usando keyring
            keyring.set_password("email_client", config.email, config.password)

            # Guardar una copia de respaldo
            self.backup_config()
            
            logger.info(f"Configuración guardada exitosamente para {config.email}")
            return True

        except Exception as e:
            logger.error(f"Error guardando configuración: {str(e)}")
            return False

    def load_config(self) -> Optional[EmailConfig]:
        """
        Carga la configuración guardada
        
        Returns:
            Optional[EmailConfig]: Objeto de configuración o None si hay error
        """
        try:
            if not self.config_file.exists():
                logger.info("No existe archivo de configuración")
                return None

            # Cargar datos del archivo
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Obtener contraseña del keyring
            password = keyring.get_password("email_client", data['email'])
            if not password:
                logger.error("No se encontró la contraseña guardada")
                return None

            # Crear objeto de configuración
            config = EmailConfig(
                smtp_server=data['smtp_server'],
                smtp_port=data['smtp_port'],
                email=data['email'],
                password=password,
                imap_server=data.get('imap_server'),
                imap_port=data.get('imap_port', 993)
            )

            logger.info(f"Configuración cargada exitosamente para {config.email}")
            return config

        except Exception as e:
            logger.error(f"Error cargando configuración: {str(e)}")
            return None

    def backup_config(self) -> bool:
        """
        Crea una copia de respaldo de la configuración
        
        Returns:
            bool: True si se creó el backup correctamente
        """
        try:
            if not self.config_file.exists():
                return False

            # Crear nombre para archivo de backup
            backup_dir = self.config_dir / "backups"
            backup_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backup_dir / f"config_backup_{timestamp}.json"

            # Copiar archivo de configuración
            with open(self.config_file, 'r', encoding='utf-8') as source:
                with open(backup_file, 'w', encoding='utf-8') as target:
                    target.write(source.read())

            # Mantener solo los últimos 5 backups
            self.cleanup_backups()
            
            logger.info(f"Backup de configuración creado: {backup_file.name}")
            return True

        except Exception as e:
            logger.error(f"Error creando backup: {str(e)}")
            return False

    def cleanup_backups(self, keep_last: int = 5) -> None:
        """
        Elimina backups antiguos manteniendo solo los más recientes
        
        Args:
            keep_last: Número de backups a mantener
        """
        try:
            backup_dir = self.config_dir / "backups"
            if not backup_dir.exists():
                return

            # Listar archivos de backup ordenados por fecha
            backup_files = sorted(
                backup_dir.glob("config_backup_*.json"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )

            # Eliminar backups antiguos
            for backup_file in backup_files[keep_last:]:
                backup_file.unlink()
                logger.info(f"Backup antiguo eliminado: {backup_file.name}")

        except Exception as e:
            logger.error(f"Error limpiando backups: {str(e)}")

    def cleanup_temp_files(self, max_age_hours: int = 24) -> None:
        """
        Elimina archivos temporales antiguos
        
        Args:
            max_age_hours: Edad máxima de los archivos en horas
        """
        try:
            if not self.temp_dir.exists():
                return

            current_time = datetime.now().timestamp()
            max_age_seconds = max_age_hours * 3600

            for temp_file in self.temp_dir.iterdir():
                file_age = current_time - temp_file.stat().st_mtime
                if file_age > max_age_seconds:
                    temp_file.unlink()
                    logger.info(f"Archivo temporal eliminado: {temp_file.name}")

        except Exception as e:
            logger.error(f"Error limpiando archivos temporales: {str(e)}")

    def create_temp_file(self, prefix: str = "temp_", suffix: str = "") -> Path:
        """
        Crea un archivo temporal
        
        Args:
            prefix: Prefijo para el nombre del archivo
            suffix: Sufijo para el nombre del archivo
            
        Returns:
            Path: Ruta al archivo temporal creado
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_file = self.temp_dir / f"{prefix}{timestamp}{suffix}"
            temp_file.touch()
            return temp_file

        except Exception as e:
            logger.error(f"Error creando archivo temporal: {str(e)}")
            raise

    def get_storage_info(self) -> Dict[str, Any]:
        """
        Obtiene información sobre el almacenamiento
        
        Returns:
            Dict con información sobre el almacenamiento
        """
        try:
            return {
                'config_dir': str(self.config_dir),
                'config_exists': self.config_file.exists(),
                'temp_files': len(list(self.temp_dir.glob('*'))),
                'backup_files': len(list((self.config_dir / "backups").glob('*.json'))) if (self.config_dir / "backups").exists() else 0,
                'last_modified': datetime.fromtimestamp(self.config_file.stat().st_mtime).isoformat() if self.config_file.exists() else None
            }

        except Exception as e:
            logger.error(f"Error obteniendo información de almacenamiento: {str(e)}")
            return {}

    def delete_config(self) -> bool:
        """
        Elimina la configuración guardada
        
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            # Crear backup antes de eliminar
            self.backup_config()

            # Eliminar archivo de configuración
            if self.config_file.exists():
                self.config_file.unlink()

            # Eliminar contraseña del keyring
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    keyring.delete_password("email_client", data['email'])
            except:
                pass

            logger.info("Configuración eliminada correctamente")
            return True

        except Exception as e:
            logger.error(f"Error eliminando configuración: {str(e)}")
            return False

    def export_config(self, export_path: Path, include_password: bool = False) -> bool:
        """
        Exporta la configuración a un archivo
        
        Args:
            export_path: Ruta donde exportar
            include_password: Si se debe incluir la contraseña encriptada
            
        Returns:
            bool: True si se exportó correctamente
        """
        try:
            if not self.config_file.exists():
                return False

            with open(self.config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)

            if include_password:
                password = keyring.get_password("email_client", config_data['email'])
                if password:
                    config_data['encrypted_password'] = encrypt_data(password)

            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4)

            logger.info(f"Configuración exportada a {export_path}")
            return True

        except Exception as e:
            logger.error(f"Error exportando configuración: {str(e)}")
            return False

    def import_config(self, import_path: Path) -> bool:
        """
        Importa una configuración desde un archivo
        
        Args:
            import_path: Ruta del archivo a importar
            
        Returns:
            bool: True si se importó correctamente
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)

            # Si hay contraseña encriptada, desencriptarla
            if 'encrypted_password' in config_data:
                password = decrypt_data(config_data['encrypted_password'])
                del config_data['encrypted_password']
            else:
                password = None

            # Crear objeto de configuración
            config = EmailConfig(
                smtp_server=config_data['smtp_server'],
                smtp_port=config_data['smtp_port'],
                email=config_data['email'],
                password=password if password else "",
                imap_server=config_data.get('imap_server'),
                imap_port=config_data.get('imap_port', 993)
            )

            # Guardar la configuración
            self.save_config(config)
            
            logger.info(f"Configuración importada desde {import_path}")
            return True

        except Exception as e:
            logger.error(f"Error importando configuración: {str(e)}")
            return False