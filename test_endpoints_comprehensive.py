#!/usr/bin/env python3
"""
Comprehensive test script to verify all API endpoints with different scenarios.
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def test_telemetry_with_anomaly():
    """Test telemetry endpoint with data that should trigger an anomaly."""
    print("\n" + "="*60)
    print("Testing POST /telemetry/ with HIGH TEMPERATURE (should trigger anomaly)")
    print("="*60)
    
    # High temperature that should trigger anomaly
    telemetry = {
        "timestamp": datetime.now().isoformat(),
        "satellite_id": "SAT-ANOMALY-TEST",
        "position_x": 7000.0,
        "position_y": 0.0,
        "position_z": 0.0,
        "velocity_x": 7.5,
        "velocity_y": 0.0,
        "velocity_z": 0.0,
        "temp_payload": 85.0,  # High temperature > 70
        "temp_battery": 65.0,  # High battery temp > 60
        "temp_bus": 28.1,
        "sensor1_value": 1.0,
        "sensor2_value": 1.0,
        "sensor3_value": 1.0,
        "comms_rssi": -80.0,
        "comms_snr": 15.0,
        "comms_packet_loss": 0.25  # High packet loss > 0.2
    }
    
    try:
        response = requests.post(f"{BASE_URL}/telemetry/", json=telemetry, timeout=5)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Telemetry received successfully")
            print(f"Anomaly Detected: {result.get('anomaly', {}).get('severity', 'unknown')}")
            print(f"Issues: {result.get('anomaly', {}).get('issues', [])}")
            print(f"Score: {result.get('anomaly', {}).get('score', 0)}")
            
            # Now check if it appears in /anomalies/latest
            print("\n" + "-"*60)
            print("Checking /anomalies/latest for the new anomaly...")
            latest_response = requests.get(f"{BASE_URL}/anomalies/latest", timeout=5)
            if latest_response.status_code == 200:
                latest_data = latest_response.json()
                anomalies = latest_data.get("data", [])
                if anomalies:
                    print(f"✅ Found {len(anomalies)} anomaly/ies in latest")
                    if len(anomalies) > 0:
                        print(f"   Latest: {anomalies[0].get('satellite_id')} - {anomalies[0].get('severity')}")
                else:
                    print("⚠️  No anomalies in latest (might be in-memory only)")
        else:
            print(f"❌ Failed: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_anomalies_history():
    """Test anomalies history endpoint with different limits."""
    print("\n" + "="*60)
    print("Testing GET /anomalies/history with different limits")
    print("="*60)
    
    for limit in [5, 10, 50]:
        try:
            response = requests.get(f"{BASE_URL}/anomalies/history", params={"limit": limit}, timeout=5)
            if response.status_code == 200:
                data = response.json()
                anomalies = data.get("data", [])
                print(f"✅ Limit {limit}: Found {len(anomalies)} anomalies")
            else:
                print(f"❌ Limit {limit}: Failed with status {response.status_code}")
        except Exception as e:
            print(f"❌ Limit {limit}: Error - {e}")

def main():
    print("="*60)
    print("COMPREHENSIVE ENDPOINT TESTS")
    print("="*60)
    
    # Test normal telemetry
    print("\n1. Testing normal telemetry (no anomalies)...")
    normal_telemetry = {
        "timestamp": datetime.now().isoformat(),
        "satellite_id": "SAT-NORMAL-1",
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
    try:
        response = requests.post(f"{BASE_URL}/telemetry/", json=normal_telemetry, timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Normal telemetry processed - Severity: {result.get('anomaly', {}).get('severity')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test anomaly detection
    test_telemetry_with_anomaly()
    
    # Test history endpoint
    test_anomalies_history()
    
    # Test root endpoint
    print("\n" + "="*60)
    print("Testing Root Endpoint")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print(f"✅ Root endpoint working: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*60)
    print("All comprehensive tests completed!")
    print("="*60)

if __name__ == "__main__":
    main()

