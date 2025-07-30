import os
from dotenv import load_dotenv
import logging
from typing import Dict, Any

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the taxi demand forecasting system."""
    
    def __init__(self):
        self.kafka_config = {
            'bootstrap_servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
            'topic_taxi_data': os.getenv('KAFKA_TOPIC_TAXI_DATA', 'taxi_data'),
            'topic_aggregated': os.getenv('KAFKA_TOPIC_AGGREGATED', 'taxi_aggregated'),
            'topic_anomalies': os.getenv('KAFKA_TOPIC_ANOMALIES', 'taxi_anomalies')
        }
        
        self.nyc_api_config = {
            'base_url': os.getenv('NYC_API_BASE_URL', 'https://data.cityofnewyork.us/resource'),
            'dataset_id': os.getenv('NYC_API_DATASET_ID', 't29m-gskq'),
            'limit': int(os.getenv('NYC_API_LIMIT', '1000'))
        }
        
        self.spark_config = {
            'master': os.getenv('SPARK_MASTER', 'local[*]'),
            'app_name': os.getenv('SPARK_APP_NAME', 'TaxiDemandForecasting')
        }
        
        self.dashboard_config = {
            'host': os.getenv('DASHBOARD_HOST', '0.0.0.0'),
            'port': int(os.getenv('DASHBOARD_PORT', '8050')),
            'flask_host': os.getenv('FLASK_HOST', '0.0.0.0'),
            'flask_port': int(os.getenv('FLASK_PORT', '5000'))
        }
        
        self.logging_config = {
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'file': os.getenv('LOG_FILE', 'logs/taxi_demand.log')
        }
    
    def get_kafka_config(self) -> Dict[str, Any]:
        """Get Kafka configuration."""
        return self.kafka_config
    
    def get_nyc_api_config(self) -> Dict[str, Any]:
        """Get NYC API configuration."""
        return self.nyc_api_config
    
    def get_spark_config(self) -> Dict[str, Any]:
        """Get Spark configuration."""
        return self.spark_config
    
    def get_dashboard_config(self) -> Dict[str, Any]:
        """Get dashboard configuration."""
        return self.dashboard_config
    
    def setup_logging(self):
        """Setup logging configuration."""
        log_level = getattr(logging, self.logging_config['level'])
        
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(self.logging_config['file']), exist_ok=True)
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.logging_config['file']),
                logging.StreamHandler()
            ]
        )

# Global config instance
config = Config() 