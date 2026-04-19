# ERP System

A comprehensive Flask-based Enterprise Resource Planning (ERP) system covering Procurement, Goods Receiving, Production, Packaging, Sales, and Financial modules.

## Features

### Modules

1. **Procurement**
   - Supplier Management
   - Purchase Orders
   - Purchase Requisitions

2. **Goods Receiving**
   - Goods Received Notes (GRN)
   - Quality Checks

3. **Production**
   - Bill of Materials (BOM)
   - Work Orders
   - Production Output Tracking

4. **Packaging**
   - Packaging Orders
   - Label Generation
   - Shipment Management

5. **Sales**
   - Customer Management
   - Sales Orders
   - Invoice Generation

6. **Financial**
   - Chart of Accounts
   - Journal Entries
   - Trial Balance Reports

## Tech Stack

- **Backend**: Flask 3.0
- **Database**: PostgreSQL with SQLAlchemy
- **Authentication**: JWT (Flask-JWT-Extended)
- **Migrations**: Flask-Migrate
- **Frontend**: HTML5, JavaScript, Bootstrap 5

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 15+

### Installation

1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```
5. Initialize database:
   ```bash
   python run.py
   ```

### Using Docker

```bash
docker-compose up -d
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Procurement
- `GET /api/procurement/suppliers` - List suppliers
- `POST /api/procurement/suppliers` - Create supplier
- `GET /api/procurement/purchase-orders` - List POs
- `POST /api/procurement/purchase-orders` - Create PO

### Sales
- `GET /api/sales/customers` - List customers
- `POST /api/sales/customers` - Create customer
- `GET /api/sales/sales-orders` - List sales orders
- `POST /api/sales/sales-orders` - Create sales order

### Financial
- `GET /api/financial/accounts` - List accounts
- `POST /api/financial/accounts` - Create account
- `GET /api/financial/journal-entries` - List journal entries
- `POST /api/financial/journal-entries` - Create journal entry
- `GET /api/financial/trial-balance` - Get trial balance

## Running Tests

```bash
pytest
```

## License

MIT
