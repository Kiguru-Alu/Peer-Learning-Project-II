 # Appointment logic
import datetime
from utils.storage import save_user_data

def show_reminders(user_data, username):
    reminders = user_data.get("reminders", [])
    
    if not reminders:
        print("\n📭 You have no upcoming reminders.")
        return

    print("\n📅 Your Appointment Reminders:")
    for idx, r in enumerate(reminders, 1):
        print(f"{idx}. {r['date']} - {r.get('time', 'Anytime')} | {r['note']}")

def add_reminder(user_data, username):
    print("\n➕ Add a New Reminder")
    date = input("Enter date (YYYY-MM-DD): ").strip()
    time = input("Enter time (optional, e.g., 14:00): ").strip()
    note = input("What is this reminder for? ").strip()

    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format.")
        return

    reminder = {"date": date, "time": time, "note": note}
    user_data.setdefault("reminders", []).append(reminder)
    save_user_data(username, user_data)
    print("✅ Reminder added successfully.")

def delete_reminder(user_data, username):
    reminders = user_data.get("reminders", [])
    if not reminders:
        print("⚠️ No reminders to delete.")
        return

    print("\n🗑️ Delete a Reminder:")
    for idx, r in enumerate(reminders, 1):
        print(f"{idx}. {r['date']} - {r.get('time', 'Anytime')} | {r['note']}")

    choice = input("Enter the number to delete or press Enter to cancel: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(reminders)):
        print("❌ Invalid choice or cancelled.")
        return

    removed = reminders.pop(int(choice)-1)
    save_user_data(username, user_data)
    print(f"🗑️ Removed reminder for {removed['date']}: {removed['note']}")