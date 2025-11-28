# Deploying TraqCheck to Vercel

This guide walks you through deploying the complete TraqCheck application to Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Push your code to GitHub
3. **OpenAI API Key**: Get one from [platform.openai.com](https://platform.openai.com)
4. **PostgreSQL Database**: Use [Neon](https://neon.tech), [Supabase](https://supabase.com), or [Railway](https://railway.app)

## Step 1: Set Up PostgreSQL Database

Since Vercel is serverless and doesn't support SQLite files, you need a PostgreSQL database.

### Option A: Neon (Recommended - Free Tier)

1. Go to [neon.tech](https://neon.tech)
2. Sign up and create a new project
3. Copy the connection string (looks like: `postgresql://user:pass@host/dbname`)
4. Save it for later

### Option B: Supabase (Free Tier)

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Go to Settings > Database
4. Copy the "Connection string" (URI format)
5. Save it for later

### Option C: Railway (Simple, Paid)

1. Go to [railway.app](https://railway.app)
2. Create new project
3. Add PostgreSQL plugin
4. Copy the `DATABASE_URL` from environment variables

## Step 2: Install Vercel CLI (Optional but Recommended)

```bash
npm install -g vercel
```

## Step 3: Deploy to Vercel

### Method 1: Deploy via Vercel Dashboard (Easiest)

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Import to Vercel**:
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Click "Import"

3. **Configure Project**:
   - Framework Preset: **Other**
   - Root Directory: `./` (leave as is)
   - Build Command: Leave empty (vercel.json handles it)
   - Output Directory: Leave empty
   - Install Command: Leave empty

4. **Add Environment Variables**:
   Click "Environment Variables" and add:
   
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   DATABASE_URL=postgresql://user:pass@host/dbname
   SECRET_KEY=your-random-secret-key-for-production
   VERCEL=1
   ```

5. **Deploy**:
   - Click "Deploy"
   - Wait 2-3 minutes for build to complete
   - Your app will be live at `https://your-project.vercel.app`

### Method 2: Deploy via CLI

1. **Login to Vercel**:
   ```bash
   vercel login
   ```

2. **Deploy**:
   ```bash
   vercel
   ```

3. **Follow prompts**:
   - Set up and deploy? **Y**
   - Which scope? Select your account
   - Link to existing project? **N**
   - Project name? **traqcheck** (or your choice)
   - In which directory? **./** (root)

4. **Add Environment Variables**:
   ```bash
   vercel env add OPENAI_API_KEY
   # Paste your API key when prompted
   
   vercel env add DATABASE_URL
   # Paste your PostgreSQL URL when prompted
   
   vercel env add SECRET_KEY
   # Enter a random secret key
   
   vercel env add VERCEL
   # Enter: 1
   ```

5. **Deploy to Production**:
   ```bash
   vercel --prod
   ```

## Step 4: Initialize Database

After deployment, you need to create the database tables:

1. **Create a temporary Python script** (`init_db.py`):
   ```python
   from sqlalchemy import create_engine
   import os
   
   # Replace with your actual DATABASE_URL
   DATABASE_URL = "postgresql://user:pass@host/dbname"
   
   from backend.models import db
   
   engine = create_engine(DATABASE_URL)
   db.metadata.create_all(engine)
   
   print("✅ Database tables created successfully!")
   ```

2. **Run locally**:
   ```bash
   cd backend
   python ../init_db.py
   ```

Or use a PostgreSQL client to run this SQL:

```sql
CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200),
    email VARCHAR(200) UNIQUE,
    phone VARCHAR(50) UNIQUE,
    company VARCHAR(200),
    designation VARCHAR(200),
    skills TEXT,
    resume_filename VARCHAR(500) UNIQUE,
    resume_path VARCHAR(500),
    extraction_status VARCHAR(50) DEFAULT 'pending',
    confidence_scores TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_candidate_email ON candidates(email);
CREATE INDEX idx_candidate_phone ON candidates(phone);
CREATE INDEX idx_candidate_name ON candidates(name);
CREATE INDEX idx_candidate_created_at ON candidates(created_at);

CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id) ON DELETE CASCADE,
    document_type VARCHAR(50),
    filename VARCHAR(500),
    file_path VARCHAR(500),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE document_requests (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id) ON DELETE CASCADE,
    request_message TEXT,
    request_type VARCHAR(50) DEFAULT 'email',
    status VARCHAR(50) DEFAULT 'sent',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Step 5: Test Your Deployment

1. **Visit your site**: `https://your-project.vercel.app`
2. **Test upload**: Try uploading a resume
3. **Check API**: Visit `https://your-project.vercel.app/api/health`

## Important Notes

### File Storage Limitations

⚠️ **Vercel serverless functions use `/tmp` directory which is ephemeral!**

Files uploaded to `/tmp` will be deleted when the function terminates. For production:

**Option 1: Use Vercel Blob Storage** (Recommended)
```bash
npm install @vercel/blob
```

**Option 2: Use AWS S3**
```bash
pip install boto3
```

**Option 3: Use Cloudinary**
```bash
pip install cloudinary
```

You'll need to update the file upload logic in `backend/app.py` to save files to cloud storage instead of local filesystem.

### Database Connection Pooling

For better performance with PostgreSQL, install:
```bash
pip install psycopg2-binary
```

Add to `requirements.txt`:
```
psycopg2-binary==2.9.9
```

### Environment Variables

Required:
- ✅ `OPENAI_API_KEY` - Your OpenAI API key
- ✅ `DATABASE_URL` - PostgreSQL connection string
- ✅ `SECRET_KEY` - Flask secret key for sessions
- ✅ `VERCEL` - Set to `1` to enable serverless mode

Optional:
- `MAX_CONTENT_LENGTH` - Default: 10485760 (10MB)

## Troubleshooting

### Build Fails

**Error**: `Module not found`
- Check `requirements.txt` includes all dependencies
- Ensure package versions are compatible

**Error**: `Build exceeded maximum duration`
- Simplify dependencies
- Remove unused packages

### Database Connection Issues

**Error**: `could not connect to server`
- Verify DATABASE_URL is correct
- Check database allows external connections
- Ensure SSL is configured (add `?sslmode=require` to URL)

**Error**: `relation "candidates" does not exist`
- Run the SQL schema creation script
- Use database management tool to verify tables exist

### API Not Working

**Error**: `500 Internal Server Error`
- Check Vercel function logs
- Verify environment variables are set
- Test locally first

**Error**: `CORS errors`
- Already handled in `app.py` with Flask-CORS
- If issues persist, check Vercel function logs

### File Upload Issues

**Error**: `No such file or directory: /tmp/uploads`
- Normal on first run
- App creates directories automatically
- Files are temporary in serverless environment

## Monitoring

### View Logs

**Vercel Dashboard**:
1. Go to your project
2. Click "Deployments"
3. Click on a deployment
4. Click "Runtime Logs"

**Via CLI**:
```bash
vercel logs
```

### Check Function Performance

1. Go to Vercel Dashboard
2. Click "Analytics"
3. View function execution time, memory usage, etc.

## Custom Domain (Optional)

1. Go to your project settings
2. Click "Domains"
3. Add your custom domain
4. Update DNS records as instructed

## Continuous Deployment

Every push to your main branch will automatically deploy to Vercel!

```bash
git add .
git commit -m "Update feature"
git push origin main
# Vercel automatically deploys!
```

## Cost Estimate

- **Vercel Hobby (Free)**:
  - 100 GB-hrs compute
  - 100 GB bandwidth
  - Unlimited deployments
  - Should be sufficient for testing/demo

- **Vercel Pro ($20/month)**:
  - 1000 GB-hrs compute
  - 1 TB bandwidth
  - Priority support

- **Database**:
  - Neon: Free tier (0.5 GB)
  - Supabase: Free tier (500 MB)
  - Railway: $5/month for 512 MB

## Next Steps

1. ✅ Set up custom domain
2. ✅ Implement cloud file storage (S3/Blob)
3. ✅ Add monitoring/analytics
4. ✅ Set up error tracking (Sentry)
5. ✅ Configure database backups
6. ✅ Add rate limiting
7. ✅ Set up CI/CD tests

## Support

For issues:
1. Check Vercel function logs
2. Review this guide
3. Check Vercel documentation: [vercel.com/docs](https://vercel.com/docs)
4. Open an issue on GitHub

---

🎉 **Congratulations!** Your TraqCheck app is now live on Vercel!
