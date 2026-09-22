from flask import Blueprint, jsonify, request
from app import db
from app.models import UserAlert, User

alerts_bp = Blueprint('alerts', __name__, url_prefix='/api/alerts')

@alerts_bp.route('', methods=['POST'])
def create_alert():
    """Subscribe to road closure alerts"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('user_id') or not data.get('area_name'):
            return jsonify({
                'success': False,
                'error': 'user_id and area_name are required'
            }), 400
        
        # Check if user exists
        user = User.query.get(data.get('user_id'))
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        alert = UserAlert(
            user_id=data.get('user_id'),
            area_name=data.get('area_name'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            radius_km=data.get('radius_km', 5.0),
            enable_sms=data.get('enable_sms', False),
            enable_email=data.get('enable_email', True),
            enable_push=data.get('enable_push', True)
        )
        
        db.session.add(alert)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': alert.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@alerts_bp.route('/<int:alert_id>', methods=['GET'])
def get_alert(alert_id):
    """Get specific alert details"""
    try:
        alert = UserAlert.query.get(alert_id)
        if not alert:
            return jsonify({
                'success': False,
                'error': 'Alert not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': alert.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@alerts_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_alerts(user_id):
    """Get all alerts for a user"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        alerts = UserAlert.query.filter_by(user_id=user_id, is_active=True).all()
        
        return jsonify({
            'success': True,
            'data': [alert.to_dict() for alert in alerts]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@alerts_bp.route('/<int:alert_id>', methods=['PUT'])
def update_alert(alert_id):
    """Update alert preferences"""
    try:
        alert = UserAlert.query.get(alert_id)
        if not alert:
            return jsonify({
                'success': False,
                'error': 'Alert not found'
            }), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if 'area_name' in data:
            alert.area_name = data['area_name']
        if 'latitude' in data:
            alert.latitude = data['latitude']
        if 'longitude' in data:
            alert.longitude = data['longitude']
        if 'radius_km' in data:
            alert.radius_km = data['radius_km']
        if 'enable_sms' in data:
            alert.enable_sms = data['enable_sms']
        if 'enable_email' in data:
            alert.enable_email = data['enable_email']
        if 'enable_push' in data:
            alert.enable_push = data['enable_push']
        if 'is_active' in data:
            alert.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': alert.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@alerts_bp.route('/<int:alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    """Unsubscribe from alerts"""
    try:
        alert = UserAlert.query.get(alert_id)
        if not alert:
            return jsonify({
                'success': False,
                'error': 'Alert not found'
            }), 404
        
        db.session.delete(alert)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Alert deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
