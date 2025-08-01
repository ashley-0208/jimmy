import json
import os
import random
import string

DATA_FILE = "data.json"


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
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                data = json.load(file)

        else:
            data = {}

        data.update(new_entry)

        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

    except Exception as e:
        return False, f"Error saving entry: {e}"


def generate_pass(length=8):
    char = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choices(char, k=length))

    return password

