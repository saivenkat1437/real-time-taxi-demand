#!/bin/bash

echo "🛑 Stopping Real-Time Taxi Demand Dashboard..."
echo "============================================================"

# Find and stop the demo process
PID=$(lsof -t -i :8050 2>/dev/null)

if [ ! -z "$PID" ]; then
    echo "🔍 Found dashboard process (PID: $PID)"
    echo "🛑 Stopping dashboard..."
    kill $PID
    
    # Wait a moment and check if it's stopped
    sleep 2
    if lsof -i :8050 > /dev/null 2>&1; then
        echo "⚠️  Process still running, force stopping..."
        kill -9 $PID
    fi
    
    echo "✅ Dashboard stopped successfully"
else
    echo "ℹ️  No dashboard process found on port 8050"
fi

# Also kill any python demo processes
DEMO_PIDS=$(pgrep -f "python.*demo.py" 2>/dev/null)
if [ ! -z "$DEMO_PIDS" ]; then
    echo "🛑 Stopping demo processes..."
    echo $DEMO_PIDS | xargs kill
    echo "✅ Demo processes stopped"
fi

echo ""
echo "📋 Status:"
if lsof -i :8050 > /dev/null 2>&1; then
    echo "❌ Dashboard is still running"
else
    echo "✅ Dashboard is stopped"
fi

echo ""
echo "💡 To restart: ./run_demo.sh" 