# 🤰 Preg-care CLI App

**Preg-care** is a command-line application designed to support pregnant women, especially in low-resource settings. It offers a range of personalized tools including weekly pregnancy tips, reminders, checkup tracking, emergency info, FAQs, nutrition advice and a symptom checker.

---

## 📦 Features

### 📝 Registration & Login
- Simple user registration and login
- User-specific data is stored locally

### 📅 Weekly Tips
- View pregnancy tips based on week
- Tips are stored in a structured JSON file

### ⏰ Reminders
- Add, view, and delete health-related reminders
- Data is user-specific and saved locally

### 🏥 Checkup Tracker
- Add medical checkups with dates and notes
- View full checkup history

### 🚨 Emergency Info
- Displays important contacts for health emergencies
- Quick reference for ambulance and clinic numbers

### ❓ FAQs
- Provides common questions and answers related to pregnancy
- Supports easy readability

### 🥦 Nutrition Tips
- Offers healthy eating advice for each trimester
- Based on expert-recommended guidelines

### 🩺 Symptom Checker
- Check if a symptom is normal or needs medical attention
- Fuzzy matching to suggest close symptoms
- Option to view a full list of common symptoms



## 📁 Project Structure
preg_care/
│
├── main.py # Main CLI entry point
├── utils/
│ ├── reminders.py # Reminder functions
│ ├── checkup.py # Checkup tracking
│ ├── emergency.py # Emergency info display
│ ├── faqs.py # FAQs loader
│ ├── nutrition.py # Nutrition tip logic
│ ├── symptoms.py # Symptom checker with fuzzy match
│ └── language.py # Language toggle logic
│
├── assets/
│ ├── tips.json # Weekly pregnancy tips
│ ├── faqs.json # Frequently asked questions
│ ├── nutrition.json # Nutrition advice
│ ├── symptoms.json # Symptom data
│ └── emergency.json # Emergency numbers
│
└── data/
└── users/ # User data (checkups, reminders, settings)


---

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git@github.com:Kiguru-Alu/Peer-Learning-Project-II.git
   cd preg-care-cli

   python3 main.py start



