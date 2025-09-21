#!/bin/bash

echo "🚀 Setting up Picture to Text OCR App..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Install Tesseract OCR
echo "📦 Installing Tesseract OCR..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt update && sudo apt install -y tesseract-ocr
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install tesseract
else
    echo "⚠️  Please install Tesseract OCR manually for your OS"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

echo "✅ Setup complete! Run 'python3 app.py' to start the app."