from app.extensions import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Establishing foreign key
    message = db.Column(db.String(255), nullable=False)
    module = db.Column(db.String(255), nullable=False)
    seen = db.Column(db.Boolean, default=False)

    # Relationship to the User model
    user = db.relationship('User', back_populates='notifications')
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)  # Renamed to snake_case
