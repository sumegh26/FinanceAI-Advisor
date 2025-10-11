"""
API Routes for FinanceAI-Advisor

This module contains all the REST API endpoints for managing financial transactions,
budgets, and generating financial insights.
"""

from flask import request
from app.api import finance_bp
from app.models.transaction import Transaction
from app.utils.validators import validate_transaction_data, ValidationError
from app.utils.exceptions import NotFoundError
from datetime import datetime
from app.extensions import db
from app.utils.response import json_response
from app.utils.logger import logger
import traceback

# Database storage added via SQLAlchemy

#Get all transactions with optional filtering
@finance_bp.route('/transactions', methods=['GET'])
def get_transactions():
    """
    Get all transactions with optional filtering
    
    Query Parameters:
        category (str, optional): Filter by category
        transaction_type (str, optional): Filter by transaction type
        start_date (str, optional): Filter by start date (ISO format)
        end_date (str, optional): Filter by end date (ISO format)
    
    Returns:
        JSON: List of transactions matching filters
    """
    try:
        # Get query parameters
        category = request.args.get('category')
        transaction_type = request.args.get('transaction_type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        filtered_transactions = Transaction.query.all()     #query all transactions from the database
        
        # Apply filters
        if category:
            filtered_transactions = [
                t for t in filtered_transactions 
                if t.category.lower() == category.lower()
            ]
        
        if transaction_type:
            filtered_transactions = [
                t for t in filtered_transactions 
                if t.transaction_type.lower() == transaction_type.lower()
            ]
        
        if start_date:
            start = datetime.fromisoformat(start_date)
            filtered_transactions = [
                t for t in filtered_transactions 
                if t.date >= start
            ]
        
        if end_date:
            end = datetime.fromisoformat(end_date)
            filtered_transactions = [
                t for t in filtered_transactions 
                if t.date <= end
            ]
        
        # Convert to dictionaries and sort by date (newest first)
        result = [t.to_dict() for t in filtered_transactions]
        result.sort(key=lambda x: x['date'], reverse=True)
        
        return json_response(True, f"Retrieved {len(result)} transactions", data=result, status_code=200)
        
    except Exception as e:
        return json_response(False, "Failed to retrieve transactions", error=str(e), status_code=500)

# Create a new transaction
@finance_bp.route('/transactions', methods=['POST'])
def create_transaction():
    """
    Create a new financial transaction
    
    Request Body:
        amount (float): Transaction amount
        category (str): Transaction category
        description (str): Transaction description
        transaction_type (str): Type ('income', 'expense', 'investment', 'transfer')
        date (str, optional): Transaction date (ISO format)
        tags (list, optional): List of tags
    
    Returns:
        JSON: Created transaction data
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data:
            raise ValidationError('No JSON data provided', ['Request must contain valid JSON data'])
        
        # Validate required fields
        validate_transaction_data(data)

        # Create new transaction
        transaction = Transaction(
            amount=data['amount'],
            category=data['category'],
            description=data['description'],
            transaction_type=data['transaction_type'],
            date=datetime.fromisoformat(data['date']) if data.get('date') else datetime.utcnow(),
            tags=','.join(data.get('tags', [])) if data.get('tags') else None
        )

        # Store transaction in the database
        db.session.add(transaction)
        db.session.commit()

        return json_response(True, "Transaction created successfully", transaction.to_dict(), status_code=201)
        
    except ValueError as e:
        return json_response(False, "Input validation failed", error=e.message, details=e.errors, status_code=400)
    
    except Exception as e:
        return json_response(False, "Failed to create transaction", error=str(e), status_code=500)

# Get a specific transaction by ID
@finance_bp.route('/transactions/<transaction_id>', methods=['GET'])
def get_transaction(transaction_id: str):
    """
    Get a specific transaction by ID
    
    Args:
        transaction_id: UUID of the transaction
    
    Returns:
        JSON: Transaction data or error message
    """
    try:
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            raise NotFoundError(f"No transaction found with ID: {transaction_id}")
        
        return json_response(True, 'Transaction retrieved successfully', data=transaction.to_dict(), status_code=200)
    
    except NotFoundError as e:
        return json_response(False, 'Not found', error=e.message, status_code=404)
    except Exception as e:
        return json_response(False, 'Failed to retrieve transaction', error=str(e), status_code=500)

# Update an existing transaction
@finance_bp.route('/transactions/<transaction_id>', methods=['PUT'])
def update_transaction(transaction_id: str):
    """
    Update an existing transaction
    
    Args:
        transaction_id: UUID of the transaction to update
    
    Request Body:
        Same as create_transaction (all fields optional for updates)
    
    Returns:
        JSON: Updated transaction data
    """
    try:
        # Get existing transaction
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            raise NotFoundError(f"No transaction found with ID: {transaction_id}")
        
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            raise ValidationError('No JSON data provided', ['Request must contain valid JSON data'])
        
        validate_transaction_data(data)  # Validate input data
        
        # Update fields if provided
        if 'amount' in data:
            transaction.amount = float(data['amount'])
        if 'category' in data:
            transaction.category = data['category'].lower().strip()
        if 'description' in data:
            transaction.description = data['description'].strip()
        if 'transaction_type' in data:
            transaction.transaction_type = data['transaction_type'].lower()
        if 'date' in data:
            transaction.date = datetime.fromisoformat(data['date'])
        if 'tags' in data:
            # Ensure tags are stored as a comma-separated string
            transaction.tags = ','.join(data['tags']) if isinstance(data['tags'], list) else data['tags']
        
        db.session.commit()

        return json_response(True, 'Transaction updated successfully', transaction.to_dict(), status_code=200)
        
    except ValueError as e:
        return json_response(False, 'Input validation failed', error=e.message, details=e.errors, status_code=400)
    except NotFoundError as e:
        return json_response(False, 'Not found', error=e.message, status_code=404)
    except Exception as e:
        return json_response(False, 'Failed to update transaction', error=str(e), status_code=500)

# Delete a transaction by ID
@finance_bp.route('/transactions/<transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id: str):
    """
    Delete a transaction
    
    Args:
        transaction_id: UUID of the transaction to delete
    
    Returns:
        JSON: Success message or error
    """
    try:
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            raise NotFoundError(f"No transaction found with ID: {transaction_id}")
        
        # Delete transaction
        db.session.delete(transaction)
        db.session.commit()

        deleted_transaction = transaction
        return json_response(True, f'Transaction {transaction_id} deleted successfully', deleted_transaction.to_dict(), status_code=200)
        
    except NotFoundError as e:
        return json_response(False, 'Not found', error=e.message, status_code=404)
    except Exception as e:
        return json_response(False, 'Failed to delete transaction', error=str(e), status_code=500)

# Get a summary of all transactions
@finance_bp.route('/transactions/summary', methods=['GET'])
def get_transactions_summary():
    """
    Get financial summary and statistics
    
    Returns:
        JSON: Summary including total income, expenses, balance, and category breakdown
    """
    try:
        transactions = list(Transaction.query.all())
        
        if not transactions:
            return json_response(True, 'No transactions found', data={
                'total_transactions': 0,
                'total_income': 0,
                'total_expenses': 0,
                'net_balance': 0,
                'categories': {},
                'transaction_types': {}, 
            }, status_code=200)

        # Calculate totals
        total_income = sum(t.amount for t in transactions if t.transaction_type == 'income')
        total_expenses = sum(abs(t.amount) for t in transactions if t.transaction_type == 'expense')
        
        # Category breakdown
        categories = {}
        transaction_types = {}
        
        for transaction in transactions:
            # Category summary
            if transaction.category not in categories:
                categories[transaction.category] = {
                    'total_amount': 0,
                    'transaction_count': 0
                }
            categories[transaction.category]['total_amount'] += transaction.amount
            categories[transaction.category]['transaction_count'] += 1
            
            # Transaction type summary
            if transaction.transaction_type not in transaction_types:
                transaction_types[transaction.transaction_type] = {
                    'total_amount': 0,
                    'transaction_count': 0
                }
            transaction_types[transaction.transaction_type]['total_amount'] += abs(transaction.amount)
            transaction_types[transaction.transaction_type]['transaction_count'] += 1
        
        summary = {
            'total_transactions': len(transactions),
            'total_income': round(total_income, 2),
            'total_expenses': round(total_expenses, 2),
            'net_balance': round(total_income - total_expenses, 2),
            'categories': categories,
            'transaction_types': transaction_types,
            'latest_transaction_date': max(t.date.isoformat() for t in transactions),
            'earliest_transaction_date': min(t.date.isoformat() for t in transactions)
        }
        
        return json_response(True, 'Financial summary generated successfully', data=summary, status_code=200)
        
    except Exception as e:
        return json_response(False, 'Failed to generate summary', error=str(e), status_code=500)

# Global error handler for ValidationError
@finance_bp.errorhandler(ValidationError) # decorator to catch ValidationError exceptions
def handle_validation_error(error):
    logger.warning(f"Validation Error: {error.message} Details: {error.errors}") # Log the validation error details
    return json_response(False, "Input validation failed", error=error.message, details=error.errors, status_code=400)

# Global error handler for NotFoundError
@finance_bp.errorhandler(NotFoundError) # decorator to catch NotFoundError exceptions
def handle_not_found_error(error):
    logger.warning(f"Not Found: {error.message}") # Log the not found error message
    return json_response(False, "Resource not found", error=error.message, status_code=404)

# Global error handler for generic exceptions
@finance_bp.errorhandler(Exception) # decorator to catch all other exceptions
def handle_generic_error(error):
    logger.error(f"Unhandled Exception: {str(error)}") # Log the error message
    logger.error(traceback.format_exc()) # Log the full stack trace
    return json_response(False, "Internal server error", error=str(error), status_code=500)

