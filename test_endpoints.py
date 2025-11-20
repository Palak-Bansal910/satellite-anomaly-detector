#!/usr/bin/env python3
"""
Test script to verify all API endpoints are working correctly.
Run this after starting the backend server.
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(method, endpoint, data=None, params=None, expected_status=200):
    """Test a single endpoint."""
    try:
        url = f"{BASE_URL}{endpoint}"
        print(f"\n{'='*60}")
        print(f"Testing {method.upper()} {endpoint}")
        print(f"{'='*60}")
        
        if method.upper() == "GET":
            response = requests.get(url, params=params, timeout=5)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=5)
        else:
            print(f"❌ Unknown method: {method}")
            return False
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == expected_status:
            print(f"✅ PASSED - Status {response.status_code}")
            try:
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2)[:500]}...")
            except:
                print(f"Response: {response.text[:200]}")
            return True
        else:
            print(f"❌ FAILED - Expected {expected_status}, got {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ FAILED - Could not connect to {BASE_URL}")
        print("Make sure the backend server is running!")
        return False
    except Exception as e:
        print(f"❌ FAILED - Error: {str(e)}")
        return False

def main():
    print("="*60)
    print("SATELLITE ANOMALY DETECTOR - API ENDPOINT TESTS")
    print("="*60)
    
    results = []
    
    # 1. Test root endpoint
    results.append(("GET", "/", test_endpoint("GET", "/")))
    
    # 2. Test GET /anomalies/latest
    results.append(("GET", "/anomalies/latest", test_endpoint("GET", "/anomalies/latest")))
    
    # 3. Test GET /anomalies/history
    results.append(("GET", "/anomalies/history", test_endpoint("GET", "/anomalies/history", params={"limit": 10})))
    
    # 4. Test POST /telemetry/ (send sample telemetry)
    sample_telemetry = {
        "timestamp": datetime.now().isoformat(),
        "satellite_id": "SAT-TEST-1",
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
    results.append(("POST", "/telemetry/", test_endpoint("POST", "/telemetry/", data=sample_telemetry)))
    
    # 5. Test POST /alerts/send (will return 503 if not configured - which is expected and more appropriate than 500)
    sample_alert = {
        "timestamp": datetime.now().isoformat(),
        "satellite_id": "SAT-TEST-1",
        "severity": "warning",
        "issues": ["High Temperature", "Packet Loss"],
        "score": 0.75
    }
    # Accept 503 (Service Unavailable) when not configured, or 200 if configured and working
    result = test_endpoint("POST", "/alerts/send", data=sample_alert, expected_status=503)
    if not result:
        # Try 200 in case it's configured
        result = test_endpoint("POST", "/alerts/send", data=sample_alert, expected_status=200)
    results.append(("POST", "/alerts/send", result))
    
    # 6. Test GET /docs (FastAPI auto-generated docs)
    results.append(("GET", "/docs", test_endpoint("GET", "/docs", expected_status=200)))
    
    # 7. Test GET /openapi.json (OpenAPI schema)
    results.append(("GET", "/openapi.json", test_endpoint("GET", "/openapi.json")))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    passed = sum(1 for _, _, result in results if result)
    total = len(results)
    
    for method, endpoint, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {method} {endpoint}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All endpoints are working correctly!")
    else:
        print("⚠️  Some endpoints need attention.")

if __name__ == "__main__":
    main()

