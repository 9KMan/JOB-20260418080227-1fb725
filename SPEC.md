# Specification: Payment Integration + Sponsorship Platform

## 1. Project Overview

**Project:** Backend Developer Needed – Payment Integration + Sponsorship Platform  
**GitHub Repo:** https://github.com/9KMan/JOB-20260418080227-1fb725  
**Tier:** MEDIUM | **Budget:** $950 fixed

### Project Summary
Multi-provider payment integration platform (Paystack / Flutterwave / Interac) with scholarship sponsorship management. Handles donations, webhook verification, PDF receipts, school/student/guardian/agent management, and notifications.

---

## 2. Technical Stack

- **Backend:** Python 3.11+ / FastAPI
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Payment Providers:** Paystack, Flutterwave, Interac
- **Notifications:** SendGrid (email), Twilio (SMS)
- **PDF Generation:** ReportLab
- **Frontend:** HTML/JavaScript (Bootstrap 5)
- **Containerization:** Docker + Docker Compose
- **Testing:** pytest

---

## 3. Database Schema

### Schools
| Field | Type | Notes |
|-------|------|-------|
| id | SERIAL PK | |
| name | VARCHAR(255) | School name |
| email | VARCHAR(255) | Contact email |
| address | TEXT | Full address |
| verification_status | VARCHAR(50) | pending / verified |
| verified_at | TIMESTAMP | nullable |
| created_at | TIMESTAMP | |

### Students
| Field | Type | Notes |
|-------|------|-------|
| id | SERIAL PK | |
| school_id | INT FK | → schools.id |
| guardian_id | INT FK | → guardians.id |
| name | VARCHAR(255) | |
| email | VARCHAR(255) | |
| created_at | TIMESTAMP | |

### Guardians
| Field | Type | Notes |
|-------|------|-------|
| id | SERIAL PK | |
| name | VARCHAR(255) | |
| email | VARCHAR(255) | |
| phone | VARCHAR(50) | |
| relationship | VARCHAR(50) | |

### Agents
| Field | Type | Notes |
|-------|------|-------|
| id | SERIAL PK | |
| name | VARCHAR(255) | |
| email | VARCHAR(255) | |
| region | VARCHAR(100) | |

**Agent-Student relationship:** Many-to-many (agent supports multiple students)

### Scholarships
| Field | Type | Notes |
|-------|------|-------|
| id | SERIAL PK | |
| student_id | INT FK | → students.id |
| agent_id | INT FK | → agents.id |
| items | JSONB | Line-item sponsorship details |
| total_amount | DECIMAL(12,2) | Target amount |
| status | VARCHAR(50) | pending / partially_funded / fully_funded |
| created_at | TIMESTAMP | |

### Payments
| Field | Type | Notes |
|-------|------|-------|
| id | SERIAL PK | |
| scholarship_id | INT FK | → scholarships.id |
| provider | VARCHAR(50) | paystack / flutterwave / interac |
| provider_reference | VARCHAR(255) | Provider's transaction ref |
| amount | DECIMAL(12,2) | |
| currency | VARCHAR(10) | USD, NGN, etc. |
| status | VARCHAR(50) | pending / verified / failed |
| verified_at | TIMESTAMP | nullable |
| created_at | TIMESTAMP | |

### Notifications
| Field | Type | Notes |
|-------|------|-------|
| id | SERIAL PK | |
| user_type | VARCHAR(50) | student / guardian / agent |
| user_id | INT | |
| notification_type | VARCHAR(50) | payment_received / deadline / verification |
| message | TEXT | |
| sent_at | TIMESTAMP | |

---

## 4. API Endpoints

### Schools
- `POST /schools` — Create school
- `GET /schools` — List schools (pagination)
- `GET /schools/{id}` — Get school details
- `PUT /schools/{id}` — Update school
- `POST /schools/{id}/verify` — Verify school (sets status=verified, verified_at=NOW)

### Students
- `POST /students` — Create student (links to school)
- `GET /students` — List students (filter by school_id, guardian_id)
- `GET /students/{id}` — Get student details
- `PUT /students/{id}` — Update student

### Guardians
- `POST /guardians` — Create guardian
- `GET /guardians` — List guardians
- `GET /guardians/{id}` — Get guardian details
- `PUT /guardians/{id}` — Update guardian

### Agents
- `POST /agents` — Create agent
- `GET /agents` — List agents
- `GET /agents/{id}` — Get agent details
- `POST /agents/{id}/students/{student_id}` — Assign student to agent

### Scholarships
- `POST /scholarships` — Create scholarship (with JSON line items)
- `GET /scholarships` — List (filter by student_id, status)
- `GET /scholarships/{id}` — Get scholarship with funding status
- `PUT /scholarships/{id}` — Update scholarship
- **Auto-funding logic:** On payment verification → update scholarship status (pending → partially_funded → fully_funded)

### Payments
- `POST /payments/initiate` — Initiate payment (Paystack/Flutterwave/Interac)
- `GET /payments` — List payments (filter by scholarship_id, status)
- `GET /payments/{id}` — Get payment details
- `POST /payments/verify/{reference}` — Server-side payment verification via provider API
- `POST /payments/receipt/{id}` — Generate PDF receipt

### Webhooks
- `POST /webhooks/paystack` — Paystack webhook (HMAC signature required)
- `POST /webhooks/flutterwave` — Flutterwave webhook (HMAC signature required)
- **Webhook logic:** Verify signature → find payment by reference → update payment status → trigger scholarship auto-funding → send notification

### Auth
- `POST /auth/login` — JWT login
- `POST /auth/register` — User registration

### Health
- `GET /health` — Health check

---

## 5. Payment Integration Details

### Paystack
- `POST https://api.paystack.co/transaction/initialize` — Initiate payment
- `GET https://api.paystack.co/transaction/verify/{reference}` — Verify payment
- **Webhook:** HMAC-SHA512 signature verification via `x_paystack_signature` header
- Environment vars: `PAYSTACK_SECRET_KEY`, `PAYSTACK_PUBLIC_KEY`, `PAYSTACK_WEBHOOK_SECRET`

### Flutterwave
- `POST https://api.flutterwave.com/v3/payments` — Initiate payment
- `GET https://api.flutterwave.com/v3/transactions/{id}/verify` — Verify
- **Webhook:** HMAC-SHA256 signature verification via `verif_hash` header
- Environment vars: `FLUTTERWAVE_SECRET_KEY`, `FLUTTERWAVE_PUBLIC_KEY`

### Interac
- E-Transfer API integration
- Environment var: `INTERAC_API_KEY`

---

## 6. Key Business Logic

### Payment Flow
1. Client initiates payment → `POST /payments/initiate` → returns provider payment URL
2. Client completes payment on provider's page
3. Provider calls webhook → `POST /webhooks/{provider}`
4. Server verifies signature → updates payment status → checks scholarship funding threshold
5. If scholarship fully funded → status = `fully_funded` → notification sent
6. Donor receives email confirmation (SendGrid) + SMS (Twilio)

### School Verification Gate
- Schools must be `verified` before payments are processed for their students
- Payments to unverified schools return HTTP 403

### Scholarship Auto-Funding
```
total_paid = SUM(verified payments for scholarship)
if total_paid >= total_amount → status = 'fully_funded'
elif total_paid > 0 → status = 'partially_funded'
else → status = 'pending'
```

### PDF Receipt
- Generated via ReportLab
- Contains: donor name, amount, currency, scholarship details, payment reference, date
- Endpoint: `GET /payments/{id}/receipt` returns PDF

---

## 7. Project Structure

```
/
├── app/
│   ├── main.py              # FastAPI app entry
│   ├── config.py            # Settings from env
│   ├── database.py          # SQLAlchemy engine + get_db
│   ├── models.py            # All SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── extensions.py        # CORS, middleware
│   ├── routers/
│   │   ├── schools.py
│   │   ├── students.py
│   │   ├── guardians.py
│   │   ├── agents.py
│   │   ├── scholarships.py
│   │   ├── payments.py
│   │   ├── webhooks.py
│   │   └── auth.py
│   └── services/
│       ├── paystack.py      # Paystack API client
│       ├── flutterwave.py   # Flutterwave API client
│       ├── interac.py       # Interac API client
│       ├── notification.py  # SendGrid + Twilio
│       ├── receipt.py       # PDF generation
│       └── reporting.py
├── frontend/                 # HTML/JS pages
│   ├── index.html
│   ├── dashboard.html
│   ├── schools.html
│   ├── students.html
│   ├── scholarships.html
│   ├── payments.html
│   ├── donate.html
│   └── js/
│       └── api.js
├── tests/
│   ├── conftest.py
│   ├── test_financial.py
│   ├── test_procurement.py
│   └── test_sales.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── init_db.py              # Database initialization script
├── .env.example
└── README.md
```

---

## 8. Acceptance Criteria

- [ ] All 7 spec items from job posting are implemented
- [ ] Paystack, Flutterwave, Interac payment initiation works (returns payment URL)
- [ ] Webhook endpoints verify HMAC signatures correctly
- [ ] Payment verification updates payment + scholarship status
- [ ] PDF receipts generate and are downloadable
- [ ] SendGrid email notifications fire on successful payment
- [ ] Twilio SMS notifications fire on payment received
- [ ] Schools must be verified before payments process (403 otherwise)
- [ ] Agent-student many-to-many relationship works
- [ ] Docker Compose starts the full stack (app + PostgreSQL)
- [ ] Unit tests pass for payment and scholarship logic
- [ ] No proposal/cover letter files in GitHub (MinIO only)

---

## 9. Configuration

Environment variables (see `.env.example`):
```
DATABASE_URL=postgresql://user:pass@localhost:5432/scholarship_db
PAYSTACK_SECRET_KEY=
PAYSTACK_PUBLIC_KEY=
PAYSTACK_WEBHOOK_SECRET=
FLUTTERWAVE_SECRET_KEY=
FLUTTERWAVE_PUBLIC_KEY=
INTERAC_API_KEY=
SENDGRID_API_KEY=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
JWT_SECRET_KEY=
APP_NAME=Scholarship Platform
VERSION=1.0.0
```
