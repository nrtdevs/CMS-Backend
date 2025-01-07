from .user import users_bp  # Import the blueprint for user routes
from .auth import auth_bp  # Import the blueprint for user routes
from .bidding import biddings_bp  # Import the blueprint for user routes
from .notification import notification_bp  # Import the blueprint for user routes
from .logs import logs_bp  # Import the blueprint for user routes
def register_routes(app):
    app.register_blueprint(users_bp, url_prefix='/api/users')  
    app.register_blueprint(auth_bp, url_prefix='/api/auth')  
    app.register_blueprint(biddings_bp, url_prefix='/api/bidding')  
    app.register_blueprint(notification_bp, url_prefix='/api/notification')  
    app.register_blueprint(logs_bp, url_prefix='/api/logs')  
