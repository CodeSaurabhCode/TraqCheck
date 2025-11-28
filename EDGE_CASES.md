# Edge Cases Handled

This document outlines all edge cases and validation mechanisms implemented in the resume parser and document collection system.

## 1. File Upload Validation

### 1.1 File Size Limits
- **Maximum Size**: 10 MB
- **Implementation**: `app.py` - `upload_resume()` endpoint
- **Response**: 400 Bad Request with message "File too large"
- **Rationale**: Prevents memory issues and abuse

### 1.2 Empty Files
- **Detection**: File size = 0 bytes
- **Implementation**: `resume_parser.py` - `parse_resume()`
- **Response**: 400 Bad Request with message "Resume file is empty"
- **Rationale**: Cannot extract meaningful data from empty files

### 1.3 Allowed File Types
- **Supported**: PDF (.pdf), DOCX (.docx), TXT (.txt)
- **Implementation**: `app.py` - file extension validation
- **Response**: 400 Bad Request with message "Only PDF, DOCX, and TXT files allowed"

## 2. Text Extraction Validation

### 2.1 PDF-Specific Issues
- **Empty PDFs**: Detects PDFs with no pages
- **Image-based PDFs**: Detects PDFs with no extractable text
- **Corrupted PDFs**: Catches `PdfReadError` and returns meaningful error
- **Implementation**: `resume_parser.py` - `extract_text_from_pdf()`

### 2.2 DOCX-Specific Issues
- **Empty Documents**: Detects DOCX with no paragraphs
- **Invalid Format**: Catches `PackageNotFoundError` for corrupted DOCX
- **Table Extraction**: Extracts text from tables in addition to paragraphs
- **Implementation**: `resume_parser.py` - `extract_text_from_docx()`

### 2.3 Minimum Content Length
- **Threshold**: 50 characters minimum
- **Implementation**: `resume_parser.py` - `parse_resume()`
- **Response**: 400 Bad Request with message "Resume text is too short"
- **Rationale**: Ensures file contains actual resume content, not just noise

## 3. Data Extraction Validation

### 3.1 Missing Identifying Information
- **Required**: At least ONE of: name, email, or phone
- **Implementation**: `resume_parser.py` - `parse_resume_with_llm()`
- **Response**: 400 Bad Request with message "Could not extract any identifying information"
- **Rationale**: Cannot create useful candidate record without any contact info

### 3.2 LLM Response Validation
- **JSON Parsing**: Validates LLM returns valid JSON
- **Structure Check**: Ensures 'data' and 'confidence_scores' fields exist
- **Null Handling**: Distinguishes between null and string "null"
- **Default Values**: Provides default confidence scores if missing

### 3.3 Data Type Validation
- **Skills Array**: Ensures skills field is always a list, not null or string
- **Confidence Scores**: Validates all scores are between 0.0 and 1.0

## 4. Duplicate Prevention

### 4.1 Duplicate by Email
- **Check**: Email uniqueness constraint in database
- **Implementation**: `models.py` - Candidate model with `unique=True` on email
- **Detection**: `app.py` - Query existing candidates before insert
- **Response**: 409 Conflict with existing candidate details

### 4.2 Duplicate by Phone
- **Check**: Phone uniqueness constraint in database
- **Implementation**: `models.py` - Candidate model with `unique=True` on phone
- **Detection**: `app.py` - Query existing candidates before insert
- **Response**: 409 Conflict with existing candidate details

### 4.3 Duplicate by Filename
- **Check**: Resume filename uniqueness
- **Implementation**: `models.py` - `unique=True` on resume_filename
- **Rationale**: Prevents uploading exact same file twice

## 5. Database Integrity

### 5.1 Primary Key Constraints
- **Implementation**: `autoincrement=True` on Candidate.id
- **Rationale**: Ensures unique, auto-generated IDs

### 5.2 Atomic Operations
- **Parse Before Insert**: Resume is parsed BEFORE creating database record
- **Rollback on Error**: Database changes rolled back if any step fails
- **File Cleanup**: Uploaded file deleted if validation or parsing fails

### 5.3 Indexes for Performance
- **Indexed Fields**: email, phone, name, created_at
- **Implementation**: `models.py` - `index=True` on frequently queried fields

## 6. Document Submission Validation

### 6.1 File Validation
- **Empty Files**: Rejects files with size = 0
- **Size Limits**: Maximum 10 MB per document
- **Multiple Files**: Validates each file in the submission

### 6.2 Duplicate Document Prevention
- **Strategy**: Replace existing documents instead of creating duplicates
- **Implementation**: `app.py` - `submit_documents()` queries existing docs
- **Rationale**: Each candidate should have one PAN and one Aadhaar

### 6.3 Candidate Validation
- **Minimum Info Check**: Ensures candidate has at least name/email/phone
- **Status Check**: Prevents requesting docs from failed extractions
- **Contact Check**: Ensures email OR phone exists before generating requests

## 7. Error Handling Strategy

### 7.1 Informative Error Messages
- All errors include specific reason for failure
- Example: "PDF file contains no extractable text (might be image-based)"
- Helps users understand what went wrong

### 7.2 Proper HTTP Status Codes
- **400 Bad Request**: Validation errors, invalid input
- **409 Conflict**: Duplicate candidates
- **500 Internal Server Error**: Unexpected errors

### 7.3 Resource Cleanup
- Files deleted from uploads folder if processing fails
- Database transactions rolled back on errors
- Prevents orphaned files and incomplete records

## 8. Security Considerations

### 8.1 File Type Restriction
- Only allows specific extensions to prevent executable uploads
- Validates MIME type matches extension

### 8.2 Size Limits
- Prevents denial-of-service via large file uploads
- Protects server disk space

### 8.3 Path Traversal Prevention
- Uses secure filename generation
- Files saved with unique names (timestamp-based)

## 9. Testing

### 9.1 Test Coverage
All edge cases can be tested using `test_edge_cases.py`:

```bash
cd backend
python test_edge_cases.py
```

### 9.2 Test Scenarios
1. ✅ Duplicate upload rejection (409)
2. ✅ Empty file rejection (400)
3. ✅ Insufficient content rejection (400)
4. ✅ No identifying data rejection (400)
5. ✅ Large file rejection (400)
6. ✅ Successful complete workflow (201)

## 10. Monitoring and Logging

### 10.1 Extraction Status
- **Values**: 'pending', 'processing', 'completed', 'failed'
- **Purpose**: Track which candidates had parsing issues
- **Use**: Can retry failed extractions or request manual review

### 10.2 Confidence Scores
- Stored for each extracted field
- Allows filtering low-confidence extractions
- Helps identify candidates needing manual verification

## Future Enhancements

### Potential Additional Validations
1. **Email Format Validation**: Regex to ensure valid email format
2. **Phone Number Normalization**: Convert all phone numbers to standard format
3. **Duplicate Detection by Name**: Fuzzy matching for similar names
4. **Rate Limiting**: Prevent too many uploads from same IP
5. **Virus Scanning**: Scan uploaded files for malware
6. **File Hash Checking**: Detect duplicate content even with different filenames
7. **Resumable Uploads**: Handle large files with chunked upload
8. **Async Processing**: Move parsing to background queue for better performance

### Monitoring Improvements
1. **Metrics**: Track upload success/failure rates
2. **Alerts**: Notify admin of high failure rates
3. **Audit Log**: Record all upload and document submission activities
4. **Performance**: Monitor parsing time and optimize slow operations
