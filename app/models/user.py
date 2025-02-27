from app.extensions import db  # Import db from extensions
from datetime import datetime
import enum
from .team import team_users
class UserTypeEnum(enum.Enum):
    user = "user"
    master_admin = "master_admin"

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column(db.String(80), nullable=False)
    lastName = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    countryCode = db.Column(db.String(120), nullable=False)
    mobileNo = db.Column(db.BigInteger, unique=True, nullable=False)
    empID = db.Column(db.String(120),unique=True, nullable=False)
    userType = db.Column(db.String(120), nullable=False, default='user')
    status = db.Column(db.Boolean, default=True)
    is_blocked = db.Column(db.Boolean, nullable=False, default=False)
    # Timestamp 
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deletedAt = db.Column(db.DateTime, nullable=True)
    
    
    # relationship
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
    role = db.relationship('Role', back_populates='users')
    notifications = db.relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    logs=db.relationship('Log', back_populates='user', cascade='all, delete-orphan')
    
    users = db.relationship(
        'Project',
        secondary='project_developers',
        back_populates='developers'
    )
    teams = db.relationship('Team', secondary=team_users, back_populates='developers')
    payments = db.relationship('Payment', back_populates='user')
