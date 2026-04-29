# Specification: Payment Integration + Sponsorship Platform

## 1. Project Overview

**Project Name:** Scholarship Payment Platform
**Project Type:** Full-stack web application with payment integration
**Core Functionality:** A scholarship sponsorship platform that integrates with multiple payment providers (Paystack, Flutterwave, Interac) to facilitate donations for school scholarships. Features include school/student management, scholarship tracking, payment processing with webhooks, and PDF receipt generation.
**Target Users:** Schools, students, guardians, agents, donors, and platform administrators

## 2. Technical Stack

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **ORM:** SQLAlchemy 2.0
- **Database:** PostgreSQL 15+

### Payment Providers
- **Paystack** - Primary African payment processor
- **Flutterwave** - Secondary African payment processor
- **Interac** - Canadian debit/payment system

### Notifications
- **Email:** SendGrid API
- **SMS:** Twilio API

### Documentation
- **PDF Generation:** ReportLab

### Frontend
- **Type:** Static HTML/JS/CSS (SPA-style)
- **API Communication:** REST API with JSON

## 3. Database Schema

### Entity Relationship Diagram

```
Schools
  └── Students (1:N)
        ├── Guardians (1:N)
        └── Scholarships (1:N)
              └── Payments (1:N)

Agents
  └── AgentStudents (N:N through association table)
        └── Students

Notifications (standalone)
```

### Tables

#### schools
| Column | Type | Constraints |
|--------|------|-------------|
| id | SERIAL | PRIMARY KEY |
| name | VARCHAR(255) | NOT NULL |
| email | VARCHAR(255) | UNIQUE |
| address | TEXT | |
| verification_status | VARCHAR(50) | DEFAULT 'pending' |
| verified_at | TIMESTAMP | NULL |
| created_at | TIMESTAMP | DEFAULT NOW() |

#### students
| Column | Type | Constraints |
|--------|------|-------------|
| id | SERIAL | PRIMARY KEY |
| school_id | INTEGER | FOREIGN KEY (schools.id) |
| first_name | VARCHAR(100) | NOT NULL |
| last_name | VARCHAR(100) | NOT NULL |
| email | VARCHAR(255) | |
| phone | VARCHAR(50) | |
| date_of_birth | DATE | |
| created_at | TIMESTAMP | DEFAULT NOW() |

#### guardians
| Column | Type | Constraints |
|--------|------|-------------|
| id | SERIAL | PRIMARY KEY |
| student_id | INTEGER | FOREIGN KEY (students.id) |
| first_name | VARCHAR(100) | NOT NULL |
| last_name | VARCHAR(100) | NOT NULL |
| email | VARCHAR(255) | |
| phone | VARCHAR(50) | |
| relationship | VARCHAR(50) | |
| created_at | TIMESTAMP | DEFAULT NOW() |

#### agents
| Column | Type | Constraints |
|--------|------|-------------|
| id | SERIAL | PRIMARY KEY |
| name | VARCHAR(255) | NOT NULL |
| email | VARCHAR(255) | UNIQUE |
| phone | VARCHAR(50) | |
| is_active | BOOLEAN | DEFAULT TRUE |
| created_at | TIMESTAMP | DEFAULT NOW() |

#### agent_students (Association Table)
| Column | Type | Constraints |
|--------|------|-------------|
| agent_id | INTEGER | FOREIGN KEY (agents.id), PRIMARY KEY |
| student_id | INTEGER | FOREIGN KEY (students.id), PRIMARY KEY |

#### scholarships
| Column | Type | Constraints |
|--------|------|-------------|
| id | SERIAL | PRIMARY KEY |
| student_id | INTEGER | FOREIGN KEY (students.id) |
| agent_id | INTEGER | FOREIGN KEY (agents.id), NULL |
| items | JSON | NOT NULL (list of scholarship items) |
| total_amount | DECIMAL(10,2) | NOT NULL |
| status | VARCHAR(50) | DEFAULT 'pending' |
| created_at | TIMESTAMP | DEFAULT NOW() |

**Scholarship Status Values:** pending, partially_funded, fully_funded

#### payments
| Column | Type | Constraints |
|--------|------|-------------|
| id | SERIAL | PRIMARY KEY |
| scholarship_id | INTEGER | FOREIGN KEY (scholarships.id), NULL |
| donor_email | VARCHAR(255) | |
| amount | DECIMAL(10,2) | NOT NULL |
| currency | VARCHAR(10) | DEFAULT 'USD' |
| payment_provider | VARCHAR(50) | |
| provider_reference | VARCHAR(255) | |
| status | VARCHAR(50) | DEFAULT 'pending' |
| verified_at | TIMESTAMP | NULL |
| created_at | TIMESTAMP | DEFAULT NOW() |

**Payment Status Values:** pending, verified, failed

#### notifications
| Column | Type | Constraints |
|--------|------|-------------|
| id | SERIAL | PRIMARY KEY |
| user_type | VARCHAR(50) | |
| user_id | INTEGER | |
| notification_type | VARCHAR(100) | |
| message | TEXT | |
| is_read | BOOLEAN | DEFAULT FALSE |
| created_at | TIMESTAMP | DEFAULT NOW() |

## 4. API Endpoints

### Schools (`/schools`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/schools` | Create a new school |
| GET | `/schools` | List all schools (paginated) |
| GET | `/schools/{id}` | Get school details |
| PUT | `/schools/{id}` | Update school |
| POST | `/schools/{id}/verify` | Verify school |
| DELETE | `/schools/{id}` | Delete school |

### Students (`/students`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/students` | Create a new student |
| GET | `/students` | List all students (paginated) |
| GET | `/students/{id}` | Get student details |
| PUT | `/students/{id}` | Update student |
| DELETE | `/students/{id}` | Delete student |

### Guardians (`/guardians`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/guardians` | Create a new guardian |
| GET | `/guardians` | List all guardians (paginated) |
| GET | `/guardians/{id}` | Get guardian details |
| PUT | `/guardians/{id}` | Update guardian |
| DELETE | `/guardians/{id}` | Delete guardian |

### Agents (`/agents`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/agents` | Create a new agent |
| GET | `/agents` | List all agents (paginated) |
| GET | `/agents/{id}` | Get agent details |
| PUT | `/agents/{id}` | Update agent |
| DELETE | `/agents/{id}` | Delete agent |
| POST | `/agents/{id}/students/{student_id}` | Assign student to agent |

### Scholarships (`/scholarships`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/scholarships` | Create a new scholarship |
| GET | `/scholarships` | List all scholarships (paginated) |
| GET | `/scholarships/{id}` | Get scholarship details |
| PUT | `/scholarships/{id}` | Update scholarship |
| DELETE | `/scholarships/{id}` | Delete scholarship |

### Payments (`/payments`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/payments/initiate` | Initiate a payment |
| GET | `/payments` | List all payments (paginated, filterable) |
| GET | `/payments/{id}` | Get payment details |
| POST | `/payments/verify/{reference}` | Verify payment status |
| POST | `/payments/receipt/{id}` | Generate PDF receipt |
| DELETE | `/payments/{id}` | Delete payment |

### Webhooks (`/webhooks`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/webhooks/paystack` | Paystack webhook handler |
| POST | `/webhooks/flutterwave` | Flutterwave webhook handler |

## 5. Services

### Payment Services

#### PaystackService
- `initiate_payment(amount, email, metadata, currency)` - Initialize a Paystack transaction
- `verify_payment(reference)` - Verify a Paystack transaction
- `verify_webhook_signature(payload, signature)` - Verify Paystack webhook signature
- `handle_webhook(payload)` - Process Paystack webhook event

#### FlutterwaveService
- `initiate_payment(amount, email, metadata, currency)` - Initialize a Flutterwave transaction
- `verify_payment(tx_ref)` - Verify a Flutterwave transaction
- `verify_webhook_signature(payload, signature)` - Verify Flutterwave webhook signature
- `handle_webhook(payload)` - Process Flutterwave webhook event

#### NotificationService
- `notify_payment_received(db, user_type, user_id, donor_email, amount, currency)` - Send payment notification
- `notify_deadline(db, user_type, user_id, deadline_message)` - Send deadline notification
- `_send_email(to_email, subject, body)` - Send email via SendGrid
- `_send_sms(to_phone, message)` - Send SMS via Twilio

#### ReceiptService
- `generate_receipt(donor_name, donor_email, amount, currency, payment_reference, payment_date, scholarship_details, student_name)` - Generate PDF receipt

## 6. Frontend Pages

| Page | Description |
|------|-------------|
| `index.html` | Main landing page |
| `login.html` | Login page |
| `dashboard.html` | Main dashboard |
| `schools.html` | School management |
| `students.html` | Student management |
| `guardians.html` | Guardian management |
| `agents.html` | Agent management |
| `scholarships.html` | Scholarship management |
| `payments.html` | Payment tracking |
| `donate.html` | Donation form |

## 7. Configuration

### Environment Variables
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

## 8. Payment Workflow

1. **Scholarship Creation:** Agent or admin creates a scholarship with line items (tuition, books, uniforms, etc.)
2. **Payment Initiation:** Donor initiates payment through `/payments/initiate` with their email and amount
3. **Provider Redirect:** Donor is redirected to Paystack/Flutterwave to complete payment
4. **Verification:** After payment, `/payments/verify/{reference}` confirms the payment
5. **Webhook Processing:** Payment provider sends webhook to update payment status
6. **Scholarship Update:** Payment status updates scholarship funding status (partially_funded/fully_funded)
7. **Notification:** Donor and student/guardian receive confirmation notifications
8. **Receipt Generation:** PDF receipt available via `/payments/receipt/{id}`

## 9. Docker Deployment

The application can be deployed using Docker Compose:

```bash
docker-compose up -d
```

This starts:
- `web` service on port 8000 (FastAPI application)
- `db` service on port 5432 (PostgreSQL database)

## 10. Testing

Run tests with:

```bash
pip install -r tests/requirements.txt
pytest tests/ -v
```

## 11. Project Structure

```
.
├── app/
│   ├── main.py              # FastAPI application entry
│   ├── config.py            # Settings configuration
│   ├── database.py          # Database connection
│   ├── schemas.py           # Pydantic schemas
│   ├── models.py            # SQLAlchemy models
│   ├── extensions.py        # Flask extensions (legacy)
│   ├── routers/             # API route handlers
│   │   ├── schools.py
│   │   ├── students.py
│   │   ├── guardians.py
│   │   ├── agents.py
│   │   ├── scholarships.py
│   │   ├── payments.py
│   │   └── webhooks.py
│   ├── services/            # Business logic services
│   │   ├── paystack.py
│   │   ├── flutterwave.py
│   │   ├── interac.py
│   │   ├── notification.py
│   │   ├── receipt.py
│   │   └── reporting.py
│   └── models/              # Legacy ERP models (deprecated)
├── frontend/                # Static frontend files
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── schools.html
│   ├── students.html
│   ├── guardians.html
│   ├── agents.html
│   ├── scholarships.html
│   ├── payments.html
│   ├── donate.html
│   ├── js/
│   └── css/
├── tests/                   # Test files
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile               # Docker image definition
├── requirements.txt         # Python dependencies
├── init_db.py               # Database initialization script
└── run.py                   # Flask run script (legacy)
```