import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import logging
from typing import List, Tuple, Optional
from ..config.email_config import EmailConfig
from ..utils.validators import validate_email

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.config: Optional[EmailConfig] = None
        self.is_connected = False
    
    def test_connection(self, config: EmailConfig) -> Tuple[bool, str]:
        """
        Prueba la conexión con el servidor SMTP
        
        Args:
            config: Configuración a probar
            
        Returns:
            tuple: (éxito, mensaje)
        """
        try:
            logger.info(f"Probando conexión a {config.smtp_server}:{config.smtp_port}")
            
            # Crear contexto SSL
            context = ssl.create_default_context()
            
            # Intentar conexión con timeout
            with smtplib.SMTP_SSL(
                config.smtp_server, 
                config.smtp_port, 
                context=context, 
                timeout=10
            ) as server:
                # Intentar login
                server.login(config.email, config.password)
                logger.info("Prueba de conexión exitosa")
                return True, "Conexión exitosa"
                
        except smtplib.SMTPAuthenticationError:
            logger.error("Error de autenticación en prueba de conexión")
            return False, "Usuario o contraseña incorrectos"
        except smtplib.SMTPConnectError:
            logger.error(f"Error conectando a {config.smtp_server}")
            return False, f"No se puede conectar al servidor {config.smtp_server}"
        except socket.timeout:
            logger.error("Timeout en prueba de conexión")
            return False, "Tiempo de espera agotado"
        except socket.gaierror:
            logger.error("Error resolviendo nombre del servidor")
            return False, "No se puede resolver el nombre del servidor"
        except Exception as e:
            logger.error(f"Error en prueba de conexión: {str(e)}")
            return False, f"Error: {str(e)}"

    def connect(self, config: EmailConfig) -> Tuple[bool, str]:
            """
            Establece la conexión con el servidor SMTP
            
            Args:
                config: Configuración del servidor
                
            Returns:
                tuple: (éxito, mensaje)
            """
            try:
                # Probar conexión primero
                success, message = self.test_connection(config)
                if success:
                    self.config = config
                    self.is_connected = True
                    return True, "Conexión establecida"
                return False, message
                    
            except Exception as e:
                logger.error(f"Error estableciendo conexión: {str(e)}")
                return False, f"Error: {str(e)}"

    def send_email(self, to_emails: List[str], subject: str, body: str, 
                  attachments: List[str] = None) -> Tuple[bool, str]:
        """
        Envía un correo electrónico
        
        Args:
            to_emails: Lista de destinatarios
            subject: Asunto del correo
            body: Cuerpo del mensaje
            attachments: Lista opcional de rutas a archivos adjuntos
            
        Returns:
            tuple: (éxito, mensaje)
        """
        if not self.is_connected or not self.config:
            return False, "No hay conexión establecida"

        try:
            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = self.config.email
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            # Adjuntar archivos
            if attachments:
                for file_path in attachments:
                    try:
                        with open(file_path, 'rb') as f:
                            part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                            msg.attach(part)
                    except Exception as e:
                        logger.error(f"Error adjuntando archivo {file_path}: {str(e)}")
                        return False, f"Error con archivo adjunto {os.path.basename(file_path)}: {str(e)}"

            # Enviar correo
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(
                self.config.smtp_server, 
                self.config.smtp_port, 
                context=context
            ) as server:
                server.login(self.config.email, self.config.password)
                server.send_message(msg)

            logger.info(f"Correo enviado exitosamente a {', '.join(to_emails)}")
            return True, "Correo enviado exitosamente"

        except smtplib.SMTPAuthenticationError:
            logger.error("Error de autenticación al enviar correo")
            return False, "Error de autenticación"
        except smtplib.SMTPException as e:
            logger.error(f"Error SMTP al enviar correo: {str(e)}")
            return False, f"Error enviando correo: {str(e)}"
        except Exception as e:
            logger.error(f"Error enviando correo: {str(e)}")
            return False, f"Error: {str(e)}"

    def is_configured(self) -> bool:
        """Verifica si hay una configuración válida"""
        return self.config is not None

    def disconnect(self):
        """Desconecta del servidor"""
        self.config = None
        self.is_connected = False
        logger.info("Desconectado del servidor")
