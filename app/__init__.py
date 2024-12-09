from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import dotenv
dotenv.load_dotenv()
db = SQLAlchemy()

def create_app():
    # Load environment variables from .env
    dotenv.load_dotenv()

    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    with app.app_context():
        from .routes import routes
        app.register_blueprint(routes)
        db.create_all()

    return app
