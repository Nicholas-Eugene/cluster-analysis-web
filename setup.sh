#!/bin/bash

echo "🚀 Setting up Indonesian Regional Clustering Web Application"
echo "============================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Setup Backend
echo ""
echo "🔧 Setting up Backend (Django)..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗃️ Running database migrations..."
python manage.py migrate

echo "✅ Backend setup completed!"

# Setup Frontend
echo ""
echo "🎨 Setting up Frontend (Vue.js)..."
cd ../fuzzy-clustering-frontend

# Install Node.js dependencies
echo "📥 Installing Node.js dependencies..."
npm install

echo "✅ Frontend setup completed!"

# Final instructions
echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To start the application:"
echo ""
echo "1. Start the backend server:"
echo "   cd backend"
echo "   source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
echo "   python manage.py runserver"
echo "   Backend will be available at: http://localhost:8000"
echo ""
echo "2. In a new terminal, start the frontend server:"
echo "   cd fuzzy-clustering-frontend"
echo "   npm run dev"
echo "   Frontend will be available at: http://localhost:5173"
echo ""
echo "3. Open your browser and navigate to http://localhost:5173"
echo ""
echo "📊 Sample data is available at: backend/sample_data_indonesia.csv"
echo "📖 For more information, see README.md"
echo ""
echo "Happy clustering! 🎯"