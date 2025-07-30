#!/usr/bin/env python3
"""
Real-Time Taxi Demand Forecasting System
Main application orchestrator
"""

import time
import logging
import threading
import signal
import sys
from typing import List
from src.utils.config import config
from src.collectors.nyc_taxi_collector import NYCTaxiCollector
from src.collectors.kafka_producer import TaxiDataProducer
from src.processors.spark_streaming_processor import SparkStreamingProcessor
from src.dashboard.real_time_dashboard import RealTimeDashboard

logger = logging.getLogger(__name__)

class TaxiDemandSystem:
    """Main orchestrator for the taxi demand forecasting system."""
    
    def __init__(self):
        # Setup logging
        config.setup_logging()
        logger.info("🚕 Initializing Real-Time Taxi Demand Forecasting System")
        
        # Initialize components
        self.collector = None
        self.producer = None
        self.processor = None
        self.dashboard = None
        
        # Threading
        self.collector_thread = None
        self.processor_thread = None
        self.dashboard_thread = None
        
        # Control flags
        self.running = False
        
        # Signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, shutting down...")
        self.stop()
        sys.exit(0)
    
    def initialize_components(self):
        """Initialize all system components."""
        try:
            logger.info("Initializing system components...")
            
            # Initialize data collector
            self.collector = NYCTaxiCollector()
            logger.info("✅ NYC Taxi Collector initialized")
            
            # Initialize Kafka producer
            self.producer = TaxiDataProducer()
            logger.info("✅ Kafka Producer initialized")
            
            # Initialize Spark processor
            self.processor = SparkStreamingProcessor()
            logger.info("✅ Spark Streaming Processor initialized")
            
            # Initialize dashboard
            self.dashboard = RealTimeDashboard()
            logger.info("✅ Real-time Dashboard initialized")
            
            logger.info("✅ All components initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize components: {e}")
            raise
    
    def start_data_collection(self):
        """Start the data collection process."""
        def collect_data():
            """Data collection loop."""
            while self.running:
                try:
                    # Fetch taxi data
                    taxi_data = self.collector.fetch_taxi_data(limit=100)
                    
                    if taxi_data:
                        # Send to Kafka
                        success = self.producer.send_taxi_data(taxi_data)
                        if success:
                            logger.info(f"📊 Collected and sent {len(taxi_data)} taxi records")
                        
                        # Get heatmap data
                        heatmap_data = self.collector.get_demand_heatmap_data(hours=1)
                        if heatmap_data:
                            self.producer.send_heatmap_data(heatmap_data)
                            logger.info(f"🗺️ Sent heatmap data for {len(heatmap_data)} locations")
                    
                    # Wait before next collection
                    time.sleep(30)  # Collect every 30 seconds
                    
                except Exception as e:
                    logger.error(f"Error in data collection: {e}")
                    time.sleep(10)  # Wait before retry
        
        self.collector_thread = threading.Thread(target=collect_data, daemon=True)
        self.collector_thread.start()
        logger.info("🚀 Data collection started")
    
    def start_streaming_processing(self):
        """Start the Spark streaming processing."""
        def run_processor():
            """Run Spark streaming processor."""
            try:
                self.processor.start_streaming()
            except Exception as e:
                logger.error(f"Error in Spark streaming: {e}")
        
        self.processor_thread = threading.Thread(target=run_processor, daemon=True)
        self.processor_thread.start()
        logger.info("🚀 Spark streaming processing started")
    
    def start_dashboard(self):
        """Start the real-time dashboard."""
        def run_dashboard():
            """Run the dashboard."""
            try:
                self.dashboard.run()
            except Exception as e:
                logger.error(f"Error in dashboard: {e}")
        
        self.dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
        self.dashboard_thread.start()
        logger.info("🚀 Dashboard started")
    
    def start(self):
        """Start the entire system."""
        try:
            logger.info("🚀 Starting Real-Time Taxi Demand Forecasting System")
            
            # Initialize components
            self.initialize_components()
            
            # Set running flag
            self.running = True
            
            # Start all components
            self.start_data_collection()
            self.start_streaming_processing()
            self.start_dashboard()
            
            logger.info("✅ System started successfully!")
            logger.info("📊 Dashboard available at: http://localhost:8050")
            logger.info("📈 Monitoring taxi demand in real-time...")
            
            # Keep main thread alive
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
            self.stop()
        except Exception as e:
            logger.error(f"❌ Error starting system: {e}")
            self.stop()
            raise
    
    def stop(self):
        """Stop the entire system."""
        logger.info("🛑 Stopping Real-Time Taxi Demand Forecasting System")
        
        # Set running flag to False
        self.running = False
        
        # Stop components
        try:
            if self.dashboard:
                self.dashboard.stop()
                logger.info("✅ Dashboard stopped")
            
            if self.processor:
                self.processor.stop_streaming()
                logger.info("✅ Spark processor stopped")
            
            if self.producer:
                self.producer.close()
                logger.info("✅ Kafka producer stopped")
            
            logger.info("✅ System stopped successfully")
            
        except Exception as e:
            logger.error(f"❌ Error stopping system: {e}")

def main():
    """Main entry point."""
    system = TaxiDemandSystem()
    
    try:
        system.start()
    except Exception as e:
        logger.error(f"❌ System failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 