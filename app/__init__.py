"""
FinanceAI-Advisor Flask Application Factory

This module contains the Flask application factory function that creates
and configures the Flask application instance with all necessary extensions
and configurations.
"""

from flask import Flask
from app.extensions import db, migrate
from app.api import finance_bp
from app.api import finance_bp
import os
from flask import request
from app.utils.logger import logger

def create_app():
    app = Flask(__name__)

    # Logging middleware
    @app.before_request
    def log_request_info():
        logger.info(f"Incoming request: {request.method} {request.url}")

    # Response logging
    @app.after_request
    def log_response_info(response):
        logger.info(f"Response status: {response.status}")
        return response

    # Database Config
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///financeai.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(finance_bp, url_prefix='/api/v1')

     # Health check endpoint
    @app.route('/health')
    def health_check():
        """Simple health check endpoint"""
        return {
            'status': 'healthy',
            'service': 'FinanceAI-Advisor',
            'version': '2.0.0'
        }, 200

    return app