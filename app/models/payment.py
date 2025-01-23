from app.extensions import db
from datetime import datetime

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float, nullable=False)  # Amount of the payment
    currency = db.Column(db.String(10), nullable=False, default='USD')  # Currency of the payment
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Date of the payment
    payment_method = db.Column(db.String(50), nullable=False)  # Method of payment (e.g., credit card, bank transfer)
    transaction_id = db.Column(db.String(100),  nullable=True)  # Unique transaction identifier
    status = db.Column(db.String(50), nullable=False, default='pending')  # Status of the payment (e.g., pending, completed, failed)
    description = db.Column(db.String(255), nullable=True)  # Optional description or notes about the payment
    payer_name = db.Column(db.String(100), nullable=True)  # Name of the person or entity making the payment
    payer_email = db.Column(db.String(100), nullable=True)  # Email of the payer
    payment_provider = db.Column(db.String(50), nullable=True)  # Name of the payment provider (e.g., PayPal, Stripe)
    receipt_url = db.Column(db.String(255), nullable=True)  # URL for the payment receipt
    refunded = db.Column(db.Boolean, default=False)  # Indicates if the payment was refunded
    refund_date = db.Column(db.DateTime, nullable=True)  # Date of the refund, if applicable
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    project_id = db.Column(db.Integer, db.ForeignKey('projects.projectId'), nullable=False)  # Foreign key to the Project model
    project = db.relationship('Project', back_populates='payments')  # Relationship to the Project model

    __table_args__ = (
        db.UniqueConstraint('project_id', 'transaction_id', name='_project_transaction_uc'),
    )
