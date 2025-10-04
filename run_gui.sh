#!/bin/bash

# TikTok Song Extractor - GUI Launcher
# This script launches the TikTok Song Extractor with GUI

echo "🎵 TikTok Song Extractor"
echo "========================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Check if tkinter is available
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ tkinter is not available. Please install tkinter:"
    echo "   Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "   CentOS/RHEL: sudo yum install tkinter"
    echo "   macOS: tkinter should be included with Python"
    exit 1
fi

# Install requirements if needed
if [ -f "requirements.txt" ]; then
    echo "📦 Installing requirements..."
    pip3 install -r requirements.txt
fi

echo "🚀 Starting TikTok Song Extractor GUI..."
echo ""

# Run the application
python3 tiktok_song_extractor.py