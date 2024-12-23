# harshCrypto.py

import os
from cryptography.fernet import Fernet, InvalidToken


def generate_key(key_path="key.key"):
    """
    Generate an encryption key and save it to a file.

    Args:
        key_path (str): Path to the key file.
    """
    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
        print(f"Key file generated: {key_path}")
    else:
        print(f"Key already exists: {key_path}")


def load_key(key_path="key.key"):
    """
    Load the encryption key from a file.

    Args:
        key_path (str): Path to the key file.

    Returns:
        bytes: The encryption key.
    """
    if os.path.exists(key_path):
        return open(key_path, "rb").read()
    else:
        raise FileNotFoundError(f"Key file not found at {key_path}")


def encrypt_file(file_path, key):
    """
    Encrypt a single file.

    Args:
        file_path (str): Path to the file to be encrypted.
        key (bytes): Encryption key.

    Raises:
        Exception: If the file cannot be encrypted.
    """
    fernet = Fernet(key)
    try:
        with open(file_path, "rb") as f:
            file_data = f.read()

        # Check if the file is already encrypted
        try:
            fernet.decrypt(file_data)
            print(f"File is already encrypted: {file_path}")
            return
        except InvalidToken:
            # Proceed with encryption if not already encrypted
            encrypted_data = fernet.encrypt(file_data)

        with open(file_path, "wb") as f:
            f.write(encrypted_data)
        print(f"File encrypted: {file_path}")
    except Exception as e:
        raise Exception(f"Failed to encrypt {file_path}: {e}")


def decrypt_file(file_path, key):
    """
    Decrypt a single file.

    Args:
        file_path (str): Path to the file to be decrypted.
        key (bytes): Encryption key.

    Raises:
        Exception: If the file cannot be decrypted.
    """
    fernet = Fernet(key)
    try:
        with open(file_path, "rb") as f:
            file_data = f.read()

        decrypted_data = fernet.decrypt(file_data)

        with open(file_path, "wb") as f:
            f.write(decrypted_data)
        print(f"File decrypted: {file_path}")
    except InvalidToken:
        print(f"File is not encrypted: {file_path}")
    except Exception as e:
        raise Exception(f"Failed to decrypt {file_path}: {e}")


def process_directory(directory_path, key, operation):
    """
    Encrypt or decrypt all files in a directory.

    Args:
        directory_path (str): Path to the directory.
        key (bytes): Encryption key.
        operation (str): 'encrypt' or 'decrypt'.

    Raises:
        ValueError: If an invalid operation is specified.
    """
    if operation not in ("encrypt", "decrypt"):
        raise ValueError("Operation must be 'encrypt' or 'decrypt'")

    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if operation == "encrypt":
                    encrypt_file(file_path, key)
                elif operation == "decrypt":
                    decrypt_file(file_path, key)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
