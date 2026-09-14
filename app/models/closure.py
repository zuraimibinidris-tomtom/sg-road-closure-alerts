from app import db
from datetime import datetime
from enum import Enum

class ClosureStatus(Enum):
    ACTIVE = "active"
    RESOLVED = "resolved"
    SCHEDULED = "scheduled"

class RoadClosure(db.Model):
    """Road closure incident model"""
    __tablename__ = 'road_closures'
    
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(255), unique=True)  # LTA incident ID
    road_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default=ClosureStatus.ACTIVE.value)
    severity = db.Column(db.String(50))  # high, medium, low
    
    # Location
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Time information
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'external_id': self.external_id,
            'road_name': self.road_name,
            'description': self.description,
            'status': self.status,
            'severity': self.severity,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'detected_at': self.detected_at.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
