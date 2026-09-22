from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__, url_prefix='/api')

@health_bp.route('/health', methods=['GET'])
def health_check():
    """API health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'message': 'Singapore Road Closure Alert API is running'
    }), 200
