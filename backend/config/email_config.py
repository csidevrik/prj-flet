from dataclasses import dataclass
from typing import Optional
import json
import os
from pathlib import Path

@dataclass
class EmailConfig:
    smtp_server: str
    smtp_port: int
    email: str
    password: str
    imap_server: Optional[str] = None
    imap_port: int = 993

    def to_dict(self):
        return {
            'smtp_server': self.smtp_server,
            'smtp_port': self.smtp_port,
            'email': self.email,
            'imap_server': self.imap_server,
            'imap_port': self.imap_port
        }

    @classmethod
    def from_dict(cls, data: dict, password: str):
        return cls(
            smtp_server=data['smtp_server'],
            smtp_port=data['smtp_port'],
            email=data['email'],
            password=password,
            imap_server=data.get('imap_server'),
            imap_port=data.get('imap_port', 993)
        )