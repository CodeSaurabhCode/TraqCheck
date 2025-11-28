# Quick Start Guide

## Fastest Way to Get Running

### Step 1: Clone and Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux
```

### Step 2: Configure API Key

Edit `backend/.env` and add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-actual-key-here
```

**Don't have an OpenAI API key?**
- Sign up at https://platform.openai.com/
- Navigate to API keys section
- Create new secret key
- Copy and paste into .env file

**Alternative: Use OpenRouter (Free)**
- Sign up at https://openrouter.ai/
- Get free API key
- Modify `config.py` to use OpenRouter endpoint

### Step 3: Start Backend

```bash
# Make sure you're in backend directory with venv activated
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Step 4: Setup Frontend (New Terminal)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Browser will open automatically at `http://localhost:3000`

### Step 5: Test the System

1. **Upload a Resume**
   - Drag and drop a PDF/DOCX resume
   - Watch the parsing progress
   - See extracted data appear

2. **View Candidate**
   - Click on the candidate row
   - View detailed profile with confidence scores

3. **Request Documents**
   - Click "Request PAN & Aadhaar" button
   - See AI-generated personalized message

4. **Upload Documents**
   - Select PAN and Aadhaar files
   - Submit documents
   - View in submitted documents section

## Troubleshooting

### Backend won't start

**Error: "ModuleNotFoundError: No module named 'flask'"**
- Solution: Activate virtual environment first
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

**Error: "OpenAI API key not set"**
- Solution: Check `.env` file exists and has valid key
```bash
# Verify .env exists
ls .env  # Should show the file

# Check content (be careful not to share!)
cat .env  # Should show OPENAI_API_KEY=sk-...
```

**Error: Database error**
- Solution: Delete old database and restart
```bash
rm candidates.db
python app.py
```

### Frontend won't start

**Error: "npm: command not found"**
- Solution: Install Node.js from https://nodejs.org/

**Error: "Cannot connect to backend"**
- Solution: Ensure backend is running on port 5000
- Check browser console for CORS errors

**Error: "Module not found"**
- Solution: Delete and reinstall node_modules
```bash
rm -rf node_modules package-lock.json
npm install
```

### Resume parsing fails

**Error: "Failed to parse resume"**
- Solution: Check file format (must be PDF or DOCX)
- Try a different resume
- Check backend logs for detailed error

**Error: "OpenAI rate limit"**
- Solution: Wait a moment and try again
- Check your OpenAI account has credits

## Sample Test Data

### Create a Sample Resume

Create a file called `sample_resume.txt` and paste:

```
JOHN DOE
Senior Software Engineer

Contact:
Email: john.doe@techcorp.com
Phone: +91-9876543210

EXPERIENCE
Tech Corp Inc. | Senior Software Engineer | 2020 - Present
- Led development of microservices architecture
- Managed team of 5 engineers
- Implemented CI/CD pipelines

SKILLS
Python, React, Node.js, Docker, Kubernetes, AWS, Machine Learning, 
RESTful APIs, PostgreSQL, MongoDB, Git, Agile/Scrum

EDUCATION
B.Tech in Computer Science | MIT | 2016-2020
```

Save as DOCX and upload to test the system.

## Next Steps

Once everything is working:

1. **Customize the AI prompts** in `backend/app/resume_parser.py` and `backend/app/agent.py`
2. **Style the frontend** by modifying CSS files
3. **Add more fields** by updating models and parser
4. **Deploy to production** using DEPLOYMENT.md guide

## Development Tips

### Hot Reload

- **Backend**: Flask auto-reloads when you save Python files (in debug mode)
- **Frontend**: React auto-reloads when you save JS/CSS files

### View Database

```bash
# Install DB browser
pip install sqlite-web

# View database
sqlite_web candidates.db
```

Open http://localhost:8080 to browse database.

### API Testing

Use curl or Postman:

```bash
# Health check
curl http://localhost:5000/api/health

# List candidates
curl http://localhost:5000/api/candidates

# Get specific candidate
curl http://localhost:5000/api/candidates/1
```

### Debug Mode

Backend debugging is enabled by default in development. Check `app.py`:
```python
app.run(debug=True, port=5000)
```

For frontend debugging:
- Open browser DevTools (F12)
- Check Console tab for errors
- Check Network tab for API calls

## Common Workflows

### Adding a New API Endpoint

1. Add route in `backend/app.py`:
```python
@app.route('/api/your-endpoint', methods=['POST'])
def your_function():
    # Your logic
    return jsonify({"result": "data"}), 200
```

2. Add service method in `frontend/src/services/api.js`:
```javascript
yourMethod: async () => {
  const response = await api.post('/your-endpoint');
  return response.data;
}
```

3. Use in component:
```javascript
const result = await candidateService.yourMethod();
```

### Modifying the LangGraph Agent

Edit `backend/app/agent.py`:

```python
# Add new node
def your_new_node(self, state: AgentState) -> AgentState:
    # Your logic
    return state

# Add to graph
workflow.add_node("your_node", self.your_new_node)
workflow.add_edge("analyze_candidate", "your_node")
```

## Resources

- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **Flask Docs**: https://flask.palletsprojects.com/
- **React Docs**: https://react.dev/
- **OpenAI API Docs**: https://platform.openai.com/docs/

## Support

If you're stuck:
1. Check error messages carefully
2. Review logs in terminal
3. Ensure all dependencies are installed
4. Verify environment variables are set
5. Try a fresh install in a new directory

Happy coding! 🚀
