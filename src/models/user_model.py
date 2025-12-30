import json
import os

FOLDER_USERS = "data/users"


def save_user_data(username, data):
    os.makedirs(FOLDER_USERS, exist_ok=True)
    filepath = os.path.join(FOLDER_USERS, f"{username.lower()}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_user_data(username):
    filepath = os.path.join(FOLDER_USERS, f"{username.lower()}.json")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def get_all_usernames():
    if not os.path.exists(FOLDER_USERS):
        return []
    return [
        f.replace(".json", "").capitalize()
        for f in os.listdir(FOLDER_USERS)
        if f.endswith(".json")
    ]
