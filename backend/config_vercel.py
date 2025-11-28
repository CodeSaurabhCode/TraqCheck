import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database - Use PostgreSQL for production/Vercel
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///candidates.db')
    
    # Fix postgres:// to postgresql:// for SQLAlchemy
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # File uploads - Use /tmp for serverless
    IS_SERVERLESS = os.getenv('VERCEL', False)
    UPLOAD_FOLDER = '/tmp/uploads' if IS_SERVERLESS else 'uploads'
    RESUMES_FOLDER = os.path.join(UPLOAD_FOLDER, 'resumes')
    DOCUMENTS_FOLDER = os.path.join(UPLOAD_FOLDER, 'documents')
    
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
    ALLOWED_RESUME_EXTENSIONS = {'pdf', 'docx', 'txt'}
    ALLOWED_DOCUMENT_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
