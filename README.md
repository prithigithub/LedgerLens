# LedgerLens

## AI-Powered Invoice Processing and Human Review System

LedgerLens is an AI-powered invoice processing application that extracts structured information from invoice images, validates the extracted data, assigns confidence scores, detects personally identifiable information (PII), and routes low-confidence invoices for human review.

The application is designed as an end-to-end production-style invoice processing system using FastAPI, Streamlit, OpenAI Vision, SQLite, Docker, Prometheus, Grafana, Pytest, GitHub Actions, and Google Cloud Run.

---

## Project Objectives

LedgerLens is designed to:

* Accept invoice images in JPG and PNG formats.
* Moderate uploaded invoice images before processing.
* Extract structured invoice data using AI vision capabilities.
* Validate extracted data using Pydantic schemas.
* Generate confidence scores for extracted invoice fields.
* Automatically approve high-confidence invoices.
* Route low-confidence invoices to a human review queue.
* Allow reviewers to approve or correct invoice data.
* Detect and redact sensitive information before logging.
* Apply watermarking to processed invoice images.
* Store invoice data in a database.
* Expose application metrics for monitoring.
* Run automated tests through CI/CD.
* Containerize the application using Docker.
* Support cloud deployment using Google Cloud Run.

---

## System Workflow

```text
                Invoice Image
                     │
                     ▼
             Upload Invoice
                     │
                     ▼
             Image Moderation
                     │
                     ▼
          AI Invoice Data Extraction
                     │
                     ▼
            Pydantic Validation
                     │
                     ▼
          Confidence Score Evaluation
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
   High Confidence        Low Confidence
          │                     │
          ▼                     ▼
 Automatic Approval       Human Review Queue
                                │
                                ▼
                        Approve / Correct
                                │
                                ▼
                         Final Invoice Data
                                │
                                ▼
                          Watermarking
                                │
                                ▼
                         Database Storage
```

---

## Key Features

### 1. Invoice Upload

The system accepts invoice images through the Streamlit frontend and FastAPI API.

Supported formats:

* JPG
* JPEG
* PNG

The invoice can be uploaded through the web interface or through the FastAPI Swagger documentation.

---

### 2. Image Moderation

Uploaded images are checked before invoice processing.

This helps prevent inappropriate or unsupported content from entering the invoice extraction pipeline.

---

### 3. AI-Powered Invoice Extraction

The system uses AI vision capabilities to extract structured invoice information from invoice images.

The extracted data includes fields such as:

* Vendor
* Invoice number
* Invoice date
* Currency
* Subtotal
* Tax
* Total
* Payment method
* Line items

---

### 4. Structured Data Validation

Extracted data is validated using Pydantic models.

Example invoice fields contain:

```text
value
confidence
```

This ensures that extracted invoice information follows the expected schema before being stored or processed further.

---

### 5. Confidence-Based Processing

Each extracted field contains a confidence score.

The system evaluates the overall confidence of the invoice.

```text
High Confidence
      ↓
Automatic Approval
```

```text
Low Confidence
      ↓
Human Review Required
```

This prevents uncertain AI-generated invoice data from being automatically approved without human verification.

---

### 6. Human Review Workflow

Low-confidence invoices are routed to a review queue.

A reviewer can:

* View the extracted invoice data.
* Review confidence scores.
* Correct incorrect fields.
* Approve the invoice after verification.

This provides human oversight for uncertain AI results.

---

### 7. PII Detection and Redaction

The application detects sensitive information such as:

* Email addresses
* Phone numbers
* Social Security numbers

Sensitive information is redacted before being written to logs.

This helps prevent accidental exposure of private information.

---

### 8. Invoice Watermarking

Processed invoice images can be watermarked using the Python Imaging Library (PIL).

Watermarking helps identify processed documents and provides an additional processing record.

---

## Technology Stack

### Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* SQLite

### AI

* OpenAI Vision API

### Frontend

* Streamlit

### Testing

* Pytest
* FastAPI TestClient

### Containerization

* Docker
* Docker Compose

### Monitoring

* Prometheus
* Grafana

### CI/CD

* GitHub Actions

### Cloud Deployment

* Google Cloud Run

---

## Project Structure

```text
LedgerLens/
│
├── backend/
│   ├── main.py
│   ├── api/
│   ├── schemas/
│   ├── services/
│   └── ...
│
├── frontend/
│   ├── home.py
│   ├── pages/
│   └── requirements.txt
│
├── monitoring/
│   ├── prometheus.yml
│   └── grafana/
│       ├── dashboards/
│       └── provisioning/
│
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_confidence.py
│   ├── test_openai.py
│   ├── test_pii.py
│   ├── test_schema.py
│   └── test_watermark.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

---

# Running the Project Locally

## Prerequisites

Install:

* Python 3.11 or later
* Docker Desktop
* Git

---

## Environment Variables

Create a local `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Never commit the real `.env` file or API key to GitHub.

The project `.gitignore` excludes sensitive files such as:

```text
.env
backend/.env
*.db
uploads/
.venv/
```

---

# Running with Docker Compose

Build and start all services:

```bash
docker compose up -d --build
```

Check the running containers:

```bash
docker compose ps
```

Stop the services:

```bash
docker compose down
```

---

## Application Services

### Streamlit Frontend

```text
http://localhost:8501
```

### FastAPI Swagger Documentation

```text
http://localhost:8000/docs
```

### Prometheus

```text
http://localhost:9090
```

### Grafana

```text
http://localhost:3001
```

The exact port may be changed in `docker-compose.yml` if the default port is already in use.

---

# API Endpoints

The FastAPI backend provides endpoints for the invoice processing workflow.

## Invoice Ingestion

```text
POST /ingest/
```

Accepts an invoice image and starts the processing workflow.

The workflow includes:

```text
Upload
  ↓
Moderation
  ↓
AI Extraction
  ↓
Validation
  ↓
Confidence Evaluation
  ↓
Approval or Human Review
```

---

## Human Review

```text
GET /review/
```

Retrieves invoices requiring human review.

---

## Invoice Approval

```text
POST /approve/
```

Approves or updates an invoice after human verification.

---

# Testing

The project includes automated tests for core application functionality.

Run the test suite:

```bash
PYTHONPATH=. pytest -v
```

Current test coverage includes:

* API health endpoint
* Low-confidence review routing
* High-confidence automatic approval
* AI moderation image input
* Email redaction
* Phone number redaction
* SSN redaction
* Invoice schema validation
* Watermark creation

Expected result:

```text
9 passed
```

The tests are designed to validate the core application logic without exposing real API keys or sensitive production data.

---

# Monitoring

LedgerLens uses Prometheus and Grafana for application monitoring.

The monitoring stack is:

```text
LedgerLens Backend
        │
        ▼
   Prometheus
        │
        ▼
     Grafana
```

Metrics can be used to monitor application behavior such as:

* Invoice processing count
* Human review count
* Processing latency
* Moderation latency
* Extraction latency
* Confidence scores
* Pending review count
* Estimated processing cost

Grafana dashboards are provisioned using configuration files stored under:

```text
monitoring/grafana/
```

---

# Docker Architecture

The Docker Compose application contains the following services:

```text
┌────────────────────┐
│ Streamlit Frontend │
│      Port 8501     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│   FastAPI Backend  │
│      Port 8000     │
└──────┬─────┬───────┘
       │     │
       │     ▼
       │  SQLite
       │
       ▼
┌────────────────────┐
│    Prometheus      │
│      Port 9090     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│      Grafana       │
│      Port 3001     │
└────────────────────┘
```

All services communicate through the Docker Compose network.

---

# CI/CD

GitHub Actions is used to automate the continuous integration workflow.

The intended CI/CD pipeline is:

```text
Developer Push
      │
      ▼
GitHub Repository
      │
      ▼
GitHub Actions
      │
      ├── Install Dependencies
      │
      ├── Run Automated Tests
      │
      ├── Build Docker Image
      │
      └── Deploy Application
```

The CI pipeline helps ensure that new code changes do not break the application.

---

# Cloud Deployment

The application is designed to support deployment to Google Cloud Run.

The deployment workflow can be:

```text
GitHub
   │
   ▼
GitHub Actions
   │
   ▼
Run Tests
   │
   ▼
Build Docker Image
   │
   ▼
Push Container Image
   │
   ▼
Deploy to Google Cloud Run
```

The production API key and other sensitive configuration values should be provided through secure environment variables or cloud secret management rather than committed to the repository.

---

# Security

The following files and data are excluded from Git version control:

```text
.env
backend/.env
*.db
uploads/
temp_uploads/
.venv/
__pycache__/
```

API keys and secrets must never be committed to the GitHub repository.

For local development, environment variables are loaded from a local `.env` file.

---

# Development Workflow

A typical development workflow is:

```bash
# Start the application
docker compose up -d --build

# Run automated tests
PYTHONPATH=. pytest -v

# Check application status
docker compose ps

# View backend logs
docker compose logs backend

# Stop the application
docker compose down
```

---

# Project Validation

Before submission, verify:

```text
✓ Docker containers start successfully
✓ Backend API is accessible
✓ Frontend is accessible
✓ Invoice upload works
✓ Swagger API works
✓ Prometheus is running
✓ Grafana is running
✓ Dashboard is available
✓ Automated tests pass
✓ API keys are not committed
✓ .env files are ignored
✓ CI/CD configuration is included
```

---

## Capstone Submission

The project repository contains:

* Source code
* Docker configuration
* Automated tests
* Monitoring configuration
* CI/CD configuration
* Project documentation

Sensitive credentials and local development files are intentionally excluded from the repository.

---

## License

This project was developed as a capstone project.
