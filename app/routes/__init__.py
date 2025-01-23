from .user import users_bp  # Import the blueprint for user routes
from .auth import auth_bp  # Import the blueprint for user routes
from .bidding import biddings_bp  # Import the blueprint for user routes
from .notification import notification_bp  # Import the blueprint for user routes
from .logs import logs_bp  # Import the blueprint for user routes
from .role import roles_bp  # Import the blueprint for role routes
from .assignment import assig_bp
from .project import projects_bp
from .team import teams_bp
from .dashboard import dashboard_bp
from .payment import payments_bp

def register_routes(app):
    app.register_blueprint(users_bp, url_prefix='/api/users')  
    app.register_blueprint(auth_bp, url_prefix='/api/auth')  
    app.register_blueprint(biddings_bp, url_prefix='/api/bidding')  
    app.register_blueprint(notification_bp, url_prefix='/api/notification')  
    app.register_blueprint(logs_bp, url_prefix='/api/logs')  
    app.register_blueprint(roles_bp, url_prefix='/api/roles')
    app.register_blueprint(assig_bp, url_prefix='/api/assigments')
    app.register_blueprint(projects_bp, url_prefix='/api/project')
    app.register_blueprint(teams_bp, url_prefix='/api/team')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(payments_bp, url_prefix='/api/payment')
    
    