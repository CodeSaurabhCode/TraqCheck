from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class Candidate(db.Model):
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), index=True)
    email = db.Column(db.String(200), unique=True, index=True, nullable=True)
    phone = db.Column(db.String(50), unique=True, index=True, nullable=True)
    company = db.Column(db.String(200))
    designation = db.Column(db.String(200))
    skills = db.Column(db.Text)
    resume_filename = db.Column(db.String(500), unique=True)
    resume_path = db.Column(db.String(500))
    extraction_status = db.Column(db.String(50), default='pending')
    confidence_scores = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    documents = db.relationship('Document', backref='candidate', lazy=True, cascade='all, delete-orphan')
    document_requests = db.relationship('DocumentRequest', backref='candidate', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'designation': self.designation,
            'skills': json.loads(self.skills) if self.skills else [],
            'resume_filename': self.resume_filename,
            'extraction_status': self.extraction_status,
            'confidence_scores': json.loads(self.confidence_scores) if self.confidence_scores else {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'documents': [doc.to_dict() for doc in self.documents],
            'document_requests': [req.to_dict() for req in self.document_requests]
        }

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    document_type = db.Column(db.String(50))
    filename = db.Column(db.String(500))
    file_path = db.Column(db.String(500))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'document_type': self.document_type,
            'filename': self.filename,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }

class DocumentRequest(db.Model):
    __tablename__ = 'document_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    request_message = db.Column(db.Text)
    request_type = db.Column(db.String(50), default='email')
    status = db.Column(db.String(50), default='sent')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'request_message': self.request_message,
            'request_type': self.request_type,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
