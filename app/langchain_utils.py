import openai
import os
import re
from datetime import datetime
from .models import HealthLog
from flask import current_app


def query_chatbot(prompt):
    """
    Handles both database queries and general questions.
    Provides generalized answers informed by database data when appropriate.
    """

    if not prompt or prompt.strip() == "":
        return "The prompt cannot be empty."

    # Set OpenAI API key
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Define database-related keywords and fields
    keywords = {
        "sleep": "sleep_hours",
        "steps": "steps",
        "water intake": "water_intake",
        "notes": "notes",
    }

    # Try to extract a date from the user's prompt (e.g., 'on 6 Dec 2024')
    date_match = re.search(r"on (\d{1,2} \w{3,9} \d{4})", prompt, re.IGNORECASE)
    date_obj = None
    if date_match:
        try:
            date_obj = datetime.strptime(date_match.group(1), "%d %b %Y").date()
            print(f"Extracted Date: {date_obj}")
        except ValueError:
            return "I couldn't understand the date in your question. Please use a format like '6 Dec 2024'."

    # Check if the prompt contains database-related keywords
    for key, column in keywords.items():
        if key in prompt.lower():
            # Handle database queries with generalization
            try:
                if date_obj:
                    # Query for specific date data
                    log = HealthLog.query.filter_by(date=date_obj).first()
                    if log:
                        # Generate a general response based on the data
                        data_value = getattr(log, column, None)
                        if key == "sleep":
                            if data_value >= 7:
                                return f"On {date_obj.strftime('%d %b %Y')}, you had {data_value} hours of sleep, which is great! Keep it up!"
                            else:
                                return f"On {date_obj.strftime('%d %b %Y')}, you had {data_value} hours of sleep. Aim for 7-8 hours for better health."
                        elif key == "steps":
                            if data_value >= 10000:
                                return f"On {date_obj.strftime('%d %b %Y')}, you walked {data_value} steps, which is excellent for your fitness goals!"
                            else:
                                return f"On {date_obj.strftime('%d %b %Y')}, you walked {data_value} steps. Try to walk at least 10,000 steps daily for optimal fitness."
                        elif key == "water intake":
                            if data_value >= 2.0:
                                return f"On {date_obj.strftime('%d %b %Y')}, you drank {data_value} liters of water, which is good hydration!"
                            else:
                                return f"On {date_obj.strftime('%d %b %Y')}, you drank {data_value} liters of water. Aim for at least 2 liters daily."
                        else:
                            return f"On {date_obj.strftime('%d %b %Y')}, your {key} was: {data_value}."
                    else:
                        return f"No health log found for {date_obj.strftime('%d %b %Y')}."
                else:
                    # General response based on all available data
                    logs = HealthLog.query.all()
                    if not logs:
                        return f"I couldn't find any data for {key}. Start logging your data to track your progress!"

                    # Compute averages or trends
                    values = [getattr(log, column, 0) for log in logs if getattr(log, column, None) is not None]
                    avg_value = sum(values) / len(values) if values else 0
                    if key == "sleep":
                        if avg_value >= 7:
                            return f"Your average sleep duration is {avg_value:.1f} hours, which is great! Keep maintaining a consistent sleep schedule."
                        else:
                            return f"Your average sleep duration is {avg_value:.1f} hours. Try to get at least 7-8 hours of sleep per night for better health."
                    elif key == "steps":
                        if avg_value >= 10000:
                            return f"Your average step count is {int(avg_value)}, which is excellent for your fitness goals!"
                        else:
                            return f"Your average step count is {int(avg_value)}. Aim for 10,000 steps daily for better fitness."
                    elif key == "water intake":
                        if avg_value >= 2.0:
                            return f"Your average water intake is {avg_value:.1f} liters, which is good! Stay hydrated!"
                        else:
                            return f"Your average water intake is {avg_value:.1f} liters. Try to drink at least 2 liters of water daily."
            except Exception as e:
                print(f"Database error: {e}")
                return "An error occurred while accessing your personal data. Please try again."

    # If no database-related keyword is found, handle the prompt as a general question
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a health assistant with access to personal health data."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=350,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return "I couldn't process your request. Please try again later."
