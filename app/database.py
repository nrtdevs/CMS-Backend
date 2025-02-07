from flask import Flask
import click
import os
from app.config import Config
from app.extensions import db, migrate  # Import extensions
from app.routes import register_routes 
from app.seeder import seed_permissions, seed_roles, seed_users
from flask_cors import CORS
from flask_socketio import SocketIO


SECRET_KEY = os.getenv('SECRET_KEY')

socketio = SocketIO(cors_allowed_origins="*")


def seed_all():
    """Run all seeders."""
    seed_permissions()
    seed_roles()
    seed_users()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db, directory="app/migrations")
    socketio.init_app(app)  # Initialize SocketIO with the app

    # Register routes
    register_routes(app)
    
      # Add custom CLI command for seeding
    @app.cli.command("seed")
    def seed():
        """Seed the database with initial data."""
        with app.app_context():
            seed_all()
            db.session.commit()
            click.echo("Database seeded successfully!")

    return app
from app import socket_events  # ✅ Import event handlers after socketio is initialized
