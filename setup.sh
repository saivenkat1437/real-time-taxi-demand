#!/bin/bash

echo "🚕 Setting up Real-Time Taxi Demand Forecasting System..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating project structure..."
mkdir -p data
mkdir -p logs
mkdir -p config
mkdir -p src
mkdir -p src/collectors
mkdir -p src/processors
mkdir -p src/dashboard
mkdir -p src/utils
mkdir -p tests

# Set up environment variables
echo "⚙️ Setting up environment variables..."
cat > .env << EOF
# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC_TAXI_DATA=taxi_data
KAFKA_TOPIC_AGGREGATED=taxi_aggregated
KAFKA_TOPIC_ANOMALIES=taxi_anomalies

# NYC Taxi API Configuration
NYC_API_BASE_URL=https://data.cityofnewyork.us/resource
NYC_API_DATASET_ID=2upz-qtsa
NYC_API_LIMIT=1000

# Spark Configuration
SPARK_MASTER=local[*]
SPARK_APP_NAME=TaxiDemandForecasting

# Dashboard Configuration
DASHBOARD_HOST=0.0.0.0
DASHBOARD_PORT=8050
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/taxi_demand.log
EOF

echo "✅ Setup complete! To activate the environment, run: source venv/bin/activate"
echo "🚀 To start the system, run: python src/main.py" 