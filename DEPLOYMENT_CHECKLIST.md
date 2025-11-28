# Vercel Deployment Checklist

Use this checklist to ensure smooth deployment to Vercel.

## ✅ Pre-Deployment Checklist

### 1. Code Ready
- [ ] All code committed to Git
- [ ] Code pushed to GitHub
- [ ] No sensitive data in code (API keys, passwords)
- [ ] `.gitignore` includes `venv/`, `node_modules/`, `.env`

### 2. Dependencies
- [ ] `requirements.txt` is up to date
- [ ] `frontend/package.json` is up to date
- [ ] All imports work correctly
- [ ] No circular dependencies

### 3. Configuration Files
- [ ] `vercel.json` exists in root
- [ ] `.vercelignore` exists in root
- [ ] `api/index.py` exists
- [ ] `frontend/.env.production` exists

### 4. External Services
- [ ] PostgreSQL database created (Neon/Supabase/Railway)
- [ ] Database connection string obtained
- [ ] OpenAI API key ready
- [ ] All API keys tested and valid

## 🚀 Deployment Steps

### Step 1: GitHub Setup
```bash
# Ensure everything is committed
git status

# Commit if needed
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```
- [ ] Code pushed to GitHub
- [ ] Repository is public or Vercel has access

### Step 2: Vercel Project Setup
1. [ ] Go to [vercel.com/new](https://vercel.com/new)
2. [ ] Click "Import" on your repository
3. [ ] Select repository
4. [ ] Click "Import"

### Step 3: Configure Build Settings
- [ ] Framework Preset: **Other**
- [ ] Root Directory: `./` (leave blank)
- [ ] Build Command: Leave empty
- [ ] Output Directory: Leave empty
- [ ] Install Command: Leave empty

### Step 4: Environment Variables
Add these environment variables in Vercel dashboard:

- [ ] `OPENAI_API_KEY` = `sk-...` (your actual key)
- [ ] `DATABASE_URL` = `postgresql://user:pass@host/dbname`
- [ ] `SECRET_KEY` = `<random-string-here>`
- [ ] `VERCEL` = `1`

**Environment for:** Production, Preview, Development (select all)

### Step 5: Deploy
- [ ] Click "Deploy"
- [ ] Wait for build to complete (2-3 minutes)
- [ ] Check for build errors

### Step 6: Initialize Database
After first deployment:

**Option A: Run SQL directly in your database**
```sql
-- Copy SQL from VERCEL_DEPLOYMENT.md
-- Execute in your PostgreSQL client
```
- [ ] SQL executed successfully
- [ ] Tables created

**Option B: Use init script**
```bash
# Set DATABASE_URL in your local .env
cd Traqcheck
python init_db.py
```
- [ ] Script ran successfully
- [ ] Tables verified

### Step 7: Test Deployment
- [ ] Visit your Vercel URL
- [ ] Homepage loads correctly
- [ ] Test API health: `https://your-app.vercel.app/api/health`
- [ ] Try uploading a resume
- [ ] Check candidate appears in dashboard
- [ ] View candidate profile
- [ ] Test document request generation

## 🧪 Post-Deployment Testing

### Frontend Tests
- [ ] Homepage loads
- [ ] Upload button works
- [ ] Dashboard displays
- [ ] Candidate table visible
- [ ] Navigation works
- [ ] Styling looks correct
- [ ] No console errors

### API Tests
```bash
# Health check
curl https://your-app.vercel.app/api/health

# Upload resume (use actual file)
curl -X POST -F "resume=@test.pdf" https://your-app.vercel.app/api/candidates/upload

# Get candidates
curl https://your-app.vercel.app/api/candidates
```

- [ ] Health check returns 200
- [ ] Upload works
- [ ] Can retrieve candidates

### Database Tests
- [ ] Data persists between requests
- [ ] No duplicate entries
- [ ] Foreign keys work correctly
- [ ] Queries are fast (<1s)

## 🔧 Troubleshooting

### Build Fails
**Error:** `Module not found`
- [ ] Check `requirements.txt` has all packages
- [ ] Verify versions are compatible
- [ ] Check `package.json` in frontend

**Error:** `Build timeout`
- [ ] Remove unused dependencies
- [ ] Optimize build process

### Runtime Errors
**Error:** `500 Internal Server Error`
- [ ] Check Vercel function logs
- [ ] Verify environment variables set
- [ ] Test API endpoint exists

**Error:** `Database connection failed`
- [ ] Verify DATABASE_URL is correct
- [ ] Check database accepts external connections
- [ ] Add `?sslmode=require` to connection string if needed

**Error:** `CORS issues`
- [ ] Check Flask-CORS is installed
- [ ] Verify CORS configuration in app.py

### File Upload Issues
**Error:** `Permission denied` or `No such file or directory`
- [ ] Normal - `/tmp` is created on first use
- [ ] Files in `/tmp` are temporary
- [ ] Consider implementing cloud storage

## 📊 Monitoring

### Check Logs
- [ ] Vercel Dashboard → Deployments → Runtime Logs
- [ ] Check for errors
- [ ] Monitor response times

### Performance
- [ ] Dashboard → Analytics
- [ ] Check function duration
- [ ] Monitor bandwidth usage
- [ ] Review error rate

## 🎯 Optional Enhancements

### Custom Domain
- [ ] Purchase domain
- [ ] Add to Vercel project
- [ ] Update DNS records
- [ ] Wait for SSL certificate

### Cloud Storage (Recommended)
Since `/tmp` is ephemeral, implement cloud storage:

- [ ] Set up Vercel Blob, S3, or Cloudinary
- [ ] Update upload logic in `app.py`
- [ ] Test file persistence
- [ ] Update download logic

### Monitoring & Alerts
- [ ] Set up Sentry for error tracking
- [ ] Configure uptime monitoring
- [ ] Set up email alerts
- [ ] Add analytics (Google Analytics, Plausible)

### Security
- [ ] Enable rate limiting
- [ ] Add authentication (optional)
- [ ] Review CORS settings
- [ ] Audit environment variables

### CI/CD
- [ ] Set up automated tests
- [ ] Configure pre-deployment checks
- [ ] Add staging environment
- [ ] Set up preview deployments

## 🎉 Success Criteria

Deployment is successful when:

- [x] Build completes without errors
- [x] Frontend loads at Vercel URL
- [x] API health check returns 200
- [x] Can upload resume successfully
- [x] Data persists in database
- [x] No errors in logs
- [x] All features working as expected

## 📝 Notes

**Important:**
- Files in `/tmp` are deleted after function execution
- Implement cloud storage for production use
- Monitor function execution time (max 10s on free tier)
- Database connection pooling recommended for high traffic

**Cost Considerations:**
- Vercel Hobby: Free for personal projects
- Database: Free tiers available (Neon, Supabase)
- OpenAI: Pay-per-use

## 🆘 Support

If you encounter issues:

1. Check [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) for detailed guide
2. Review Vercel function logs
3. Test locally first
4. Check [Vercel Documentation](https://vercel.com/docs)
5. Create GitHub issue with:
   - Error message
   - Steps to reproduce
   - Vercel logs
   - Environment details

---

**Last Updated:** November 28, 2025  
**Version:** 1.0.0
