#!/usr/bin/env python
"""Main application entry point"""
import os
from app import create_app

if __name__ == '__main__':
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    
    host = os.getenv('SERVER_HOST', '0.0.0.0')
    port = int(os.getenv('SERVER_PORT', 5000))
    debug = config_name == 'development'
    
    print(f"🚀 Starting Singapore Road Closure Alert API...")
    print(f"📍 Server: http://{host}:{port}")
    print(f"🔧 Environment: {config_name}")
    
    app.run(host=host, port=port, debug=debug)
