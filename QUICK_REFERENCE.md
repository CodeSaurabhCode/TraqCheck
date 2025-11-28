# Quick Reference Guide

## Edge Case Handling Quick Reference

### Common Upload Errors and Solutions

#### ❌ Error: "File too large. Maximum size is 10 MB"
**Cause**: Resume file exceeds 10 MB size limit  
**Solution**: Compress PDF or reduce image quality before uploading

#### ❌ Error: "Resume file is empty"
**Cause**: Uploaded file has 0 bytes  
**Solution**: Check file is not corrupted; try re-saving and uploading again

#### ❌ Error: "Invalid file format. Only PDF and DOCX allowed"
**Cause**: File extension not in allowed list  
**Solution**: Convert resume to PDF or DOCX format before uploading

#### ❌ Error: "Resume text is too short (less than 50 characters)"
**Cause**: File contains insufficient text content  
**Solution**: Ensure resume has actual content; may be an image-based PDF requiring OCR

#### ❌ Error: "PDF file contains no extractable text (might be image-based)"
**Cause**: PDF is scanned or image-based without OCR layer  
**Solution**: Use OCR software to convert to searchable PDF, or retype content

#### ❌ Error: "Could not extract any identifying information from resume"
**Cause**: Resume parser couldn't find name, email, or phone number  
**Solution**: Ensure resume clearly lists contact information (name, email, or phone)

#### ⚠️ Status: 409 Conflict - "Candidate with this email already exists"
**Cause**: Another resume with same email already uploaded  
**Solution**: 
- This is expected behavior preventing duplicates
- Use existing candidate record instead
- Response includes existing candidate ID for reference

#### ⚠️ Status: 409 Conflict - "Candidate with this phone number already exists"
**Cause**: Another resume with same phone number already uploaded  
**Solution**: Similar to email conflict; use existing record

---

## Testing Commands

### Run Edge Case Tests
```bash
cd backend
python test_edge_cases.py
```

**What it tests**:
- ✅ Duplicate upload rejection
- ✅ Empty file rejection
- ✅ Invalid content rejection
- ✅ Missing identifying data rejection
- ✅ File size limit enforcement
- ✅ Complete successful workflow

### Database Management
```bash
cd backend
python db_manager.py
```

**Available operations**:
1. Show Statistics - View total candidates, extraction statuses, document counts
2. Show Recent Candidates - Display last N candidates with details
3. Check for Duplicates - Find duplicate email/phone records
4. Cleanup Orphaned Files - Remove files without database records
5. Cleanup Failed Extractions - Delete candidates with failed parsing
6. Reset Database - Complete wipe (requires double confirmation)

---

## API Endpoints Reference

### Upload Resume
```http
POST /api/candidates/upload
Content-Type: multipart/form-data

resume: <file>
```

**Success Response** (201):
```json
{
  "id": 1,
  "message": "Resume uploaded and parsed successfully",
  "candidate": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "extraction_status": "completed"
  }
}
```

**Error Responses**:
- 400: Validation error (see error messages above)
- 409: Duplicate candidate (email or phone exists)
- 500: Server error

### Get Candidates
```http
GET /api/candidates
```

### Get Single Candidate
```http
GET /api/candidates/<id>
```

### Request Documents
```http
POST /api/candidates/<id>/request-documents
```

**Validations**:
- Candidate must have valid email OR phone
- Extraction status must be 'completed' (not 'failed')
- Candidate must have at least basic info (name/email/phone)

### Submit Documents
```http
POST /api/candidates/<id>/submit-documents
Content-Type: multipart/form-data

pan_card: <file>
aadhar_card: <file>
```

**Validations**:
- Files cannot be empty (size > 0)
- Files cannot exceed 10 MB
- Replaces existing documents (no duplicates)

### Delete Candidate
```http
DELETE /api/candidates/<id>
```

**What it does**:
- Deletes candidate record
- Deletes associated documents
- Deletes uploaded resume file
- Deletes document request records

---

## Database Schema

### Candidate Table
```sql
id              INTEGER PRIMARY KEY AUTOINCREMENT
name            VARCHAR(255) INDEXED
email           VARCHAR(255) UNIQUE INDEXED NULLABLE
phone           VARCHAR(20) UNIQUE INDEXED NULLABLE
company         VARCHAR(255)
designation     VARCHAR(255)
skills          TEXT (JSON array)
resume_filename VARCHAR(255) UNIQUE
extraction_status VARCHAR(20) DEFAULT 'pending'
confidence_score FLOAT
created_at      DATETIME INDEXED
updated_at      DATETIME
```

**Constraints**:
- `email` must be unique (no duplicates)
- `phone` must be unique (no duplicates)
- `resume_filename` must be unique
- At least one of name/email/phone required

### Document Table
```sql
id              INTEGER PRIMARY KEY AUTOINCREMENT
candidate_id    INTEGER FOREIGN KEY
document_type   VARCHAR(50) (PAN/Aadhaar)
filename        VARCHAR(255)
uploaded_at     DATETIME
```

### DocumentRequest Table
```sql
id              INTEGER PRIMARY KEY AUTOINCREMENT
candidate_id    INTEGER FOREIGN KEY
email_content   TEXT
sms_content     TEXT
request_status  VARCHAR(20) DEFAULT 'sent'
created_at      DATETIME
```

---

## File Storage

### Resume Files
**Location**: `backend/uploads/resumes/`  
**Naming**: `resume_<timestamp>_<secure_filename>`  
**Cleanup**: Deleted when candidate deleted or upload fails

### Submitted Documents
**Location**: `backend/uploads/documents/`  
**Naming**: `<document_type>_<timestamp>_<secure_filename>`  
**Cleanup**: Deleted when candidate deleted

---

## Validation Rules Summary

### File Upload
- ✅ Maximum size: 10 MB
- ✅ Allowed types: PDF, DOCX, TXT
- ✅ File must not be empty (size > 0)
- ✅ Unique filename per candidate

### Text Extraction
- ✅ Minimum 50 characters extracted
- ✅ Must handle PDFs with/without text layer
- ✅ Must handle DOCX with paragraphs and tables
- ✅ Proper error handling for corrupted files

### Data Extraction
- ✅ At least ONE of: name, email, or phone required
- ✅ Email must be unique across all candidates
- ✅ Phone must be unique across all candidates
- ✅ Skills stored as JSON array
- ✅ Confidence scores tracked per field

### Document Requests
- ✅ Candidate must have email OR phone
- ✅ Extraction status must be 'completed'
- ✅ Cannot request from failed extractions

### Document Submission
- ✅ Files cannot be empty
- ✅ Maximum 10 MB per file
- ✅ Replaces existing documents (no duplicates)
- ✅ Atomic operations (rollback on error)

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'X'"
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

### Server Won't Start
1. Check virtual environment is activated
2. Verify all packages installed
3. Check port 5000 is not in use
4. Verify OPENAI_API_KEY in .env file

### Test Script Fails
1. Ensure server is running first: `python app.py`
2. Check server is on port 5000
3. Verify database file exists: `candidates.db`

### Database Issues
Use `db_manager.py`:
```bash
python db_manager.py
# Choose option 1 to see statistics
# Choose option 3 to check for duplicates
```

### Duplicate Detection Not Working
- Check database constraints: `unique=True` on email, phone fields
- Verify indexes exist (run db_manager.py)
- Check application logs for constraint errors

### Files Not Being Deleted
- Run `db_manager.py` → Option 4 (Cleanup Orphaned Files)
- Check folder permissions
- Verify file paths in database match actual files

---

## Production Checklist

Before deploying to production:

- [ ] Set strong SECRET_KEY in environment
- [ ] Use production database (PostgreSQL recommended)
- [ ] Set DEBUG=False
- [ ] Enable HTTPS
- [ ] Set proper CORS origins
- [ ] Configure file upload limits in web server
- [ ] Set up automated backups
- [ ] Configure logging
- [ ] Set up monitoring/alerting
- [ ] Review and test all edge cases
- [ ] Load test with concurrent uploads
- [ ] Set up rate limiting

---

## Performance Tips

### For Large Volume
1. **Use background jobs**: Move parsing to Celery/RQ queue
2. **Add caching**: Cache frequently accessed candidates
3. **Database optimization**: Add more indexes based on query patterns
4. **File storage**: Move to S3/cloud storage for scalability
5. **Connection pooling**: Configure SQLAlchemy pool size

### Monitoring Metrics
- Upload success/failure rate
- Average parsing time
- Failed extraction percentage
- Duplicate rejection rate
- API response times
- Database query performance

---

## Support

### Getting Help
1. Check error message for specific issue
2. Review this quick reference guide
3. Check `EDGE_CASES.md` for detailed explanations
4. Review `IMPLEMENTATION_SUMMARY.md` for technical details
5. Run `db_manager.py` to inspect database state

### Reporting Issues
Include:
- Error message (exact text)
- File type and size being uploaded
- Extraction status from database
- Backend logs from terminal
- Steps to reproduce

---

## Version Information

**Last Updated**: December 2024  
**Backend**: Flask 3.0.0, SQLAlchemy 3.1.1  
**AI**: LangGraph 1.0.4, LangChain 1.1.0, OpenAI GPT-3.5-turbo  
**Database**: SQLite (development), PostgreSQL (production ready)
