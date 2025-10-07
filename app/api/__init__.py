"""
API Blueprint Module

This module defines the main API blueprint that contains all the routes
for the FinanceAI-Advisor application.
"""

from flask import Blueprint

# Create the main API blueprint
finance_bp = Blueprint('finance_api', __name__)

# Import routes to register them with the blueprint
from app.api import routes
