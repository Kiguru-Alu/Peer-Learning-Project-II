# Entry point with menu logic
from utils.auth import register_user, login_user
from utils.tips import show_weekly_tip
from utils.checkup import add_checkup, view_checkup_history
from utils.reminders import show_reminders, add_reminder, delete_reminder
from utils.profile import update_pregnancy_week
from utils.emergency import display_emergency_info
from utils.faqs import display_faqs
from utils.nutrition import display_nutrition_tips
from utils.symptoms import check_symptom

def show_main_menu(username, user_data):
    while True:
        print("\n==== Preg-care Main Menu ====")
        print("1. View Weekly Tip")
        print("2. Add Check-up Record")
        print("3. View Check-up History")
        print("4. Reminders")
        print("5. Update Pregnancy Week")
        print("6. Emergency Info")
        print("7. Frequently Asked Questions")
        print("8. Nutrition Tips")
        print("9. Check Symptoms")
        print("10. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            show_weekly_tip(user_data)
        elif choice == '2':
            add_checkup(user_data, username)
        elif choice == '3':
            view_checkup_history(user_data)
        elif choice == '4':
            print("\n1. View Reminders\n2. Add Reminder\n3. Delete Reminder")
            r = input("Choose: ").strip()
            if r == '1':
                show_reminders(user_data, username)
            elif r == '2':
                add_reminder(user_data, username)
            elif r == '3':
                delete_reminder(user_data, username)
        elif choice == '5':
            update_pregnancy_week(user_data, username)
        elif choice == '6':
            display_emergency_info()
        elif choice == '7':
            display_faqs()
        elif choice == '8':
            display_nutrition_tips()
        elif choice == '9':
            check_symptom()
        elif choice == '10':
            print(f"👋 Goodbye, {username.capitalize()}! Stay healthy.")
            break
        else:
            print("⚠️ Invalid option. Try another.")

def main():
    print("👶 Welcome to Preg-care CLI App 👶")
    print("---------------------------------")

    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            username, user_data = register_user()
            if username and user_data:
                show_main_menu(username, user_data)
        elif choice == '2':
            username, user_data = login_user()
            if username and user_data:
                show_main_menu(username, user_data)
            else:
                print("⚠️ Login failed. Try again.")
        elif choice == '3':
            print("👋 Goodbye! Take care.")
            break
        else:
            print("⚠️ Invalid option. Try again.")

    show_main_menu(username, user_data)

if __name__ == "__main__":
    main()
