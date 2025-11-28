# TraqCheck - AI-Powered Resume Parser & Document Collection System

<div align="center">

![TraqCheck](https://img.shields.io/badge/TraqCheck-Resume%20Parser-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![React](https://img.shields.io/badge/React-18.2.0-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-AI%20Agent-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

**An intelligent full-stack application that parses resumes, extracts candidate information, and uses AI agents to autonomously collect PAN and Aadhaar documents.**

[Live Demo](https://traqcheck-eq4kg6661-saurabh-kshirsagars-projects.vercel.app) | [Documentation](#documentation) | [Report Bug](https://github.com/CodeSaurabhCode/TraqCheck/issues)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Setup](#environment-setup)
- [Usage](#usage)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

TraqCheck is a modern HR automation tool that streamlines the candidate onboarding process. It leverages OpenAI's GPT models and LangGraph framework to create intelligent agents that can:

- **Parse resumes** and extract structured candidate information
- **Autonomously request** missing documents (PAN, Aadhaar)
- **Track document collection** status
- **Provide a seamless** candidate experience

Perfect for HR teams looking to automate repetitive document collection tasks!

---

## ✨ Features

### 🚀 Core Features

- **📄 Resume Parsing**: Upload PDF/TXT resumes and extract:
  - Name, Email, Phone
  - Skills, Experience
  - Education, Location
  
- **🤖 AI Agent (LangGraph)**: Autonomous document collection workflow
  - Analyzes candidate data
  - Requests missing documents
  - Tracks submission status
  - Provides intelligent follow-ups

- **💼 Candidate Dashboard**: 
  - View all candidates at a glance
  - Real-time document status tracking
  - Professional, responsive UI

- **📱 Document Submission Portal**:
  - Candidates can upload documents via unique links
  - Supports image uploads (PAN, Aadhaar)
  - Automatic status updates

### 🛡️ Advanced Features

- **Edge Case Handling**:
  - Duplicate prevention (phone/email)
  - Input validation & sanitization
  - Comprehensive error handling
  - Database constraints

- **Production Ready**:
  - PostgreSQL database (Neon)
  - Serverless deployment (Vercel)
  - Environment-based configuration
  - Secure file uploads

---

## 🛠️ Tech Stack

### Backend
- **Python 3.9+** - Core backend language
- **Flask 3.0.0** - Web framework
- **LangGraph** - AI agent orchestration
- **LangChain** - LLM integration
- **OpenAI GPT-4** - Language model
- **SQLAlchemy** - ORM
- **PostgreSQL** - Production database
- **SQLite** - Development database

### Frontend
- **React 18.2.0** - UI framework
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **React Dropzone** - File uploads
- **CSS3** - Styling

### DevOps
- **Vercel** - Hosting & deployment
- **GitHub** - Version control
- **Neon** - PostgreSQL hosting

---

## 🏗️ Architecture

```
┌─────────────────┐
│   React Frontend│
│   (Vercel)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Flask API     │
│   (Serverless)  │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────┐
│LangGraph│ │PostgreSQL│
│  Agent  │ │  (Neon)  │
└─────────┘ └──────────┘
```

### AI Agent Workflow (LangGraph)

```
Upload Resume
     │
     ▼
Parse & Extract Data
     │
     ▼
Analyze Missing Docs ◄──────┐
     │                      │
     ▼                      │
Request Documents           │
     │                      │
     ▼                      │
Track Status ───────────────┘
     │
     ▼
Complete ✓
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+** installed
- **Node.js 16+** and npm
- **Git** for version control
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **PostgreSQL** (optional for production)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/CodeSaurabhCode/TraqCheck.git
cd TraqCheck
```

2. **Backend Setup**
```bash
# Create virtual environment
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r ../requirements.txt
```

3. **Frontend Setup**
```bash
cd ../frontend
npm install
```

### Environment Setup

1. **Create `.env` file in project root**
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration (Production)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Flask Configuration
SECRET_KEY=your_secret_key_here
FLASK_ENV=development

# Deployment
VERCEL=0
```

2. **Create `frontend/.env.production`**
```bash
REACT_APP_API_URL=/api
```

### Initialize Database

```bash
# For development (SQLite)
python init_db.py

# For production (PostgreSQL)
# Set DATABASE_URL in .env first
python init_db.py
```

---

## 💻 Usage

### Development Mode

**Start Backend:**
```bash
cd backend
python app.py
# Server runs on http://localhost:5000
```

**Start Frontend:**
```bash
cd frontend
npm start
# App runs on http://localhost:3000
```

### Using the Application

1. **Upload Resume**
   - Click "Upload Resume" on dashboard
   - Select PDF or TXT file
   - Wait for parsing to complete

2. **View Candidates**
   - Dashboard shows all candidates
   - Click on a candidate to view details
   - See document collection status

3. **Request Documents**
   - Click "Request Documents" on candidate profile
   - AI agent generates personalized request
   - Unique submission link is created

4. **Submit Documents** (Candidate View)
   - Open the submission link
   - Upload PAN and Aadhaar images
   - Submit and track status

---

## 🌐 Deployment

### Deploy to Vercel

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Login to Vercel**
```bash
vercel login
```

3. **Deploy**
```bash
vercel --prod
```

4. **Configure Environment Variables**
```bash
vercel env add OPENAI_API_KEY production
vercel env add DATABASE_URL production
vercel env add SECRET_KEY production
vercel env add VERCEL production
```

5. **Redeploy**
```bash
vercel --prod
```

**Live Application**: Your app will be available at `https://your-project.vercel.app`

---

## 📚 API Documentation

### Endpoints

#### **POST** `/api/parse-resume`
Upload and parse a resume.

**Request:**
```javascript
FormData {
  file: File (PDF/TXT)
}
```

**Response:**
```json
{
  "success": true,
  "candidate": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "skills": ["Python", "React"],
    "experience": "5 years",
    "education": "BS Computer Science",
    "location": "New York"
  }
}
```

#### **GET** `/api/candidates`
Get all candidates.

**Response:**
```json
{
  "candidates": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "documents_status": "pending"
    }
  ]
}
```

#### **GET** `/api/candidate/<id>`
Get candidate details by ID.

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "skills": ["Python", "React"],
  "documents": [
    {
      "type": "PAN",
      "status": "submitted",
      "file_path": "/uploads/pan_123.jpg"
    }
  ]
}
```

#### **POST** `/api/request-documents/<candidate_id>`
Request documents from candidate.

**Response:**
```json
{
  "success": true,
  "message": "Document requests created",
  "request_token": "unique_token_123"
}
```

#### **POST** `/api/submit-document/<token>`
Submit a document (candidate endpoint).

**Request:**
```javascript
FormData {
  document_type: "PAN" | "AADHAAR",
  file: File (Image)
}
```

**Response:**
```json
{
  "success": true,
  "message": "Document submitted successfully"
}
```

---

## 📁 Project Structure

```
TraqCheck/
│
├── backend/                 # Flask backend
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   ├── db_manager.py       # Database models & operations
│   ├── resume_parser.py    # Resume parsing logic
│   ├── agent.py            # LangGraph AI agent
│   ├── uploads/            # Uploaded files
│   └── venv/               # Virtual environment
│
├── frontend/               # React frontend
│   ├── public/            # Static assets
│   ├── src/
│   │   ├── components/    # React components
│   │   │   └── Navbar.js
│   │   ├── pages/         # Page components
│   │   │   ├── Dashboard.js
│   │   │   └── CandidateProfile.js
│   │   ├── services/      # API services
│   │   │   └── api.js
│   │   ├── App.js         # Root component
│   │   └── index.js       # Entry point
│   └── package.json
│
├── api/                    # Vercel serverless functions
│   └── index.py           # API entry point
│
├── .env                    # Environment variables
├── .gitignore             # Git ignore rules
├── vercel.json            # Vercel configuration
├── requirements.txt       # Python dependencies
├── init_db.py             # Database initialization
└── README.md              # This file
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint for JavaScript code
- Write descriptive commit messages
- Add tests for new features
- Update documentation

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** - For GPT-4 and language models
- **LangChain** - For LLM integration framework
- **LangGraph** - For AI agent orchestration
- **Vercel** - For seamless deployment
- **Neon** - For PostgreSQL hosting

---

## 📧 Contact

**Saurabh Kshirsagar**
- GitHub: [@CodeSaurabhCode](https://github.com/CodeSaurabhCode)
- Project Link: [https://github.com/CodeSaurabhCode/TraqCheck](https://github.com/CodeSaurabhCode/TraqCheck)

---

## 🎉 Demo

Visit the live application: **[TraqCheck Demo](https://traqcheck-eq4kg6661-saurabh-kshirsagars-projects.vercel.app)**

---

<div align="center">

Made with ❤️ by Saurabh Kshirsagar

⭐ Star this repo if you find it helpful!

</div>
