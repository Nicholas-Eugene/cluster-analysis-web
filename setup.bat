@echo off
echo 🚀 Setting up Indonesian Regional Clustering Web Application
echo =============================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3 is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ first.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed

REM Setup Backend
echo.
echo 🔧 Setting up Backend (Django)...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo 📥 Installing Python dependencies...
pip install -r requirements.txt

REM Run migrations
echo 🗃️ Running database migrations...
python manage.py migrate

echo ✅ Backend setup completed!

REM Setup Frontend
echo.
echo 🎨 Setting up Frontend (Vue.js)...
cd ..\fuzzy-clustering-frontend

REM Install Node.js dependencies
echo 📥 Installing Node.js dependencies...
npm install

echo ✅ Frontend setup completed!

REM Final instructions
echo.
echo 🎉 Setup completed successfully!
echo.
echo To start the application:
echo.
echo 1. Start the backend server:
echo    cd backend
echo    venv\Scripts\activate.bat
echo    python manage.py runserver
echo    Backend will be available at: http://localhost:8000
echo.
echo 2. In a new terminal, start the frontend server:
echo    cd fuzzy-clustering-frontend
echo    npm run dev
echo    Frontend will be available at: http://localhost:5173
echo.
echo 3. Open your browser and navigate to http://localhost:5173
echo.
echo 📊 Sample data is available at: backend\sample_data_indonesia.csv
echo 📖 For more information, see README.md
echo.
echo Happy clustering! 🎯
pause