from utils.storage import save_user_data
import mysql.connector
from utils.my_sql_storage import db_config
from utils.storage import save_user_data


def update_pregnancy_week(user_data, username):
    print("\n🔄 Update Pregnancy Week")
    try:
        week = int(input("Enter your current pregnancy week (1–40): ").strip())
        if 1 <= week <= 40:
            user_data["current_week"] = week
            save_user_data(username, user_data)  # Save to JSON

            # Save to MySQL
            try:
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()

                query = "UPDATE users SET current_week = %s WHERE name = %s"
                cursor.execute(query, (week, username))
                connection.commit()

                print(f"✅ Pregnancy week updated to {week} (JSON + MySQL).")
            except mysql.connector.Error as err:
                print(f"⚠️ MySQL Update Error: {err}")
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
        else:
            print("❌ Please enter a number between 1 and 40.")
    except ValueError:
        print("❌ Invalid input. Please enter a number.")