 # Registration/Login system
import datetime
import mysql.connector
from utils.my_sql_storage import db_config, save_user, get_user
from utils.storage import save_user_data, load_user_data, list_all_users

def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def register_user():
    print("\n--- New User Registration ---")
    username = input("Enter your name: ").strip().lower()
    age = input("Enter your age: ").strip()

    while True:
        due_date = input("Enter your estimated due date (YYYY-MM-DD): ").strip()
        if is_valid_date(due_date):
            break
        print("❌ Invalid date format. Please try again.")

    week_input = input("Do you want to enter your current pregnancy week manually? (y/n): ").strip().lower()
    if week_input == 'y':
        current_week = int(input("Enter your current pregnancy week (1-40): "))
    else:
        current_week = calculate_week_from_due_date(due_date)

    user_data = {
        "name": username,
        "age": age,
        "due_date": due_date,
        "current_week": current_week,
        "checkups": [],
        "reminders": []
    }

    save_user_data(username, user_data)
    print(f"✅ Registered successfully as '{username}'!")
    save_user(user_data)    
    return username, user_data




def login_user():
    print("\n--- Login ---")
    name = input("Enter your full name: ").strip().lower()

    # First try MySQL
    user = get_user(name)
    if user:
        print(f"✅ Welcome back, {user['name'].capitalize()} (from cloud)!")
        return name, user

    # Fallback to JSON list selection if not found in MySQL
    users = list_all_users()
    if not users:
        print("⚠️ No users found. Please register first.")
        return None, None

    print("Available Users:")
    for idx, username in enumerate(users, 1):
        print(f"{idx}. {username}")

    while True:
        choice = input("Select user by number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(users):
            username = users[int(choice)-1]
            data = load_user_data(username)
            print(f"✅ Logged in as '{username}'")
            return username, data
        print("❌ Invalid selection. Try again.")

def calculate_week_from_due_date(due_date_str):
    due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
    today = datetime.date.today()
    delta = (due_date - today).days
    week = 40 - (delta // 7)
    return max(1, min(week, 40))  # Clamp between 1 and 40