 # Appointment logic
import datetime
from utils.storage import save_user_data
import mysql.connector
from utils.my_sql_storage import db_config , add_reminder_to_db, get_reminders, delete_reminder_by_index

def show_reminders(user_data, username):
    # ✅ Try fetching from MySQL
    try:
        reminders = get_reminders(username)
        if reminders:
            print("\n📅 Your Appointment Reminders (from MySQL):")
            for idx, r in enumerate(reminders, 1):
                print(f"{idx}. {r['date']} - {r.get('time', 'Anytime')} | {r['reminder']}")
            return
    except Exception as err:
        print(f"⚠️ MySQL Fetch Error: {err}")

    # ✅ Fallback to JSON
    reminders = user_data.get("reminders", [])
    if not reminders:
        print("\n📭 You have no upcoming reminders.")
        return

    print("\n📅 Your Appointment Reminders (from JSON):")
    for idx, r in enumerate(reminders, 1):
        print(f"{idx}. {r['date']} - {r.get('time', 'Anytime')} | {r['note']}")


def add_reminder(user_data, username):
    print("\n➕ Add a New Reminder")
    date_str = input("Enter date (YYYY-MM-DD): ").strip()
    time_str = input("Enter time (optional, e.g., 14:00): ").strip()
    note = input("What is this reminder for? ").strip()

    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("❌ Invalid date format.")
        return

    # Save to JSON (as strings)
    reminder_for_json = {
        "date": date_str,
        "time": time_str,
        "note": note
    }
    user_data.setdefault("reminders", []).append(reminder_for_json)
    save_user_data(username, user_data)

    # Save to MySQL (with date object)
    try:
        add_reminder_to_db(username, date_obj, time_str, note)
        print("✅ Reminder added successfully (JSON + MySQL).")
    except Exception as e:
        print(f"⚠️ MySQL Insert Error: {e}")


def delete_reminder(user_data, username):
    # Fetch reminders from MySQL first
    reminders = get_reminders(username)
    if not reminders:
        print("⚠️ No reminders found to delete.")
        return

    print("\n🗑️ Select a Reminder to Delete:")
    for idx, r in enumerate(reminders, 1):
        time_str = r.get("time", "Anytime")
        note_str = r.get("reminder", r.get("note", "No note"))
        print(f"{idx}. {r['date']} - {time_str} | {note_str}")

    choice = input("Enter the number of the reminder to delete or press Enter to cancel: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(reminders)):
        print("❌ Invalid choice or cancelled.")
        return

    index_to_delete = int(choice) - 1

    # Delete from MySQL by index
    delete_reminder_by_index(username, index_to_delete)

    # Delete from JSON reminders list if exists
    json_reminders = user_data.get("reminders", [])
    if json_reminders:
        # We try to match the reminder by fields
        to_delete = reminders[index_to_delete]
        user_data["reminders"] = [
            r for r in json_reminders
            if not (r.get("date") == to_delete["date"] and
                    r.get("time") == to_delete.get("time") and
                    (r.get("note") == to_delete.get("note") or r.get("reminder") == to_delete.get("reminder")))
        ]
        save_user_data(username, user_data)
        print("🗑️ Reminder deleted from JSON as well.")
