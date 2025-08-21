#!/bin/bash

# Alba Cars Scraper Suite Runner
# ==============================

echo "🚗 Alba Cars UAE Scraper Suite"
echo "=============================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "⚡ Installing dependencies..."
    pip install -r requirements.txt > /dev/null 2>&1
fi

# Run the main application
echo "🚀 Starting Alba Cars Scraper Suite..."
echo ""
python3 main.py

# Deactivate virtual environment
deactivate 