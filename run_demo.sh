#!/bin/bash

echo "🚕 Real-Time Taxi Demand Forecasting System - Demo Runner"
echo "============================================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run './setup.sh' first to set up the environment."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if demo.py exists
if [ ! -f "demo.py" ]; then
    echo "❌ demo.py not found!"
    exit 1
fi

echo "🚀 Starting demo dashboard..."
echo "📊 Dashboard will be available at: http://localhost:8050"
echo "⏹️  Press Ctrl+C to stop"
echo "============================================================"

# Run the demo
python demo.py 