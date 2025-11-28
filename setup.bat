@echo off
echo ========================================
echo TraqCheck Setup Script
echo ========================================
echo.

echo Step 1: Setting up Backend...
cd backend

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing Python dependencies...
pip install -r requirements.txt

echo Creating .env file...
if not exist .env (
    copy .env.example .env
    echo.
    echo ==========================================
    echo IMPORTANT: Edit backend\.env file and add your OpenAI API key!
    echo ==========================================
    echo.
)

cd ..

echo.
echo Step 2: Setting up Frontend...
cd frontend

echo Installing Node.js dependencies...
call npm install

cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Edit backend\.env and add your OPENAI_API_KEY
echo 2. Open TWO terminal windows:
echo.
echo    Terminal 1 - Backend:
echo    cd backend
echo    venv\Scripts\activate
echo    python app.py
echo.
echo    Terminal 2 - Frontend:
echo    cd frontend
echo    npm start
echo.
echo 3. Browser will open at http://localhost:3000
echo.
echo For detailed instructions, see QUICKSTART.md
echo ========================================
pause
