 # Load, save, update user data
import json
import os
import datetime

DATA_FOLDER = "data/users"

def normalize_dates(obj):
    """
    Recursively convert all datetime.date or datetime.datetime objects to ISO string format in a dict or list.
    """
    if isinstance(obj, dict):
        return {k: normalize_dates(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [normalize_dates(item) for item in obj]
    elif isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    else:
        return obj


def ensure_data_folder():
    os.makedirs(DATA_FOLDER, exist_ok=True)

def get_user_file_path(username):
    return os.path.join(DATA_FOLDER, f"preg_user_{username.lower()}.json")

# def save_user_data(username, data):
#     ensure_data_folder()
#     file_path = get_user_file_path(username)
#     normalized_data = normalize_dates(data)   # Convert dates to strings
#     with open(file_path, 'w') as f:
#         json.dump(data, f, indent=4)
def save_user_data(username, data):
    filename = get_user_file_path(username)
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2, default=str)  # ⬅️ fixes JSON errors
    except Exception as e:
        print(f"❌ Failed to save JSON data: {e}")



def load_user_data(username):
    file_path = get_user_file_path(username)
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r') as f:
        return json.load(f)

def list_all_users():
    ensure_data_folder()
    users = []
    for filename in os.listdir(DATA_FOLDER):
        if filename.startswith("preg_user_") and filename.endswith(".json"):
            username = filename[len("preg_user_"):-len(".json")]
            users.append(username)
    return users