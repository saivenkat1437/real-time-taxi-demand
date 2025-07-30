#!/usr/bin/env python3
"""
Dataset Checking Script for Real-Time Taxi Demand Forecasting System
"""

import requests
import json
from datetime import datetime
from src.collectors.mock_data_generator import MockTaxiDataGenerator
from src.collectors.nyc_taxi_collector import NYCTaxiCollector
from src.utils.config import config

def check_nyc_api_dataset():
    """Check NYC API dataset"""
    print("🌐 NYC API DATASET CHECK")
    print("=" * 50)
    
    try:
        collector = NYCTaxiCollector()
        
        print(f"📋 Dataset ID: {collector.dataset_id}")
        print(f"🌐 API URL: {collector.base_url}/{collector.dataset_id}.json")
        print(f"📏 Limit: {collector.limit} records")
        
        # Test API connection
        print("\n🔍 Testing API connection...")
        url = f"{collector.base_url}/{collector.dataset_id}.json"
        params = {'$limit': 1}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API connection successful")
            print(f"📊 Retrieved {len(data)} sample records")
            
            if data:
                print("\n📋 Sample Record Structure:")
                sample = data[0]
                for key, value in list(sample.items())[:10]:  # Show first 10 fields
                    print(f"   • {key}: {value}")
                
                print(f"   • ... and {len(sample) - 10} more fields")
                
                return True
        else:
            print(f"❌ API connection failed: {response.status_code}")
            print(f"📋 Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Error checking NYC API dataset: {e}")
        return False

def check_mock_dataset():
    """Check mock dataset"""
    print("\n🎭 MOCK DATASET CHECK")
    print("=" * 50)
    
    try:
        generator = MockTaxiDataGenerator()
        
        print(f"📍 Location IDs: {len(generator.location_ids)} locations (1-50)")
        print(f"🚗 Vendor IDs: {generator.vendor_ids}")
        print(f"💳 Payment Types: {generator.payment_types}")
        
        # Generate sample data
        print("\n📊 Generating sample data...")
        taxi_data = generator.generate_taxi_data(count=5)
        heatmap_data = generator.get_demand_heatmap_data(hours=1)
        
        print(f"✅ Generated {len(taxi_data)} taxi trips")
        print(f"✅ Generated {len(heatmap_data)} heatmap locations")
        
        # Show sample data
        print("\n📋 Sample Taxi Trips:")
        for i, trip in enumerate(taxi_data[:3], 1):
            print(f"   Trip {i}:")
            print(f"     🆔 ID: {trip['trip_id']}")
            print(f"     📍 Pickup: Location {trip['pickup_location_id']} ({trip['pickup_latitude']:.4f}, {trip['pickup_longitude']:.4f})")
            print(f"     📍 Dropoff: Location {trip['dropoff_location_id']} ({trip['dropoff_latitude']:.4f}, {trip['dropoff_longitude']:.4f})")
            print(f"     💰 Fare: ${trip['fare_amount']:.2f}")
            print(f"     📏 Distance: {trip['trip_distance']:.2f} miles")
            print(f"     👥 Passengers: {trip['passenger_count']}")
            print(f"     🚗 Vendor: {trip['vendor_id']}")
            print()
        
        print("📋 Sample Heatmap Locations:")
        for i, location in enumerate(heatmap_data[:3], 1):
            print(f"   Location {i}:")
            print(f"     🆔 ID: {location['location_id']}")
            print(f"     📍 Coordinates: ({location['latitude']:.4f}, {location['longitude']:.4f})")
            print(f"     🚕 Trip Count: {location['trip_count']}")
            print(f"     💰 Total Fare: ${location['total_fare']:.2f}")
            print(f"     📊 Demand Level: {location['demand_level']}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking mock dataset: {e}")
        return False

def check_dataset_statistics():
    """Check dataset statistics"""
    print("\n📊 DATASET STATISTICS")
    print("=" * 50)
    
    try:
        generator = MockTaxiDataGenerator()
        
        # Generate larger sample for statistics
        taxi_data = generator.generate_taxi_data(count=100)
        heatmap_data = generator.get_demand_heatmap_data(hours=1)
        
        # Calculate statistics
        total_fare = sum(trip['fare_amount'] for trip in taxi_data)
        avg_fare = total_fare / len(taxi_data)
        total_distance = sum(trip['trip_distance'] for trip in taxi_data)
        avg_distance = total_distance / len(taxi_data)
        
        # Vendor distribution
        vendors = {}
        for trip in taxi_data:
            vendor = trip['vendor_id']
            vendors[vendor] = vendors.get(vendor, 0) + 1
        
        # Demand level distribution
        demand_levels = {}
        for location in heatmap_data:
            level = location['demand_level']
            demand_levels[level] = demand_levels.get(level, 0) + 1
        
        print(f"🚕 Total Trips: {len(taxi_data)}")
        print(f"💰 Total Fare: ${total_fare:.2f}")
        print(f"💰 Average Fare: ${avg_fare:.2f}")
        print(f"📏 Total Distance: {total_distance:.2f} miles")
        print(f"📏 Average Distance: {avg_distance:.2f} miles")
        print(f"📍 Total Locations: {len(heatmap_data)}")
        
        print(f"\n🚗 Vendor Distribution:")
        for vendor, count in vendors.items():
            percentage = (count / len(taxi_data)) * 100
            print(f"   {vendor}: {count} trips ({percentage:.1f}%)")
        
        print(f"\n📊 Demand Level Distribution:")
        for level, count in demand_levels.items():
            percentage = (count / len(heatmap_data)) * 100
            print(f"   {level.capitalize()}: {count} locations ({percentage:.1f}%)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error calculating statistics: {e}")
        return False

def check_dataset_quality():
    """Check dataset quality"""
    print("\n🔍 DATASET QUALITY CHECK")
    print("=" * 50)
    
    try:
        generator = MockTaxiDataGenerator()
        taxi_data = generator.generate_taxi_data(count=50)
        
        # Check data quality
        valid_records = 0
        required_fields = [
            'trip_id', 'pickup_datetime', 'dropoff_datetime',
            'pickup_location_id', 'dropoff_location_id',
            'passenger_count', 'trip_distance', 'fare_amount',
            'pickup_latitude', 'pickup_longitude',
            'dropoff_latitude', 'dropoff_longitude'
        ]
        
        for record in taxi_data:
            if all(field in record for field in required_fields):
                valid_records += 1
        
        quality_percentage = (valid_records / len(taxi_data)) * 100
        
        print(f"📊 Total Records: {len(taxi_data)}")
        print(f"✅ Valid Records: {valid_records}")
        print(f"📊 Data Quality: {quality_percentage:.1f}%")
        
        # Check coordinate ranges
        lat_range = [min(r['pickup_latitude'] for r in taxi_data), max(r['pickup_latitude'] for r in taxi_data)]
        lon_range = [min(r['pickup_longitude'] for r in taxi_data), max(r['pickup_longitude'] for r in taxi_data)]
        
        print(f"\n📍 Coordinate Ranges:")
        print(f"   Latitude: {lat_range[0]:.4f} to {lat_range[1]:.4f}")
        print(f"   Longitude: {lon_range[0]:.4f} to {lon_range[1]:.4f}")
        
        # Check if coordinates are in NYC area
        nyc_lat_range = (40.6, 40.9)
        nyc_lon_range = (-74.1, -73.7)
        
        lat_in_range = nyc_lat_range[0] <= lat_range[0] and lat_range[1] <= nyc_lat_range[1]
        lon_in_range = nyc_lon_range[0] <= lon_range[0] and lon_range[1] <= nyc_lon_range[1]
        
        print(f"\n🗽 NYC Area Validation:")
        print(f"   Latitude in NYC range: {'✅' if lat_in_range else '❌'}")
        print(f"   Longitude in NYC range: {'✅' if lon_in_range else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking data quality: {e}")
        return False

def main():
    """Main dataset checking function"""
    print("🚕 Real-Time Taxi Demand Forecasting System - Dataset Check")
    print("=" * 70)
    print(f"🕐 Check time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    checks = [
        ("NYC API Dataset", check_nyc_api_dataset),
        ("Mock Dataset", check_mock_dataset),
        ("Dataset Statistics", check_dataset_statistics),
        ("Dataset Quality", check_dataset_quality)
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
    print("\n" + "=" * 70)
    print("📋 DATASET CHECK SUMMARY")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All dataset checks passed! Data is ready for use.")
    else:
        print("⚠️  Some dataset checks failed. Mock data is available for testing.")
    
    print("\n💡 Quick Commands:")
    print("   📊 View data: python view_data.py")
    print("   🖥️  Start dashboard: ./run_demo.sh")
    print("   📋 Check logs: tail -20 logs/taxi_demand.log")

if __name__ == "__main__":
    main() 