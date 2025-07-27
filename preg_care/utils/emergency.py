 # utils/emergency.py
import json


def load_emergency_data():
   try:
       with open("assets/emergency.json", "r") as file:
           return json.load(file)
   except FileNotFoundError:
       print("Emergency data file not found.")
       return {}
   except json.JSONDecodeError:
       print("Error decoding emergency data.")
       return {}


def display_emergency_info():
   data = load_emergency_data()
   if not data:
       return


   print("\n📞 Emergency Contacts")
   print("-" * 30)
   for contact in data.get("emergency_contacts", []):
       print(f"{contact['name']} - {contact['number']}")
       print(f"  {contact['description']}\n")


   steps = data.get("emergency_steps", {})
   if not steps:
       print("No emergency steps available.")
       return


   print("\n🚨 Emergency Conditions")
   print("-" * 30)
   conditions = list(steps.keys())
   for i, condition in enumerate(conditions, 1):
       print(f"{i}. {condition.replace('_', ' ').title()}")


   try:
       choice = int(input("\nSelect a condition to view steps (0 to exit): "))
       if choice == 0:
           return
       selected = conditions[choice - 1]


       print(f"\n📝 Steps for {selected.replace('_', ' ').title()}:")
       for step in steps[selected]:
           print(f"- {step}")
   except (ValueError, IndexError):
       print("Invalid selection. Please try again.")


   # Show general notes
   notes = data.get("notes", "")
   if notes:
       print("\n📌 Note:")
       print(notes)

