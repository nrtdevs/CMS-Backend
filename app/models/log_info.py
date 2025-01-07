from app.extensions import db  # Import db from extensions



class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(250), nullable=True)
    ipAddress = db.Column(db.String(80), nullable=True)
    userAgent = db.Column(db.String(250), nullable=True)
    device = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


 # Relationship with User
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='logs')
    
    @property
    def serialized_user(self):
        """Serialize the related user details."""
        if not self.user:
            return None
        return {
            "id": self.user.id,
            "firstName": self.user.firstName,
            "lastName": self.user.lastName,
            "email": self.user.email,
            "role": self.user.role,
            "mobileNo": self.user.mobileNo,
        }
    