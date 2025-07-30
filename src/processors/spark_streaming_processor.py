import json
import logging
from typing import Dict, Any, List
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from src.utils.config import config

logger = logging.getLogger(__name__)

class SparkStreamingProcessor:
    """Spark Streaming processor for real-time taxi data analysis."""
    
    def __init__(self):
        self.spark_config = config.get_spark_config()
        self.kafka_config = config.get_kafka_config()
        
        # Initialize Spark session
        self.spark = None
        self.ssc = None
        self._initialize_spark()
    
    def _initialize_spark(self):
        """Initialize Spark session and streaming context."""
        try:
            self.spark = SparkSession.builder \
                .appName(self.spark_config['app_name']) \
                .master(self.spark_config['master']) \
                .config("spark.sql.adaptive.enabled", "true") \
                .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
                .config("spark.sql.adaptive.skewJoin.enabled", "true") \
                .getOrCreate()
            
            # Create streaming context
            self.ssc = StreamingContext(self.spark.sparkContext, batchDuration=10)
            
            logger.info("Spark session and streaming context initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Spark: {e}")
            raise
    
    def create_taxi_schema(self) -> StructType:
        """Create schema for taxi data."""
        return StructType([
            StructField("trip_id", StringType(), True),
            StructField("pickup_datetime", StringType(), True),
            StructField("dropoff_datetime", StringType(), True),
            StructField("pickup_location_id", IntegerType(), True),
            StructField("dropoff_location_id", IntegerType(), True),
            StructField("passenger_count", IntegerType(), True),
            StructField("trip_distance", DoubleType(), True),
            StructField("fare_amount", DoubleType(), True),
            StructField("tip_amount", DoubleType(), True),
            StructField("total_amount", DoubleType(), True),
            StructField("payment_type", StringType(), True),
            StructField("vendor_id", StringType(), True),
            StructField("rate_code_id", IntegerType(), True),
            StructField("store_and_fwd_flag", StringType(), True),
            StructField("pickup_latitude", DoubleType(), True),
            StructField("pickup_longitude", DoubleType(), True),
            StructField("dropoff_latitude", DoubleType(), True),
            StructField("dropoff_longitude", DoubleType(), True),
            StructField("collected_at", StringType(), True),
            StructField("data_source", StringType(), True),
            StructField("pickup_hour", IntegerType(), True),
            StructField("pickup_day", IntegerType(), True),
            StructField("pickup_month", IntegerType(), True),
            StructField("pickup_year", IntegerType(), True),
            StructField("is_weekend", BooleanType(), True),
            StructField("is_rush_hour", BooleanType(), True)
        ])
    
    def process_taxi_stream(self):
        """Process taxi data stream from Kafka."""
        try:
            # Create Kafka stream
            kafka_stream = KafkaUtils.createDirectStream(
                self.ssc,
                [self.kafka_config['topic_taxi_data']],
                {"metadata.broker.list": self.kafka_config['bootstrap_servers']}
            )
            
            # Parse JSON messages
            parsed_stream = kafka_stream.map(lambda x: json.loads(x[1]))
            
            # Convert to DataFrame
            taxi_df = parsed_stream.map(lambda x: (
                x.get('trip_id'),
                x.get('pickup_datetime'),
                x.get('dropoff_datetime'),
                x.get('pickup_location_id'),
                x.get('dropoff_location_id'),
                x.get('passenger_count'),
                x.get('trip_distance'),
                x.get('fare_amount'),
                x.get('tip_amount'),
                x.get('total_amount'),
                x.get('payment_type'),
                x.get('vendor_id'),
                x.get('rate_code_id'),
                x.get('store_and_fwd_flag'),
                x.get('pickup_latitude'),
                x.get('pickup_longitude'),
                x.get('dropoff_latitude'),
                x.get('dropoff_longitude'),
                x.get('collected_at'),
                x.get('data_source'),
                x.get('pickup_hour'),
                x.get('pickup_day'),
                x.get('pickup_month'),
                x.get('pickup_year'),
                x.get('is_weekend'),
                x.get('is_rush_hour')
            ))
            
            # Apply schema
            taxi_df_with_schema = taxi_df.map(lambda x: x)
            
            # Aggregate by location and time window
            def aggregate_by_location(rdd):
                if rdd.isEmpty():
                    return
                
                # Convert to DataFrame
                df = self.spark.createDataFrame(rdd, self.create_taxi_schema())
                
                # Aggregate by location
                location_agg = df.groupBy("pickup_location_id") \
                    .agg(
                        count("*").alias("trip_count"),
                        sum("fare_amount").alias("total_fare"),
                        avg("fare_amount").alias("avg_fare"),
                        sum("trip_distance").alias("total_distance"),
                        avg("trip_distance").alias("avg_distance"),
                        sum("passenger_count").alias("total_passengers"),
                        avg("passenger_count").alias("avg_passengers")
                    )
                
                # Convert to JSON and send to aggregated topic
                aggregated_data = location_agg.toJSON().collect()
                for record in aggregated_data:
                    logger.info(f"Aggregated data: {record}")
                
                return aggregated_data
            
            # Apply aggregation
            taxi_df_with_schema.foreachRDD(aggregate_by_location)
            
            logger.info("Taxi stream processing started")
            
        except Exception as e:
            logger.error(f"Error in process_taxi_stream: {e}")
            raise
    
    def detect_anomalies(self):
        """Detect anomalies in taxi demand patterns."""
        try:
            # Create Kafka stream for aggregated data
            kafka_stream = KafkaUtils.createDirectStream(
                self.ssc,
                [self.kafka_config['topic_aggregated']],
                {"metadata.broker.list": self.kafka_config['bootstrap_servers']}
            )
            
            # Parse JSON messages
            parsed_stream = kafka_stream.map(lambda x: json.loads(x[1]))
            
            def detect_anomalies_in_batch(rdd):
                if rdd.isEmpty():
                    return
                
                # Convert to list for processing
                records = rdd.collect()
                
                for record in records:
                    try:
                        data = json.loads(record) if isinstance(record, str) else record
                        
                        # Simple anomaly detection based on trip count
                        trip_count = data.get('trip_count', 0)
                        avg_fare = data.get('avg_fare', 0)
                        
                        # Define anomaly thresholds
                        high_demand_threshold = 20  # trips per location
                        low_demand_threshold = 2    # trips per location
                        fare_anomaly_threshold = 50  # dollars
                        
                        anomalies = []
                        
                        if trip_count > high_demand_threshold:
                            anomalies.append({
                                'type': 'high_demand',
                                'location_id': data.get('pickup_location_id'),
                                'value': trip_count,
                                'threshold': high_demand_threshold,
                                'timestamp': time.time()
                            })
                        
                        if trip_count < low_demand_threshold and trip_count > 0:
                            anomalies.append({
                                'type': 'low_demand',
                                'location_id': data.get('pickup_location_id'),
                                'value': trip_count,
                                'threshold': low_demand_threshold,
                                'timestamp': time.time()
                            })
                        
                        if avg_fare > fare_anomaly_threshold:
                            anomalies.append({
                                'type': 'high_fare',
                                'location_id': data.get('pickup_location_id'),
                                'value': avg_fare,
                                'threshold': fare_anomaly_threshold,
                                'timestamp': time.time()
                            })
                        
                        # Log anomalies
                        for anomaly in anomalies:
                            logger.warning(f"Anomaly detected: {anomaly}")
                        
                    except Exception as e:
                        logger.error(f"Error processing record for anomaly detection: {e}")
                        continue
            
            # Apply anomaly detection
            parsed_stream.foreachRDD(detect_anomalies_in_batch)
            
            logger.info("Anomaly detection started")
            
        except Exception as e:
            logger.error(f"Error in detect_anomalies: {e}")
            raise
    
    def calculate_demand_forecast(self):
        """Calculate demand forecast based on historical patterns."""
        try:
            # Create Kafka stream for aggregated data
            kafka_stream = KafkaUtils.createDirectStream(
                self.ssc,
                [self.kafka_config['topic_aggregated']],
                {"metadata.broker.list": self.kafka_config['bootstrap_servers']}
            )
            
            # Parse JSON messages
            parsed_stream = kafka_stream.map(lambda x: json.loads(x[1]))
            
            def forecast_demand(rdd):
                if rdd.isEmpty():
                    return
                
                # Convert to list for processing
                records = rdd.collect()
                
                for record in records:
                    try:
                        data = json.loads(record) if isinstance(record, str) else record
                        
                        # Simple forecasting based on current demand
                        current_demand = data.get('trip_count', 0)
                        location_id = data.get('pickup_location_id')
                        
                        # Simple forecasting logic (can be enhanced with ML models)
                        forecast_next_hour = int(current_demand * 1.1)  # 10% increase
                        forecast_next_2_hours = int(current_demand * 1.2)  # 20% increase
                        
                        forecast_data = {
                            'location_id': location_id,
                            'current_demand': current_demand,
                            'forecast_1_hour': forecast_next_hour,
                            'forecast_2_hours': forecast_next_2_hours,
                            'confidence': 0.8,
                            'timestamp': time.time()
                        }
                        
                        logger.info(f"Demand forecast: {forecast_data}")
                        
                    except Exception as e:
                        logger.error(f"Error in demand forecasting: {e}")
                        continue
            
            # Apply forecasting
            parsed_stream.foreachRDD(forecast_demand)
            
            logger.info("Demand forecasting started")
            
        except Exception as e:
            logger.error(f"Error in calculate_demand_forecast: {e}")
            raise
    
    def start_streaming(self):
        """Start the Spark streaming context."""
        try:
            # Start processing streams
            self.process_taxi_stream()
            self.detect_anomalies()
            self.calculate_demand_forecast()
            
            # Start the streaming context
            logger.info("Starting Spark streaming context...")
            self.ssc.start()
            self.ssc.awaitTermination()
            
        except KeyboardInterrupt:
            logger.info("Stopping Spark streaming context...")
            self.ssc.stop(stopSparkContext=True, stopGraceFully=True)
        except Exception as e:
            logger.error(f"Error in start_streaming: {e}")
            self.ssc.stop(stopSparkContext=True, stopGraceFully=True)
            raise
    
    def stop_streaming(self):
        """Stop the Spark streaming context."""
        if self.ssc:
            self.ssc.stop(stopSparkContext=True, stopGraceFully=True)
            logger.info("Spark streaming context stopped")
        
        if self.spark:
            self.spark.stop()
            logger.info("Spark session stopped")

import time 