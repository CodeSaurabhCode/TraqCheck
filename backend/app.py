from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

from config import Config
from models import db, Candidate, Document, DocumentRequest
from resume_parser import ResumeParser
from agent import DocumentRequestAgent

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app)
    db.init_app(app)
    
    os.makedirs(app.config['RESUMES_FOLDER'], exist_ok=True)
    os.makedirs(app.config['DOCUMENTS_FOLDER'], exist_ok=True)
    
    resume_parser = ResumeParser()
    document_agent = DocumentRequestAgent()
    
    def allowed_file(filename, allowed_extensions):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({"status": "ok", "message": "Server is running"}), 200
    
    @app.route('/api/candidates/upload', methods=['POST'])
    def upload_resume():
        """Upload and parse resume with edge case handling"""
        try:
            # Validate file presence
            if 'resume' not in request.files:
                return jsonify({"error": "No resume file provided"}), 400
            
            file = request.files['resume']
            
            # Validate file selection
            if file.filename == '':
                return jsonify({"error": "No file selected"}), 400
            
            # Validate file format
            if not allowed_file(file.filename, app.config['ALLOWED_RESUME_EXTENSIONS']):
                return jsonify({"error": "Invalid file format. Only PDF and DOCX allowed"}), 400
            
            # Validate file size (check if file is empty)
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)  # Reset file pointer
            
            if file_size == 0:
                return jsonify({"error": "Uploaded file is empty"}), 400
            
            if file_size > app.config['MAX_CONTENT_LENGTH']:
                return jsonify({"error": f"File size exceeds maximum allowed size of {app.config['MAX_CONTENT_LENGTH'] / (1024*1024)}MB"}), 400
            
            # Save file temporarily
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')  # Add microseconds for uniqueness
            unique_filename = f"{timestamp}_{filename}"
            file_path = os.path.join(app.config['RESUMES_FOLDER'], unique_filename)
            file.save(file_path)
            
            # Parse resume first before creating database record
            try:
                parsed_data = resume_parser.parse_resume(file_path)
                
                # Validate that at least some data was extracted
                data = parsed_data.get('data', {})
                name = data.get('name')
                email = data.get('email')
                phone = data.get('phone')
                
                # Check if extraction was minimally successful
                if not name and not email and not phone:
                    # Delete the uploaded file
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    return jsonify({
                        "error": "Failed to extract any candidate information from resume. Please ensure the resume contains readable text with at least name, email, or phone number."
                    }), 400
                
                # Check for duplicate candidate based on email or phone
                duplicate = None
                if email:
                    duplicate = Candidate.query.filter_by(email=email).first()
                    if duplicate:
                        # Delete the uploaded file
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        return jsonify({
                            "error": f"A candidate with email '{email}' already exists (ID: {duplicate.id})",
                            "duplicate_candidate_id": duplicate.id
                        }), 409  # 409 Conflict
                
                if not duplicate and phone:
                    duplicate = Candidate.query.filter_by(phone=phone).first()
                    if duplicate:
                        # Delete the uploaded file
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        return jsonify({
                            "error": f"A candidate with phone '{phone}' already exists (ID: {duplicate.id})",
                            "duplicate_candidate_id": duplicate.id
                        }), 409  # 409 Conflict
                
                # Create candidate record with extracted data
                candidate = Candidate(
                    name=name,
                    email=email,
                    phone=phone,
                    company=data.get('company'),
                    designation=data.get('designation'),
                    skills=json.dumps(data.get('skills', [])),
                    confidence_scores=json.dumps(parsed_data.get('confidence_scores', {})),
                    resume_filename=unique_filename,
                    resume_path=file_path,
                    extraction_status='completed'
                )
                
                db.session.add(candidate)
                db.session.commit()
                
                return jsonify({
                    "message": "Resume uploaded and parsed successfully",
                    "candidate": candidate.to_dict()
                }), 201
                
            except ValueError as ve:
                # Delete the uploaded file on parsing error
                if os.path.exists(file_path):
                    os.remove(file_path)
                return jsonify({
                    "error": f"Invalid resume format: {str(ve)}"
                }), 400
                
            except Exception as e:
                # Delete the uploaded file on any error
                if os.path.exists(file_path):
                    os.remove(file_path)
                return jsonify({
                    "error": f"Failed to parse resume: {str(e)}"
                }), 500
                
        except Exception as e:
            return jsonify({"error": f"Server error: {str(e)}"}), 500
    
    @app.route('/api/candidates', methods=['GET'])
    def get_candidates():
        try:
            candidates = Candidate.query.order_by(Candidate.created_at.desc()).all()
            return jsonify({
                "candidates": [c.to_dict() for c in candidates]
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/candidates/<int:id>', methods=['GET'])
    def get_candidate(id):
        try:
            candidate = Candidate.query.get_or_404(id)
            return jsonify(candidate.to_dict()), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 404
    
    @app.route('/api/candidates/<int:id>/request-documents', methods=['POST'])
    def request_documents(id):
        """Generate AI document request with validation"""
        try:
            candidate = Candidate.query.get_or_404(id)
            
            # Validate candidate has minimum required information
            if not candidate.name and not candidate.email and not candidate.phone:
                return jsonify({
                    "error": "Cannot generate document request. Candidate has insufficient information."
                }), 400
            
            # Validate candidate is not in failed state
            if candidate.extraction_status == 'failed':
                return jsonify({
                    "error": "Cannot generate document request for candidate with failed extraction status."
                }), 400
            
            # Check if contact information exists
            if not candidate.email and not candidate.phone:
                return jsonify({
                    "error": "Cannot generate document request. Candidate has no email or phone number."
                }), 400
            
            candidate_data = {
                "name": candidate.name or "Candidate",
                "email": candidate.email,
                "phone": candidate.phone,
                "company": candidate.company,
                "designation": candidate.designation
            }
            
            result = document_agent.request_documents(candidate_data)
            
            doc_request = DocumentRequest(
                candidate_id=candidate.id,
                request_message=result['request_message'],
                request_type=result['request_type'],
                status='sent'
            )
            db.session.add(doc_request)
            db.session.commit()
            
            return jsonify({
                "message": "Document request generated successfully",
                "request": doc_request.to_dict(),
                "agent_logs": result.get('messages', [])
            }), 201
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/candidates/<int:id>/submit-documents', methods=['POST'])
    def submit_documents(id):
        """Submit candidate documents with validation"""
        try:
            candidate = Candidate.query.get_or_404(id)
            
            # Validate that files are provided
            if 'pan' not in request.files and 'aadhaar' not in request.files:
                return jsonify({"error": "No documents provided. Please upload PAN or Aadhaar."}), 400
            
            uploaded_docs = []
            
            # Handle PAN document
            if 'pan' in request.files:
                pan_file = request.files['pan']
                if pan_file.filename != '':
                    if not allowed_file(pan_file.filename, app.config['ALLOWED_DOCUMENT_EXTENSIONS']):
                        return jsonify({"error": "Invalid PAN file format. Only PDF, JPG, JPEG, PNG allowed"}), 400
                    
                    # Check file size
                    pan_file.seek(0, os.SEEK_END)
                    file_size = pan_file.tell()
                    pan_file.seek(0)
                    
                    if file_size == 0:
                        return jsonify({"error": "PAN file is empty"}), 400
                    
                    if file_size > app.config['MAX_CONTENT_LENGTH']:
                        return jsonify({"error": f"PAN file size exceeds maximum allowed"}), 400
                    
                    # Check if PAN already exists for this candidate
                    existing_pan = Document.query.filter_by(
                        candidate_id=id, 
                        document_type='pan'
                    ).first()
                    
                    if existing_pan:
                        # Delete old PAN file
                        if os.path.exists(existing_pan.file_path):
                            os.remove(existing_pan.file_path)
                        # Delete old record
                        db.session.delete(existing_pan)
                    
                    filename = secure_filename(pan_file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    unique_filename = f"PAN_{id}_{timestamp}_{filename}"
                    file_path = os.path.join(app.config['DOCUMENTS_FOLDER'], unique_filename)
                    pan_file.save(file_path)
                    
                    doc = Document(
                        candidate_id=id,
                        document_type='pan',
                        filename=unique_filename,
                        file_path=file_path
                    )
                    db.session.add(doc)
                    uploaded_docs.append('PAN')
            
            # Handle Aadhaar document
            if 'aadhaar' in request.files:
                aadhaar_file = request.files['aadhaar']
                if aadhaar_file.filename != '':
                    if not allowed_file(aadhaar_file.filename, app.config['ALLOWED_DOCUMENT_EXTENSIONS']):
                        return jsonify({"error": "Invalid Aadhaar file format. Only PDF, JPG, JPEG, PNG allowed"}), 400
                    
                    # Check file size
                    aadhaar_file.seek(0, os.SEEK_END)
                    file_size = aadhaar_file.tell()
                    aadhaar_file.seek(0)
                    
                    if file_size == 0:
                        return jsonify({"error": "Aadhaar file is empty"}), 400
                    
                    if file_size > app.config['MAX_CONTENT_LENGTH']:
                        return jsonify({"error": f"Aadhaar file size exceeds maximum allowed"}), 400
                    
                    # Check if Aadhaar already exists for this candidate
                    existing_aadhaar = Document.query.filter_by(
                        candidate_id=id, 
                        document_type='aadhaar'
                    ).first()
                    
                    if existing_aadhaar:
                        # Delete old Aadhaar file
                        if os.path.exists(existing_aadhaar.file_path):
                            os.remove(existing_aadhaar.file_path)
                        # Delete old record
                        db.session.delete(existing_aadhaar)
                    
                    filename = secure_filename(aadhaar_file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    unique_filename = f"AADHAAR_{id}_{timestamp}_{filename}"
                    file_path = os.path.join(app.config['DOCUMENTS_FOLDER'], unique_filename)
                    aadhaar_file.save(file_path)

                    doc = Document(
                        candidate_id=id,
                        document_type='aadhaar',
                        filename=unique_filename,
                        file_path=file_path
                    )
                    db.session.add(doc)
                    uploaded_docs.append('Aadhaar')
            
            if not uploaded_docs:
                return jsonify({"error": "No valid documents provided"}), 400
            
            db.session.commit()
            
            return jsonify({
                "message": f"Documents uploaded successfully: {', '.join(uploaded_docs)}",
                "candidate": candidate.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Failed to upload documents: {str(e)}"}), 500
    
    @app.route('/api/documents/<path:filename>', methods=['GET'])
    def get_document(filename):
        try:
            return send_from_directory(app.config['DOCUMENTS_FOLDER'], filename)
        except Exception as e:
            return jsonify({"error": str(e)}), 404
    
    @app.route('/api/candidates/<int:id>', methods=['DELETE'])
    def delete_candidate(id):
        """Delete a candidate and associated files"""
        try:
            candidate = Candidate.query.get_or_404(id)
            
            # Delete resume file
            if candidate.resume_path and os.path.exists(candidate.resume_path):
                os.remove(candidate.resume_path)
            
            # Delete document files
            for document in candidate.documents:
                if document.file_path and os.path.exists(document.file_path):
                    os.remove(document.file_path)
            
            # Delete database record (cascade will delete related records)
            db.session.delete(candidate)
            db.session.commit()
            
            return jsonify({
                "message": f"Candidate {id} deleted successfully"
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Failed to delete candidate: {str(e)}"}), 500

    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
