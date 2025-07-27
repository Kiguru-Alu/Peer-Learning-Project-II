import json


def load_faqs():
   try:
       with open("assets/faqs.json", "r") as file:
           return json.load(file)
   except FileNotFoundError:
       print("FAQs data file not found.")
       return []
   except json.JSONDecodeError:
       print("Error decoding FAQs data.")
       return []
      
def display_faqs():
   faqs = load_faqs()
   if not faqs:
       return


   print("\n❓ Frequently Asked Questions")
   print("-" * 40)


   for i, faq in enumerate(faqs, 1):
       print(f"{i}. {faq['question']}")


   try:
       choice = int(input("\nEnter the number of a question to view the answer (0 to exit): "))
       if choice == 0:
           return
       selected = faqs[choice - 1]
       print(f"\n🗨️ Answer:\n{selected['answer']}")
   except (ValueError, IndexError):
       print("Invalid selection.")

