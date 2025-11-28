# TraqCheck Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│                      (React Frontend)                            │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Dashboard  │  │   Candidate  │  │    Resume    │          │
│  │     Page     │  │   Profile    │  │    Upload    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/REST API
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FLASK BACKEND                               │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Routes                             │  │
│  │  • POST /api/candidates/upload                           │  │
│  │  • GET  /api/candidates                                  │  │
│  │  • GET  /api/candidates/<id>                            │  │
│  │  • POST /api/candidates/<id>/request-documents          │  │
│  │  • POST /api/candidates/<id>/submit-documents           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                      │
│     ┌──────────────────────┼──────────────────────┐             │
│     ▼                      ▼                      ▼             │
│  ┌────────┐          ┌──────────┐          ┌──────────┐        │
│  │ Resume │          │ LangGraph│          │ Document │        │
│  │ Parser │          │  Agent   │          │  Handler │        │
│  └────────┘          └──────────┘          └──────────┘        │
└─────────────────────────────────────────────────────────────────┘
       │                     │                      │
       │                     │                      │
       ▼                     ▼                      ▼
┌──────────┐          ┌──────────┐          ┌──────────┐
│  OpenAI  │          │ LangChain│          │   File   │
│   API    │          │  & LLM   │          │  Storage │
│          │          │          │          │          │
│ GPT-3.5  │          │ Prompts  │          │ Uploads/ │
└──────────┘          └──────────┘          └──────────┘
       │                     │
       └─────────────────────┘
                  │
                  ▼
           ┌─────────────┐
           │  Database   │
           │  SQLAlchemy │
           │             │
           │  - Candidate│
           │  - Document │
           │  - Request  │
           └─────────────┘
```

## Data Flow

### 1. Resume Upload Flow

```
User uploads PDF/DOCX
       │
       ▼
Frontend (ResumeUpload component)
       │
       ▼
POST /api/candidates/upload
       │
       ▼
Flask Backend
       │
       ├─► Save file to uploads/resumes/
       │
       ├─► Create Candidate record (status: processing)
       │
       ▼
Resume Parser
       │
       ├─► Extract text (PyPDF2/python-docx)
       │
       ▼
LLM (GPT-3.5)
       │
       ├─► Parse structured data
       ├─► Generate confidence scores
       │
       ▼
Update Candidate record
       │
       ├─► name, email, phone, company, designation, skills
       ├─► confidence_scores JSON
       ├─► status: completed
       │
       ▼
Return to Frontend
       │
       ▼
Display in Dashboard
```

### 2. Document Request Flow (LangGraph Agent)

```
User clicks "Request Documents"
       │
       ▼
POST /api/candidates/<id>/request-documents
       │
       ▼
LangGraph Agent Initialization
       │
       ▼
┌─────────────────────────────────────┐
│   LangGraph State Machine           │
│                                      │
│   State: AgentState {                │
│     candidate_name: str              │
│     candidate_email: str             │
│     candidate_phone: str             │
│     request_message: str             │
│     request_type: str                │
│     messages: List[str]              │
│   }                                  │
└─────────────────────────────────────┘
       │
       ▼
Node 1: analyze_candidate
       │
       ├─► Check email availability
       ├─► Check phone availability
       ├─► Decide request type (email/sms)
       │
       ▼
Conditional Edge (Router)
       │
       ├─── email available? ──► Node 2a: generate_email_request
       │                                    │
       │                                    ├─► LLM generates personalized email
       │                                    ├─► Subject line + body
       │                                    └─► Update state.request_message
       │
       └─── phone only? ──────► Node 2b: generate_sms_request
                                           │
                                           ├─► LLM generates SMS (< 160 chars)
                                           └─► Update state.request_message
       │
       ▼
End State (return result)
       │
       ▼
Create DocumentRequest record
       │
       ▼
Return to Frontend
       │
       └─► Display generated message
       └─► Show agent logs
```

### 3. Document Upload Flow

```
User selects PAN/Aadhaar files
       │
       ▼
POST /api/candidates/<id>/submit-documents
       │
       ▼
Flask Backend
       │
       ├─► Validate file types (pdf, jpg, png)
       │
       ├─► Save to uploads/documents/
       │   ├─► PAN_{candidate_id}_{timestamp}_{filename}
       │   └─► AADHAAR_{candidate_id}_{timestamp}_{filename}
       │
       ├─► Create Document records
       │
       ▼
Return to Frontend
       │
       ▼
Display submitted documents
```

## Component Details

### Backend Components

#### 1. Resume Parser (`app/resume_parser.py`)

```python
class ResumeParser:
    - extract_text_from_pdf()
    - extract_text_from_docx()
    - parse_resume_with_llm()
    - parse_resume()  # Main entry point
```

**Features:**
- Supports PDF and DOCX formats
- Uses LLM for intelligent extraction
- Returns structured data + confidence scores

#### 2. LangGraph Agent (`app/agent.py`)

```python
class DocumentRequestAgent:
    - analyze_candidate()      # Node
    - generate_email_request() # Node
    - generate_sms_request()   # Node
    - route_request_type()     # Router
    - request_documents()      # Entry point
```

**Features:**
- State-based workflow
- Conditional routing
- Personalized message generation
- Logging and traceability

#### 3. Database Models (`app/models.py`)

```python
Candidate:
    - id, name, email, phone, company, designation
    - skills (JSON), confidence_scores (JSON)
    - extraction_status, resume_path
    - relationships: documents, document_requests

Document:
    - id, candidate_id, document_type
    - filename, file_path, uploaded_at

DocumentRequest:
    - id, candidate_id, request_message
    - request_type, status, created_at
```

### Frontend Components

#### 1. Dashboard (`pages/Dashboard.js`)
- Upload section with ResumeUpload component
- Candidate list with CandidateTable component
- Real-time updates

#### 2. Candidate Profile (`pages/CandidateProfile.js`)
- Detailed candidate information
- Confidence scores visualization
- Document request interface
- Document upload interface

#### 3. Resume Upload (`components/ResumeUpload.js`)
- Drag-and-drop interface
- Upload progress tracking
- Error handling

#### 4. Candidate Table (`components/CandidateTable.js`)
- Sortable, clickable rows
- Status badges
- Document count

## Technology Stack Details

### Backend
```
Flask 3.0.0          - Web framework
SQLAlchemy 3.1.1     - ORM
LangGraph 0.0.20     - Agent framework
LangChain 0.1.0      - LLM integration
OpenAI 1.6.1         - GPT API client
PyPDF2 3.0.1         - PDF parsing
python-docx 1.1.0    - DOCX parsing
Flask-CORS 4.0.0     - CORS handling
```

### Frontend
```
React 18.2.0         - UI framework
React Router 6.20.0  - Routing
Axios 1.6.2          - HTTP client
react-dropzone 14.2.3 - File upload
```

## Security Considerations

1. **API Keys**: Stored in .env, never committed
2. **File Uploads**: 
   - Type validation (extensions)
   - Size limits (16MB)
   - Secure filename handling
3. **CORS**: Configured for frontend origin
4. **SQL Injection**: Protected by SQLAlchemy ORM
5. **File Paths**: Secure with werkzeug.secure_filename()

## Scalability Considerations

### Current (MVP)
- SQLite database
- Local file storage
- Synchronous processing

### Production Recommendations
- PostgreSQL for database
- S3/Cloudinary for file storage
- Celery for async processing
- Redis for caching
- Rate limiting on API
- Authentication & authorization

## Deployment Architecture

```
┌─────────────────────────────────────┐
│         Static Site Host             │
│         (Vercel/Render)              │
│                                      │
│    React App (built/bundled)        │
└─────────────────────────────────────┘
              │
              │ API Calls
              ▼
┌─────────────────────────────────────┐
│         Web Service Host             │
│         (Render/Railway)             │
│                                      │
│    Flask Backend + Gunicorn         │
└─────────────────────────────────────┘
              │
              ├─────► PostgreSQL Database
              │
              ├─────► OpenAI API
              │
              └─────► File Storage (S3/local)
```

## Performance Metrics

- **Resume Upload**: ~2-5 seconds (depends on LLM)
- **Document Request**: ~3-7 seconds (LLM generation)
- **Document Upload**: <1 second
- **Dashboard Load**: <500ms

## Error Handling

1. **Resume Parsing Errors**: Caught and logged, status set to 'failed'
2. **LLM Errors**: Fallback to basic extraction, retry logic
3. **File Upload Errors**: Validated before processing
4. **Network Errors**: Frontend displays user-friendly messages

## Monitoring & Logging

- Flask development logs (stdout)
- Agent execution logs (returned to frontend)
- Database transaction logs
- Frontend console logs (development)

## Future Enhancements

1. **Email/SMS Integration**: Actually send requests (SendGrid, Twilio)
2. **Document Verification**: OCR to verify PAN/Aadhaar authenticity
3. **Bulk Upload**: Process multiple resumes at once
4. **Advanced Search**: Filter candidates by skills, company, etc.
5. **Analytics Dashboard**: Metrics on parsing accuracy, document collection rate
6. **Multi-language Support**: Parse resumes in multiple languages
7. **Background Jobs**: Async processing with Celery
8. **Real-time Updates**: WebSocket for live status updates
