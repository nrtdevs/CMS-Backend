from app.extensions import db
from datetime import datetime


class Permission(db.Model):
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-incrementing primary key
    name = db.Column(db.Enum('create', 'read', 'update', 'reject', name='permission_types'), nullable=False)  # Permission type
    perm_grp = db.Column(db.Enum('user', 'admin', 'project', 'bidding', name='permission_groups'), nullable=False)  # Permission group
    status = db.Column(db.Boolean, nullable=False, default=True)  # Active status

    # Timestamp 
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)