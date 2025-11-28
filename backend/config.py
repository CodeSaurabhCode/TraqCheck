import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database - Support both SQLite (dev) and PostgreSQL (production)
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///candidates.db'
    
    # Fix postgres:// to postgresql:// for SQLAlchemy (Heroku/Railway compatibility)
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File uploads - Use /tmp for serverless environments
    IS_SERVERLESS = os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME')
    UPLOAD_FOLDER = '/tmp/uploads' if IS_SERVERLESS else (os.environ.get('UPLOAD_FOLDER') or 'uploads')
    RESUMES_FOLDER = os.path.join(UPLOAD_FOLDER, 'resumes')
    DOCUMENTS_FOLDER = os.path.join(UPLOAD_FOLDER, 'documents')
    
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH') or 10 * 1024 * 1024)  # 10MB default
    ALLOWED_RESUME_EXTENSIONS = {'pdf', 'docx', 'txt'}
    ALLOWED_DOCUMENT_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
