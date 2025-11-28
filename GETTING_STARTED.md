# Getting Started with TraqCheck

## 🎯 What You've Built

A production-ready, AI-powered resume parsing and document collection system with:
- ✅ Flask backend with LangGraph agent framework
- ✅ React frontend with modern UI
- ✅ OpenAI GPT-3.5 integration
- ✅ Complete CRUD operations
- ✅ File upload handling
- ✅ Confidence scoring system
- ✅ Ready for deployment

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Backend Dependencies

```powershell
# Open terminal in project root
cd backend

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure OpenAI API Key

```powershell
# Copy example env file
copy .env.example .env

# Edit .env file
notepad .env
```

Add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

**Get API Key:**
- Go to https://platform.openai.com/api-keys
- Sign up or log in
- Create new secret key
- Copy and paste into .env

### Step 3: Start Backend

```powershell
# Make sure you're in backend directory with venv activated
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 4: Install Frontend Dependencies (New Terminal)

```powershell
# Open NEW terminal
cd frontend

# Install dependencies
npm install
```

### Step 5: Start Frontend

```powershell
# In frontend directory
npm start
```

Browser opens automatically at http://localhost:3000

## 🎬 Test the Application

### 1. Upload Resume

**Option A: Use sample resume**
- Copy `sample_resume.txt` content
- Paste into a Word document
- Save as `John_Doe_Resume.docx`
- Drag and drop to upload area

**Option B: Use your own resume**
- Any PDF or DOCX file
- Max 16MB

### 2. Watch Parsing

- Progress bar shows upload status
- Backend extracts text and sends to GPT-3.5
- Data appears in table with confidence scores

### 3. View Candidate Profile

- Click on candidate row in table
- See all extracted fields
- Note confidence percentages

### 4. Request Documents (LangGraph Agent!)

- Click "Request PAN & Aadhaar" button
- AI agent analyzes candidate
- Generates personalized email/SMS
- View agent logs

### 5. Upload Documents

- Select PAN card image/PDF
- Select Aadhaar image/PDF
- Click "Submit Documents"
- See documents in submitted section

## 📊 Understanding the Output

### Extraction Example

When you upload a resume, you'll see:

```json
{
  "name": "John Doe",
  "email": "john.doe@techcorp.com",
  "phone": "+91-9876543210",
  "company": "Tech Corp Inc.",
  "designation": "Senior Software Engineer",
  "skills": [
    "Python", "React", "Flask", "Docker", 
    "AWS", "PostgreSQL", "Machine Learning"
  ],
  "confidence_scores": {
    "name": 0.95,      // 95% confident
    "email": 0.98,     // 98% confident
    "phone": 0.92,     // 92% confident
    "company": 0.88,   // 88% confident
    "designation": 0.90,  // 90% confident
    "skills": 0.85     // 85% confident
  }
}
```

### Document Request Example

```
SUBJECT: Identity Verification Documents Required

BODY:
Dear John Doe,

I hope this email finds you well. We are pleased to move forward 
with your application for the Senior Software Engineer position 
at Tech Corp Inc.

As part of our standard verification process, we kindly request 
you to submit the following identity documents:

1. PAN Card (Permanent Account Number)
2. Aadhaar Card

These documents are required for employment record verification 
and compliance purposes. You can easily upload these documents 
through our secure portal by clicking the link below or using 
the document upload section in your candidate profile.

We appreciate your prompt attention to this matter. If you have 
any questions or concerns, please don't hesitate to reach out.

Best regards,
HR Team
```

## 🔧 Customization Ideas

### 1. Modify Extraction Fields

Edit `backend/app/resume_parser.py`:

```python
# Add new fields to extract
prompt = ChatPromptTemplate.from_messages([
    ("system", """Extract these fields:
    - name
    - email
    - phone
    - company
    - designation
    - skills
    - years_of_experience  # New field!
    - education  # New field!
    """)
])
```

Update model in `backend/app/models.py`:

```python
class Candidate(db.Model):
    # ... existing fields ...
    years_of_experience = db.Column(db.Integer)
    education = db.Column(db.String(500))
```

### 2. Customize AI Agent Messages

Edit `backend/app/agent.py`:

```python
def generate_email_request(self, state: AgentState) -> AgentState:
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a friendly HR assistant. 
        Generate a warm, personalized email...
        
        [Modify this prompt to change tone and style]
        """)
    ])
```

### 3. Add More Document Types

Edit `backend/app/models.py`:

```python
# document_type can be: pan, aadhaar, passport, license
document_type = db.Column(db.String(50))
```

Update frontend to handle new types.

### 4. Change UI Colors

Edit `frontend/src/pages/Dashboard.css`:

```css
.dashboard-header {
  /* Change gradient colors */
  background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
}
```

## 🐛 Troubleshooting

### Backend Issues

**"Virtual environment not activated"**
```powershell
# Windows
backend\venv\Scripts\activate

# Check if active - prompt should show (venv)
```

**"OpenAI API Error"**
```powershell
# Verify API key is set
type backend\.env

# Should show: OPENAI_API_KEY=sk-...
# If not, edit .env and add key
```

**"Port 5000 already in use"**
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

### Frontend Issues

**"Cannot connect to backend"**
- Ensure backend is running on http://localhost:5000
- Check browser console (F12) for errors
- Verify no CORS errors

**"Module not found"**
```powershell
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Parsing Issues

**"Low confidence scores"**
- Resume might be poorly formatted
- Try a different resume
- Check if text is extractable (not image-based PDF)

**"Extraction failed"**
- Check backend logs for detailed error
- Verify OpenAI API has credits
- Check resume file is valid PDF/DOCX

## 📚 File Structure Reference

```
d:\Traqcheck\
├── backend\
│   ├── app\
│   │   ├── __init__.py
│   │   ├── models.py         ← Database schemas
│   │   ├── resume_parser.py  ← Resume parsing logic
│   │   └── agent.py           ← LangGraph agent ⭐
│   ├── uploads\
│   │   ├── resumes\          ← Uploaded resumes
│   │   └── documents\        ← Uploaded documents
│   ├── venv\                  ← Virtual environment
│   ├── app.py                 ← Flask application
│   ├── config.py              ← Configuration
│   ├── requirements.txt       ← Python dependencies
│   └── .env                   ← Environment variables
│
├── frontend\
│   ├── public\
│   │   └── index.html
│   ├── src\
│   │   ├── components\
│   │   │   ├── ResumeUpload.js    ← Drag-drop component
│   │   │   └── CandidateTable.js  ← Table component
│   │   ├── pages\
│   │   │   ├── Dashboard.js       ← Main dashboard
│   │   │   └── CandidateProfile.js ← Profile view
│   │   ├── services\
│   │   │   └── api.js             ← API calls
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── node_modules\
│
├── README.md              ← Main documentation
├── QUICKSTART.md         ← This file
├── ARCHITECTURE.md       ← Technical details
├── DEPLOYMENT.md         ← Deploy instructions
├── DEMO_GUIDE.md         ← Video guide
├── PROJECT_SUMMARY.md    ← Complete summary
├── CHECKLIST.md          ← Pre-submission checklist
├── sample_resume.txt     ← Test data
├── setup.bat             ← Auto setup (Windows)
└── setup.sh              ← Auto setup (Unix)
```

## 🎥 Recording Your Demo

Follow DEMO_GUIDE.md for detailed instructions.

Quick tips:
1. Practice once before recording
2. Have sample resume ready
3. Explain LangGraph agent (key feature!)
4. Show agent logs
5. Keep under 5 minutes

## 📤 Deploying to Production

See DEPLOYMENT.md for complete instructions.

Quick deploy to Render:
1. Push code to GitHub
2. Create Render account
3. New Web Service (backend)
4. New Static Site (frontend)
5. Add environment variables
6. Done!

## 🎓 Learning Points

### LangGraph Concepts Used

1. **State Management**: AgentState TypedDict
2. **Node Functions**: analyze_candidate, generate_email_request
3. **Conditional Routing**: Based on email/phone availability
4. **Graph Compilation**: StateGraph.compile()
5. **State Transitions**: Node → Router → Node → End

### Architecture Patterns

1. **MVC Pattern**: Separation of concerns
2. **RESTful API**: Standard HTTP methods
3. **ORM**: SQLAlchemy for database
4. **Component-Based UI**: React components
5. **Service Layer**: API abstraction

## 📞 Need Help?

1. Check error messages in terminal
2. Review documentation files
3. Check browser console (F12)
4. Verify environment setup
5. Test with sample data

## ✨ Next Steps

Once running locally:

1. ✅ Test all features
2. ✅ Customize UI/branding
3. ✅ Add more fields
4. ✅ Deploy to production
5. ✅ Record demo video
6. ✅ Push to GitHub
7. ✅ Submit!

---

**You're all set!** 🚀

The system is complete and ready to demonstrate. Focus on explaining the LangGraph agent implementation - that's what makes this solution special!

Good luck with your challenge! 🎯
