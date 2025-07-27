import json


def load_nutrition_tips():
   try:
       with open("assets/nutrition.json", "r") as file:
           return json.load(file)
   except FileNotFoundError:
       print("Nutrition tips file not found.")
       return {}
   except json.JSONDecodeError:
       print("Error decoding nutrition tips data.")
       return {}


def display_nutrition_tips():
   tips = load_nutrition_tips()
   if not tips:
       return


   print("\n🍎 Nutrition Tips")
   print("-" * 30)
   print("1. General Tips")
   print("2. First Trimester")
   print("3. Second Trimester")
   print("4. Third Trimester")


   try:
       choice = int(input("\nSelect a category (0 to exit): "))
       category_map = {
           1: "general",
           2: "first_trimester",
           3: "second_trimester",
           4: "third_trimester"
       }


       if choice == 0:
           return


       selected = category_map.get(choice)
       if selected and selected in tips:
           print(f"\n📝 {selected.replace('_', ' ').title()} Tips:")
           for item in tips[selected]:
               print(f"- {item}")
       else:
           print("Invalid selection.")
   except ValueError:
       print("Invalid input. Please enter a number.")


