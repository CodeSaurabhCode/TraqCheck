# TraqCheck - Resume Parser & Document Collection System

A full-stack AI-powered system that parses resumes, extracts candidate information using LLMs, and uses a LangGraph agent to autonomously generate personalized document requests.

## 📚 Documentation

- **[Quick Reference Guide](QUICK_REFERENCE.md)** - Common errors, API reference, troubleshooting
- **[Edge Cases Documentation](EDGE_CASES.md)** - Detailed validation and edge case handling
- **[Implementation Summary](IMPLEMENTATION_SUMMARY.md)** - Complete list of improvements and fixes
- **[Quickstart Guide](QUICKSTART.md)** - Get started in 5 minutes
- **[Deployment Guide](DEPLOYMENT.md)** - Production deployment instructions

## 🎯 Features

- **Resume Upload & Parsing**: Drag-and-drop interface for PDF/DOCX resumes with AI-powered extraction
- **Robust Validation**: Comprehensive edge case handling with duplicate prevention
- **Candidate Dashboard**: View all candidates with extraction status and document collection progress
- **AI Agent Integration**: LangGraph-powered agent generates personalized PAN/Aadhaar document requests
- **Document Management**: Upload and track identity documents (PAN & Aadhaar)
- **Confidence Scores**: View extraction confidence for each field
- **RESTful API**: Complete backend API for all operations
- **Data Integrity**: Unique constraints, proper validation, atomic operations

## 🏗️ Architecture

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **AI/ML**: 
  - OpenAI GPT-3.5-turbo for resume parsing
  - LangGraph for agent orchestration
  - LangChain for LLM integration
- **Resume Parsing**: PyPDF2 (PDF) + python-docx (DOCX)

### Frontend
- **Framework**: React 18
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **File Upload**: react-dropzone
- **Styling**: CSS3 with modern gradients

### LangGraph Agent Flow
```
Entry: analyze_candidate
  ↓
Route by availability (email/phone)
  ↓
generate_email_request OR generate_sms_request
  ↓
Return personalized message
```

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- OpenAI API key (or compatible API endpoint)

## 🚀 Installation & Setup

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create `.env` file:
```bash
cp .env.example .env
```

6. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_api_key_here
FLASK_ENV=development
DATABASE_URL=sqlite:///candidates.db
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

7. Run the backend server:
```bash
python app.py
```

Backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

Frontend will run on `http://localhost:3000`

## 🎬 Usage

1. **Upload Resume**: 
   - Drag & drop or click to upload a PDF/DOCX resume
   - System automatically extracts candidate information
   - View extraction confidence scores

2. **View Candidates**:
   - Dashboard shows all candidates in a table
   - Click any row to view detailed profile

3. **Request Documents**:
   - In candidate profile, click "Request PAN & Aadhaar"
   - AI agent generates personalized email/SMS request
   - View generated message and agent logs

4. **Submit Documents**:
   - Upload PAN and/or Aadhaar documents
   - View submitted documents with timestamps

## 📡 API Endpoints

### Candidates
- `POST /api/candidates/upload` - Upload and parse resume
- `GET /api/candidates` - List all candidates
- `GET /api/candidates/<id>` - Get candidate details

### Documents
- `POST /api/candidates/<id>/request-documents` - Generate AI document request
- `POST /api/candidates/<id>/submit-documents` - Upload PAN/Aadhaar
- `GET /api/documents/<filename>` - Serve document file

### Health
- `GET /api/health` - Health check

## 🗂️ Project Structure

```
traqcheck/
├── backend/
│   ├── app/
│   │   ├── models.py          # Database models
│   │   ├── resume_parser.py   # Resume parsing logic
│   │   └── agent.py            # LangGraph AI agent
│   ├── uploads/
│   │   ├── resumes/            # Uploaded resumes
│   │   └── documents/          # Uploaded documents
│   ├── app.py                  # Flask application
│   ├── config.py               # Configuration
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # Environment variables
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ResumeUpload.js
│   │   │   └── CandidateTable.js
│   │   ├── pages/
│   │   │   ├── Dashboard.js
│   │   │   └── CandidateProfile.js
│   │   ├── services/
│   │   │   └── api.js          # API client
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
└── README.md
```

## 🚢 Deployment

### Quick Deploy to Vercel (Recommended)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/CodeSaurabhCode/TraqCheck)

**See detailed guide**: [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)

**Quick Steps**:
1. Click the button above or push to GitHub
2. Import repository to Vercel
3. Add environment variables:
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `DATABASE_URL` - PostgreSQL connection string (get from [Neon](https://neon.tech) or [Supabase](https://supabase.com))
   - `SECRET_KEY` - Random secret key
   - `VERCEL` - Set to `1`
4. Deploy!

### Option 1: Render

**Backend:**
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:create_app()`
   - Environment Variables: Add `OPENAI_API_KEY`

**Frontend:**
1. Create a new Static Site on Render
2. Configure:
   - Build Command: `npm install && npm run build`
   - Publish Directory: `build`
   - Add environment variable: `REACT_APP_API_URL=https://your-backend.onrender.com/api`

### Option 2: Railway

1. Create new project
2. Add PostgreSQL plugin
3. Deploy backend and frontend as separate services
4. Configure environment variables

### Option 3: Vercel (Frontend) + Render (Backend)

**Frontend on Vercel:**
```bash
cd frontend
vercel --prod
```

**Backend on Render:** Follow Render instructions above

## 🔧 Configuration

### Backend Environment Variables
```env
OPENAI_API_KEY=your_key_here
FLASK_ENV=production
DATABASE_URL=sqlite:///candidates.db  # or PostgreSQL URL
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
SECRET_KEY=your_secret_key_here
```

### Frontend Environment Variables
```env
REACT_APP_API_URL=http://localhost:5000/api
```

## 🧪 Testing

Test the API with curl:

```bash
# Health check
curl http://localhost:5000/api/health

# Upload resume
curl -X POST -F "resume=@path/to/resume.pdf" http://localhost:5000/api/candidates/upload

# Get candidates
curl http://localhost:5000/api/candidates

# Request documents
curl -X POST http://localhost:5000/api/candidates/1/request-documents
```

## 🧪 Testing & Utilities

### Run Edge Case Tests
```bash
cd backend
python test_edge_cases.py
```

Tests include:
- ✅ Duplicate upload rejection
- ✅ Empty file validation
- ✅ Invalid content detection
- ✅ Missing identifying data rejection
- ✅ File size limit enforcement
- ✅ Complete successful workflow

### Database Management
```bash
cd backend
python db_manager.py
```

Features:
- View database statistics
- Show recent candidates
- Detect duplicate records
- Cleanup orphaned files
- Remove failed extractions
- Reset database (with confirmation)

### Edge Cases Handled

The system includes comprehensive validation:

1. **Duplicate Prevention**: Unique constraints on email, phone, filename
2. **File Validation**: Size limits, type checking, empty file detection
3. **Content Validation**: Minimum text length, identifying information required
4. **Parse-Before-Insert**: Only creates DB records for successfully parsed resumes
5. **Atomic Operations**: Rollback on errors, cleanup on failures
6. **Error Recovery**: Proper error messages, file cleanup on validation failure

See **[EDGE_CASES.md](EDGE_CASES.md)** for complete details.

## 🎥 Demo Video Guide

For your Loom recording, showcase:

1. **Architecture Overview** (30s)
   - Show project structure
   - Explain tech stack
   - Highlight LangGraph agent flow

2. **Upload Resume** (1m)
   - Drag and drop resume
   - Show parsing progress
   - View extracted data with confidence scores

3. **Trigger Document Request** (1.5m)
   - Click on candidate
   - Generate AI document request
   - Show email/SMS message
   - Display agent logs

4. **Upload Documents** (1m)
   - Upload PAN and Aadhaar
   - View submitted documents

5. **Code Walkthrough** (1m)
   - Show LangGraph agent code
   - Explain state management
   - Demonstrate routing logic

## 🛠️ Technology Stack

- **Backend**: Flask, SQLAlchemy, LangGraph, LangChain, OpenAI
- **Frontend**: React, React Router, Axios, react-dropzone
- **Database**: SQLite (dev), PostgreSQL (production)
- **AI**: GPT-3.5-turbo via OpenAI API
- **Agent Framework**: LangGraph for stateful agent workflows

## 📝 License

MIT License - feel free to use this project for learning and development.

## 🤝 Contributing

This is a challenge project, but suggestions and improvements are welcome!

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

Built with ❤️ using LangGraph, Flask, and React
