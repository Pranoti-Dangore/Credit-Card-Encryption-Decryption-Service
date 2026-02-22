import json
import os
import base64
import uuid
from cryptography.fernet import Fernet

DATA_FILE = "storage.json"
KEY_FILE = "secret.key"


# Generate or load encryption key
def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return key


# Mask credit card
def mask_pan(pan):
    return "**** **** **** " + pan[-4:]


# Generate token
def generate_token():
    return "TK_" + uuid.uuid4().hex[:8]


# Load storage
def load_storage():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


# Save storage
def save_storage(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def encrypt_pan(pan, cipher):
    encrypted = cipher.encrypt(pan.encode())
    return base64.urlsafe_b64encode(encrypted).decode()


def decrypt_pan(token, cipher, storage):
    if token not in storage:
        print("Token not found.")
        return
    encrypted_data = base64.urlsafe_b64decode(storage[token].encode())
    decrypted = cipher.decrypt(encrypted_data).decode()
    print("Decrypted PAN:", decrypted)


def main():
    key = load_key()
    cipher = Fernet(key)
    storage = load_storage()

    print("\nCredit Card Encryption System")
    print("1. Encrypt Card")
    print("2. Decrypt Card")
    choice = input("Select option: ")

    if choice == "1":
        pan = input("Enter credit card number: ")

        if len(pan) < 12:
            print("Invalid card number")
            return

        encrypted_pan = encrypt_pan(pan, cipher)
        token = generate_token()

        storage[token] = encrypted_pan
        save_storage(storage)

        print("\nCard Encrypted Successfully")
        print("Token:", token)
        print("Masked Card:", mask_pan(pan))
        print("Raw PAN is NOT stored.")

    elif choice == "2":
        token = input("Enter token: ")
        decrypt_pan(token, cipher, storage)

    else:
        print("Invalid option")


if __name__ == "__main__":
    main()