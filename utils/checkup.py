 # Add/view checkups
import datetime
from utils.storage import save_user_data
import mysql.connector
from utils.my_sql_storage import db_config, add_checkup_mysql, get_checkups

def add_checkup(user_data, username):
    print("\n🩺 Add Check-Up Record")
    date = input("Date of visit (YYYY-MM-DD): ").strip()
    doctor = input("Doctor/Hospital name: ").strip()
    notes = input("Any notes? (optional): ").strip()

    try:
        # Confirm the format is valid
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format.")
        return

    # ✅ Use string for date (works for both JSON and MySQL)
    record = {"date": date, "doctor": doctor, "notes": notes}
    user_data.setdefault("checkups", []).append(record)

    # ✅ Save to JSON
    save_user_data(username, user_data)

    # ✅ Save to MySQL
    add_checkup_mysql(username, date, doctor, notes)

    print("✅ Check-up record saved.")



def view_checkup_history(user_data, username):
    # Try fetching from MySQL first
    try:
        checkups = get_checkups(username)
    except mysql.connector.Error as err:
        print(f"⚠️ MySQL Fetch Error: {err}")
        checkups = []

    # ✅ Only fallback to JSON if MySQL returned nothing
    if not checkups:
        checkups = user_data.get("checkups", [])

    if not checkups:
        print("📭 No check-up records found.")
        return

    print("\n📚 Check-Up History:")
    for idx, c in enumerate(checkups, 1):
        print(f"{idx}. {c['date']} - {c['doctor']}")
        if c.get("notes"):
            print(f"    📝 Notes: {c['notes']}")
