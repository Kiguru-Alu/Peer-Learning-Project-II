import json
import difflib
# difflib.get_close_matches() provides fuzzy matching so users don't have to be exact.






def load_symptoms():
   try:
       with open("assets/symptoms.json", "r") as file:
           return json.load(file)
   except FileNotFoundError:
       print("Symptom data file not found.")
       return {}
   except json.JSONDecodeError:
       print("Error decoding symptom data.")
       return {}


def show_all_symptoms(data):
   print("\n📋 Common Symptoms:")
   print("-" * 30)
   print("🟢 Normal Symptoms:")
   for s in data.get("normal", {}):
       print(f" - {s.replace('_', ' ')}")


   print("\n🔴 Warning Symptoms:")
   for s in data.get("warning", {}):
       print(f" - {s.replace('_', ' ')}")
   print()


def check_symptom():
   data = load_symptoms()
   if not data:
       return


   while True:
       print("\n🩺 Symptom Checker")
       print("-" * 30)
       print("1. Check a Symptom")
       print("2. View All Common Symptoms")
       print("3. Go Back")
       choice = input("Choose an option: ").strip()


       if choice == '1':
           symptom = input("Enter a symptom (e.g., 'back pain', 'blurred vision'): ").strip().lower().replace(" ", "_")
           all_symptoms = list(data.get("normal", {}).keys()) + list(data.get("warning", {}).keys())
           match = difflib.get_close_matches(symptom, all_symptoms, n=1, cutoff=0.6)


           if match:
               matched_symptom = match[0]
               if matched_symptom in data["normal"]:
                   print("\n✅ Normal Symptom:")
                   print(data["normal"][matched_symptom])
               else:
                   print("\n⚠️ Warning Symptom:")
                   print(data["warning"][matched_symptom])
                   print("👉 Please contact a healthcare provider.")
           else:
               print("\n❓ Symptom not found. Try again or view the symptom list.")


       elif choice == '2':
           show_all_symptoms(data)


       elif choice == '3':
           break
       else:
           print("⚠️ Invalid choice. Try again.")

