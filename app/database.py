from flask import Flask
import click
import os
from app.config import Config
from app.extensions import db, migrate  # Import extensions
from app.routes import register_routes 
from app.models import User
from werkzeug.security import generate_password_hash
 
SECRET_KEY = os.getenv('SECRET_KEY')


def seed_users():
    """Seed the User table with initial data."""
    master = User.query.filter_by(userType='master_admin').first()
    if(master):
        print("Master Admin Already Exists")
        return
    Hashed_Password=generate_password_hash('admin@2025')
    users = [
        User(firstName="Master",lastName="Admin",countryCode='+91',mobileNo=7987809375, email="nrt@gmail.com",password=Hashed_Password,userType='master_admin',empID='NRT-89',role='CEO'),
    ]
    
    db.session.bulk_save_objects(users)
    db.session.commit()
    print("User table seeded successfully!")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db, directory="app/migrations")

    # Register routes
    register_routes(app)
    
      # Add custom CLI command for seeding
    @app.cli.command("seed")
    def seed():
        """Seed the database with initial data."""
        with app.app_context():
            seed_users()
            db.session.commit()
            click.echo("Database seeded successfully!")

    return app
