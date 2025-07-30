#!/usr/bin/env python3
"""
Test script for Real-Time Taxi Demand Forecasting System
"""

import sys
import time
import logging
from src.utils.config import config
from src.collectors.nyc_taxi_collector import NYCTaxiCollector
from src.collectors.kafka_producer import TaxiDataProducer

def test_nyc_collector():
    """Test NYC taxi data collector."""
    print("🧪 Testing NYC Taxi Collector...")
    
    try:
        collector = NYCTaxiCollector()
        
        # Test basic data fetching
        data = collector.fetch_taxi_data(limit=10)
        print(f"✅ Fetched {len(data)} taxi records")
        
        if data:
            print(f"📊 Sample record: {data[0]}")
        
        # Test heatmap data
        heatmap_data = collector.get_demand_heatmap_data(hours=1)
        print(f"🗺️ Generated heatmap data for {len(heatmap_data)} locations")
        
        return True
        
    except Exception as e:
        print(f"❌ NYC Collector test failed: {e}")
        return False

def test_kafka_producer():
    """Test Kafka producer."""
    print("🧪 Testing Kafka Producer...")
    
    try:
        producer = TaxiDataProducer()
        
        # Test with sample data
        sample_data = [{
            'trip_id': 'test_trip_1',
            'pickup_datetime': '2024-01-01T12:00:00',
            'pickup_location_id': 1,
            'fare_amount': 25.50,
            'trip_distance': 5.2,
            'passenger_count': 2
        }]
        
        success = producer.send_taxi_data(sample_data)
        print(f"✅ Kafka producer test: {'Success' if success else 'Failed'}")
        
        producer.close()
        return success
        
    except Exception as e:
        print(f"❌ Kafka Producer test failed: {e}")
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

def test_api_connectivity():
    """Test NYC API connectivity."""
    print("🧪 Testing NYC API Connectivity...")
    
    try:
        import requests
        
        api_config = config.get_nyc_api_config()
        url = f"{api_config['base_url']}/{api_config['dataset_id']}.json"
        params = {'$limit': 1}
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ NYC API connectivity: {len(data)} records received")
        
        return True
        
    except Exception as e:
        print(f"❌ NYC API connectivity test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚕 Real-Time Taxi Demand Forecasting System - Test Suite")
    print("=" * 60)
    
    # Setup logging
    config.setup_logging()
    
    tests = [
        ("Configuration", test_config),
        ("NYC API Connectivity", test_api_connectivity),
        ("NYC Taxi Collector", test_nyc_collector),
        ("Kafka Producer", test_kafka_producer),
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
    print(f"\n{'='*60}")
    print("📊 Test Results Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to run.")
        print("\n🚀 To start the system:")
        print("   1. Start Kafka: ./kafka_setup.sh")
        print("   2. Activate venv: source venv/bin/activate")
        print("   3. Run system: python src/main.py")
        print("   4. Open dashboard: http://localhost:8050")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 