import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

# ---------------- DB CONFIG ----------------
db_config = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": "peer_learning_project2"
}

# ---------------- CONNECTION ----------------
def get_connection():
    try:
        return mysql.connector.connect(**db_config)
    except Error as e:
        print(f"⚠️ Connection Error: {e}")
        return None

# ---------------- TEST CONNECTION (optional) ----------------
try:
    print("Attempting to connect to the database...")
    connection = get_connection()
    if connection and connection.is_connected():
        db_info = connection.get_server_info()
        print(f"✅ Connected to MySQL Server version {db_info}")
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        database = cursor.fetchone()
        print(f"📂 Connected to database: {database[0]}")
        cursor.close()
        connection.close()
except Error as err:
    print(f"⚠️ Database error: {err}")

# ---------------- USER FUNCTIONS ----------------


def get_user(username):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE name = %s", (username, ))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    except Error as e:
        print(f"MySQL Error (get_user): {e}")
        return None

def get_user_id(username):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE name = %s", (username, ))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return row[0]
        return None
    except Error as e:
        print(f"MySQL Error (get_user_id): {e}")
        return None

def save_user(user):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO users (name, age, due_date, current_week)
        VALUES (%s, %s, %s, %s )
        ON DUPLICATE KEY UPDATE
            age = VALUES(age),
            due_date = VALUES(due_date),
            current_week = VALUES(current_week)
        """
        cursor.execute(query, (user["name"], user["age"], user["due_date"], user["current_week"],))
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(f"MySQL Error (save_user): {e}")

def list_users():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM users")
        users = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return users
    except Error as e:
        print(f"MySQL Error (list_users): {e}")
        return []

# ---------------- REMINDER FUNCTIONS ----------------

def get_reminders(username):
    user_id = get_user_id(username)
    if user_id is None:
        print(f"User '{username}' not found in DB.")
        return []

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reminders WHERE user_id = %s ORDER BY date", (user_id,))
        reminders = cursor.fetchall()
        cursor.close()
        conn.close()
        return reminders
    except Error as e:
        print(f"MySQL Error (get_reminders): {e}")
        return []

def add_reminder_to_db(username, date, time, note):
    user_id = get_user_id(username)
    if user_id is None:
        print(f"User '{username}' not found in DB.")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Ensure the table has columns `date`, `time`, and `reminder`
        query = "INSERT INTO reminders (user_id, date, time, reminder) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (user_id, date, time, note))
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Reminder added to database.")
    except Error as e:
        print(f"MySQL Error (add_reminder_to_db): {e}")

def delete_reminder_by_index(username, index):
    user_id = get_user_id(username)
    if user_id is None:
        print(f"User '{username}' not found in DB.")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM reminders WHERE user_id = %s ORDER BY date", (user_id,))
        reminder_ids = [row[0] for row in cursor.fetchall()]

        if 0 <= index < len(reminder_ids):
            reminder_id = reminder_ids[index]
            cursor.execute("DELETE FROM reminders WHERE id = %s", (reminder_id,))
            conn.commit()
            print("🗑️ Reminder deleted successfully.")
        else:
            print("❌ Invalid index.")

        cursor.close()
        conn.close()
    except Error as e:
        print(f"MySQL Error (delete_reminder_by_index): {e}")

# ---------------- CHECKUPS ----------------

def get_checkups(username):
    user_id = get_user_id(username)
    if user_id is None:
        print(f"User '{username}' not found in DB.")
        return []

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM checkups WHERE user_id = %s ORDER BY date DESC", (user_id,))
        checkups = cursor.fetchall()
        cursor.close()
        conn.close()
        return checkups
    except Error as e:
        print(f"MySQL Error (get_checkups): {e}")
        return []

def add_checkup_mysql(username, date, doctor, notes):
    user_id = get_user_id(username)
    if user_id is None:
        print(f"User '{username}' not found in DB.")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO checkups (user_id, date, doctor, notes) VALUES (%s, %s, %s, %s)",
            (user_id, date, doctor, notes)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(f"MySQL Error (add_checkup): {e}")