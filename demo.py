#!/usr/bin/env python3
"""
Demo script for Real-Time Taxi Demand Forecasting System
Runs the dashboard with mock data for immediate testing
"""

import sys
import time
import logging
from src.utils.config import config
from src.dashboard.simple_dashboard import SimpleDashboard

def main():
    """Run the demo dashboard."""
    print("🚕 Real-Time Taxi Demand Forecasting System - Demo")
    print("=" * 60)
    print("📊 Starting dashboard with mock data...")
    print("🌐 Dashboard will be available at: http://localhost:8050")
    print("🔄 Data updates every 5 seconds")
    print("⏹️  Press Ctrl+C to stop")
    print("=" * 60)
    
    # Setup logging
    config.setup_logging()
    
    try:
        # Create and run dashboard
        dashboard = SimpleDashboard()
        
        print("✅ Dashboard initialized successfully!")
        print("🚀 Starting dashboard...")
        
        # Run the dashboard
        dashboard.run()
        
    except KeyboardInterrupt:
        print("\n🛑 Demo stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 