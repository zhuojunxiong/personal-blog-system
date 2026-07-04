import secrets
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent

_SECRET_FILE = Path(__file__).parent / "instance" / ".secret_key"
_CSRF_SECRET_FILE = Path(__file__).parent / "instance" / ".csrf_secret_key"


def _get_or_create_secret(env_var, file_path):
    if os.getenv(env_var):
        return os.getenv(env_var)
    if file_path.exists():
        return file_path.read_text().strip()
    key = secrets.token_hex(32)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(key)
    return key


class Config:
    SECRET_KEY = _get_or_create_secret("SECRET_KEY", _SECRET_FILE)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'instance' / 'personal_blog.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AI_API_KEY = os.getenv("AI_API_KEY", "")
    AI_BASE_URL = os.getenv("AI_BASE_URL", "https://api.deepseek.com")
    AI_MODEL = os.getenv("AI_MODEL", "deepseek-chat")
    AI_TIMEOUT = int(os.getenv("AI_TIMEOUT", "30"))
    AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "2000"))
    AI_ENABLED = os.getenv("AI_ENABLED", "1") == "1"
    WTF_CSRF_SECRET_KEY = _get_or_create_secret("WTF_CSRF_SECRET_KEY", _CSRF_SECRET_FILE)
