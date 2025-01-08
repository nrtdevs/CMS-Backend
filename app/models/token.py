from app.extensions import db
from datetime import datetime

class Token(db.Model):
    __tablename__ = 'tokens'
    tokenId = db.Column(db.Integer, primary_key=True)
    accessToken = db.Column(db.String(250), nullable=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expiryAt = db.Column(db.DateTime, default=datetime.utcnow)
    
