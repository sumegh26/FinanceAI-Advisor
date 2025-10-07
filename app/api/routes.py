"""
API Routes for FinanceAI-Advisor

This module contains all the REST API endpoints for managing financial transactions,
budgets, and generating financial insights.
"""

from flask import request, jsonify
from app.api import finance_bp
from app.models.transaction import Transaction
from app.utils.validators import validate_transaction_data
from datetime import datetime
from typing import Dict, List


# In-memory storage(will be replaced with database in future)
transactions_store: Dict[str, Transaction] = {}


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
        
        # Start with all transactions
        filtered_transactions = list(transactions_store.values())
        
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
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result),
            'message': f'Retrieved {len(result)} transactions'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve transactions'
        }), 500


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
            return jsonify({
                'success': False,
                'error': 'No JSON data provided',
                'message': 'Request must contain valid JSON data'
            }), 400
        
        # Validate required fields
        validation_result = validate_transaction_data(data)
        if not validation_result['valid']:
            return jsonify({
                'success': False,
                'error': 'Validation failed',
                'message': validation_result['message'],
                'details': validation_result['errors']
            }), 400
        
        # Create new transaction
        transaction = Transaction(
            amount=data['amount'],
            category=data['category'],
            description=data['description'],
            transaction_type=data['transaction_type'],
            date=datetime.fromisoformat(data['date']) if data.get('date') else None,
            tags=data.get('tags', [])
        )
        
        # Store transaction
        transactions_store[transaction.id] = transaction
        
        return jsonify({
            'success': True,
            'data': transaction.to_dict(),
            'message': 'Transaction created successfully'
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'Invalid data format',
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to create transaction'
        }), 500


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
        if transaction_id not in transactions_store:
            return jsonify({
                'success': False,
                'error': 'Transaction not found',
                'message': f'No transaction found with ID: {transaction_id}'
            }), 404
        
        transaction = transactions_store[transaction_id]
        
        return jsonify({
            'success': True,
            'data': transaction.to_dict(),
            'message': 'Transaction retrieved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve transaction'
        }), 500


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
        if transaction_id not in transactions_store:
            return jsonify({
                'success': False,
                'error': 'Transaction not found',
                'message': f'No transaction found with ID: {transaction_id}'
            }), 404
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided',
                'message': 'Request must contain valid JSON data'
            }), 400
        
        # Get existing transaction
        transaction = transactions_store[transaction_id]
        
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
            transaction.tags = data['tags']
        
        return jsonify({
            'success': True,
            'data': transaction.to_dict(),
            'message': 'Transaction updated successfully'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'Invalid data format',
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to update transaction'
        }), 500


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
        if transaction_id not in transactions_store:
            return jsonify({
                'success': False,
                'error': 'Transaction not found',
                'message': f'No transaction found with ID: {transaction_id}'
            }), 404
        
        # Delete transaction
        deleted_transaction = transactions_store.pop(transaction_id)
        
        return jsonify({
            'success': True,
            'message': f'Transaction {transaction_id} deleted successfully',
            'deleted_transaction': deleted_transaction.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to delete transaction'
        }), 500


@finance_bp.route('/transactions/summary', methods=['GET'])
def get_transactions_summary():
    """
    Get financial summary and statistics
    
    Returns:
        JSON: Summary including total income, expenses, balance, and category breakdown
    """
    try:
        transactions = list(transactions_store.values())
        
        if not transactions:
            return jsonify({
                'success': True,
                'data': {
                    'total_transactions': 0,
                    'total_income': 0,
                    'total_expenses': 0,
                    'net_balance': 0,
                    'categories': {},
                    'transaction_types': {}
                },
                'message': 'No transactions found'
            }), 200
        
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
        
        return jsonify({
            'success': True,
            'data': summary,
            'message': 'Financial summary generated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate summary'
        }), 500
