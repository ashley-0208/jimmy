import json
import os
import random
import string
from cryptography.fernet import Fernet


DATA_FILE = "data.json"


def load_decrypted_data():
    try:
        decrypt_file(DATA_FILE)
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        encrypt_file(DATA_FILE)
        return data

    except Exception as e:
        print(f"Failed to load decrypted data: {e}")
        return {}, f"{e}"


def add_entry(web, user, pswd):
    if not web or not user or not pswd:
        return False, "All fields are required"

    new_entry = {
        web: {
            "username": user,
            "password": pswd
        }

    }

    try:
        decrypt_file("data.json")
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                data = json.load(file)

        else:
            data = {}
        data.update(new_entry)

        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
        encrypt_file("data.json")

        return True, "Entry saved successfully."

    except Exception as e:
        print(f"Error saving entry: {e}")
        return False, f"Error saving entry: {e}"


def search_entry(web):
    if not os.path.exists(DATA_FILE):
        return False, "No data file found."

    try:
        data = load_decrypted_data()

        if web in data:
            username = data[web]["username"]
            password = data[web]["password"]
            return True, (username, password)
        elif not web:
            return False, "Please enter website name."
        else:
            return False, "no entry found!"

    except Exception as e:
        print(f"Error reading file: {e}")
        return False, f"{e}"


def generate_pass(length=8):
    char = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choices(char, k=length))

    return password


def load_all_data():
    if not os.path.exists("data.json"):
        return {}
    try:
        data, _ = load_decrypted_data()
        return data

    except:
        return {}


def delete_data_by_website(web):
    if not os.path.exists("data.json"):
        return False

    try:
        decrypt_file("data.json")
        with open("data.json", "r") as file:
            data = json.load(file)

        if web in data:
            del data[web]
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
            encrypt_file("data.json")
            return True

        else:
            return False

    except Exception as e:
        print(f"{e}")
        return False, f"{e}"


def edit_data_by_website(old_web, new_web, new_user, new_pass):
    if not os.path.exists("data.json"):
        return False

    try:
        decrypt_file("data.json")
        with open("data.json", "r") as file:
            data = json.load(file)

        if old_web not in data:
            return  False
        else:
            del data[old_web]
            data[new_web] = {
                "username": new_user,
                "password": new_pass
            }
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
            encrypt_file("data.json")
            return True

    except Exception as e:
        print(f"{e}")
        return False, f"{e}"


# ---- ENCRYPTION AND DECRYPTION ----
def load_key():
    with open("secret.key", "rb") as f:
        return f.read()


def encrypt_file(filename):
    key = load_key()
    fernet = Fernet(key)

    with open(filename, "rb") as f:
        original = f.read()

    encrypted = fernet.encrypt(original)

    with open(filename, "wb") as en_f:
        en_f.write(encrypted)


encrypt_file("data.json")


def decrypt_file(filename):
    key = load_key()
    fernet = Fernet(key)

    with open(filename, "rb") as en_f:
        encrypted = en_f.read()

    try:
        decrypted = fernet.decrypt(encrypted)
        with open(filename, "wb") as dec_f:
            dec_f.write(decrypted)
        return True

    except Exception as e:
        print(f"Failed to decrypt: {e}")
        return False, f"Failed to decrypt: {e}"
