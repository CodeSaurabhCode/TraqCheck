# Deployment Guide

## Prerequisites
- GitHub account
- Render/Railway/Vercel account
- OpenAI API key

## Deployment to Render

### Backend Deployment

1. **Prepare for Production**

Add to `backend/requirements.txt`:
```
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

2. **Create `render.yaml`** (optional, for infrastructure as code)

3. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

4. **Deploy on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: traqcheck-backend
     - **Environment**: Python 3
     - **Build Command**: `cd backend && pip install -r requirements.txt`
     - **Start Command**: `cd backend && gunicorn app:create_app()`
     - **Environment Variables**:
       - `OPENAI_API_KEY`: your_openai_key
       - `DATABASE_URL`: (auto-provided if using Render PostgreSQL)
       - `FLASK_ENV`: production
   - Click "Create Web Service"

5. **Add PostgreSQL Database** (Optional but recommended)
   - In your service dashboard, click "New +" → "PostgreSQL"
   - Link it to your web service
   - Update `DATABASE_URL` in environment variables

### Frontend Deployment

1. **Update API URL**

Create `frontend/.env.production`:
```
REACT_APP_API_URL=https://traqcheck-backend.onrender.com/api
```

2. **Deploy on Render**
   - Click "New +" → "Static Site"
   - Connect repository
   - Configure:
     - **Name**: traqcheck-frontend
     - **Build Command**: `cd frontend && npm install && npm run build`
     - **Publish Directory**: `frontend/build`
     - **Environment Variables**:
       - `REACT_APP_API_URL`: https://your-backend-url.onrender.com/api
   - Click "Create Static Site"

## Deployment to Railway

1. **Install Railway CLI** (optional)
```bash
npm install -g @railway/cli
```

2. **Deploy Backend**
   - Go to [Railway](https://railway.app/)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Add PostgreSQL plugin
   - Configure environment variables
   - Set start command: `cd backend && python app.py`

3. **Deploy Frontend**
   - Add new service to same project
   - Configure build command: `cd frontend && npm install && npm run build`
   - Add environment variable: `REACT_APP_API_URL`

## Deployment to Vercel (Frontend Only)

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Deploy**
```bash
cd frontend
vercel --prod
```

3. **Configure Environment**
   - In Vercel dashboard, add environment variable:
   - `REACT_APP_API_URL`: your backend URL

## Environment Configuration

### Production Backend (.env)
```env
OPENAI_API_KEY=sk-...
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@host:port/db
SECRET_KEY=generate-strong-random-key-here
MAX_CONTENT_LENGTH=16777216
```

### Production Frontend (.env.production)
```env
REACT_APP_API_URL=https://your-backend-url.com/api
```

## Post-Deployment Checklist

- [ ] Backend health check working (`/api/health`)
- [ ] CORS configured correctly
- [ ] Database tables created
- [ ] File upload directories exist and writable
- [ ] OpenAI API key valid and working
- [ ] Frontend can connect to backend API
- [ ] Resume upload and parsing working
- [ ] Document request generation working
- [ ] Document upload working

## Troubleshooting

### Issue: CORS errors
**Solution**: Ensure Flask-CORS is configured and backend URL is correct in frontend

### Issue: Database not found
**Solution**: Ensure database tables are created. Add to `app.py`:
```python
with app.app_context():
    db.create_all()
```

### Issue: File upload fails
**Solution**: Ensure upload directories exist and have write permissions

### Issue: OpenAI API errors
**Solution**: Verify API key is set correctly and has credits

## Monitoring

- Check Render/Railway logs for errors
- Monitor OpenAI API usage
- Set up alerts for failed uploads or parsing errors

## Scaling Considerations

1. **Database**: Migrate from SQLite to PostgreSQL for production
2. **File Storage**: Use S3/Cloudinary for file storage instead of local filesystem
3. **Background Jobs**: Use Celery for async resume parsing
4. **Caching**: Add Redis for caching candidate data
5. **Rate Limiting**: Add rate limiting to API endpoints
