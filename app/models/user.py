from app.extensions import db  # Import db from extensions
from datetime import datetime
import enum
from .Notification import  Notification
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
    role = db.Column(db.String(120), nullable=False)
    userType = db.Column(db.String(120), nullable=False, default='user')
    status = db.Column(db.Boolean, default=True)
    is_blocked = db.Column(db.Boolean, nullable=False, default=False)
    
    #Realtionship to the Notification Model
    notifications = db.relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
    )


    # Timestamp for when the record is created
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Timestamp for when the record is last updated
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Timestamp for when the record is deleted (soft delete)
    deletedAt = db.Column(db.DateTime, nullable=True)

    
