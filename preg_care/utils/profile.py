from utils.storage import save_user_data

def update_pregnancy_week(user_data, username):
    print("\n🔄 Update Pregnancy Week")
    try:
        week = int(input("Enter your current pregnancy week (1–40): ").strip())
        if 1 <= week <= 40:
            user_data["current_week"] = week
            save_user_data(username, user_data)
            print(f"✅ Pregnancy week updated to {week}.")
        else:
            print("❌ Please enter a number between 1 and 40.")
    except ValueError:
        print("❌ Invalid input. Please enter a number.")