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

    def connect(self, config: EmailConfig) -> Tuple[bool, str]:
        """Establece la conexión con el servidor SMTP"""
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(config.smtp_server, config.smtp_port, context=context) as server:
                server.login(config.email, config.password)
                self.config = config
                self.is_connected = True
                logger.info(f"Conexión exitosa a {config.smtp_server}")
                return True, "Conexión exitosa"
        except Exception as e:
            logger.error(f"Error de conexión: {str(e)}")
            return False, f"Error: {str(e)}"

    def send_email(self, to_emails: List[str], subject: str, body: str, 
                  attachments: List[str] = None) -> Tuple[bool, str]:
        """Envía un correo electrónico"""
        if not self.is_connected:
            return False, "No hay conexión establecida"

        # Validar correos destinatarios
        for email in to_emails:
            if not validate_email(email):
                return False, f"Correo inválido: {email}"

        try:
            msg = MIMEMultipart()
            msg['From'] = self.config.email
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            if attachments:
                for file_path in attachments:
                    with open(file_path, 'rb') as f:
                        part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                        msg.attach(part)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.config.smtp_server, self.config.smtp_port, context=context) as server:
                server.login(self.config.email, self.config.password)
                server.send_message(msg)

            logger.info(f"Correo enviado exitosamente a {', '.join(to_emails)}")
            return True, "Correo enviado exitosamente"

        except Exception as e:
            logger.error(f"Error enviando correo: {str(e)}")
            return False, f"Error: {str(e)}"
