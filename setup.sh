#!/bin/bash
# Setup script for Japanese Subtitle Generator

echo "=========================================="
echo "Japanese Subtitle Generator - Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check FFmpeg
echo ""
echo "Checking FFmpeg..."
ffmpeg -version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ FFmpeg is not installed."
    echo "Please install FFmpeg:"
    echo "  macOS: brew install ffmpeg"
    echo "  Linux: sudo apt install ffmpeg"
    exit 1
fi
echo "✓ FFmpeg found"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi
echo "✓ Virtual environment created"

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing dependencies..."
echo "This may take a few minutes..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "=========================================="
echo "✓ Setup complete!"
echo "=========================================="
echo ""
echo "To run the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the app: python main.py"
echo ""
echo "To deactivate virtual environment:"
echo "  deactivate"
echo ""
