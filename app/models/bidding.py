from app.extensions import db
from datetime import datetime


class Bidding(db.Model):
    __tablename__ = 'biddings'
    bidId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    projectName = db.Column(db.String(80),unique=True,  nullable=False)
    projectDescription = db.Column(db.String(300), nullable=True) 
    currency= db.Column(db.String(80), nullable=True)
    bidAmount = db.Column(db.Integer, nullable=True)
    platform = db.Column(db.String(80), nullable=False)
    bidDate = db.Column(db.Date, nullable=False, default=datetime.utcnow)    
    status = db.Column(db.String(120), nullable=False, default='pending')
    clientName = db.Column(db.String(80), nullable=False)
    clientEmail = db.Column(db.String(120),  nullable=False)
    countryCode = db.Column(db.String(120), nullable=False)
    clientContact = db.Column(db.BigInteger, nullable=False)
    clientCompany = db.Column(db.String(120), nullable=True)
    clientLocation = db.Column(db.String(120), nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    
    # Timestamp 
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True) 
      
    # relationship
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', foreign_keys=[userId], backref='biddings', lazy=True)

    projectId = db.Column(db.Integer, db.ForeignKey('projects.projectId', use_alter=True), nullable=True)
    project = db.relationship('Project', backref='biddings', lazy=True, 
                              foreign_keys=[projectId])
    
    
    commission = db.Column(db.Boolean, nullable=False)

    approvedBy = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    approved = db.relationship('User', foreign_keys=[approvedBy], backref='approved_biddings', lazy=True)    