from flask import Blueprint, jsonify, request
from app import db
from app.models import RoadClosure

closures_bp = Blueprint('closures', __name__, url_prefix='/api/closures')

@closures_bp.route('', methods=['GET'])
def get_closures():
    """Get all road closures with optional filtering"""
    try:
        status = request.args.get('status')
        severity = request.args.get('severity')
        
        query = RoadClosure.query
        
        if status:
            query = query.filter_by(status=status)
        if severity:
            query = query.filter_by(severity=severity)
        
        # Order by most recent first
        query = query.order_by(RoadClosure.updated_at.desc())
        closures = query.all()
        
        return jsonify({
            'success': True,
            'data': [closure.to_dict() for closure in closures]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@closures_bp.route('/<int:closure_id>', methods=['GET'])
def get_closure(closure_id):
    """Get specific closure details"""
    try:
        closure = RoadClosure.query.get(closure_id)
        if not closure:
            return jsonify({
                'success': False,
                'error': 'Closure not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': closure.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@closures_bp.route('', methods=['POST'])
def create_closure():
    """Create a new road closure"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('road_name'):
            return jsonify({
                'success': False,
                'error': 'road_name is required'
            }), 400
        
        closure = RoadClosure(
            road_name=data.get('road_name'),
            description=data.get('description'),
            status=data.get('status', 'active'),
            severity=data.get('severity', 'medium'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            external_id=data.get('external_id'),
            start_time=data.get('start_time'),
            end_time=data.get('end_time')
        )
        
        db.session.add(closure)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': closure.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@closures_bp.route('/<int:closure_id>', methods=['PUT'])
def update_closure(closure_id):
    """Update an existing closure"""
    try:
        closure = RoadClosure.query.get(closure_id)
        if not closure:
            return jsonify({
                'success': False,
                'error': 'Closure not found'
            }), 404
        
        data = request.get_json()
        
        # Update fields if provided
        if 'road_name' in data:
            closure.road_name = data['road_name']
        if 'description' in data:
            closure.description = data['description']
        if 'status' in data:
            closure.status = data['status']
        if 'severity' in data:
            closure.severity = data['severity']
        if 'latitude' in data:
            closure.latitude = data['latitude']
        if 'longitude' in data:
            closure.longitude = data['longitude']
        if 'end_time' in data:
            closure.end_time = data['end_time']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': closure.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@closures_bp.route('/<int:closure_id>', methods=['DELETE'])
def delete_closure(closure_id):
    """Delete a closure"""
    try:
        closure = RoadClosure.query.get(closure_id)
        if not closure:
            return jsonify({
                'success': False,
                'error': 'Closure not found'
            }), 404
        
        db.session.delete(closure)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Closure deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
