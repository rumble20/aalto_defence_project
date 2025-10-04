#!/usr/bin/env python3
"""
Network Accessibility Test for Military Hierarchy System
This script tests if all services are accessible from the local WiFi network.
"""

import requests
import sys
import time
import json
from datetime import datetime

# Your local IP address
LOCAL_IP = "10.3.35.27"

# Service endpoints to test
SERVICES = {
    "Backend API": {
        "url": f"http://{LOCAL_IP}:8000",
        "endpoints": [
            "/",
            "/docs",
            "/units",
            "/soldiers",
            "/hierarchy"
        ]
    },
    "Main Dashboard": {
        "url": f"http://{LOCAL_IP}:3000",
        "endpoints": ["/"]
    },
    "Reports UI": {
        "url": f"http://{LOCAL_IP}:3001", 
        "endpoints": ["/"]
    }
}

def test_endpoint(service_name, base_url, endpoint, timeout=10):
    """Test if a specific endpoint is accessible."""
    full_url = f"{base_url}{endpoint}"
    try:
        print(f"  Testing {endpoint}...")
        response = requests.get(full_url, timeout=timeout)
        
        if response.status_code == 200:
            print(f"    OK {endpoint} - Status: {response.status_code}")
            return True
        else:
            print(f"    WARNING {endpoint} - Status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"    ERROR {endpoint} - Connection refused")
        return False
    except requests.exceptions.Timeout:
        print(f"    ERROR {endpoint} - Timeout after {timeout}s")
        return False
    except Exception as e:
        print(f"    ERROR {endpoint} - Error: {e}")
        return False

def test_service(service_name, service_config):
    """Test all endpoints for a service."""
    print(f"\nTesting {service_name}")
    print(f"Base URL: {service_config['url']}")
    print("-" * 50)
    
    results = {}
    base_url = service_config['url']
    
    for endpoint in service_config['endpoints']:
        results[endpoint] = test_endpoint(service_name, base_url, endpoint)
    
    # Overall service status
    successful_endpoints = sum(1 for success in results.values() if success)
    total_endpoints = len(results)
    
    if successful_endpoints == total_endpoints:
        print(f"SUCCESS {service_name} - ALL ENDPOINTS ACCESSIBLE")
        return True
    elif successful_endpoints > 0:
        print(f"PARTIAL {service_name} - PARTIALLY ACCESSIBLE ({successful_endpoints}/{total_endpoints})")
        return False
    else:
        print(f"FAILED {service_name} - NOT ACCESSIBLE")
        return False

def test_api_functionality():
    """Test API functionality by making actual requests."""
    print(f"\nTesting API Functionality")
    print("-" * 50)
    
    api_base = f"http://{LOCAL_IP}:8000"
    
    # Test 1: Get system status
    try:
        response = requests.get(f"{api_base}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"OK System Status: {data.get('status', 'unknown')}")
            print(f"   MQTT Connected: {data.get('mqtt_connected', False)}")
        else:
            print(f"ERROR System Status: HTTP {response.status_code}")
    except Exception as e:
        print(f"ERROR System Status: {e}")
    
    # Test 2: Get soldiers
    try:
        response = requests.get(f"{api_base}/soldiers", timeout=10)
        if response.status_code == 200:
            data = response.json()
            soldier_count = len(data.get('soldiers', []))
            print(f"OK Soldiers: {soldier_count} found")
        else:
            print(f"ERROR Soldiers: HTTP {response.status_code}")
    except Exception as e:
        print(f"ERROR Soldiers: {e}")
    
    # Test 3: Get units
    try:
        response = requests.get(f"{api_base}/units", timeout=10)
        if response.status_code == 200:
            data = response.json()
            unit_count = len(data.get('units', []))
            print(f"OK Units: {unit_count} found")
        else:
            print(f"ERROR Units: HTTP {response.status_code}")
    except Exception as e:
        print(f"ERROR Units: {e}")

def test_from_external_perspective():
    """Test as if accessing from another device on the network."""
    print(f"\nExternal Device Simulation")
    print("-" * 50)
    print("Testing as if accessing from another device on your WiFi...")
    
    # Test basic connectivity
    test_urls = [
        f"http://{LOCAL_IP}:8000/",
        f"http://{LOCAL_IP}:3000/",
        f"http://{LOCAL_IP}:3001/"
    ]
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=5)
            service_name = url.split(':')[-2].split('.')[-1] + ":" + url.split(':')[-1].split('/')[0]
            if response.status_code == 200:
                print(f"OK {service_name} - Accessible from network")
            else:
                print(f"WARNING {service_name} - Status {response.status_code}")
        except Exception as e:
            print(f"ERROR {service_name} - {e}")

def main():
    """Run comprehensive network accessibility tests."""
    print("=" * 70)
    print("Military Hierarchy System - Network Accessibility Test")
    print("=" * 70)
    print(f"Testing from IP: {LOCAL_IP}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test each service
    service_results = {}
    for service_name, service_config in SERVICES.items():
        service_results[service_name] = test_service(service_name, service_config)
    
    # Test API functionality
    test_api_functionality()
    
    # Test external perspective
    test_from_external_perspective()
    
    # Summary
    print("\n" + "=" * 70)
    print("NETWORK ACCESSIBILITY SUMMARY")
    print("=" * 70)
    
    all_accessible = True
    for service_name, accessible in service_results.items():
        status = "ACCESSIBLE" if accessible else "NOT ACCESSIBLE"
        print(f"{service_name}: {status}")
        if not accessible:
            all_accessible = False
    
    print()
    if all_accessible:
        print("SUCCESS! All services are accessible from your WiFi network!")
        print()
        print("Access URLs for other devices on your WiFi:")
        print(f"  - Backend API: http://{LOCAL_IP}:8000")
        print(f"  - API Documentation: http://{LOCAL_IP}:8000/docs")
        print(f"  - Main Dashboard: http://{LOCAL_IP}:3000")
        print(f"  - Reports UI: http://{LOCAL_IP}:3001")
        print()
        print("Share these URLs with team members on the same WiFi network!")
    else:
        print("Some services are not accessible. Troubleshooting steps:")
        print()
        print("1. Check Windows Firewall:")
        print("   - Open Windows Defender Firewall")
        print("   - Allow Python and Node.js through firewall")
        print("   - Or temporarily disable firewall for testing")
        print()
        print("2. Verify Network:")
        print("   - Ensure all devices are on the same WiFi network")
        print("   - Try pinging this machine: ping 10.3.35.27")
        print()
        print("3. Check Services:")
        print("   - Make sure all services are running")
        print("   - Check for port conflicts")
        print("   - Restart services if needed")
        print()
        print("4. Test from another device:")
        print("   - Open browser on phone/laptop")
        print("   - Try accessing the URLs above")
    
    print()
    return 0 if all_accessible else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)