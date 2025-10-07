# 🤖 FinanceAI-Advisor

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)


## 🎯 Project Overview

**AI-Driven Personal Finance Management Platform with Intelligent Insights**

FinanceAI-Advisor is a comprehensive, AI-powered financial management system that evolves from basic transaction tracking into a sophisticated financial advisor. Built with modern Python technologies and designed for scalability, this platform demonstrates enterprise-level software architecture while solving real-world financial management challenges.

### Problem Statement
Most people struggle with:
- Manual expense tracking and categorization
- Understanding spending patterns and financial health
- Making informed investment and budgeting decisions
- Lack of personalized financial insights
- Complex financial planning tools

### Solution
FinanceAI-Advisor provides:
- **Intelligent Transaction Management**: Automated categorization and smart insights
- **AI-Powered Analytics**: Machine learning-driven financial patterns recognition
- **Personalized Recommendations**: Custom budget optimization and investment advice
- **Predictive Insights**: Future spending forecasts and goal tracking
- **Comprehensive Reporting**: Beautiful visualizations and detailed financial reports

---

## 🏗️ Architecture & Design Decisions

### Technical Architecture Evolution

#### **Current Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Client    │───▶│   Flask API     │───▶│   In-Memory     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Project Structure Rationale

```
FinanceAI-Advisor/
├── app/                   # Main application package (Application Factory Pattern)
│   ├── __init__.py        # Flask app factory - creates and configures Flask app
│   ├── api/               # REST API layer
│   │   ├── __init__.py    # Blueprint registration
│   │   └── routes.py      # All API endpoints and business logic
│   ├── models/            # Data models layer
│   │   └── transaction.py # Transaction data model with validation
│   └── utils/             # Utility functions
│       └── validators.py  # Input validation logic
├── tests/                 # Test suite
├── run.py                # Application entry point
└── requirements.txt      # Dependencies

```
## 🚀 Features

### Current Features

#### ✅ **Core Transaction Management**
- **Full CRUD Operations**: Create, Read, Update, Delete transactions
- **Rich Data Model**: Support for categories, tags, descriptions, and metadata
- **Transaction Types**: Income, Expense, Investment, Transfer
- **Automatic Timestamps**: Created and transaction date tracking

#### ✅ **Advanced Filtering & Search**
- **Category Filtering**: Find transactions by category
- **Date Range Queries**: Filter by custom date ranges
- **Transaction Type Filtering**: Separate income from expenses
- **Multi-Parameter Combinations**: Complex query support

#### ✅ **Financial Analytics**
- **Real-Time Calculations**: Live balance and total calculations
- **Category Breakdown**: Spending analysis by category
- **Transaction Summaries**: Count and amount aggregations
- **Time-Based Insights**: Date range analytics

#### ✅ **Professional API Design**
- **RESTful Endpoints**: Standard HTTP methods and status codes
- **JSON Responses**: Consistent response format with success/error indicators
- **Error Handling**: Comprehensive error messages and validation feedback
- **Health Monitoring**: Service health check endpoint

#### ✅ **Data Validation & Security**
- **Input Sanitization**: Prevents malformed data
- **Required Field Validation**: Ensures data completeness
- **Type Checking**: Validates data types and formats
- **Business Rule Enforcement**: Amount validation, category rules

#### ✅ **Testing Infrastructure**
- **Unit Tests**: Comprehensive API endpoint testing
- **Test Coverage**: High test coverage for critical functions
- **Automated Testing**: pytest integration with CI/CD ready
- **Mock Data**: Consistent test fixtures

### ⏭ Upcoming Features

#### ✅ **Phase 1: Core Platform (Current)**

- Flask + SQLite + REST API + Basic Validation


#### 🔄 **Phase 2: Data Persistence**
- SQLite/PostgreSQL database integration
- Database migrations and schema management
- Connection pooling and optimization
- Data backup and recovery

#### 🔄 **Phase 3: AI Integration**
- LangChain integration for natural language processing
- OpenAI GPT for financial insights and recommendations
- Automated transaction categorization using ML
- Spending pattern recognition and alerts

#### 🔄 **Phase 4: Advanced AI Features**
- Multi-agent workflows for complex financial analysis
- Investment recommendation engine
- Risk assessment and portfolio optimization
- Goal-based financial planning

#### 🔄 **Phase 5: Production Ready**
- Docker containerization
- CI/CD pipeline with GitHub Actions
- Production deployment configuration
- Performance monitoring and logging

---

### 🗝 Key Design Decisions

#### 1. **Application Factory Pattern**
**Decision**: Use Flask Application Factory  
**Rationale**:
- **Testability**: Enables creation of app instances with different configurations
- **Scalability**: Supports multiple environments (dev, test, prod)
- **Maintainability**: Centralizes app configuration and initialization
- **Best Practice**: Follows official Flask recommendations

#### 2. **Blueprint-Based Modular Architecture**
**Decision**: Organize routes using Flask Blueprints  
**Rationale**:
- **Separation of Concerns**: Each blueprint handles specific functionality
- **Scalability**: Easy to add new feature modules
- **Team Development**: Multiple developers can work on different blueprints
- **URL Organization**: Clean, RESTful API structure

#### 3. **Model-First Design**
**Decision**: Start with comprehensive data models  
**Rationale**:
- **Data Integrity**: Ensures consistent data structure
- **Validation**: Built-in data validation and sanitization
- **Serialization**: Easy conversion between Python objects and JSON
- **Future-Proof**: Ready for database integration

#### 4. **In-Memory Storage (Phase 1)**
**Decision**: Use Python dictionaries for initial storage  
**Rationale**:
- **Rapid Prototyping**: Quick setup without database complexity
- **Learning Focus**: Concentrate on API design and business logic
- **Easy Testing**: Predictable state for unit tests
- **Migration Path**: Clear upgrade path to persistent storage

#### 5. **Comprehensive Input Validation**
**Decision**: Separate validation layer with detailed error handling  
**Rationale**:
- **Security**: Prevents injection attacks and data corruption
- **User Experience**: Clear error messages guide API users
- **Maintainability**: Centralized validation logic
- **Professional Standards**: Enterprise-level input handling

#### 6. **RESTful API Design**
**Decision**: Follow REST conventions strictly  
**Rationale**:
- **Industry Standard**: Familiar to all developers
- **HTTP Semantics**: Proper use of HTTP methods and status codes
- **Statelessness**: Scalable and cacheable
- **Documentation**: Self-describing API structure

---



## ⚡ Quick Start

### Prerequisites

- **Python**: Version 3.12 or higher
- **Git**: For version control
- **Virtual Environment**: Python venv or conda
- **Code Editor**: VS Code (recommended) or PyCharm

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/FinanceAI-Advisor.git
cd FinanceAI-Advisor

# 2. Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# 5. Run the application
python run.py
```

### Verification Steps

```bash
# 1. Test health endpoint
curl http://127.0.0.1:5000/health

# 2. Create a test transaction
curl -X POST http://127.0.0.1:5000/api/v1/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 1000,
    "category": "salary",
    "description": "Monthly salary",
    "transaction_type": "income"
  }'

# 3. Get all transactions
curl http://127.0.0.1:5000/api/v1/transactions

# 4. Run tests
pytest tests/ -v
```

---

## 📚 API Documentation

### Base Configuration

- **Base URL**: `http://127.0.0.1:5000/api/v1`
- **Content-Type**: `application/json`
- **Response Format**: JSON with consistent structure

### Response Format

```json
{
    "success": true,
    "data": { ... },
    "message": "Operation completed successfully",
    "errors": []  // Only present on validation failures
}
```

### Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/transactions` | List all transactions |
| POST | `/api/v1/transactions` | Create new transaction |
| GET | `/api/v1/transactions/{id}` | Get specific transaction |
| PUT | `/api/v1/transactions/{id}` | Update transaction |
| DELETE | `/api/v1/transactions/{id}` | Delete transaction |
| GET | `/api/v1/transactions/summary` | Financial summary |

### Detailed Endpoint Documentation

#### Create Transaction
```http
POST /api/v1/transactions
Content-Type: application/json

{
    "amount": 2500.00,
    "category": "salary",
    "description": "Monthly salary payment",
    "transaction_type": "income",
    "date": "2024-10-07T10:30:00",  // Optional, defaults to now
    "tags": ["work", "monthly"]      // Optional
}
```

**Response**:
```json
{
    "success": true,
    "data": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "amount": 2500.0,
        "category": "salary",
        "description": "Monthly salary payment",
        "transaction_type": "income",
        "date": "2024-10-07T10:30:00",
        "created_at": "2024-10-07T10:30:15.123456",
        "tags": ["work", "monthly"]
    },
    "message": "Transaction created successfully"
}
```

#### Query Parameters for GET /transactions

| Parameter | Type | Description |
|-----------|------|-------------|
| `category` | string | Filter by category |
| `transaction_type` | string | income, expense, investment, transfer |
| `start_date` | string | ISO format date (YYYY-MM-DDTHH:MM:SS) |
| `end_date` | string | ISO format date (YYYY-MM-DDTHH:MM:SS) |

#### Error Responses

```json
{
    "success": false,
    "error": "Validation failed",
    "message": "Invalid transaction data",
    "details": [
        "'amount' is required",
        "'transaction_type' must be one of: income, expense, investment, transfer"
    ]
}
```

### Example API Calls

```bash
# Create income transaction
curl -X POST http://127.0.0.1:5000/api/v1/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 5000,
    "category": "salary",
    "description": "October 2024 salary",
    "transaction_type": "income",
    "tags": ["job", "monthly"]
  }'

# Create expense transaction
curl -X POST http://127.0.0.1:5000/api/v1/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "amount": -200,
    "category": "groceries",
    "description": "Weekly grocery shopping",
    "transaction_type": "expense",
    "tags": ["food", "weekly"]
  }'

# Get transactions filtered by category
curl "http://127.0.0.1:5000/api/v1/transactions?category=salary"

# Get financial summary
curl http://127.0.0.1:5000/api/v1/transactions/summary

# Update transaction
curl -X PUT http://127.0.0.1:5000/api/v1/transactions/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description",
    "tags": ["updated", "modified"]
  }'
```
## 🤝 Contributing
Contribution & Branching
```
main: stable code

develop: active changes

feature/: prefix for new features
```

Pull Request Guidelines
```
Submit changes to a feature or develop branch.

Write clear commit and PR messages.

Only document implemented functionality.
```

<div align="center">

### 🚀 Ready to Transform Financial Management with AI?

**[⚡ Get Started](#-quick-start) | [📚 Read the Docs](#-api-documentation) | [🤝 Contribute](#-contributing) | [⭐ Star on GitHub](https://github.com/sumegh26/FinanceAI-Advisor)**

---

</div>
