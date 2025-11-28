# Quick Setup Script - Run this after deployment

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  TraqCheck - Post-Deployment Setup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Step 1: Database Setup
Write-Host "Step 1: Database Setup`n" -ForegroundColor Yellow
Write-Host "Choose a PostgreSQL provider:" -ForegroundColor White
Write-Host "  1. Neon (Recommended - Free)" -ForegroundColor Green
Write-Host "  2. Supabase (Free)" -ForegroundColor Green
Write-Host "  3. Railway (Paid)" -ForegroundColor Yellow
Write-Host "`nOpen one of these URLs:" -ForegroundColor White
Write-Host "  Neon:     https://console.neon.tech/signup" -ForegroundColor Cyan
Write-Host "  Supabase: https://supabase.com/dashboard" -ForegroundColor Cyan
Write-Host "  Railway:  https://railway.app" -ForegroundColor Cyan
Write-Host "`nCreate a database and copy the connection string.`n" -ForegroundColor White

$databaseUrl = Read-Host "Paste your DATABASE_URL here (postgresql://...)"

if ([string]::IsNullOrWhiteSpace($databaseUrl)) {
    Write-Host "`nNo database URL provided. Exiting..." -ForegroundColor Red
    exit
}

# Step 2: Add Environment Variables
Write-Host "`nStep 2: Adding Environment Variables...`n" -ForegroundColor Yellow

Write-Host "Adding DATABASE_URL..." -ForegroundColor White
$env:DATABASE_URL = $databaseUrl
vercel env add DATABASE_URL production <<< $databaseUrl

Write-Host "`nEnter your OpenAI API Key (sk-...):" -ForegroundColor White
$openaiKey = Read-Host -AsSecureString
$openaiKeyPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($openaiKey))
vercel env add OPENAI_API_KEY production <<< $openaiKeyPlain

Write-Host "`nAdding SECRET_KEY..." -ForegroundColor White
$secretKey = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
vercel env add SECRET_KEY production <<< $secretKey

Write-Host "`nAdding VERCEL flag..." -ForegroundColor White
vercel env add VERCEL production <<< "1"

# Step 3: Initialize Database
Write-Host "`nStep 3: Initialize Database...`n" -ForegroundColor Yellow
Write-Host "Creating database tables..." -ForegroundColor White

# Create .env file for local testing
@"
DATABASE_URL=$databaseUrl
OPENAI_API_KEY=$openaiKeyPlain
SECRET_KEY=$secretKey
"@ | Out-File -FilePath "backend\.env" -Encoding UTF8

# Run init script
python init_db.py

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "Your app is live at:" -ForegroundColor White
Write-Host "https://traqcheck.vercel.app`n" -ForegroundColor Cyan

Write-Host "Test it:" -ForegroundColor White
Write-Host "  curl https://traqcheck.vercel.app/api/health`n" -ForegroundColor Gray

Write-Host "Press any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
