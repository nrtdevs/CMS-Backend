from flask import Flask
from app.config import Config
from app.extensions import db, migrate  # Import extensions
from app.routes import register_routes  # Import register_routes function

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db, directory="app/migrations")

    # Register routes
    register_routes(app)

    return app
