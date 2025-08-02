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

        return True, "Entry saved successfully."

    except Exception as e:
        return False, f"Error saving entry: {e}"


def search_entry(web):
    if not os.path.exists(DATA_FILE):
        return False, "No data file found."

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        if web in data:
            username = data[web]["username"]
            password = data[web]["password"]
            return True, (username, password)
        elif not web:
            return False, "Please enter website name."
        else:
            return False, "no entry found!"

    except Exception as e:
        return False, f"Error reading file: {e}"


def generate_pass(length=8):
    char = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choices(char, k=length))

    return password


def load_all_data():
    if not os.path.exists("data.json"):
        return {}
    with open("data.json", "r") as file:
        return json.load(file)


def delete_data_by_website(web):
    if not os.path.exists("data.json"):
        return False

    try:
        with open("data.json", "r") as file:
            data = json.load(file)

        if web in data:
            del data[web]
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
            return True

        else:
            return False

    except Exception as e:
        return False, print(f"{e}")


def edit_data_by_website(old_web, new_web, new_user, new_pass):
    if not os.path.exists("data.json"):
        return False

    try:
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
            return True

    except Exception as e:
        return False, print(f"{e}")
