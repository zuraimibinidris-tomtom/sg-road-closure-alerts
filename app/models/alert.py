from app import db
from datetime import datetime

class UserAlert(db.Model):
    """User alert subscription model"""
    __tablename__ = 'user_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Alert criteria
    area_name = db.Column(db.String(255), nullable=False)  # e.g., "Marina Bay", "Orchard"
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    radius_km = db.Column(db.Float, default=5.0)  # Alert radius in kilometers
    
    # Notification preferences
    enable_sms = db.Column(db.Boolean, default=False)
    enable_email = db.Column(db.Boolean, default=True)
    enable_push = db.Column(db.Boolean, default=True)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'area_name': self.area_name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'radius_km': self.radius_km,
            'enable_sms': self.enable_sms,
            'enable_email': self.enable_email,
            'enable_push': self.enable_push,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
