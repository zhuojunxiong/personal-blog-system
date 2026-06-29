import secrets
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'instance' / 'personal_blog.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AI_API_KEY = os.getenv("AI_API_KEY", "")
    AI_BASE_URL = os.getenv("AI_BASE_URL", "https://api.deepseek.com")
    AI_MODEL = os.getenv("AI_MODEL", "deepseek-chat")
    AI_TIMEOUT = int(os.getenv("AI_TIMEOUT", "30"))
    AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "2000"))
    AI_ENABLED = os.getenv("AI_ENABLED", "1") == "1"
    WTF_CSRF_SECRET_KEY = os.getenv("WTF_CSRF_SECRET_KEY") or secrets.token_hex(32)
