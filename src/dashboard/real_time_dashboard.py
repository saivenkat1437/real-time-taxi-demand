import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List
from kafka import KafkaConsumer
import threading
import time
from src.utils.config import config

logger = logging.getLogger(__name__)

class RealTimeDashboard:
    """Real-time dashboard for taxi demand visualization."""
    
    def __init__(self):
        self.dashboard_config = config.get_dashboard_config()
        self.kafka_config = config.get_kafka_config()
        
        # Initialize Dash app
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.app.title = "Real-Time Taxi Demand Forecasting"
        
        # Data storage
        self.demand_data = []
        self.anomaly_data = []
        self.heatmap_data = []
        
        # Kafka consumer
        self.consumer = None
        self._initialize_kafka_consumer()
        
        # Setup dashboard layout
        self._setup_layout()
        self._setup_callbacks()
        
        # Start data collection thread
        self.data_thread = threading.Thread(target=self._collect_data, daemon=True)
        self.data_thread.start()
    
    def _initialize_kafka_consumer(self):
        """Initialize Kafka consumer for real-time data."""
        try:
            self.consumer = KafkaConsumer(
                self.kafka_config['topic_aggregated'],
                self.kafka_config['topic_anomalies'],
                bootstrap_servers=self.kafka_config['bootstrap_servers'],
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                auto_offset_reset='latest',
                enable_auto_commit=True,
                group_id='dashboard_consumer'
            )
            logger.info("Kafka consumer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka consumer: {e}")
            raise
    
    def _setup_layout(self):
        """Setup the dashboard layout."""
        self.app.layout = dbc.Container([
            # Header
            dbc.Row([
                dbc.Col([
                    html.H1("🚕 Real-Time Taxi Demand Forecasting", 
                           className="text-center mb-4"),
                    html.Hr()
                ])
            ]),
            
            # Main content
            dbc.Row([
                # Demand Overview
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("📊 Demand Overview"),
                        dbc.CardBody([
                            dcc.Graph(id='demand-overview-graph'),
                            dcc.Interval(
                                id='demand-interval',
                                interval=5000,  # Update every 5 seconds
                                n_intervals=0
                            )
                        ])
                    ])
                ], width=6),
                
                # Anomaly Alerts
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("🚨 Anomaly Alerts"),
                        dbc.CardBody([
                            html.Div(id='anomaly-alerts'),
                            dcc.Interval(
                                id='anomaly-interval',
                                interval=3000,  # Update every 3 seconds
                                n_intervals=0
                            )
                        ])
                    ])
                ], width=6)
            ], className="mb-4"),
            
            # Heatmap and Forecast
            dbc.Row([
                # Demand Heatmap
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("🗺️ Demand Heatmap"),
                        dbc.CardBody([
                            dcc.Graph(id='demand-heatmap'),
                            dcc.Interval(
                                id='heatmap-interval',
                                interval=10000,  # Update every 10 seconds
                                n_intervals=0
                            )
                        ])
                    ])
                ], width=6),
                
                # Demand Forecast
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("🔮 Demand Forecast"),
                        dbc.CardBody([
                            dcc.Graph(id='demand-forecast'),
                            dcc.Interval(
                                id='forecast-interval',
                                interval=15000,  # Update every 15 seconds
                                n_intervals=0
                            )
                        ])
                    ])
                ], width=6)
            ], className="mb-4"),
            
            # Statistics Cards
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(id='total-trips', className="text-center"),
                            html.P("Total Trips", className="text-center text-muted")
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(id='active-locations', className="text-center"),
                            html.P("Active Locations", className="text-center text-muted")
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(id='avg-fare', className="text-center"),
                            html.P("Average Fare", className="text-center text-muted")
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(id='anomaly-count', className="text-center"),
                            html.P("Anomalies Detected", className="text-center text-muted")
                        ])
                    ])
                ], width=3)
            ])
        ], fluid=True)
    
    def _setup_callbacks(self):
        """Setup dashboard callbacks."""
        
        @self.app.callback(
            Output('demand-overview-graph', 'figure'),
            Input('demand-interval', 'n_intervals')
        )
        def update_demand_overview(n):
            """Update demand overview graph."""
            if not self.demand_data:
                return self._create_empty_figure("No demand data available")
            
            # Create time series of demand
            df = pd.DataFrame(self.demand_data[-50:])  # Last 50 records
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df.get('timestamp', []),
                y=df.get('trip_count', []),
                mode='lines+markers',
                name='Trip Count',
                line=dict(color='blue', width=2)
            ))
            
            fig.update_layout(
                title="Real-Time Trip Demand",
                xaxis_title="Time",
                yaxis_title="Number of Trips",
                height=400,
                showlegend=True
            )
            
            return fig
        
        @self.app.callback(
            Output('anomaly-alerts', 'children'),
            Input('anomaly-interval', 'n_intervals')
        )
        def update_anomaly_alerts(n):
            """Update anomaly alerts."""
            if not self.anomaly_data:
                return html.P("No anomalies detected", className="text-muted")
            
            alerts = []
            for anomaly in self.anomaly_data[-10:]:  # Last 10 anomalies
                alert_color = "danger" if anomaly.get('type') == 'high_demand' else "warning"
                alert_icon = "🚨" if anomaly.get('type') == 'high_demand' else "⚠️"
                
                alerts.append(
                    dbc.Alert([
                        html.Strong(f"{alert_icon} {anomaly.get('type', 'Unknown')}"),
                        html.Br(),
                        f"Location: {anomaly.get('location_id', 'Unknown')}",
                        html.Br(),
                        f"Value: {anomaly.get('value', 0)}",
                        html.Br(),
                        f"Threshold: {anomaly.get('threshold', 0)}"
                    ], color=alert_color, className="mb-2")
                )
            
            return alerts
        
        @self.app.callback(
            Output('demand-heatmap', 'figure'),
            Input('heatmap-interval', 'n_intervals')
        )
        def update_demand_heatmap(n):
            """Update demand heatmap."""
            if not self.heatmap_data:
                return self._create_empty_figure("No heatmap data available")
            
            df = pd.DataFrame(self.heatmap_data)
            
            if df.empty:
                return self._create_empty_figure("No heatmap data available")
            
            fig = px.scatter_mapbox(
                df,
                lat='latitude',
                lon='longitude',
                size='trip_count',
                color='trip_count',
                hover_name='location_id',
                hover_data=['trip_count', 'avg_fare'],
                color_continuous_scale='Reds',
                zoom=10,
                center={'lat': 40.7128, 'lon': -74.0060}  # NYC coordinates
            )
            
            fig.update_layout(
                mapbox_style='open-street-map',
                title="Taxi Demand Heatmap",
                height=400
            )
            
            return fig
        
        @self.app.callback(
            Output('demand-forecast', 'figure'),
            Input('forecast-interval', 'n_intervals')
        )
        def update_demand_forecast(n):
            """Update demand forecast."""
            if not self.demand_data:
                return self._create_empty_figure("No forecast data available")
            
            # Simple forecasting visualization
            df = pd.DataFrame(self.demand_data[-20:])  # Last 20 records
            
            if df.empty:
                return self._create_empty_figure("No forecast data available")
            
            fig = go.Figure()
            
            # Current demand
            fig.add_trace(go.Scatter(
                x=df.get('timestamp', []),
                y=df.get('trip_count', []),
                mode='lines+markers',
                name='Current Demand',
                line=dict(color='blue', width=2)
            ))
            
            # Forecast (simple extrapolation)
            if len(df) > 1:
                last_demand = df['trip_count'].iloc[-1]
                forecast_values = [last_demand * 1.1, last_demand * 1.2, last_demand * 1.3]
                forecast_times = [
                    datetime.now() + timedelta(hours=1),
                    datetime.now() + timedelta(hours=2),
                    datetime.now() + timedelta(hours=3)
                ]
                
                fig.add_trace(go.Scatter(
                    x=forecast_times,
                    y=forecast_values,
                    mode='lines+markers',
                    name='Forecast',
                    line=dict(color='red', width=2, dash='dash')
                ))
            
            fig.update_layout(
                title="Demand Forecast (Next 3 Hours)",
                xaxis_title="Time",
                yaxis_title="Predicted Trips",
                height=400,
                showlegend=True
            )
            
            return fig
        
        @self.app.callback(
            [Output('total-trips', 'children'),
             Output('active-locations', 'children'),
             Output('avg-fare', 'children'),
             Output('anomaly-count', 'children')],
            Input('demand-interval', 'n_intervals')
        )
        def update_statistics(n):
            """Update statistics cards."""
            if not self.demand_data:
                return "0", "0", "$0.00", "0"
            
            df = pd.DataFrame(self.demand_data)
            
            total_trips = df['trip_count'].sum() if 'trip_count' in df.columns else 0
            active_locations = len(df['pickup_location_id'].unique()) if 'pickup_location_id' in df.columns else 0
            avg_fare = f"${df['avg_fare'].mean():.2f}" if 'avg_fare' in df.columns else "$0.00"
            anomaly_count = len(self.anomaly_data)
            
            return str(total_trips), str(active_locations), avg_fare, str(anomaly_count)
    
    def _create_empty_figure(self, message: str):
        """Create an empty figure with a message."""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=400
        )
        return fig
    
    def _collect_data(self):
        """Collect data from Kafka topics."""
        try:
            for message in self.consumer:
                try:
                    data = message.value
                    topic = message.topic
                    
                    if topic == self.kafka_config['topic_aggregated']:
                        if isinstance(data, dict) and data.get('type') == 'heatmap':
                            self.heatmap_data = data.get('data', [])
                        else:
                            self.demand_data.append(data)
                    
                    elif topic == self.kafka_config['topic_anomalies']:
                        self.anomaly_data.append(data)
                    
                    # Keep only recent data
                    if len(self.demand_data) > 1000:
                        self.demand_data = self.demand_data[-500:]
                    
                    if len(self.anomaly_data) > 100:
                        self.anomaly_data = self.anomaly_data[-50:]
                    
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in data collection: {e}")
    
    def run(self):
        """Run the dashboard."""
        try:
            logger.info(f"Starting dashboard on {self.dashboard_config['host']}:{self.dashboard_config['port']}")
            self.app.run(
                host=self.dashboard_config['host'],
                port=self.dashboard_config['port'],
                debug=False
            )
        except Exception as e:
            logger.error(f"Error running dashboard: {e}")
            raise
    
    def stop(self):
        """Stop the dashboard."""
        if self.consumer:
            self.consumer.close()
            logger.info("Dashboard stopped") 