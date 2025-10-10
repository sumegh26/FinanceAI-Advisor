"""
FinanceAI-Advisor Application Entry Point

This is the main entry point for running the FinanceAI-Advisor Flask application.
It creates the Flask app instance and runs the development server.
"""

from app import create_app
import os

# Create Flask application instance
app = create_app()

# Allows flask db commands to work
# @app.cli.command("show-db")
# @with_appcontext
# def show_db():
#     """Test to check DB connection."""
#     click.echo(f"Database is connected! Current Database URI: {db.get_engine().url}")

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("=" * 50)
    print("🚀 FinanceAI-Advisor Starting Up")
    print("=" * 50)
    print(f"Environment: {'Development' if debug else 'Production'}")
    print(f"Server: http://{host}:{port}")
    print(f"Health Check: http://{host}:{port}/health")
    print(f"API Base: http://{host}:{port}/api/v1")
    print("=" * 50)
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=debug
    )
