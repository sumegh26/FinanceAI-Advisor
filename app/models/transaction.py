"""
Transaction Model

This module defines the Transaction data model for financial transactions
including income, expenses, investments, and other financial activities.
"""

from app.extensions import db
from datetime import datetime

class Transaction(db.Model):
        
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
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=True)
    transaction_type = db.Column(db.String(32), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.Column(db.Text, nullable=True)  # Store JSON string for simplicity

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "transaction_type": self.transaction_type,
            "date": self.date.isoformat(),
            "created_at": self.created_at.isoformat(),
            "tags": self.tags.split(',') if self.tags else []
        }