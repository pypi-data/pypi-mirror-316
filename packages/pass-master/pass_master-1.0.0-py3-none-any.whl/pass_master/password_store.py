from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import json
import os
from pathlib import Path
import keyring
from typing import Optional, List, Tuple

class PasswordStore:
    def __init__(self):
        self.app_name = "pass-master"
        self.storage_path = Path.home() / ".pass-master"
        self.storage_file = self.storage_path / "passwords.enc"
        self._ensure_storage_exists()
        
    def _ensure_storage_exists(self):
        """Create storage directory if it doesn't exist"""
        self.storage_path.mkdir(exist_ok=True)
        if not self.storage_file.exists():
            self._save_encrypted({})

    def _get_master_key(self) -> bytes:
        """Get or create master key from system keyring"""
        key = keyring.get_password(self.app_name, "master_key")
        if key is None:
            key = base64.b64encode(Fernet.generate_key()).decode()
            keyring.set_password(self.app_name, "master_key", key)
        return base64.b64decode(key)

    def _get_fernet(self) -> Fernet:
        """Create Fernet instance with master key"""
        return Fernet(self._get_master_key())

    def _save_encrypted(self, data: dict):
        """Save encrypted data to file"""
        f = self._get_fernet()
        encrypted = f.encrypt(json.dumps(data).encode())
        self.storage_file.write_bytes(encrypted)

    def _load_encrypted(self) -> dict:
        """Load and decrypt data from file"""
        if not self.storage_file.exists():
            return {}
        f = self._get_fernet()
        encrypted = self.storage_file.read_bytes()
        decrypted = f.decrypt(encrypted)
        return json.loads(decrypted)

    def add_password(self, service: str, username: str, password: str, category: Optional[str] = None):
        """Add or update a password entry"""
        data = self._load_encrypted()
        data[service] = {
            "username": username,
            "password": password,
            "category": category
        }
        self._save_encrypted(data)

    def get_password(self, service: str) -> Optional[Tuple[str, str, Optional[str]]]:
        """Get password entry for a service"""
        data = self._load_encrypted()
        if service in data:
            entry = data[service]
            return entry["username"], entry["password"], entry.get("category")
        return None

    def delete_password(self, service: str) -> bool:
        """Delete a password entry"""
        data = self._load_encrypted()
        if service in data:
            del data[service]
            self._save_encrypted(data)
            return True
        return False

    def list_services(self, category: Optional[str] = None) -> List[Tuple[str, str, Optional[str]]]:
        """List all stored services, optionally filtered by category"""
        data = self._load_encrypted()
        result = []
        for service, entry in data.items():
            if category is None or entry.get("category") == category:
                result.append((
                    service,
                    entry["username"],
                    entry.get("category")
                ))
        return sorted(result)

    def search_services(self, query: str) -> List[Tuple[str, str, Optional[str]]]:
        """Search for services matching query"""
        data = self._load_encrypted()
        result = []
        query = query.lower()
        for service, entry in data.items():
            if (query in service.lower() or 
                query in entry["username"].lower() or 
                (entry.get("category") and query in entry["category"].lower())):
                result.append((
                    service,
                    entry["username"],
                    entry.get("category")
                ))
        return sorted(result)

    def export_data(self) -> dict:
        """Export all password data"""
        return self._load_encrypted() 