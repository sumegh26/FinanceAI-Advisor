"""
Data Validation Utilities

This module contains functions for validating input data
to ensure data integrity and security.
"""

from typing import Dict, Any, List
# from app.utils.exceptions import ValidationError
from app.utils.exceptions import ValidationError

def validate_transaction_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate transaction data for creation/update
    
    Args:
        data: Dictionary containing transaction data
    
    Returns:
        Dict: Validation result with 'valid' boolean, 'message', and 'errors'
    """
    errors = []
    
    # Validate required fields
    required_fields = ['amount', 'category', 'description', 'transaction_type']
    
    for field in required_fields:
        if field not in data or data[field] is None:
            errors.append(f"'{field}' is required")
        elif isinstance(data[field], str) and not data[field].strip():
            errors.append(f"'{field}' cannot be empty")
    
    # Validate amount
    if 'amount' in data:
        try:
            amount = float(data['amount'])
            if amount == 0:
                errors.append("Amount cannot be zero")
        except (ValueError, TypeError):
            errors.append("Amount must be a valid number")
    
    # Validate transaction_type
    valid_types = ['income', 'expense', 'investment', 'transfer']
    if 'transaction_type' in data:
        if data['transaction_type'].lower() not in valid_types:
            errors.append(f"Transaction type must be one of: {', '.join(valid_types)}")
    
    # Validate tags if provided
    if 'tags' in data and data['tags'] is not None:
        if not isinstance(data['tags'], list):
            errors.append("Tags must be a list")
        elif not all(isinstance(tag, str) for tag in data['tags']):
            errors.append("All tags must be strings")
    
    # Validate date if provided
    if 'date' in data and data['date'] is not None:
        try:
            from datetime import datetime
            datetime.fromisoformat(data['date'])
        except ValueError:
            errors.append("Date must be in ISO format (YYYY-MM-DDTHH:MM:SS)")
    
    if errors:
        raise ValidationError("Invalid transaction data", errors)
    else:
        is_valid = True
        message = "Validation successful"
    
    return {
        'valid': is_valid,
        'message': message,
        'errors': errors
    }


def validate_query_params(params: Dict[str, str]) -> Dict[str, Any]:
    """
    Validate query parameters for filtering
    
    Args:
        params: Dictionary of query parameters
    
    Returns:
        Dict: Validation result
    """
    errors = []
    
    # Validate date parameters
    for date_param in ['start_date', 'end_date']:
        if date_param in params and params[date_param]:
            try:
                from datetime import datetime
                datetime.fromisoformat(params[date_param])
            except ValueError:
                errors.append(f"{date_param} must be in ISO format")
    
    # Validate transaction_type if provided
    if 'transaction_type' in params and params['transaction_type']:
        valid_types = ['income', 'expense', 'investment', 'transfer']
        if params['transaction_type'].lower() not in valid_types:
            errors.append(f"Transaction type must be one of: {', '.join(valid_types)}")
    
    is_valid = len(errors) == 0
    
    return {
        'valid': is_valid,
        'errors': errors
    }
