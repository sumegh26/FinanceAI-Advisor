"""
FinanceAI-Advisor Flask Application Factory

This module contains the Flask application factory function that creates
and configures the Flask application instance with all necessary extensions
and configurations.
"""

from flask import Flask
from app.api import finance_bp
import os
from dotenv import load_dotenv


def create_app():
    """
    Application factory function that creates and configures Flask app
    
    Returns:
        Flask: Configured Flask application instance
    """
    # Load environment variables
    load_dotenv()
    
    # Create Flask app instance
    app = Flask(__name__)
    
    # Configure app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Register blueprints
    app.register_blueprint(finance_bp, url_prefix='/api/v1')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Simple health check endpoint"""
        return {
            'status': 'healthy',
            'service': 'FinanceAI-Advisor',
            'version': '1.0.0'
        }, 200
    
    return app
