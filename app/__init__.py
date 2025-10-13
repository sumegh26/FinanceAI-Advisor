"""
FinanceAI-Advisor Flask Application Factory

This module contains the Flask application factory function that creates
and configures the Flask application instance with all necessary extensions
and configurations.
"""

from flask import Flask
from app.extensions import db, migrate, limiter
from app.api import finance_bp
from app.api import finance_bp
import os
from flask import request
from app.utils.logger import logger
from flask import jsonify

def create_app():
    app = Flask(__name__)

    # rate limit exceeded handler
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({
            "success": False,
            "message": "Rate limit exceeded",
            "error": "Too many requests"
        }), 429

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

    # Conditionally disable limiter in development
    if os.getenv("FLASK_ENV") == "development":
        limiter.enabled = False

    limiter.init_app(app)

    # Register blueprints
    app.register_blueprint(finance_bp, url_prefix='/api/v1')

     # Health check endpoint
    @app.route('/health')
    def health_check():
        """Simple health check endpoint"""
        return {
            'status': 'healthy',
            'service': 'FinanceAI-Advisor',
            'version': '0.3.0'
        }, 200

    return app
