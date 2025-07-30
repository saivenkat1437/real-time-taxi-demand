# 🚕 Real-Time Taxi Demand Forecasting System - Complete Data Flow & Monitoring Guide

## 📊 **DATASETS USED**

### 🚕 **1. NYC Open Data API Dataset**
- **Dataset ID**: `t29m-gskq`
- **API URL**: `https://data.cityofnewyork.us/resource/t29m-gskq.json`
- **Description**: NYC Taxi & Limousine Commission (TLC) Trip Records
- **Data Type**: Real NYC taxi trip data
- **Coverage**: New York City area
- **Update Frequency**: Monthly

**Dataset Fields:**
```
• trip_id: Unique trip identifier
• pickup_datetime: Trip start time
• dropoff_datetime: Trip end time
• pulocationid: Pickup location ID
• dolocationid: Dropoff location ID
• passenger_count: Number of passengers
• trip_distance: Distance in miles
• fare_amount: Base fare
• tip_amount: Tip amount
• total_amount: Total fare including tip
• payment_type: Payment method
• vendorid: Taxi vendor ID
• pickup_latitude/longitude: Pickup coordinates
• dropoff_latitude/longitude: Dropoff coordinates
```

### 🎭 **2. Mock Data Generator**
- **Purpose**: Local testing and development
- **Generation**: Realistic synthetic data
- **Coverage**: NYC area coordinates
- **Real-time**: Generates fresh data on demand

**Mock Data Features:**
```
• 50 different location IDs
• 3 vendor types (CMT, VTS, DDS)
• Realistic fare calculations
• NYC coordinate boundaries (40.6-40.9 lat, -74.1 to -73.7 lon)
• Time-based features (rush hour, weekend)
• Distance-based pricing
```

## 🔄 **DATA FLOW ARCHITECTURE**

### 📊 **1. Data Collection Layer**

#### 🚕 **NYC API Collector** (`src/collectors/nyc_taxi_collector.py`)
- Fetches real taxi data from NYC Open Data API
- Processes raw data into standardized format
- Adds metadata (time features, coordinates)
- Handles API rate limits and errors
- **Methods**:
  - `fetch_taxi_data()`: Get recent taxi trips
  - `get_recent_trips()`: Get trips from last N hours
  - `get_demand_by_location()`: Location-specific demand
  - `get_demand_heatmap_data()`: Heatmap visualization data

#### 🎭 **Mock Data Generator** (`src/collectors/mock_data_generator.py`)
- Generates synthetic taxi trip data
- Creates realistic NYC coordinates
- Simulates fare calculations
- Provides consistent data for testing
- **Methods**:
  - `generate_taxi_data()`: Create mock taxi trips
  - `get_demand_heatmap_data()`: Generate heatmap data
  - `get_demand_by_location()`: Location-specific demand

### 📊 **2. Data Processing Layer** (Planned)

#### ⚡ **Spark Streaming** (`src/processors/spark_streaming_processor.py`)
- Real-time data aggregation
- Anomaly detection
- Demand forecasting
- Location-based analytics

### 📊 **3. Data Storage Layer** (Planned)

#### 🗄️ **Kafka Topics**
- `taxi_data`: Raw trip data
- `taxi_aggregated`: Processed aggregations
- `taxi_anomalies`: Detected anomalies

### 📊 **4. Visualization Layer**

#### 📈 **Dash Dashboard** (`src/dashboard/simple_dashboard.py`)
- Real-time demand heatmap
- Trip statistics
- Anomaly alerts
- Interactive charts

## 📋 **LOGGING SYSTEM**

### 📁 **Log File Location**
```
logs/taxi_demand.log
```

### 📊 **Log Levels**
- 🔍 **DEBUG**: Detailed debugging information
- ℹ️ **INFO**: General information messages
- ⚠️ **WARNING**: Warning messages
- ❌ **ERROR**: Error messages
- 🚨 **CRITICAL**: Critical error messages

### 📝 **Logged Events**
- Data collection events
- API request/response
- Data processing steps
- Dashboard access
- Error occurrences
- System startup/shutdown

### 🔍 **How to Check Logs**

```bash
# View all logs
cat logs/taxi_demand.log

# Last 20 lines
tail -20 logs/taxi_demand.log

# Follow live logs
tail -f logs/taxi_demand.log

# Search for errors
grep ERROR logs/taxi_demand.log

# Search for specific events
grep "Generated.*mock taxi records" logs/taxi_demand.log
```

## ⚙️ **SYSTEM CONFIGURATION**

### 📊 **Kafka Configuration**
```
Bootstrap Servers: localhost:9092
Taxi Data Topic: taxi_data
Aggregated Topic: taxi_aggregated
Anomalies Topic: taxi_anomalies
```

### 🌐 **NYC API Configuration**
```
Base URL: https://data.cityofnewyork.us/resource
Dataset ID: t29m-gskq
Limit: 1000 records
```

### 📊 **Dashboard Configuration**
```
Host: 0.0.0.0
Port: 8050
URL: http://localhost:8050
```

### 📋 **Logging Configuration**
```
Log File: logs/taxi_demand.log
Log Level: INFO
```

## 📊 **SYSTEM MONITORING**

### 🔍 **Health Checks**
```bash
# Comprehensive health check
python health_check.py

# Quick status check
./check_status.sh
```

### 📊 **Data Monitoring**
```bash
# View sample data
python view_data.py

# Comprehensive data check
python check_data.py
```

### 🖥️ **Dashboard Monitoring**
```bash
# Start dashboard
./run_demo.sh

# Access dashboard
http://localhost:8050

# Stop dashboard
./stop_demo.sh
```

### 📋 **Log Monitoring**
```bash
# Follow live logs
tail -f logs/taxi_demand.log

# Search for errors
grep ERROR logs/taxi_demand.log

# View recent activity
tail -20 logs/taxi_demand.log
```

## 🎭 **DATA GENERATION EXAMPLES**

### 📊 **Sample Taxi Trip Data**
```json
{
  "trip_id": "mock_trip_1753839225611",
  "pickup_datetime": "2025-07-29T19:54:01.050907",
  "dropoff_datetime": "2025-07-29T20:46:01.050907",
  "pickup_location_id": 23,
  "dropoff_location_id": 7,
  "passenger_count": 6,
  "trip_distance": 17.45,
  "fare_amount": 43.62,
  "tip_amount": 3.73,
  "total_amount": 49.85,
  "payment_type": "2",
  "vendor_id": "DDS",
  "pickup_latitude": 40.7152,
  "pickup_longitude": -74.0328,
  "dropoff_latitude": 40.7886,
  "dropoff_longitude": -73.7229,
  "collected_at": "2025-07-29T20:28:15.696529",
  "data_source": "mock_generator",
  "pickup_hour": 19,
  "pickup_day": 1,
  "pickup_month": 7,
  "pickup_year": 2025,
  "is_weekend": false,
  "is_rush_hour": true
}
```

### 🗺️ **Sample Heatmap Data**
```json
{
  "location_id": 46,
  "trip_count": 22,
  "total_fare": 748.32,
  "avg_fare": 34.01,
  "latitude": 40.8185,
  "longitude": -74.0218,
  "demand_level": "high"
}
```

## 🔄 **REAL-TIME DATA FLOW**

### 📊 **Current Flow (Mock Data)**
1. **Data Generation**: Mock data generator creates taxi trips every 5 seconds
2. **Data Processing**: Data is processed and formatted
3. **Dashboard Update**: Dashboard receives data and updates visualizations
4. **Logging**: All events are logged to `logs/taxi_demand.log`

### 📊 **Planned Flow (Real Data)**
1. **Data Collection**: NYC API collector fetches real taxi data
2. **Kafka Streaming**: Data is streamed to Kafka topics
3. **Spark Processing**: Spark Streaming processes data in real-time
4. **Anomaly Detection**: System detects unusual patterns
5. **Dashboard Visualization**: Real-time updates on dashboard

## 💡 **QUICK COMMANDS**

### 📊 **Data Viewing**
```bash
# View sample data
python view_data.py

# Check data quality
python check_data.py

# Generate fresh data
python -c "from src.collectors.mock_data_generator import MockTaxiDataGenerator; g = MockTaxiDataGenerator(); print(g.generate_taxi_data(1))"
```

### 🔍 **Log Monitoring**
```bash
# View recent logs
tail -20 logs/taxi_demand.log

# Follow live logs
tail -f logs/taxi_demand.log

# Search for specific events
grep "Generated.*mock taxi records" logs/taxi_demand.log
```

### 🖥️ **Dashboard Control**
```bash
# Start dashboard
./run_demo.sh

# Stop dashboard
./stop_demo.sh

# Check status
./check_status.sh
```

### 📋 **System Health**
```bash
# Health check
python health_check.py

# Status check
./check_status.sh
```

## 🎯 **KEY FEATURES**

### ✅ **Working Features**
- Mock data generation with realistic NYC coordinates
- Real-time dashboard with live updates
- Comprehensive logging system
- Health monitoring and status checks
- Data quality validation
- Interactive visualizations

### 🚧 **Planned Features**
- Real NYC API data integration
- Kafka streaming infrastructure
- Spark Streaming processing
- Anomaly detection algorithms
- Advanced demand forecasting
- Real-time alerts and notifications

---

*This system provides a complete foundation for real-time taxi demand forecasting with both mock data for development and real data integration capabilities.* 