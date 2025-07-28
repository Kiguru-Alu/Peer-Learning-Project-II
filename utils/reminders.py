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




def normalize_reminder(r):
    return {
        "date": str(r.get("date", "")).strip(),
        "time": str(r.get("time", "")).strip(),
        "note": str(r.get("note") or r.get("reminder") or "").strip()
    }

def delete_reminder(user_data, username):
    reminders = get_reminders(username)
    if not reminders:
        print("⚠️ No reminders found to delete.")
        return

    print("\n🗑️ Select a Reminder to Delete:")
    for idx, r in enumerate(reminders, 1):
        date_str = str(r.get("date", ""))
        time_str = str(r.get("time", "Anytime"))
        note_str = str(r.get("note") or r.get("reminder") or "No note")
        print(f"{idx}. {date_str} - {time_str} | {note_str}")

    choice = input("Enter the number of the reminder to delete or press Enter to cancel: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(reminders)):
        print("❌ Invalid choice or cancelled.")
        return

    index_to_delete = int(choice) - 1
    to_delete = normalize_reminder(reminders[index_to_delete])

    # Delete from MySQL
    delete_reminder_by_index(username, index_to_delete)

    # Delete from JSON
    json_reminders = user_data.get("reminders", [])
    updated_reminders = []
    deleted = False

    for r in json_reminders:
        current = normalize_reminder(r)
        print(f"Comparing: {current} == {to_delete}")  # Debug log

        if current == to_delete:
            deleted = True
            continue  # Skip this item
        updated_reminders.append(r)

    if deleted:
        user_data["reminders"] = updated_reminders
        save_user_data(username, user_data)
        print("✅ Reminder deleted from JSON.")
    else:
        print("⚠️ Reminder deleted from MySQL, but no match found in JSON.")