@echo off
echo ========================================
echo   TraqCheck - Vercel Deployment Script
echo ========================================
echo.

REM Check if vercel CLI is installed
where vercel >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing Vercel CLI...
    call npm install -g vercel
)

echo.
echo Step 1: Login to Vercel
echo ------------------------
call vercel login

echo.
echo Step 2: Deploy to Vercel
echo ------------------------
call vercel --prod

echo.
echo ========================================
echo   Deployment Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Get your PostgreSQL database URL from Neon/Supabase
echo 2. Add environment variables to Vercel:
echo    - OPENAI_API_KEY
echo    - DATABASE_URL
echo    - SECRET_KEY
echo    - VERCEL=1
echo.
echo Run: vercel env add OPENAI_API_KEY
echo Then: vercel env add DATABASE_URL
echo Then: vercel env add SECRET_KEY
echo Then: vercel env add VERCEL
echo.
pause
