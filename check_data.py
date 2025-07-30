#!/usr/bin/env python3
"""
Data Checking Script for Real-Time Taxi Demand Forecasting System
"""

import json
import os
import sys
from datetime import datetime
from src.collectors.mock_data_generator import MockTaxiDataGenerator
from src.utils.config import config

def check_mock_data():
    """Check mock data generation"""
    print("🔍 Checking Mock Data Generation...")
    print("=" * 50)
    
    try:
        generator = MockTaxiDataGenerator()
        
        # Generate sample data
        taxi_data = generator.generate_taxi_data(count=5)
        heatmap_data = generator.get_demand_heatmap_data(hours=1)
        location_data = generator.get_location_demand_data()
        
        print(f"✅ Taxi Records Generated: {len(taxi_data)}")
        print(f"✅ Heatmap Locations: {len(heatmap_data)}")
        print(f"✅ Location Demand Points: {len(location_data)}")
        
        # Show sample data
        if taxi_data:
            print("\n📊 Sample Taxi Record:")
            sample = taxi_data[0]
            for key, value in sample.items():
                print(f"   {key}: {value}")
        
        if heatmap_data:
            print(f"\n🗺️  Sample Heatmap Data:")
            sample = heatmap_data[0]
            print(f"   Location: ({sample['lat']}, {sample['lng']})")
            print(f"   Demand Level: {sample['demand_level']}")
            print(f"   Color: {sample['color']}")
        
        return True
    except Exception as e:
        print(f"❌ Error generating mock data: {e}")
        return False

def check_logs():
    """Check system logs"""
    print("\n📋 Checking System Logs...")
    print("=" * 50)
    
    log_file = "logs/taxi_demand.log"
    if os.path.exists(log_file):
        print(f"✅ Log file exists: {log_file}")
        
        # Get file size
        size = os.path.getsize(log_file)
        print(f"📏 Log file size: {size} bytes")
        
        # Show last few lines
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()
                print(f"📝 Total log lines: {len(lines)}")
                
                if lines:
                    print("\n🕐 Last 5 log entries:")
                    for line in lines[-5:]:
                        print(f"   {line.strip()}")
        except Exception as e:
            print(f"❌ Error reading log file: {e}")
    else:
        print("⚠️  Log file not found")

def check_configuration():
    """Check system configuration"""
    print("\n⚙️  Checking System Configuration...")
    print("=" * 50)
    
    try:
        # Load configuration
        cfg = config
        
        print("✅ Configuration loaded successfully")
        print(f"📊 Dashboard Host: {cfg.dashboard_config['host']}")
        print(f"📊 Dashboard Port: {cfg.dashboard_config['port']}")
        print(f"📊 Kafka Bootstrap Servers: {cfg.kafka_config['bootstrap_servers']}")
        print(f"📊 NYC API Dataset ID: {cfg.nyc_api_config['dataset_id']}")
        
        return True
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return False

def check_data_structure():
    """Check data directory structure"""
    print("\n📁 Checking Data Directory Structure...")
    print("=" * 50)
    
    directories = ['data', 'logs', 'config']
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"✅ {directory}/ directory exists")
            files = os.listdir(directory)
            if files:
                print(f"   📄 Files: {', '.join(files)}")
            else:
                print(f"   📄 Empty directory")
        else:
            print(f"⚠️  {directory}/ directory not found")

def check_real_time_data():
    """Check if real-time data is being generated"""
    print("\n🔄 Checking Real-Time Data Generation...")
    print("=" * 50)
    
    try:
        generator = MockTaxiDataGenerator()
        
        print("🔄 Generating real-time data samples...")
        
        # Generate multiple samples
        for i in range(3):
            taxi_data = generator.generate_taxi_data(count=3)
            heatmap_data = generator.get_demand_heatmap_data(hours=1)
            
            print(f"   Sample {i+1}: {len(taxi_data)} taxi records, {len(heatmap_data)} heatmap points")
            
            # Show a sample record
            if taxi_data:
                sample = taxi_data[0]
                print(f"      Sample trip: {sample['pickup_location']} → {sample['dropoff_location']}")
                print(f"      Fare: ${sample['fare_amount']:.2f}")
        
        print("✅ Real-time data generation working properly")
        return True
    except Exception as e:
        print(f"❌ Error in real-time data generation: {e}")
        return False

def check_data_quality():
    """Check data quality and validation"""
    print("\n🔍 Checking Data Quality...")
    print("=" * 50)
    
    try:
        generator = MockTaxiDataGenerator()
        taxi_data = generator.generate_taxi_data(count=10)
        
        # Check data quality
        valid_records = 0
        total_fare = 0
        locations = set()
        
        for record in taxi_data:
            # Check required fields
            required_fields = ['pickup_location', 'dropoff_location', 'fare_amount', 'trip_duration']
            if all(field in record for field in required_fields):
                valid_records += 1
                total_fare += record['fare_amount']
                locations.add(record['pickup_location'])
                locations.add(record['dropoff_location'])
        
        print(f"✅ Valid Records: {valid_records}/{len(taxi_data)}")
        print(f"💰 Average Fare: ${total_fare/len(taxi_data):.2f}")
        print(f"📍 Unique Locations: {len(locations)}")
        print(f"📊 Data Quality: {(valid_records/len(taxi_data)*100):.1f}%")
        
        return True
    except Exception as e:
        print(f"❌ Error in data quality check: {e}")
        return False

def main():
    """Run comprehensive data check"""
    print("🚕 Real-Time Taxi Demand Forecasting System - Data Check")
    print("=" * 60)
    print(f"🕐 Check time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    checks = [
        ("Mock Data Generation", check_mock_data),
        ("System Logs", check_logs),
        ("Configuration", check_configuration),
        ("Data Structure", check_data_structure),
        ("Real-Time Data", check_real_time_data),
        ("Data Quality", check_data_quality)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} check failed: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 DATA CHECK SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All data checks passed! System is ready.")
    else:
        print("⚠️  Some data checks failed. Please review the issues above.")
    
    print("\n💡 To view live data:")
    print("   ./run_demo.sh  # Start the dashboard")
    print("   http://localhost:8050  # View in browser")

if __name__ == "__main__":
    main() 