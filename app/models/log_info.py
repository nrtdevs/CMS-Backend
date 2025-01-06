from app.extensions import db  # Import db from extensions



class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(250), nullable=True)
    userId = db.Column(db.Integer, nullable=False)
    ipAddress = db.Column(db.String(80), nullable=True)
    userAgent = db.Column(db.String(250), nullable=True)
    device = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


    