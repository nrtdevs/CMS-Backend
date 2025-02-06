from app.extensions import db
from datetime import datetime



# Association table for the many-to-many relationship between Assignment and Remark
assignment_remarks = db.Table('assignment_remarks',
    db.Column('assignment_id', db.Integer, db.ForeignKey('assignments.id'), primary_key=True),
    db.Column('remark_id', db.Integer, db.ForeignKey('remarks.id'), primary_key=True)
)


class Remark(db.Model):
    __tablename__ = 'remarks'

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    remark = db.Column(db.Text, nullable=False)  # Remark text
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Automatically stores the timestamp

    # Many-to-many relationship with the Assignment model using the association table
    assignments = db.relationship('Assignment', secondary=assignment_remarks, back_populates='remarks')
    
    
