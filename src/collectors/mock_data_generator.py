import random
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from src.utils.config import config

logger = logging.getLogger(__name__)

class MockTaxiDataGenerator:
    """Generates mock taxi data for testing purposes."""
    
    def __init__(self):
        self.location_ids = list(range(1, 51))  # 50 locations
        self.vendor_ids = ['CMT', 'VTS', 'DDS']
        self.payment_types = ['1', '2', '3', '4', '5', '6']
        
    def generate_taxi_data(self, count: int = 100) -> List[Dict[str, Any]]:
        """
        Generate mock taxi trip data.
        
        Args:
            count: Number of records to generate
            
        Returns:
            List of mock taxi trip records
        """
        data = []
        current_time = datetime.now()
        
        for i in range(count):
            # Generate random pickup time within last hour
            pickup_time = current_time - timedelta(
                minutes=random.randint(0, 60),
                seconds=random.randint(0, 59)
            )
            
            # Generate random trip duration (5-60 minutes)
            trip_duration = random.randint(5, 60)
            dropoff_time = pickup_time + timedelta(minutes=trip_duration)
            
            # Generate random coordinates in NYC area
            pickup_lat = random.uniform(40.6, 40.9)
            pickup_lon = random.uniform(-74.1, -73.7)
            dropoff_lat = random.uniform(40.6, 40.9)
            dropoff_lon = random.uniform(-74.1, -73.7)
            
            # Calculate distance
            distance = self._calculate_distance(
                pickup_lat, pickup_lon, dropoff_lat, dropoff_lon
            )
            
            # Generate fare based on distance
            base_fare = 2.50
            distance_fare = distance * 2.50
            tip_amount = random.uniform(0, distance_fare * 0.2)
            total_amount = base_fare + distance_fare + tip_amount
            
            record = {
                'trip_id': f"mock_trip_{int(time.time() * 1000) + i}",
                'pickup_datetime': pickup_time.isoformat(),
                'dropoff_datetime': dropoff_time.isoformat(),
                'pickup_location_id': random.choice(self.location_ids),
                'dropoff_location_id': random.choice(self.location_ids),
                'passenger_count': random.randint(1, 6),
                'trip_distance': round(distance, 2),
                'fare_amount': round(distance_fare, 2),
                'tip_amount': round(tip_amount, 2),
                'total_amount': round(total_amount, 2),
                'payment_type': random.choice(self.payment_types),
                'vendor_id': random.choice(self.vendor_ids),
                'rate_code_id': random.randint(1, 6),
                'store_and_fwd_flag': random.choice(['Y', 'N']),
                'pickup_latitude': round(pickup_lat, 6),
                'pickup_longitude': round(pickup_lon, 6),
                'dropoff_latitude': round(dropoff_lat, 6),
                'dropoff_longitude': round(dropoff_lon, 6),
                'collected_at': datetime.now().isoformat(),
                'data_source': 'mock_generator',
                'pickup_hour': pickup_time.hour,
                'pickup_day': pickup_time.weekday(),
                'pickup_month': pickup_time.month,
                'pickup_year': pickup_time.year,
                'is_weekend': pickup_time.weekday() >= 5,
                'is_rush_hour': pickup_time.hour in [7, 8, 9, 17, 18, 19]
            }
            
            data.append(record)
        
        logger.info(f"Generated {len(data)} mock taxi records")
        return data
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate approximate distance between two points."""
        # Simple distance calculation (not exact but good for mock data)
        lat_diff = abs(lat1 - lat2)
        lon_diff = abs(lon1 - lon2)
        return (lat_diff + lon_diff) * 50  # Rough conversion to miles
    
    def get_demand_heatmap_data(self, hours: int = 1) -> List[Dict[str, Any]]:
        """
        Generate mock heatmap data.
        
        Args:
            hours: Time window in hours
            
        Returns:
            List of mock heatmap data
        """
        heatmap_data = []
        
        for location_id in random.sample(self.location_ids, 20):  # 20 random locations
            trip_count = random.randint(1, 25)
            avg_fare = random.uniform(10, 50)
            
            # Generate coordinates for this location
            lat = random.uniform(40.6, 40.9)
            lon = random.uniform(-74.1, -73.7)
            
            heatmap_data.append({
                'location_id': location_id,
                'trip_count': trip_count,
                'total_fare': trip_count * avg_fare,
                'avg_fare': avg_fare,
                'latitude': lat,
                'longitude': lon,
                'demand_level': 'high' if trip_count > 15 else 'medium' if trip_count > 8 else 'low'
            })
        
        logger.info(f"Generated heatmap data for {len(heatmap_data)} locations")
        return heatmap_data
    
    def get_demand_by_location(self, location_id: int, hours: int = 1) -> Dict[str, Any]:
        """
        Generate mock demand data for a specific location.
        
        Args:
            location_id: Location ID
            hours: Time window in hours
            
        Returns:
            Mock demand statistics
        """
        trip_count = random.randint(0, 30)
        avg_fare = random.uniform(10, 50)
        avg_distance = random.uniform(2, 15)
        avg_passengers = random.uniform(1, 4)
        
        return {
            'location_id': location_id,
            'trip_count': trip_count,
            'total_fare': trip_count * avg_fare,
            'avg_fare': avg_fare,
            'total_distance': trip_count * avg_distance,
            'avg_distance': avg_distance,
            'passenger_count': int(trip_count * avg_passengers),
            'avg_passengers': avg_passengers,
            'timestamp': datetime.now().isoformat()
        } 