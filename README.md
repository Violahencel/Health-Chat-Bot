# Health Chatbot

## Overview
This project is a health monitoring chatbot built with Flask, LangChain, and OpenAI. It helps track daily routines such as exercise, hydration, sleep, and diet.

## Features
- Track and log daily health activities.
- Get real-time feedback and suggestions from the chatbot.
- Store data in a database for analytics.

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/health_chatbot.git
   cd health_chatbot


2.Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate
Install dependencies:

3.pip install -r requirements.txt

4.Set up environment variables in a .env file:
DATABASE_URL=sqlite:///health.db
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_secret_key


5.Run the application:
$env:FLASK_APP="run.py"
flask run
Access the app at http://127.0.0.1:5000.

Future Enhancements
Add user authentication for multiple users.
Include reminders and notifications for missed activities.
Visualize health data trends.




health_chatbot/
├── app/
│   ├── __init__.py       # Initialize Flask app
│   ├── routes.py         # API routes and chatbot logic
│   ├── models.py         # Database models
│   ├── langchain_utils.py # LangChain integration functions
│   └── templates/
│       └── index.html    # Frontend (Optional, for Flask web interface)
├── static/
│   └── style.css         # CSS for frontend (Optional)
├── config.py             # App and database configuration
├── requirements.txt      # Python dependencies
├── run.py                # Main entry point
└── README.md             # Project documentation