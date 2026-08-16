import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fuzzyhash-analyzer-soc-secret-key-2026-prod'
    
    # Database
    DB_DIR = os.path.join(BASE_DIR, 'database')
    os.makedirs(DB_DIR, exist_ok=True)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(DB_DIR, 'fuzzyhash.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Uploads & Storage
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    REPORT_FOLDER = os.path.join(BASE_DIR, 'reports', 'generated')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(REPORT_FOLDER, exist_ok=True)
    
    # File Validation Limits
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB default
    ALLOWED_EXTENSIONS = {
        'txt', 'log', 'bin', 'dat', 'dll', 'exe', 'sys', 'elf',
        'pdf', 'doc', 'docx', 'py', 'js', 'html', 'css', 'json',
        'xml', 'zip', 'tar', 'gz', 'png', 'jpg', 'jpeg', 'c', 'cpp'
    }
    
    # Session Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
