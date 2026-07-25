from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///ledgerlens.db")
    CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.75"))
    MODERATION_REVIEW_THRESHOLD = float(os.getenv("MODERATION_REVIEW_THRESHOLD", "0.30"))
    MODERATION_BLOCK_THRESHOLD = float(os.getenv("MODERATION_BLOCK_THRESHOLD", "0.70"))
    API_URL = os.getenv("API_URL", "http://localhost:8000")
    APP_NAME = os.getenv("APP_NAME", "LedgerLens")
    GPT4O_INPUT_COST_PER_1K = float(os.getenv("GPT4O_INPUT_COST_PER_1K", "0.005"))
    GPT4O_OUTPUT_COST_PER_1K = float(os.getenv("GPT4O_OUTPUT_COST_PER_1K", "0.015"))


settings = Settings()
