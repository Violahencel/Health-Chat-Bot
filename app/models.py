from . import db

class HealthLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    steps = db.Column(db.Integer, nullable=True)
    water_intake = db.Column(db.Float, nullable=True)  # Liters
    sleep_hours = db.Column(db.Float, nullable=True)  # Hours
    notes = db.Column(db.Text, nullable=True)
