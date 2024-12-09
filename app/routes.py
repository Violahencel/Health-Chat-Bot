from flask import Blueprint, render_template, request, jsonify
from .models import HealthLog
from .langchain_utils import query_chatbot
from . import db
from datetime import datetime

# Create a Blueprint for routes
routes = Blueprint("routes", __name__)

@routes.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if not user_input:
            return render_template("index.html", error="Please enter a valid input.")

        try:
            # Query the chatbot with the user input
            chatbot_response = query_chatbot(user_input)
            # Split response into lines or bullet points for better UI display
            response_lines = chatbot_response.split("\n") if chatbot_response else ["No response available."]
        except Exception as e:
            print(f"Error querying chatbot: {e}")
            response_lines = ["Sorry, something went wrong with the chatbot."]
        
        # Render the page with chatbot response
        return render_template(
            "index.html", 
            user_input=user_input, 
            response_lines=response_lines, 
            message=None, 
            error=None
        )
    return render_template("index.html", message=None, error=None)

@routes.route("/api/logs", methods=["POST"])
def log_health_data():
    try:
        # Get data from the request (for API or form submissions)
        data = request.json if request.is_json else request.form

        # Check if an entry already exists for the given date
        existing_log = HealthLog.query.filter_by(date=data["date"]).first()

        if existing_log:
            # Update the existing entry with new data
            existing_log.steps = int(data.get("steps", 0))
            existing_log.water_intake = float(data.get("water_intake", 0))
            existing_log.sleep_hours = float(data.get("sleep_hours", 0))
            existing_log.notes = data.get("notes", "")
        else:
            # Create a new HealthLog entry
            new_log = HealthLog(
                date=data["date"],
                steps=int(data.get("steps", 0)),
                water_intake=float(data.get("water_intake", 0)),
                sleep_hours=float(data.get("sleep_hours", 0)),
                notes=data.get("notes", "")
            )
            db.session.add(new_log)

        # Commit changes to the database
        db.session.commit()
        return jsonify({"message": "Health log saved successfully!"}), 201
    except Exception as e:
        print(f"Error saving health log: {e}")
        return jsonify({"error": "Failed to save health log. Please try again."}), 400

@routes.route("/api/logs/<date>", methods=["GET"])
def get_health_log(date):
    try:
        # Convert the date string to a proper date object
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()

        # Query the database for the specified date
        log = HealthLog.query.filter_by(date=date_obj).first()
        if log:
            # Return the health log as JSON
            return jsonify({
                "date": log.date.strftime("%Y-%m-%d"),
                "steps": log.steps,
                "water_intake": log.water_intake,
                "sleep_hours": log.sleep_hours,
                "notes": log.notes
            }), 200
        else:
            return jsonify({"message": f"No health log found for date {date}."}), 404
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    except Exception as e:
        print(f"Error retrieving health log: {e}")
        return jsonify({"error": "Failed to retrieve health log. Please try again."}), 500

@routes.route("/retrieve-data", methods=["GET"])
def retrieve_data():
    date = request.args.get("date")
    if not date:
        return render_template("index.html", error="Please provide a valid date to retrieve data.", message=None)

    try:
        # Convert the date string to a proper date object
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()

        # Query the database for the specified date
        log = HealthLog.query.filter_by(date=date_obj).first()
        if log:
            # Render the retrieved data
            retrieved_data = {
                "date": log.date.strftime("%Y-%m-%d"),
                "steps": log.steps,
                "water_intake": log.water_intake,
                "sleep_hours": log.sleep_hours,
                "notes": log.notes
            }
            return render_template("index.html", retrieved_data=retrieved_data, message=None, error=None)
        else:
            return render_template("index.html", error=f"No health data found for {date}.", retrieved_data=None, message=None)
    except ValueError:
        return render_template("index.html", error="Invalid date format. Use YYYY-MM-DD.", retrieved_data=None, message=None)
    except Exception as e:
        print(f"Error retrieving health log: {e}")
        return render_template("index.html", error="Failed to retrieve health data. Please try again.", retrieved_data=None, message=None)
