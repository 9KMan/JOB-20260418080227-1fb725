# Payment Integration + Sponsorship Platform

A production-ready scholarship sponsorship platform with payment integration for Paystack, Flutterwave, and Interac.

## Features

- **Multi-Provider Payment Integration**: Paystack, Flutterwave, and Interac support
- **Webhook Handling**: Secure webhook processing with signature verification
- **Scholarship Management**: Full CRUD for scholarships with line-item sponsorship
- **School Verification Flow**: Verify schools before processing payments
- **Donation System**: Complete donation workflow with PDF receipt generation
- **Notification System**: Email (SendGrid) and SMS (Twilio) notifications
- **Database Design**: Schools, Students, Guardians, Agents relationships

## Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Payments**: Paystack, Flutterwave, Interac
- **Notifications**: SendGrid (email), Twilio (SMS)
- **Documentation**: PDF receipt generation with ReportLab

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/9KMan/JOB-20260418080227-1fb725.git
cd JOB-20260418080227-1fb725
```

2. Create virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Initialize the database:
```bash
python init_db.py
```

5. Run the application:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Deployment

```bash
docker-compose up -d
```

## API Endpoints

### Schools
- `POST /schools` - Create school
- `GET /schools` - List schools
- `GET /schools/{id}` - Get school details
- `PUT /schools/{id}` - Update school
- `POST /schools/{id}/verify` - Verify school

### Students
- `POST /students` - Create student
- `GET /students` - List students
- `GET /students/{id}` - Get student details
- `PUT /students/{id}` - Update student

### Guardians
- `POST /guardians` - Create guardian
- `GET /guardians` - List guardians
- `GET /guardians/{id}` - Get guardian details

### Agents
- `POST /agents` - Create agent
- `GET /agents` - List agents
- `GET /agents/{id}` - Get agent details
- `POST /agents/{id}/students/{student_id}` - Assign student to agent

### Scholarships
- `POST /scholarships` - Create scholarship
- `GET /scholarships` - List scholarships
- `GET /scholarships/{id}` - Get scholarship details
- `PUT /scholarships/{id}` - Update scholarship

### Payments
- `POST /payments/initiate` - Initiate payment
- `GET /payments/{id}` - Get payment details
- `GET /payments` - List payments
- `POST /payments/verify/{reference}` - Verify payment
- `POST /payments/receipt/{id}` - Generate PDF receipt

### Webhooks
- `POST /webhooks/paystack` - Paystack webhook
- `POST /webhooks/flutterwave` - Flutterwave webhook

## Configuration

Environment variables (see `.env.example`):

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `PAYSTACK_SECRET_KEY` | Paystack secret key |
| `PAYSTACK_PUBLIC_KEY` | Paystack public key |
| `PAYSTACK_WEBHOOK_SECRET` | Paystack webhook secret |
| `FLUTTERWAVE_SECRET_KEY` | Flutterwave secret key |
| `FLUTTERWAVE_PUBLIC_KEY` | Flutterwave public key |
| `FLUTTERWAVE_WEBHOOK_SECRET` | Flutterwave webhook secret |
| `INTERAC_API_KEY` | Interac API key |
| `SENDGRID_API_KEY` | SendGrid API key |
| `TWILIO_ACCOUNT_SID` | Twilio account SID |
| `TWILIO_AUTH_TOKEN` | Twilio auth token |
| `TWILIO_PHONE_NUMBER` | Twilio phone number |

## Database Schema

```
Schools
  └── Students
        ├── Guardians
        └── Scholarships
              └── Payments

Agents
  └── AgentStudents (many-to-many)
        └── Students
```

## Testing

```bash
pip install -r tests/requirements.txt
pytest tests/ -v
```

## License

MIT