import json
import logging
import time
from typing import Dict, Any, List
from kafka import KafkaProducer
from kafka.errors import KafkaError
from src.utils.config import config

logger = logging.getLogger(__name__)

class TaxiDataProducer:
    """Kafka producer for streaming taxi data."""
    
    def __init__(self):
        self.kafka_config = config.get_kafka_config()
        self.bootstrap_servers = self.kafka_config['bootstrap_servers']
        self.topic_taxi_data = self.kafka_config['topic_taxi_data']
        self.topic_aggregated = self.kafka_config['topic_aggregated']
        self.topic_anomalies = self.kafka_config['topic_anomalies']
        
        # Initialize Kafka producer
        self.producer = None
        self._initialize_producer()
    
    def _initialize_producer(self):
        """Initialize Kafka producer with proper configuration."""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                acks='all',
                retries=3,
                batch_size=16384,
                linger_ms=10,
                buffer_memory=33554432
            )
            logger.info(f"Kafka producer initialized successfully for {self.bootstrap_servers}")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka producer: {e}")
            raise
    
    def send_taxi_data(self, taxi_records: List[Dict[str, Any]]) -> bool:
        """
        Send taxi data to Kafka topic.
        
        Args:
            taxi_records: List of taxi trip records
            
        Returns:
            True if successful, False otherwise
        """
        if not self.producer:
            logger.error("Kafka producer not initialized")
            return False
        
        try:
            success_count = 0
            for record in taxi_records:
                # Use trip_id as key for partitioning
                key = record.get('trip_id', str(time.time()))
                
                # Send to taxi_data topic
                future = self.producer.send(
                    topic=self.topic_taxi_data,
                    key=key,
                    value=record
                )
                
                # Wait for the send to complete
                try:
                    record_metadata = future.get(timeout=10)
                    success_count += 1
                    logger.debug(f"Record sent to {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")
                except KafkaError as e:
                    logger.error(f"Failed to send record: {e}")
                    continue
            
            # Flush to ensure all messages are sent
            self.producer.flush()
            logger.info(f"Successfully sent {success_count}/{len(taxi_records)} records to {self.topic_taxi_data}")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"Error sending taxi data to Kafka: {e}")
            return False
    
    def send_aggregated_data(self, aggregated_data: Dict[str, Any]) -> bool:
        """
        Send aggregated data to Kafka topic.
        
        Args:
            aggregated_data: Aggregated taxi demand data
            
        Returns:
            True if successful, False otherwise
        """
        if not self.producer:
            logger.error("Kafka producer not initialized")
            return False
        
        try:
            key = f"agg_{int(time.time())}"
            future = self.producer.send(
                topic=self.topic_aggregated,
                key=key,
                value=aggregated_data
            )
            
            record_metadata = future.get(timeout=10)
            logger.info(f"Aggregated data sent to {record_metadata.topic} partition {record_metadata.partition}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending aggregated data to Kafka: {e}")
            return False
    
    def send_anomaly_alert(self, anomaly_data: Dict[str, Any]) -> bool:
        """
        Send anomaly alert to Kafka topic.
        
        Args:
            anomaly_data: Anomaly detection data
            
        Returns:
            True if successful, False otherwise
        """
        if not self.producer:
            logger.error("Kafka producer not initialized")
            return False
        
        try:
            key = f"anomaly_{int(time.time())}"
            future = self.producer.send(
                topic=self.topic_anomalies,
                key=key,
                value=anomaly_data
            )
            
            record_metadata = future.get(timeout=10)
            logger.warning(f"Anomaly alert sent to {record_metadata.topic} partition {record_metadata.partition}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending anomaly alert to Kafka: {e}")
            return False
    
    def send_heatmap_data(self, heatmap_data: List[Dict[str, Any]]) -> bool:
        """
        Send heatmap data to Kafka topic.
        
        Args:
            heatmap_data: Heatmap visualization data
            
        Returns:
            True if successful, False otherwise
        """
        if not self.producer:
            logger.error("Kafka producer not initialized")
            return False
        
        try:
            key = f"heatmap_{int(time.time())}"
            future = self.producer.send(
                topic=self.topic_aggregated,
                key=key,
                value={
                    'type': 'heatmap',
                    'data': heatmap_data,
                    'timestamp': time.time()
                }
            )
            
            record_metadata = future.get(timeout=10)
            logger.info(f"Heatmap data sent to {record_metadata.topic} partition {record_metadata.partition}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending heatmap data to Kafka: {e}")
            return False
    
    def close(self):
        """Close the Kafka producer."""
        if self.producer:
            self.producer.close()
            logger.info("Kafka producer closed")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 