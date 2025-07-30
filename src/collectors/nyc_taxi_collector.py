import requests
import pandas as pd
import json
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from src.utils.config import config

logger = logging.getLogger(__name__)

class NYCTaxiCollector:
    """Collects NYC taxi data from the NYC Open Data API."""
    
    def __init__(self):
        self.api_config = config.get_nyc_api_config()
        self.base_url = self.api_config['base_url']
        self.dataset_id = self.api_config['dataset_id']
        self.limit = self.api_config['limit']
        
    def fetch_taxi_data(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Fetch taxi data from NYC Open Data API.
        
        Args:
            limit: Number of records to fetch (defaults to config limit)
            
        Returns:
            List of taxi trip records
        """
        try:
            limit = limit or self.limit
            url = f"{self.base_url}/{self.dataset_id}.json"
            params = {
                '$limit': limit,
                '$order': 'pickup_datetime DESC'
            }
            
            logger.info(f"Fetching taxi data from {url}")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully fetched {len(data)} taxi records")
            
            return self._process_raw_data(data)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching taxi data: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in fetch_taxi_data: {e}")
            return []
    
    def _process_raw_data(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process raw taxi data and add metadata.
        
        Args:
            raw_data: Raw data from API
            
        Returns:
            Processed taxi data with additional metadata
        """
        processed_data = []
        
        for record in raw_data:
            try:
                # Extract and validate key fields
                processed_record = {
                    'trip_id': record.get('trip_id', f"trip_{int(time.time() * 1000)}"),
                    'pickup_datetime': record.get('pickup_datetime'),
                    'dropoff_datetime': record.get('dropoff_datetime'),
                    'pickup_location_id': record.get('pulocationid'),
                    'dropoff_location_id': record.get('dolocationid'),
                    'passenger_count': int(record.get('passenger_count', 1)),
                    'trip_distance': float(record.get('trip_distance', 0)),
                    'fare_amount': float(record.get('fare_amount', 0)),
                    'tip_amount': float(record.get('tip_amount', 0)),
                    'total_amount': float(record.get('total_amount', 0)),
                    'payment_type': record.get('payment_type'),
                    'vendor_id': record.get('vendorid'),
                    'rate_code_id': record.get('ratecodeid'),
                    'store_and_fwd_flag': record.get('store_and_fwd_flag'),
                    'pickup_latitude': float(record.get('pickup_latitude', 0)),
                    'pickup_longitude': float(record.get('pickup_longitude', 0)),
                    'dropoff_latitude': float(record.get('dropoff_latitude', 0)),
                    'dropoff_longitude': float(record.get('dropoff_longitude', 0)),
                    'collected_at': datetime.now().isoformat(),
                    'data_source': 'nyc_open_data'
                }
                
                # Add time-based features
                if processed_record['pickup_datetime']:
                    pickup_dt = datetime.fromisoformat(processed_record['pickup_datetime'].replace('Z', '+00:00'))
                    processed_record.update({
                        'pickup_hour': pickup_dt.hour,
                        'pickup_day': pickup_dt.weekday(),
                        'pickup_month': pickup_dt.month,
                        'pickup_year': pickup_dt.year,
                        'is_weekend': pickup_dt.weekday() >= 5,
                        'is_rush_hour': pickup_dt.hour in [7, 8, 9, 17, 18, 19]
                    })
                
                processed_data.append(processed_record)
                
            except (ValueError, TypeError) as e:
                logger.warning(f"Skipping invalid record: {e}")
                continue
        
        logger.info(f"Processed {len(processed_data)} valid records")
        return processed_data
    
    def get_recent_trips(self, hours: int = 1) -> List[Dict[str, Any]]:
        """
        Get recent taxi trips from the last N hours.
        
        Args:
            hours: Number of hours to look back
            
        Returns:
            List of recent taxi trips
        """
        try:
            # Calculate time range
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=hours)
            
            url = f"{self.base_url}/{self.dataset_id}.json"
            params = {
                '$limit': self.limit,
                '$where': f"pickup_datetime >= '{start_time.isoformat()}' AND pickup_datetime <= '{end_time.isoformat()}'",
                '$order': 'pickup_datetime DESC'
            }
            
            logger.info(f"Fetching recent trips from {start_time} to {end_time}")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return self._process_raw_data(data)
            
        except Exception as e:
            logger.error(f"Error fetching recent trips: {e}")
            return []
    
    def get_demand_by_location(self, location_id: int, hours: int = 1) -> Dict[str, Any]:
        """
        Get demand data for a specific location.
        
        Args:
            location_id: Location ID to analyze
            hours: Time window in hours
            
        Returns:
            Demand statistics for the location
        """
        trips = self.get_recent_trips(hours)
        location_trips = [trip for trip in trips if trip.get('pickup_location_id') == location_id]
        
        if not location_trips:
            return {
                'location_id': location_id,
                'trip_count': 0,
                'total_fare': 0,
                'avg_fare': 0,
                'total_distance': 0,
                'avg_distance': 0,
                'passenger_count': 0,
                'avg_passengers': 0
            }
        
        total_fare = sum(trip.get('fare_amount', 0) for trip in location_trips)
        total_distance = sum(trip.get('trip_distance', 0) for trip in location_trips)
        total_passengers = sum(trip.get('passenger_count', 0) for trip in location_trips)
        
        return {
            'location_id': location_id,
            'trip_count': len(location_trips),
            'total_fare': total_fare,
            'avg_fare': total_fare / len(location_trips),
            'total_distance': total_distance,
            'avg_distance': total_distance / len(location_trips),
            'passenger_count': total_passengers,
            'avg_passengers': total_passengers / len(location_trips),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_demand_heatmap_data(self, hours: int = 1) -> List[Dict[str, Any]]:
        """
        Get demand heatmap data for all locations.
        
        Args:
            hours: Time window in hours
            
        Returns:
            List of demand data for heatmap visualization
        """
        trips = self.get_recent_trips(hours)
        
        # Group by location
        location_demand = {}
        for trip in trips:
            location_id = trip.get('pickup_location_id')
            if location_id:
                if location_id not in location_demand:
                    location_demand[location_id] = {
                        'location_id': location_id,
                        'trip_count': 0,
                        'total_fare': 0,
                        'avg_lat': 0,
                        'avg_lon': 0,
                        'latitudes': [],
                        'longitudes': []
                    }
                
                location_demand[location_id]['trip_count'] += 1
                location_demand[location_id]['total_fare'] += trip.get('fare_amount', 0)
                location_demand[location_id]['latitudes'].append(trip.get('pickup_latitude', 0))
                location_demand[location_id]['longitudes'].append(trip.get('pickup_longitude', 0))
        
        # Calculate averages
        heatmap_data = []
        for location_id, data in location_demand.items():
            if data['latitudes'] and data['longitudes']:
                avg_lat = sum(data['latitudes']) / len(data['latitudes'])
                avg_lon = sum(data['longitudes']) / len(data['longitudes'])
                
                heatmap_data.append({
                    'location_id': location_id,
                    'trip_count': data['trip_count'],
                    'total_fare': data['total_fare'],
                    'avg_fare': data['total_fare'] / data['trip_count'],
                    'latitude': avg_lat,
                    'longitude': avg_lon,
                    'demand_level': 'high' if data['trip_count'] > 10 else 'medium' if data['trip_count'] > 5 else 'low'
                })
        
        return heatmap_data 