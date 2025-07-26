# Add/view checkups
import datetime
from utils.storage import save_user_data

def add_checkup(user_data, username) :
    print("\n🩺 Add Check-Up Record")
    date = input("Date of visit (YYYY-MM-DD) : ").strip()
    doctor = input("Doctor/Hospital name: ").strip()
    notes = input("Any notes? (optional): ").strip()

    try:
       datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
       print("❌ Invalid date format.")
       return

   record = {"date": date, "doctor": doctor, "notes": notes}
   user_data.setdefault("checkups", []).append(record)
   save_user_data(username, user_data)
   print("✅ Check-up record saved.")


def view_checkup_history(user_data):
   checkups = user_data.get("checkups", [])
   if not checkups:
       print("📭 No check-up records found.")
       return


   print("\n📚 Check-Up History:")
   for idx, c in enumerate(checkups, 1):
       print(f"{idx}. {c['date']} - {c['doctor']}")
       if c.get("notes"):
           print(f"    📝 Notes: {c['notes']}")

