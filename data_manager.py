import os
import json
import shutil
import base64
import hashlib
from pathlib import Path
from cryptography.fernet import Fernet


class DataManager:
    def __init__(self):
        # Dictionary to store username, password length, and salt associated with each domain
        self.username_dict = {}
        self.length_dict = {}
        self.checkbox_dict = {}
        self.salt_dict = {}

        # Determine the data directory path based on the platform
        if os.name == 'posix':  # iOS and Android use POSIX paths
            # Use internal app storage directory
            self.data_dir = Path("Kitpass")
        elif os.name == 'nt':  # Windows
            self.data_dir = Path(os.getenv("APPDATA")) / "Kitpass"
        else:
            raise NotImplementedError("Platform not supported")

        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load_data(self, key):
        """
        Load the encrypted data from the file, decrypt it, and update the dictionaries.
        """
        data_file = self.data_dir / "data.json"
        if data_file.exists():
            with data_file.open("rb") as file:
                encrypted_data = file.read()

            decrypted_data = self.decrypt_data(encrypted_data, key)
            if decrypted_data:
                data = json.loads(decrypted_data)
                self.username_dict = data.get("username_dict", {})
                self.length_dict = data.get("length_dict", {})
                self.checkbox_dict = data.get("checkbox_dict", {})
                self.salt_dict = data.get("salt_dict", {})
                return decrypted_data
            return None

        else:  # Le fichier n'existe pas, initialisez les dictionnaires vides
            self.username_dict = {}
            self.length_dict = {}
            self.checkbox_dict = {}
            self.salt_dict = {}
            self.save_data(key)
            with data_file.open("rb") as file:
                encrypted_data = file.read()
            decrypted_data = self.decrypt_data(encrypted_data, key)
            data = json.loads(decrypted_data)
            return decrypted_data

    def save_data(self, key):
        """
        Encrypt the data and save it to the file.
        """
        data = {
            "username_dict": self.username_dict,
            "length_dict": self.length_dict,
            "checkbox_dict": self.checkbox_dict,
            "salt_dict": self.salt_dict,
        }
        data_json = json.dumps(data)
        encrypted_data = self.encrypt_data(data_json, key)

        data_file = self.data_dir / "data.json"
        with data_file.open("wb") as file:
            file.write(encrypted_data)

    def encrypt_data(self, data, master_password):
        """
        Encrypt the data using Fernet encryption with the master password as the key.
        """
        # Derive a key from the master password using a key derivation function
        key = hashlib.pbkdf2_hmac(
            "sha256",
            master_password,
            b"salt",  # Replace with a proper salt value
            100000,  # Number of iterations (adjust as needed)
            dklen=32,  # Key length in bytes
        )

        # Use the derived key to initialize Fernet encryption
        cipher_suite = Fernet(base64.urlsafe_b64encode(key))

        # Encrypt the data
        encrypted_data = cipher_suite.encrypt(data.encode())

        return encrypted_data

    def decrypt_data(self, encrypted_data, master_password):
        """
        Decrypt the data using Fernet decryption with the master password as the key.
        """
        # Derive the key from the master password (same as in encrypt_data)
        key = hashlib.pbkdf2_hmac(
            "sha256",
            master_password,
            b"salt",  # Replace with the same salt used for encryption
            100000,  # Number of iterations (adjust as needed)
            dklen=32,  # Key length in bytes
        )

        try:
            # Use the derived key to initialize Fernet decryption
            cipher_suite = Fernet(base64.urlsafe_b64encode(key))

            # Decrypt the data
            decrypted_data = cipher_suite.decrypt(encrypted_data).decode()

            return decrypted_data
        except Exception as e:
            print("Error decrypting data:", e)
            return None

    def export_data(self, filename, download_path=None):
        """
        Export the data to a JSON file in the specified location.
        """
        data_json = self.data_dir / "data.json"

        if os.name == 'nt':
            # Créez le chemin complet du fichier d'exportation
            export_file_path = os.path.join(download_path, filename)
            # Utilisez shutil.copy pour copier le fichier data.json
            shutil.copy(str(data_json), export_file_path)

        # if os.name == 'posix':
            from androidstorage4kivy import ShareSheet, SharedStorage

            # Lisez le contenu du fichier data.json
            with open(data_json, "r") as f:
                data_content = f.read()

            # Créez un fichier dans le répertoire de cache avec le contenu
            filename = os.path.join(
                SharedStorage().get_cache_dir(), 'data.json')
            with open(filename, "w") as f:
                f.write(data_content)

            # Insérez le fichier dans le stockage partagé de l'application
            file = SharedStorage().copy_to_shared(filename)
            ShareSheet().share_file(file)
            return file

    def import_data(self, source_file):
        destination_path = self.data_dir / "data.json"
        if os.name == 'nt':
            try:
                shutil.move(source_file, destination_path)
            except FileNotFoundError:
                shutil.copy(source_file, destination_path)
        # if os.name == 'posix':
            from androidstorage4kivy import SharedStorage

            # Lisez le contenu du fichier data.json
            with open(destination_path, "r") as f:
                data_content = f.read()

            with open(source_file, "w") as f:
                f.write(data_content)

            SharedStorage().delete_shared(source_file)

    def reset_data(self, file):
        data_path = self.data_dir / file
        data_path.unlink()
