from flask import Blueprint

# Create blueprints
from app.routes.closures import closures_bp
from app.routes.alerts import alerts_bp
from app.routes.health import health_bp

__all__ = ['closures_bp', 'alerts_bp', 'health_bp']
