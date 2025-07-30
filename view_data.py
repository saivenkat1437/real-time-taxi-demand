#!/usr/bin/env python3
"""
Simple Data Viewer for Real-Time Taxi Demand Forecasting System
"""

from src.collectors.mock_data_generator import MockTaxiDataGenerator
from datetime import datetime

def view_taxi_data():
    """View sample taxi data"""
    print("🚕 TAXI TRIP DATA")
    print("=" * 50)
    
    generator = MockTaxiDataGenerator()
    taxi_data = generator.generate_taxi_data(count=5)
    
    for i, trip in enumerate(taxi_data, 1):
        print(f"\n📊 Trip {i}:")
        print(f"   🆔 Trip ID: {trip['trip_id']}")
        print(f"   📍 Pickup: Location {trip['pickup_location_id']} ({trip['pickup_latitude']:.4f}, {trip['pickup_longitude']:.4f})")
        print(f"   📍 Dropoff: Location {trip['dropoff_location_id']} ({trip['dropoff_latitude']:.4f}, {trip['dropoff_longitude']:.4f})")
        print(f"   👥 Passengers: {trip['passenger_count']}")
        print(f"   📏 Distance: {trip['trip_distance']:.2f} miles")
        print(f"   💰 Fare: ${trip['fare_amount']:.2f}")
        print(f"   💰 Tip: ${trip['tip_amount']:.2f}")
        print(f"   💰 Total: ${trip['total_amount']:.2f}")
        print(f"   🕐 Pickup: {trip['pickup_datetime']}")
        print(f"   🕐 Dropoff: {trip['dropoff_datetime']}")
        print(f"   🚗 Vendor: {trip['vendor_id']}")

def view_heatmap_data():
    """View heatmap data"""
    print("\n🗺️  HEATMAP DATA")
    print("=" * 50)
    
    generator = MockTaxiDataGenerator()
    heatmap_data = generator.get_demand_heatmap_data(hours=1)
    
    print(f"📍 Total Locations: {len(heatmap_data)}")
    
    for i, location in enumerate(heatmap_data[:10], 1):  # Show first 10
        print(f"\n📍 Location {i}:")
        print(f"   🆔 Location ID: {location['location_id']}")
        print(f"   📍 Coordinates: ({location['latitude']:.4f}, {location['longitude']:.4f})")
        print(f"   🚕 Trip Count: {location['trip_count']}")
        print(f"   💰 Total Fare: ${location['total_fare']:.2f}")
        print(f"   💰 Average Fare: ${location['avg_fare']:.2f}")
        print(f"   📊 Demand Level: {location['demand_level']}")

def view_statistics():
    """View data statistics"""
    print("\n📊 DATA STATISTICS")
    print("=" * 50)
    
    generator = MockTaxiDataGenerator()
    taxi_data = generator.generate_taxi_data(count=20)
    heatmap_data = generator.get_demand_heatmap_data(hours=1)
    
    # Calculate statistics
    total_fare = sum(trip['fare_amount'] for trip in taxi_data)
    avg_fare = total_fare / len(taxi_data)
    total_distance = sum(trip['trip_distance'] for trip in taxi_data)
    avg_distance = total_distance / len(taxi_data)
    total_passengers = sum(trip['passenger_count'] for trip in taxi_data)
    
    # Demand levels
    demand_levels = {}
    for location in heatmap_data:
        level = location['demand_level']
        demand_levels[level] = demand_levels.get(level, 0) + 1
    
    print(f"🚕 Total Trips: {len(taxi_data)}")
    print(f"💰 Total Fare: ${total_fare:.2f}")
    print(f"💰 Average Fare: ${avg_fare:.2f}")
    print(f"📏 Total Distance: {total_distance:.2f} miles")
    print(f"📏 Average Distance: {avg_distance:.2f} miles")
    print(f"👥 Total Passengers: {total_passengers}")
    print(f"📍 Total Locations: {len(heatmap_data)}")
    
    print(f"\n📊 Demand Distribution:")
    for level, count in demand_levels.items():
        print(f"   {level.capitalize()}: {count} locations")

def main():
    """Main data viewer"""
    print("🚕 Real-Time Taxi Demand Forecasting System - Data Viewer")
    print("=" * 60)
    print(f"🕐 View time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        view_taxi_data()
        view_heatmap_data()
        view_statistics()
        
        print("\n" + "=" * 60)
        print("✅ Data viewing completed successfully!")
        print("\n💡 To see live data updates:")
        print("   ./run_demo.sh  # Start the dashboard")
        print("   http://localhost:8050  # View in browser")
        
    except Exception as e:
        print(f"❌ Error viewing data: {e}")

if __name__ == "__main__":
    main() 