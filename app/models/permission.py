from app.extensions import db
from datetime import datetime
from slugify import slugify

class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(155), nullable=False)
    slug = db.Column(db.String(155), unique=True, nullable=False)
    permission_group = db.Column(db.String(155), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    # Many-to-Many Relationship with Role
    roles = db.relationship(
        'Role',
        secondary='role_permissions',
        back_populates='permissions'
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.name and not self.slug:
            combined_name_group = f"{self.name} {self.permission_group}"
            self.slug = slugify(combined_name_group).lower()
