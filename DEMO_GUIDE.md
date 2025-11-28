# TraqCheck

## Video Demo Structure (5 minutes)

### 1. Introduction (30 seconds)
- "Hi, I'm presenting TraqCheck - an AI-powered resume parser and document collection system"
- "This system helps HR teams automatically extract candidate information and intelligently request identity documents"

### 2. Architecture Overview (45 seconds)
**Show project structure on screen**
- Backend: Flask + LangGraph agent framework
- Frontend: React with drag-and-drop interface
- Database: SQLAlchemy with SQLite/PostgreSQL
- AI: OpenAI GPT-3.5 for parsing, LangGraph for agent orchestration

**Highlight key components:**
```
Backend:
- resume_parser.py: Extracts data from PDF/DOCX using LLM
- agent.py: LangGraph state machine for document requests
- models.py: Database schema for candidates, documents, requests

Frontend:
- ResumeUpload: Drag-and-drop with progress
- CandidateTable: Dashboard view
- CandidateProfile: Detail view with AI interaction
```

### 3. Demo: Upload Resume (60 seconds)
**Show in browser:**
1. Open dashboard at localhost:3000
2. Drag a sample resume (PDF or DOCX) to upload area
3. Show upload progress bar
4. Explain: "While uploading, the backend uses PyPDF2/python-docx to extract text"
5. Show extracted data appearing in table:
   - Name, email, phone, company, designation, skills
   - Highlight confidence scores for each field
6. Explain: "GPT-3.5 analyzes resume text and extracts structured data with confidence scores"

### 4. Demo: View Candidate Profile (45 seconds)
**Click on candidate row:**
1. Show detailed profile view
2. Point out:
   - All extracted fields with confidence percentages
   - Color-coded confidence (green >80%, orange >50%, red <50%)
   - Skills displayed as tags
   - Empty documents section (0/2 documents)

### 5. Demo: AI Document Request (90 seconds)
**The key feature - LangGraph agent:**

1. Click "Request PAN & Aadhaar" button
2. **Show backend terminal:** Agent processing logs
3. **Explain the LangGraph flow while it runs:**
   ```
   State Machine Flow:
   1. analyze_candidate: Examines candidate data
   2. Router: Decides email vs SMS based on availability
   3. generate_email_request: Creates personalized message
   4. Returns with structured output
   ```

4. **Show generated request message:**
   - Personalized greeting with candidate name
   - References their company and designation
   - Professional explanation of document need
   - Clear submission instructions

5. **Expand agent logs section:**
   - "Analyzing candidate: [Name]"
   - "Generated personalized email request"

6. **Show code briefly** (agent.py):
   ```python
   # LangGraph state graph
   workflow.add_node("analyze_candidate", ...)
   workflow.add_node("generate_email_request", ...)
   workflow.add_conditional_edges(...)
   ```

### 6. Demo: Upload Documents (45 seconds)
**Scroll to upload section:**
1. Select PAN card image/PDF
2. Select Aadhaar image/PDF
3. Click "Submit Documents"
4. Show success message
5. See documents appear in "Submitted Documents" section
6. Note document count changes to 2/2 in table

### 7. Technical Highlights (30 seconds)
**Show code snippets quickly:**

**Resume Parser (resume_parser.py):**
```python
# LLM extracts structured data with confidence scores
result = llm.invoke({
    "resume_text": text,
    # Returns: {data: {...}, confidence_scores: {...}}
})
```

**LangGraph Agent (agent.py):**
```python
# State-based agent workflow
class AgentState(TypedDict):
    candidate_name: str
    request_message: str
    messages: Sequence[str]

workflow = StateGraph(AgentState)
```

### 8. Deployment & Conclusion (15 seconds)
- "Ready for deployment to Render, Railway, or Vercel"
- "All code available in GitHub repository"
- "Uses free tier OpenAI API"
- "Thank you!"

## Key Points to Emphasize

1. **LangGraph Integration**: This is the unique selling point
   - State-based agent architecture
   - Conditional routing based on candidate data
   - Structured output with logging

2. **Production-Ready Features**:
   - Confidence scores for data quality
   - Progress indicators
   - Error handling
   - Clean UI/UX

3. **Scalability**:
   - Database abstraction (SQLite → PostgreSQL)
   - Modular architecture
   - API-first design

## Sample Resume for Demo

Create a sample resume with:
- Name: John Doe
- Email: john.doe@example.com
- Phone: +91-9876543210
- Company: Tech Corp
- Designation: Senior Software Engineer
- Skills: Python, React, Machine Learning, Docker

## Screen Recording Tips

1. **Prepare environment:**
   - Clean browser (no extra tabs)
   - Terminal with clear font
   - VS Code with key files open

2. **Recording flow:**
   - Start with architecture diagram
   - Switch to browser for demo
   - Show terminal for backend logs
   - Quick code walkthrough
   - End with deployment docs

3. **Timing:**
   - Speak clearly and at moderate pace
   - Practice transitions between sections
   - Keep under 5 minutes total

## GitHub Repository Setup

Before recording, ensure:
- [ ] All code committed
- [ ] README.md complete
- [ ] .env.example provided (no actual keys!)
- [ ] .gitignore configured
- [ ] Screenshots/architecture diagram added
- [ ] License file added (MIT)

Good luck with your demo! 🎬
