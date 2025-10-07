"""
Transaction Model

This module defines the Transaction data model for financial transactions
including income, expenses, investments, and other financial activities.
"""

from datetime import datetime
from typing import Dict, List, Optional
import uuid


class Transaction:
    """
    Transaction model representing a financial transaction
    
    Attributes:
        id (str): Unique transaction identifier
        amount (float): Transaction amount (positive for income, negative for expense)
        category (str): Transaction category (e.g., 'groceries', 'salary', 'rent')
        description (str): Human readable transaction description
        transaction_type (str): Type of transaction ('income', 'expense', 'investment', 'transfer')
        date (datetime): When the transaction occurred
        created_at (datetime): When the record was created
        tags (List[str]): Optional tags for additional categorization
    """
    
    def __init__(
        self, 
        amount: float, 
        category: str, 
        description: str, 
        transaction_type: str,
        date: Optional[datetime] = None,
        tags: Optional[List[str]] = None
    ):
        """
        Initialize a new Transaction
        
        Args:
            amount: Transaction amount
            category: Transaction category
            description: Transaction description
            transaction_type: Type of transaction
            date: Transaction date (defaults to current time)
            tags: Optional list of tags
        """
        self.id = str(uuid.uuid4())
        self.amount = float(amount)
        self.category = category.lower().strip()
        self.description = description.strip()
        self.transaction_type = transaction_type.lower()
        self.date = date or datetime.now()
        self.created_at = datetime.now()
        self.tags = tags or []
    
    def to_dict(self) -> Dict:
        """
        Convert transaction to dictionary representation
        
        Returns:
            Dict: Transaction data as dictionary
        """
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'transaction_type': self.transaction_type,
            'date': self.date.isoformat(),
            'created_at': self.created_at.isoformat(),
            'tags': self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Transaction':
        """
        Create Transaction instance from dictionary data
        
        Args:
            data: Dictionary containing transaction data
            
        Returns:
            Transaction: New transaction instance
        """
        transaction = cls(
            amount=data['amount'],
            category=data['category'],
            description=data['description'],
            transaction_type=data['transaction_type'],
            date=datetime.fromisoformat(data.get('date', datetime.now().isoformat())),
            tags=data.get('tags', [])
        )
        # Preserve original ID if provided
        if 'id' in data:
            transaction.id = data['id']
        return transaction
    
    def __repr__(self) -> str:
        """String representation of transaction"""
        return f"Transaction(id='{self.id}', amount={self.amount}, category='{self.category}')"
