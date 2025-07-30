#!/bin/bash

echo "🚕 Real-Time Taxi Demand Forecasting System - Status Check"
echo "============================================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run: ./setup.sh"
    exit 1
fi

# Check if dashboard is running
echo "🔍 Checking dashboard status..."
if curl -s http://localhost:8050 > /dev/null 2>&1; then
    echo "✅ Dashboard is running at http://localhost:8050"
    echo "📊 Dashboard is accessible and serving data"
else
    echo "❌ Dashboard is not running"
    echo "   Start it with: ./run_demo.sh"
fi

# Check if port 8050 is in use
echo "🔍 Checking port 8050..."
if lsof -i :8050 > /dev/null 2>&1; then
    echo "✅ Port 8050 is active"
    PID=$(lsof -t -i :8050 2>/dev/null)
    if [ ! -z "$PID" ]; then
        echo "   Process ID: $PID"
    fi
else
    echo "❌ Port 8050 is not in use"
fi

# Check virtual environment
echo "🔍 Checking virtual environment..."
if [[ "$VIRTUAL_ENV" == *"venv"* ]]; then
    echo "✅ Virtual environment is active"
else
    echo "⚠️  Virtual environment is not active"
    echo "   Activate with: source venv/bin/activate"
fi

# Run health check if virtual environment is active
if [[ "$VIRTUAL_ENV" == *"venv"* ]]; then
    echo ""
    echo "🔧 Running comprehensive health check..."
    python health_check.py
else
    echo ""
    echo "💡 To run full health check:"
    echo "   source venv/bin/activate && python health_check.py"
fi

echo ""
echo "📋 Quick Commands:"
echo "   Start demo: ./run_demo.sh"
echo "   Health check: source venv/bin/activate && python health_check.py"
echo "   Stop dashboard: pkill -f 'python.*demo.py'"
echo "   View logs: tail -f logs/taxi_demand.log" 