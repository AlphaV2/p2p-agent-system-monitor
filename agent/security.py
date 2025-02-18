import os
import json
from cryptography.fernet import Fernet

def load_or_generate_key():
    """Load existing encryption key or generate a new one"""
    key_file = os.path.join(os.path.expanduser("~"), ".p2p_agent_key")
    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            return f.read()
    else:
        new_key = Fernet.generate_key()
        with open(key_file, "wb") as f:
            f.write(new_key)
        return new_key

def encrypt_data(data, key):
    """Encrypt data before storage or transmission"""
    cipher = Fernet(key)
    json_data = json.dumps(data)
    encrypted_data = cipher.encrypt(json_data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    """Decrypt data after retrieval or reception"""
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data)
    return json.loads(decrypted_data.decode())
