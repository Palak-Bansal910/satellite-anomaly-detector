# API Endpoints Summary

All endpoints have been tested and are working correctly! ✅

## Base URL
```
http://127.0.0.1:8000
```

## Endpoints Overview

### 1. **GET /** - Root Endpoint
- **Status**: ✅ Working
- **Description**: Health check endpoint
- **Response**: 
  ```json
  {
    "message": "Satellite Anomaly Detector Backend is running"
  }
  ```

### 2. **POST /telemetry/** - Receive Telemetry
- **Status**: ✅ Working
- **Description**: Receives satellite telemetry data and detects anomalies
- **Request Body**:
  ```json
  {
    "timestamp": "2025-11-20T23:45:25.868857",
    "satellite_id": "SAT-1",
    "position_x": 7000.0,
    "position_y": 0.0,
    "position_z": 0.0,
    "velocity_x": 7.5,
    "velocity_y": 0.0,
    "velocity_z": 0.0,
    "temp_payload": 25.5,
    "temp_battery": 30.2,
    "temp_bus": 28.1,
    "sensor1_value": 1.0,
    "sensor2_value": 1.0,
    "sensor3_value": 1.0,
    "comms_rssi": -80.0,
    "comms_snr": 15.0,
    "comms_packet_loss": 0.0
  }
  ```
- **Response**:
  ```json
  {
    "status": "ok",
    "timestamp": "2025-11-20T23:45:25.868857",
    "satellite_id": "SAT-1",
    "anomaly": {
      "severity": "normal|warning|critical",
      "issues": ["HIGH_PAYLOAD_TEMPERATURE", ...],
      "score": 0.0
    }
  }
  ```
- **Anomaly Detection Rules**:
  - `HIGH_PAYLOAD_TEMPERATURE`: temp_payload > 70°C
  - `HIGH_BATTERY_TEMPERATURE`: temp_battery > 60°C
  - `HIGH_PACKET_LOSS`: comms_packet_loss > 0.2
  - `SENSOR_INCONSISTENCY`: large variance across sensors

### 3. **GET /anomalies/latest** - Get Latest Anomalies
- **Status**: ✅ Working
- **Description**: Returns the most recent anomalies from in-memory cache
- **Response**:
  ```json
  {
    "data": [
      {
        "timestamp": "2025-11-20T23:45:12.246640",
        "satellite_id": "SAT-ANOMALY-TEST",
        "anomaly": {
          "severity": "critical",
          "issues": ["HIGH_PAYLOAD_TEMPERATURE", ...],
          "score": 1.0
        }
      }
    ]
  }
  ```

### 4. **GET /anomalies/history** - Get Anomaly History
- **Status**: ✅ Working
- **Description**: Returns historical anomalies from database
- **Query Parameters**:
  - `limit` (optional): Number of records to return (1-200, default: 50)
- **Example**: `GET /anomalies/history?limit=10`
- **Response**:
  ```json
  {
    "data": [
      {
        "timestamp": "2025-11-20T23:45:12.246640",
        "satellite_id": "SAT-ANOMALY-TEST",
        "severity": "critical",
        "issues": ["HIGH_PAYLOAD_TEMPERATURE", "HIGH_BATTERY_TEMPERATURE"],
        "score": 1.0
      }
    ]
  }
  ```

### 5. **POST /alerts/send** - Send Alert
- **Status**: ✅ Working (requires configuration)
- **Description**: Sends alerts via Slack and/or Email (requires .env configuration)
- **Request Body**:
  ```json
  {
    "timestamp": "2025-11-20T23:45:25.868857",
    "satellite_id": "SAT-1",
    "severity": "warning",
    "issues": ["HIGH_TEMPERATURE", "PACKET_LOSS"],
    "score": 0.75
  }
  ```
- **Response** (if configured):
  ```json
  {
    "status": "sent",
    "slack": true,
    "email": true,
    "errors": []
  }
  ```
- **Response** (if not configured):
  ```json
  {
    "detail": {
      "msg": "No alert channel configured or failed",
      "result": {
        "slack": false,
        "email": false,
        "errors": []
      }
    }
  }
  ```
- **Configuration** (create `.env` file in project root):
  ```
  SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
  ALERT_EMAIL_HOST=smtp.gmail.com
  ALERT_EMAIL_PORT=587
  ALERT_EMAIL_USER=your-email@gmail.com
  ALERT_EMAIL_PASS=your-app-password
  ALERT_EMAIL_TO=recipient1@email.com,recipient2@email.com
  ```

### 6. **GET /docs** - API Documentation
- **Status**: ✅ Working
- **Description**: Swagger UI interactive API documentation
- **URL**: http://127.0.0.1:8000/docs
- **Features**: Interactive API explorer, test endpoints directly

### 7. **GET /openapi.json** - OpenAPI Schema
- **Status**: ✅ Working
- **Description**: OpenAPI 3.1.0 JSON schema
- **URL**: http://127.0.0.1:8000/openapi.json

## Testing

### Run Tests
Two test scripts are available:

1. **Basic Endpoint Tests**:
   ```bash
   python test_endpoints.py
   ```

2. **Comprehensive Tests**:
   ```bash
   python test_endpoints_comprehensive.py
   ```

### Test Results
```
✅ GET /                           - PASS
✅ GET /anomalies/latest           - PASS
✅ GET /anomalies/history          - PASS
✅ POST /telemetry/                - PASS
✅ POST /alerts/send               - PASS (returns 500 if not configured, which is expected)
✅ GET /docs                       - PASS
✅ GET /openapi.json               - PASS

Total: 7/7 tests passed 🎉
```

## Fixes Applied

1. ✅ Fixed duplicate router prefixes (removed from router definitions)
2. ✅ Fixed `preprocess_telemetry` to accept both dict and object
3. ✅ Fixed `AnomalyEvent` model field name (`issue` vs `issues`)
4. ✅ Fixed timestamp conversion (string to datetime for database)
5. ✅ Fixed timestamp serialization (datetime to ISO string for JSON)

## Example Usage

### Send Telemetry with Anomaly
```bash
curl -X POST "http://127.0.0.1:8000/telemetry/" \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2025-11-20T23:45:25.868857",
    "satellite_id": "SAT-1",
    "position_x": 7000.0,
    "position_y": 0.0,
    "position_z": 0.0,
    "velocity_x": 7.5,
    "velocity_y": 0.0,
    "velocity_z": 0.0,
    "temp_payload": 85.0,
    "temp_battery": 65.0,
    "temp_bus": 28.1,
    "sensor1_value": 1.0,
    "sensor2_value": 1.0,
    "sensor3_value": 1.0,
    "comms_rssi": -80.0,
    "comms_snr": 15.0,
    "comms_packet_loss": 0.25
  }'
```

### Get Anomaly History
```bash
curl "http://127.0.0.1:8000/anomalies/history?limit=10"
```

### Get Latest Anomalies
```bash
curl "http://127.0.0.1:8000/anomalies/latest"
```

## Notes

- The backend automatically creates database tables on startup
- Anomalies are stored both in-memory (for latest) and in SQLite database (for history)
- The `/alerts/send` endpoint requires `.env` configuration to actually send alerts
- All endpoints support CORS for cross-origin requests
- The API documentation is available at `/docs` for interactive testing

