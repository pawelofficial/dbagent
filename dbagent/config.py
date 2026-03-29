import os


LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4")
LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")

DB_PATH: str = os.getenv("DB_PATH", "database.db")

MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY_SECONDS: float = float(os.getenv("RETRY_DELAY_SECONDS", "1.0"))

ALLOWED_QUERY_TYPES: list[str] = ["SELECT", "PRAGMA", "EXPLAIN"]
MAX_RESULT_ROWS: int = int(os.getenv("MAX_RESULT_ROWS", "500"))

HOST: str = os.getenv("HOST", "127.0.0.1")
PORT: int = int(os.getenv("PORT", "8000"))
