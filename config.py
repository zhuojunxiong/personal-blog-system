from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = "dev-secret-key-change-before-production"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'instance' / 'personal_blog.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
