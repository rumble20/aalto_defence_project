#!/usr/bin/env python3
"""
Test script to verify network access to the military hierarchy system.
This script tests if the services are accessible from the local network.
"""

import requests
import sys
import time

# Your local IP address
LOCAL_IP = "10.3.35.27"

# Service endpoints
SERVICES = {
    "Backend API": f"http://{LOCAL_IP}:8000",
    "Main Dashboard": f"http://{LOCAL_IP}:3000", 
    "Reports UI": f"http://{LOCAL_IP}:3001"
}

def test_service(name, url, timeout=5):
    """Test if a service is accessible."""
    try:
        print(f"Testing {name} at {url}...")
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"✅ {name} is accessible!")
            return True
        else:
            print(f"❌ {name} returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {name} is not accessible (connection refused)")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ {name} timed out after {timeout} seconds")
        return False
    except Exception as e:
        print(f"❌ {name} error: {e}")
        return False

def main():
    """Test all services for network accessibility."""
    print("=" * 60)
    print("Military Hierarchy System - Network Access Test")
    print("=" * 60)
    print(f"Testing services on IP: {LOCAL_IP}")
    print()
    
    results = {}
    
    for name, url in SERVICES.items():
        results[name] = test_service(name, url)
        print()
    
    print("=" * 60)
    print("Test Results Summary:")
    print("=" * 60)
    
    all_accessible = True
    for name, accessible in results.items():
        status = "✅ ACCESSIBLE" if accessible else "❌ NOT ACCESSIBLE"
        print(f"{name}: {status}")
        if not accessible:
            all_accessible = False
    
    print()
    if all_accessible:
        print("🎉 All services are accessible from the network!")
        print()
        print("You can now access the system from other devices on your WiFi:")
        for name, url in SERVICES.items():
            print(f"  {name}: {url}")
    else:
        print("⚠️  Some services are not accessible. Please check:")
        print("  1. Make sure all services are running")
        print("  2. Check Windows Firewall settings")
        print("  3. Verify the IP address is correct")
        print("  4. Ensure devices are on the same network")
    
    print()
    return 0 if all_accessible else 1

if __name__ == "__main__":
    sys.exit(main())
