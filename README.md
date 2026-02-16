# AI-Powered Automated Attendance System (Cloud Integrated)

A professional-grade facial recognition system that authenticates users and logs attendance to a Supabase Cloud database in real-time. Built as part of a Cloud Developer internship for AB Infotech Solutions.

## 🚀 Features
- **Facial Recognition**: Uses the dlib-powered `face_recognition` model for high-accuracy identification.
- **Cloud Database**: Integrated with **Supabase (PostgreSQL)** for secure, remote data storage.
- **Intelligent 12 AM Reset**: Prevents duplicate entries by checking the database for existing logs within the current calendar day.
- **Daily/Weekly Reporting**: Dedicated reporting tool to summarize attendance data.
- **Dynamic UI**: Live webcam feed with color-coded bounding boxes.

## 🛠️ Tech Stack
- **Language**: Python 3.12+
- **Libraries**: OpenCV, face_recognition, Supabase, python-dotenv, setuptools

## 📂 Project Structure
- `images/` : Store authorized personnel photos (e.g., "Sanket_B.jpg")
- `.env` : Private API Keys (Supabase URL & Key)
- `.gitignore` : Prevents sensitive files from being uploaded
- `database.py` : Cloud connection and Daily-Reset filtering
- `main.py` : Main application loop and camera UI
- `recognition.py` : Face encoding and image processing
- `reports.py` : Data analysis tool for Daily/Weekly summaries

## ⚙️ Setup & Installation
1. Clone the Project:
   git clone <your-github-link-here>
   cd week-3-project

2. Initialize Environment:
   python -m venv venv
   .\venv\Scripts\activate

3. Install Core Dependencies:
   pip install opencv-python face_recognition supabase python-dotenv setuptools

4. Environment Configuration:
   Create a .env file in the root directory:
   SUPABASE_URL=your_project_url
   SUPABASE_KEY=your_service_role_key

## How to Use
1. Enrollment: Place a clear image of yourself in the images/ folder.
2. Running the App: Execute "python main.py". The camera will open and identify you.
3. Once-per-Day Rule: The system logs you once per day. Subsequent sightings are ignored.
4. Generating Reports: Run "python reports.py" and choose between 1-day or 7-day summary.

---
Developer: Sanket Bololikar
Project Objective: Automate and digitize attendance management using Cloud and AI.