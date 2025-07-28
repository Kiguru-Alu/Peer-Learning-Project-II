 # Weekly tips logic
import json
import os

TIPS_FILE = "assets/tips.json"

def load_all_tips():
    if not os.path.exists(TIPS_FILE):
        print("⚠️ Tips file not found.")
        return {}
    with open(TIPS_FILE, 'r') as f:
        return json.load(f)

def get_tip_for_week(week):
    tips = load_all_tips()
    tip = tips.get(str(week))
    if not tip:
        return "No specific tip found for this week. Just stay healthy and follow your checkups!"
    return tip

def show_weekly_tip(user_data):
    week = user_data.get("current_week")
    if not week:
        print("⚠️ Cannot determine current pregnancy week.")
        return

    print(f"\n🗓️ Weekly Tip for Week {week}")
    print("-" * 30)
    tip = get_tip_for_week(week)
    print(tip)
    print("-" * 30)
