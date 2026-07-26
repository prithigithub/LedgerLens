# LedgerLens

## AI-Powered Invoice Processing and Human Review Platform

LedgerLens is an AI-powered invoice processing platform that extracts structured information from invoice images, validates the extracted data, assigns confidence scores, detects personally identifiable information (PII), and routes low-confidence invoices for human review.

The application is designed as an end-to-end production-style system using:

* FastAPI
* Streamlit
* OpenAI Vision
* Pydantic
* SQLAlchemy
* SQLite
* Docker
* Docker Compose
* Prometheus
* Grafana
* Pytest
* GitHub Actions
* Linux VPS deployment
* CloudPanel
* Nginx reverse proxy
* Let's Encrypt HTTPS

The application is deployed on a production VPS and is accessible through secure HTTPS domains.

---

## Live Deployment

### Frontend

```text
https://ledgerlens.prithibhandari.co.in
```

The Streamlit frontend provides the user interface for:

* Home
* Dashboard
* History
* Human Review
* Invoice Upload

---

### Backend API

```text
https://api.prithibhandari.co.in
```

The FastAPI backend provides the invoice processing API.

---

### Swagger API Documentation

```text
https://api.prithibhandari.co.in/docs
```

The Swagger interface allows API endpoints to be tested interactively.

---

### Monitoring

Prometheus:

```text
https://prometheus.prithibhandari.co.in
```

Grafana:

```text
https://grafana.prithibhandari.co.in
```

The monitoring services are deployed using Docker and exposed securely through CloudPanel reverse proxies and HTTPS.

---

# Project Objectives

LedgerLens is designed to:

* Accept invoice images in JPG, JPEG, and PNG formats.
* Moderate uploaded invoice images before processing.
* Detect whether uploaded images contain invoices.
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
* Run automated tests through CI.
* Build and validate Docker containers through GitHub Actions.
* Deploy the application on a production VPS using Docker Compose.
* Provide secure HTTPS access through CloudPanel and Let's Encrypt.

---

# System Workflow

```text
                    Invoice Image
                         │
                         ▼
                 Streamlit Upload
                         │
                         ▼
                  FastAPI Backend
                         │
                         ▼
                  Image Moderation
                         │
                         ▼
                  Invoice Detection
                         │
                         ▼
                AI Invoice Extraction
                         │
                         ▼
                  Pydantic Validation
                         │
                         ▼
               Confidence Evaluation
                         │
                 ┌───────┴────────┐
                 │                │
                 ▼                ▼
          High Confidence    Low Confidence
                 │                │
                 ▼                ▼
        Automatic Approval   Human Review Queue
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
                                  │
                                  ▼
                              Monitoring
                         Prometheus + Grafana
```

---

# Key Features

## 1. Invoice Upload

The system accepts invoice images through the Streamlit frontend and FastAPI API.

Supported formats:

* JPG
* JPEG
* PNG

Invoices can be uploaded through the web application or tested through the FastAPI Swagger documentation.

---

## 2. Image Moderation

Uploaded images are checked before invoice processing.

The moderation process helps identify inappropriate or unsupported content before it enters the invoice processing workflow.

Images may be:

* Approved for processing
* Sent for moderation review
* Blocked based on moderation results

---

## 3. Invoice Detection

The system verifies whether an uploaded image is likely to contain an invoice.

This helps prevent unrelated images from being processed as invoices.

---

## 4. AI-Powered Invoice Extraction

LedgerLens uses AI vision capabilities to extract structured information from invoice images.

The invoice schema includes:

* Vendor
* Invoice number
* Invoice date
* Currency
* Subtotal
* Tax
* Total
* Line items
* Overall confidence

Example line-item information includes:

* Description
* Quantity
* Unit price
* Amount
* Confidence score

---

## 5. Structured Data Validation

Extracted data is validated using Pydantic models.

Invoice fields contain structured values and confidence scores.

Example:

```text
Field
├── value
└── confidence
```

This ensures that extracted invoice information follows the expected application schema before being stored or processed.

---

## 6. Confidence-Based Processing

Each extracted invoice field receives a confidence score.

The system evaluates the overall confidence of the invoice.

```text
High Confidence
      │
      ▼
Automatic Approval
```

```text
Low Confidence
      │
      ▼
Human Review Required
```

This prevents uncertain AI-generated data from being automatically approved without human verification.

---

## 7. Human Review Workflow

Low-confidence invoices are routed to a review queue.

A reviewer can:

* View extracted invoice data.
* Review confidence scores.
* Identify missing or uncertain fields.
* Correct incorrect information.
* Approve the invoice after verification.

This provides human oversight for uncertain AI results.

---

## 8. PII Detection and Redaction

The application detects sensitive information such as:

* Email addresses
* Phone numbers
* Social Security numbers

Sensitive information is redacted before being written to logs.

This helps reduce the risk of accidentally exposing private information through application logs.

---

## 9. Invoice Watermarking

Processed invoice images can be watermarked using the Python Imaging Library (PIL).

Watermarking helps identify processed documents and provides an additional processing record.

---

## 10. Database Storage

Invoice processing results and document metadata are stored using SQLAlchemy.

The application currently uses SQLite for database storage.

Stored information includes data such as:

* Document filename
* Processing status
* Confidence score
* Extracted invoice data
* Reviewed invoice data
* Watermarked file path
* Creation timestamp

---

# Technology Stack

## Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* SQLite

## AI

* OpenAI Vision API

## Frontend

* Streamlit

## Image Processing

* Pillow

## Testing

* Pytest
* FastAPI TestClient
* HTTPX

## Containerization

* Docker
* Docker Compose

## Monitoring

* Prometheus
* Grafana
* Prometheus Client

## CI/CD

* GitHub Actions

## Production Infrastructure

* Linux VPS
* CloudPanel
* Nginx Reverse Proxy
* Let's Encrypt SSL/TLS

---

# Project Structure

```text
LedgerLens/
│
├── backend/
│   ├── main.py
│   ├── config.py
│   │
│   ├── api/
│   │   ├── ingest.py
│   │   ├── review.py
│   │   ├── approve.py
│   │   ├── documents.py
│   │   └── metrics.py
│   │
│   ├── database/
│   ├── models/
│   ├── schemas/
│   └── services/
│
├── frontend/
│   ├── home.py
│   ├── config.py
│   ├── requirements.txt
│   │
│   └── pages/
│       ├── dashboard.py
│       ├── history.py
│       ├── review.py
│       └── upload.py
│
├── monitoring/
│   ├── prometheus.yml
│   │
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
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── requirements.txt
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

Create a local `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///ledgerlens.db
CONFIDENCE_THRESHOLD=0.75
MODERATION_REVIEW_THRESHOLD=0.30
MODERATION_BLOCK_THRESHOLD=0.70
API_URL=http://127.0.0.1:8000
APP_NAME=LedgerLens
```

Never commit the real `.env` file or API key to GitHub.

The `.gitignore` file excludes sensitive files such as:

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

Check running containers:

```bash
docker compose ps
```

Stop the services:

```bash
docker compose down
```

View backend logs:

```bash
docker compose logs backend
```

View frontend logs:

```bash
docker compose logs frontend
```

---

# Local Application Services

## Streamlit Frontend

```text
http://localhost:8501
```

## FastAPI API

```text
http://localhost:8000
```

## FastAPI Swagger Documentation

```text
http://localhost:8000/docs
```

## Prometheus

```text
http://localhost:9090
```

## Grafana

```text
http://localhost:3001
```

The exact ports can be changed in `docker-compose.yml`.

---

# Production Deployment Architecture

The production application is deployed on a Linux VPS using Docker Compose.

```text
                         Internet
                            │
                            ▼
              ┌─────────────────────────┐
              │       CloudPanel         │
              │   Nginx Reverse Proxy    │
              │     Let's Encrypt SSL    │
              └────────────┬────────────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
      ledgerlens.       api.         grafana.
      prithibhandari    prithibhandari  prithibhandari
      .co.in            .co.in          .co.in
             │             │             │
             ▼             ▼             ▼
        Port 8501      Port 8000      Port 3001
             │             │             │
             ▼             ▼             ▼
        Streamlit      FastAPI       Grafana
```

Prometheus is also deployed as part of the Docker Compose monitoring stack.

---

# Production URLs

## Frontend

```text
https://ledgerlens.prithibhandari.co.in
```

## Backend API

```text
https://api.prithibhandari.co.in
```

## Swagger UI

```text
https://api.prithibhandari.co.in/docs
```

## Prometheus

```text
https://prometheus.prithibhandari.co.in
```

## Grafana

```text
https://grafana.prithibhandari.co.in
```

---

# API Endpoints

The FastAPI backend provides endpoints for the invoice processing workflow.

## Health Check

```text
GET /health
```

Example:

```bash
curl https://api.prithibhandari.co.in/health
```

Expected response:

```json
{
  "status": "running",
  "application": "LedgerLens"
}
```

---

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
Invoice Detection
  ↓
AI Extraction
  ↓
Validation
  ↓
Confidence Evaluation
  ↓
Automatic Approval or Human Review
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

## Documents

```text
GET /documents/
```

Retrieves processed invoice documents and their extracted data.

---

## Metrics

```text
GET /metrics
```

Exposes Prometheus-compatible application metrics.

---

# Testing

The project includes automated tests for core application functionality.

Run the test suite:

```bash
python -m pytest -v
```

Current tests include:

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

The tests validate core application logic without exposing real production API keys or sensitive production data.

---

# Monitoring

LedgerLens uses Prometheus and Grafana for application monitoring.

The monitoring architecture is:

```text
LedgerLens Backend
        │
        ▼
   /metrics
        │
        ▼
   Prometheus
        │
        ▼
     Grafana
```

The application exposes metrics such as:

* Total documents processed
* Human review count
* Processing latency
* Moderation latency
* Extraction latency
* Confidence scores
* Pending review count
* Estimated processing cost

Example Prometheus metric:

```text
ledgerlens_documents_total
```

Prometheus scrapes metrics from the FastAPI backend.

Grafana visualizes the collected metrics through dashboards.

Grafana dashboards and provisioning configuration are stored under:

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
└─────────┬──────────┘
          │
          ▼
       SQLite
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

The frontend communicates with the backend using the configured API URL.

---

# CI/CD

GitHub Actions is used to automate continuous integration and Docker validation.

The current CI workflow:

```text
Developer Push
      │
      ▼
GitHub Repository
      │
      ▼
GitHub Actions
      │
      ├── Checkout Repository
      │
      ├── Set Up Python 3.11
      │
      ├── Install Dependencies
      │
      ├── Run Automated Tests
      │
      ├── Create Temporary CI Environment File
      │
      ├── Validate Docker Compose
      │
      └── Build Docker Images
```

The CI workflow runs on a temporary GitHub Actions runner.

The `.env` file created during CI is only used inside that temporary CI environment and is not created on the production VPS.

The production VPS has its own separate `.env` file.

---

# Environment Separation

The project separates development, CI, and production environments.

```text
Local Development
        │
        ▼
Local .env
        │
        ▼
Local Docker Compose


GitHub Actions
        │
        ▼
Temporary CI Environment
        │
        ▼
Temporary CI Configuration


Production VPS
        │
        ▼
VPS .env
        │
        ▼
Production Docker Compose
```

The production `.env` file is never committed to GitHub.

The `.env` file on the VPS remains separate from the GitHub repository.

When new code is pulled from GitHub, the production `.env` file is not overwritten.

---

# VPS Deployment Workflow

The production application is deployed on a Linux VPS.

The deployment process is:

```text
Developer
    │
    ▼
Git Commit
    │
    ▼
GitHub Repository
    │
    ▼
GitHub Actions
    │
    ├── Run Tests
    │
    └── Build Docker Images
    │
    ▼
VPS
    │
    ▼
git pull origin main
    │
    ▼
docker compose up -d --build
    │
    ▼
Updated Production Application
```

The VPS production environment contains its own:

```text
.env
```

This file contains production configuration and secrets and is intentionally excluded from Git.

---

# CloudPanel and HTTPS

CloudPanel is used to manage the production VPS and reverse proxy configuration.

Each major service is exposed through a separate subdomain.

```text
ledgerlens.prithibhandari.co.in
        │
        ▼
Streamlit Frontend
        │
        ▼
127.0.0.1:8501
```

```text
api.prithibhandari.co.in
        │
        ▼
FastAPI Backend
        │
        ▼
127.0.0.1:8000
```

```text
grafana.prithibhandari.co.in
        │
        ▼
Grafana
        │
        ▼
127.0.0.1:3001
```

HTTPS certificates are provided through Let's Encrypt.

This provides encrypted communication between users and the production application.

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
*.swp
```

API keys and secrets must never be committed to the GitHub repository.

For local development, environment variables are loaded from a local `.env` file.

For production, environment variables are stored in a separate `.env` file on the VPS.

The production `.env` file is not part of the Git repository.

---

# Development Workflow

A typical development workflow is:

```bash
# Start the application
docker compose up -d --build

# Run automated tests
python -m pytest -v

# Check application status
docker compose ps

# View backend logs
docker compose logs backend

# View frontend logs
docker compose logs frontend

# Stop the application
docker compose down
```

---

# Production Maintenance

On the VPS, the application can be updated using:

```bash
cd /home/prithibhandari/ledgerlens
```

Pull the latest code:

```bash
git pull origin main
```

Rebuild and restart the services:

```bash
docker compose up -d --build
```

Check the services:

```bash
docker compose ps
```

Check backend health:

```bash
curl https://api.prithibhandari.co.in/health
```

View backend logs:

```bash
docker compose logs backend
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
✓ Monitoring metrics are collected
✓ Dashboard is available
✓ Human review workflow works
✓ Automated tests pass
✓ API keys are not committed
✓ .env files are ignored
✓ CI workflow runs successfully
✓ Docker images build successfully
✓ Production VPS deployment works
✓ HTTPS is enabled
✓ CloudPanel reverse proxies are configured
```

---

# Capstone Submission

The project repository contains:

* Source code
* FastAPI backend
* Streamlit frontend
* Docker configuration
* Docker Compose configuration
* Automated tests
* Monitoring configuration
* Prometheus configuration
* Grafana configuration
* GitHub Actions CI configuration
* Project documentation

Sensitive credentials and local development files are intentionally excluded from the repository.

The production application is deployed on a Linux VPS and accessed through secure HTTPS domains.

---

## License

This project was developed as a capstone project.
