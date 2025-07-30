#!/usr/bin/env python3
"""
Health Check Script for Real-Time Taxi Demand Forecasting System
"""

import requests
import time
import json
import sys
from datetime import datetime

def check_dashboard_availability():
    """Check if the dashboard is accessible"""
    print("🔍 Checking dashboard availability...")
    try:
        response = requests.get("http://localhost:8050", timeout=5)
        if response.status_code == 200:
            print("✅ Dashboard is accessible at http://localhost:8050")
            return True
        else:
            print(f"❌ Dashboard returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Dashboard is not accessible - connection refused")
        return False
    except Exception as e:
        print(f"❌ Error checking dashboard: {e}")
        return False

def check_dashboard_data():
    """Check if the dashboard is serving data"""
    print("📊 Checking dashboard data endpoints...")
    try:
        # Check if the dashboard is serving the main page
        response = requests.get("http://localhost:8050", timeout=5)
        if "Real-Time Taxi Demand" in response.text:
            print("✅ Dashboard is serving the main page")
        else:
            print("⚠️  Dashboard page content seems unusual")
        
        return True
    except Exception as e:
        print(f"❌ Error checking dashboard data: {e}")
        return False

def check_system_components():
    """Check if all system components are working"""
    print("🔧 Checking system components...")
    
    # Test imports
    try:
        from src.utils.config import config
        print("✅ Configuration module loaded")
    except Exception as e:
        print(f"❌ Configuration module error: {e}")
        return False
    
    try:
        from src.collectors.mock_data_generator import MockTaxiDataGenerator
        generator = MockTaxiDataGenerator()
        taxi_data = generator.generate_taxi_data(count=5)
        if len(taxi_data) == 5:
            print("✅ Mock data generator working")
        else:
            print("❌ Mock data generator not producing expected data")
            return False
    except Exception as e:
        print(f"❌ Mock data generator error: {e}")
        return False
    
    try:
        from src.dashboard.simple_dashboard import SimpleDashboard
        dashboard = SimpleDashboard()
        print("✅ Dashboard component initialized")
    except Exception as e:
        print(f"❌ Dashboard component error: {e}")
        return False
    
    return True

def check_virtual_environment():
    """Check if virtual environment is active"""
    print("🐍 Checking virtual environment...")
    import sys
    if "venv" in sys.executable:
        print("✅ Virtual environment is active")
        return True
    else:
        print("❌ Virtual environment is not active")
        print("   Run: source venv/bin/activate")
        return False

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("📦 Checking dependencies...")
    
    required_packages = [
        'dash', 'plotly', 'pandas', 'numpy', 'requests',
        'flask', 'kafka', 'pyspark'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required dependencies are installed")
        return True

def run_performance_test():
    """Run a quick performance test"""
    print("⚡ Running performance test...")
    
    try:
        from src.collectors.mock_data_generator import MockTaxiDataGenerator
        generator = MockTaxiDataGenerator()
        
        start_time = time.time()
        for i in range(10):
            data = generator.generate_taxi_data(count=100)
            heatmap = generator.get_demand_heatmap_data(hours=1)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if duration < 5.0:  # Should complete in under 5 seconds
            print(f"✅ Performance test passed ({duration:.2f}s)")
            return True
        else:
            print(f"⚠️  Performance test slow ({duration:.2f}s)")
            return False
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def main():
    """Run comprehensive health check"""
    print("🚕 Real-Time Taxi Demand Forecasting System - Health Check")
    print("=" * 60)
    print(f"🕐 Check time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    checks = [
        ("Virtual Environment", check_virtual_environment),
        ("Dependencies", check_dependencies),
        ("System Components", check_system_components),
        ("Dashboard Availability", check_dashboard_availability),
        ("Dashboard Data", check_dashboard_data),
        ("Performance", run_performance_test)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        print(f"\n{'='*20} {check_name} {'='*20}")
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} check failed with exception: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📋 HEALTH CHECK SUMMARY")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 ALL CHECKS PASSED! System is running smoothly.")
        print("\n🌐 Access your dashboard at: http://localhost:8050")
        print("📊 The dashboard updates every 5 seconds with mock data")
        return 0
    else:
        print("⚠️  Some checks failed. Please review the issues above.")
        print("\n💡 Quick fixes:")
        print("   - Activate venv: source venv/bin/activate")
        print("   - Install deps: pip install -r requirements.txt")
        print("   - Start demo: ./run_demo.sh")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 