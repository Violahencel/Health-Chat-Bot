import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "") # add secret key you can take it from ChatGPT
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", " ") # Add your server name and password
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.getenv("") #Add Openai key
