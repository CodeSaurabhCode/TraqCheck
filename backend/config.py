import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///candidates.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    RESUMES_FOLDER = os.path.join(UPLOAD_FOLDER, 'resumes')
    DOCUMENTS_FOLDER = os.path.join(UPLOAD_FOLDER, 'documents')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH') or 16 * 1024 * 1024)
    ALLOWED_RESUME_EXTENSIONS = {'pdf', 'docx'}
    ALLOWED_DOCUMENT_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
