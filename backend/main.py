from dotenv import load_dotenv

# Load environment variables before importing application modules
load_dotenv()

import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.database.database import Base, engine

# Import models before creating database tables
from backend.models.document import Document
from backend.models.review import ReviewQueue

# Import API routers
from backend.api import ingest
from backend.api import documents
from backend.api import review
from backend.api import approval
from backend.api import metrics



# Create required directories


UPLOADS_DIR = "uploads"

os.makedirs(UPLOADS_DIR, exist_ok=True)



# Create database tables


Base.metadata.create_all(bind=engine)



# FastAPI Application


app = FastAPI(
    title="LedgerLens API",
    description="AI Invoice Intelligence Platform",
    version="1.0.0",
)



# Serve uploaded files


app.mount(
    "/uploads",
    StaticFiles(directory=UPLOADS_DIR),
    name="uploads",
)



# Register API Routes


app.include_router(ingest.router)
app.include_router(documents.router)
app.include_router(review.router)
app.include_router(approval.router)
app.include_router(metrics.router)



# Health Check


@app.get("/health")
def health():
    return {
        "status": "running",
        "application": "LedgerLens",
    }



# Root Endpoint


@app.get("/")
def root():
    return {
        "application": "LedgerLens",
        "message": "AI Invoice Processing Platform",
        "docs": "/docs",
    }