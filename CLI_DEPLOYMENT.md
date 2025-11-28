# CLI Deployment Guide - TraqCheck

Follow these commands in order to deploy your app.

## Prerequisites

Make sure you have:
- Git installed
- Node.js installed
- Your code pushed to GitHub

## Step 1: Install Vercel CLI

```powershell
npm install -g vercel
```

## Step 2: Login to Vercel

```powershell
vercel login
```

This will open your browser. Login with GitHub/GitLab/Email.

## Step 3: Deploy to Vercel

```powershell
# Navigate to project root (if not already there)
cd D:\Traqcheck

# Deploy (first time setup)
vercel
```

Answer the prompts:
- **Set up and deploy?** → `Y`
- **Which scope?** → Select your account
- **Link to existing project?** → `N`
- **What's your project's name?** → `traqcheck` (or your choice)
- **In which directory is your code located?** → `./`

Then deploy to production:
```powershell
vercel --prod
```

## Step 4: Set Up PostgreSQL Database

### Option A: Neon (Recommended - Free)

1. Go to https://console.neon.tech/signup
2. Sign up with GitHub
3. Create new project: `traqcheck-db`
4. Copy the connection string (looks like: `postgresql://user:pass@host/db`)

### Option B: Supabase (Alternative - Free)

1. Go to https://supabase.com/dashboard
2. Sign up with GitHub
3. Create new project
4. Go to Settings → Database
5. Copy Connection String (URI mode)

### Option C: Railway (Simple - Paid after free tier)

```powershell
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Create project
railway init

# Add PostgreSQL
railway add

# Get connection string
railway variables
```

## Step 5: Add Environment Variables to Vercel

```powershell
# Add OpenAI API Key
vercel env add OPENAI_API_KEY
# When prompted, paste: sk-your-actual-api-key-here
# Select: Production, Preview, Development (space to select all)

# Add Database URL
vercel env add DATABASE_URL
# When prompted, paste: postgresql://user:pass@host/dbname
# Select: Production, Preview, Development

# Add Secret Key
vercel env add SECRET_KEY
# When prompted, paste any random string like: my-super-secret-key-123
# Select: Production, Preview, Development

# Add Vercel flag
vercel env add VERCEL
# When prompted, enter: 1
# Select: Production, Preview, Development
```

## Step 6: Redeploy with Environment Variables

```powershell
vercel --prod
```

## Step 7: Initialize Database

Now we need to create the database tables.

### Method 1: Using Python script (Easier)

1. Add your DATABASE_URL to `backend/.env`:
```env
DATABASE_URL=postgresql://user:pass@host/dbname
```

2. Run the init script:
```powershell
python init_db.py
```

### Method 2: Using SQL directly

Connect to your PostgreSQL database and run:

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

## Step 8: Test Your Deployment

```powershell
# Your app is now live at the URL Vercel provided
# Example: https://traqcheck.vercel.app

# Test the API
curl https://your-app.vercel.app/api/health

# Or visit in browser
start https://your-app.vercel.app
```

## Troubleshooting

### If deployment fails:

**Check logs:**
```powershell
vercel logs
```

**Check environment variables:**
```powershell
vercel env ls
```

**Remove and re-add a variable:**
```powershell
vercel env rm OPENAI_API_KEY
vercel env add OPENAI_API_KEY
```

### If database connection fails:

1. Verify DATABASE_URL format:
   - Should be: `postgresql://user:password@host:port/database`
   - NOT: `postgres://` (Vercel auto-converts this)

2. Check if database allows external connections

3. Try adding `?sslmode=require` to the end:
   ```
   postgresql://user:pass@host/db?sslmode=require
   ```

### If build fails:

1. Check requirements.txt is correct
2. Ensure all files are committed to git
3. Try deploying again: `vercel --prod --force`

## Quick Command Reference

```powershell
# Deploy
vercel --prod

# View logs
vercel logs

# List projects
vercel ls

# List environment variables
vercel env ls

# Remove project (careful!)
vercel remove traqcheck

# Get deployment URL
vercel ls
```

## Success!

Your app should now be live! 🎉

Visit your Vercel URL and test:
1. Upload a resume
2. View candidates
3. Check candidate profile
4. Request documents

## Next Steps

1. **Custom Domain** (optional):
   ```powershell
   vercel domains add yourdomain.com
   ```

2. **Set up monitoring**:
   - Check Vercel Dashboard → Analytics
   - Set up error tracking (Sentry)

3. **Implement cloud storage**:
   - Files in /tmp are temporary
   - Use Vercel Blob, S3, or Cloudinary for production

---

Need help? Check:
- Vercel docs: https://vercel.com/docs
- Your deployment logs: `vercel logs`
- GitHub issues: Create one with error details
