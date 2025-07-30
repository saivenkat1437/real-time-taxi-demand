#!/usr/bin/env python3
"""
Simple test script for Real-Time Taxi Demand Forecasting System
(Works without Kafka for basic functionality testing)
"""

import sys
import time
import logging
from src.utils.config import config
from src.collectors.mock_data_generator import MockTaxiDataGenerator
from src.dashboard.simple_dashboard import SimpleDashboard

def test_mock_generator():
    """Test mock data generator."""
    print("🧪 Testing Mock Data Generator...")
    
    try:
        generator = MockTaxiDataGenerator()
        
        # Test basic data generation
        data = generator.generate_taxi_data(count=10)
        print(f"✅ Generated {len(data)} mock taxi records")
        
        if data:
            print(f"📊 Sample record: {data[0]}")
        
        # Test heatmap data
        heatmap_data = generator.get_demand_heatmap_data(hours=1)
        print(f"🗺️ Generated heatmap data for {len(heatmap_data)} locations")
        
        # Test location demand
        location_demand = generator.get_demand_by_location(1, hours=1)
        print(f"📍 Location demand data: {location_demand}")
        
        return True
        
    except Exception as e:
        print(f"❌ Mock Generator test failed: {e}")
        return False

def test_config():
    """Test configuration loading."""
    print("🧪 Testing Configuration...")
    
    try:
        # Test config loading
        kafka_config = config.get_kafka_config()
        nyc_config = config.get_nyc_api_config()
        dashboard_config = config.get_dashboard_config()
        
        print(f"✅ Kafka config: {kafka_config['bootstrap_servers']}")
        print(f"✅ NYC API config: {nyc_config['base_url']}")
        print(f"✅ Dashboard config: {dashboard_config['host']}:{dashboard_config['port']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_dashboard():
    """Test dashboard initialization."""
    print("🧪 Testing Dashboard...")
    
    try:
        # Test dashboard creation (without starting it)
        dashboard = SimpleDashboard()
        print("✅ Simple Dashboard initialized successfully")
        
        # Test dashboard layout
        if hasattr(dashboard, 'app') and dashboard.app:
            print("✅ Dashboard app created")
            return True
        else:
            print("❌ Dashboard app not created")
            return False
        
    except Exception as e:
        print(f"❌ Simple Dashboard test failed: {e}")
        return False

def test_mock_data_flow():
    """Test the complete data flow with mock data."""
    print("🧪 Testing Mock Data Flow...")
    
    try:
        generator = MockTaxiDataGenerator()
        
        # Generate data
        taxi_data = generator.generate_taxi_data(count=50)
        heatmap_data = generator.get_demand_heatmap_data(hours=1)
        
        print(f"✅ Generated {len(taxi_data)} taxi records")
        print(f"✅ Generated {len(heatmap_data)} heatmap points")
        
        # Test data processing
        total_trips = sum(record.get('trip_count', 1) for record in taxi_data)
        total_fare = sum(record.get('fare_amount', 0) for record in taxi_data)
        avg_fare = total_fare / len(taxi_data) if taxi_data else 0
        
        print(f"📊 Total trips: {total_trips}")
        print(f"💰 Total fare: ${total_fare:.2f}")
        print(f"📈 Average fare: ${avg_fare:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Mock data flow test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚕 Real-Time Taxi Demand Forecasting System - Simple Test Suite")
    print("=" * 70)
    
    # Setup logging
    config.setup_logging()
    
    tests = [
        ("Configuration", test_config),
        ("Mock Data Generator", test_mock_generator),
        ("Dashboard", test_dashboard),
        ("Mock Data Flow", test_mock_data_flow),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*70}")
    print("📊 Test Results Summary:")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for development.")
        print("\n🚀 To run the system with mock data:")
        print("   1. Activate venv: source venv/bin/activate")
        print("   2. Run with mock data: python src/main.py --mock")
        print("   3. Open dashboard: http://localhost:8050")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 