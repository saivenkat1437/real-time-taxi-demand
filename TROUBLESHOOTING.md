# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### ❌ "No module named 'dash'" Error
**Problem**: You're trying to run the system without activating the virtual environment.

**Solution**:
```bash
# Activate the virtual environment first
source venv/bin/activate

# Then run the demo
python demo.py
```

**Alternative**: Use the convenience script
```bash
./run_demo.sh
```

### ❌ "No module named 'src'" Error
**Problem**: Python can't find the src module.

**Solution**:
```bash
# Make sure you're in the project directory
cd /path/to/Real_time_taxi_demand

# Activate virtual environment
source venv/bin/activate

# Run from the project root
python demo.py
```

### ❌ "app.run_server has been replaced by app.run" Error
**Problem**: Using an older Dash API.

**Solution**: This has been fixed in the latest code. Update to the latest version.

### ❌ Dashboard not loading
**Problem**: Dashboard won't start or is not accessible.

**Solutions**:
1. **Check if port 8050 is available**:
   ```bash
   lsof -i :8050
   ```

2. **Try a different port**:
   ```bash
   # Edit .env file
   DASHBOARD_PORT=8051
   ```

3. **Check firewall settings**:
   ```bash
   # Allow the port
   sudo ufw allow 8050
   ```

### ❌ Kafka Connection Failed
**Problem**: Kafka is not running.

**Solutions**:
1. **For testing without Kafka**:
   ```bash
   ./run_demo.sh  # Uses mock data
   ```

2. **For full system with Kafka**:
   ```bash
   # Start Docker
   docker --version
   
   # Start Kafka
   ./kafka_setup.sh
   
   # Run full system
   python src/main.py
   ```

### ❌ Virtual Environment Issues
**Problem**: Virtual environment is corrupted or missing.

**Solution**:
```bash
# Remove old environment
rm -rf venv

# Recreate environment
./setup.sh
```

### ❌ Dependencies Issues
**Problem**: Missing or conflicting dependencies.

**Solution**:
```bash
# Activate environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### ❌ NYC API Issues
**Problem**: NYC API is not responding.

**Solution**: The system uses mock data by default for reliability. No action needed.

## 🔍 Debug Mode

To run with detailed logging:
```bash
# Set debug logging
export LOG_LEVEL=DEBUG

# Run demo
./run_demo.sh
```

## 📊 Health Check

Run the test suite to verify everything is working:
```bash
source venv/bin/activate
python test_simple.py
```

Expected output: All 4 tests should pass ✅

## 📞 Getting Help

1. **Check logs**: Look in `logs/taxi_demand.log`
2. **Run tests**: `python test_simple.py`
3. **Check environment**: `which python` (should show venv path)
4. **Verify dependencies**: `pip list | grep dash`

## 🚀 Quick Fixes

### Most Common Issues:
1. **Forgot to activate venv**: `source venv/bin/activate`
2. **Wrong directory**: Make sure you're in the project root
3. **Port conflict**: Change port in `.env` file
4. **Dependencies**: Reinstall with `pip install -r requirements.txt`

### Emergency Reset:
```bash
# Complete reset
rm -rf venv
./setup.sh
./run_demo.sh
``` 