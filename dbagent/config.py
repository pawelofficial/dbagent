import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

AUTH_USERNAME: str = os.getenv("AUTH_USERNAME", "admin")
AUTH_PASSWORD: str = os.getenv("AUTH_PASSWORD", "admin")
AUTH_SECRET: str = os.getenv("AUTH_SECRET", "change-me-in-production")

LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4")
LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")

DB_PATH: str = os.getenv("DB_PATH", "database.db")
CHAT_DB_PATH: str = os.getenv("CHAT_DB_PATH", "chats.db")

MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY_SECONDS: float = float(os.getenv("RETRY_DELAY_SECONDS", "1.0"))

ALLOWED_QUERY_TYPES: list[str] = ["SELECT", "PRAGMA", "EXPLAIN"]
MAX_RESULT_ROWS: int = int(os.getenv("MAX_RESULT_ROWS", "500"))

HOST: str = os.getenv("HOST", "127.0.0.1")
PORT: int = int(os.getenv("PORT", "8000"))
