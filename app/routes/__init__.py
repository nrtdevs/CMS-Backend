from .user import users_bp  # Import the blueprint for user routes

def register_routes(app):
    app.register_blueprint(users_bp, url_prefix='/api/users')  
