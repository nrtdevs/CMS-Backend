from .user import users_bp  # Import the blueprint for user routes
from .auth import auth_bp  # Import the blueprint for user routes
from .logs import logs_bp
def register_routes(app):
    app.register_blueprint(users_bp, url_prefix='/api/users')  
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(logs_bp, url_prefix='/api/logs')
  
