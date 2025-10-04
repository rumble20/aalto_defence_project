#!/usr/bin/env python3
"""
Quick Network Test - Verify WiFi accessibility
This script provides a simple way to test if the services are accessible from the network.
"""

import requests
import sys

# Your network IP
LOCAL_IP = "10.3.35.27"

def test_url(url, name):
    """Test a single URL and return status."""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"OK {name}: {url} - ACCESSIBLE")
            return True
        else:
            print(f"ERROR {name}: {url} - Status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"ERROR {name}: {url} - CONNECTION REFUSED")
        return False
    except Exception as e:
        print(f"ERROR {name}: {url} - ERROR: {e}")
        return False

def main():
    """Quick test of all services."""
    print("=" * 60)
    print("QUICK NETWORK ACCESSIBILITY TEST")
    print("=" * 60)
    print(f"Testing IP: {LOCAL_IP}")
    print()
    
    # Test URLs
    services = [
        (f"http://{LOCAL_IP}:8000/", "Backend API"),
        (f"http://{LOCAL_IP}:8000/docs", "API Documentation"),
        (f"http://{LOCAL_IP}:3000/", "Main Dashboard"),
        (f"http://{LOCAL_IP}:3001/", "Reports UI")
    ]
    
    results = []
    for url, name in services:
        results.append(test_url(url, name))
    
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    accessible_count = sum(results)
    total_count = len(results)
    
    if accessible_count == total_count:
        print("SUCCESS! ALL SERVICES ARE ACCESSIBLE FROM YOUR WIFI NETWORK!")
        print()
        print("Share these URLs with team members:")
        for url, name in services:
            print(f"  {name}: {url}")
        print()
        print("Anyone on your WiFi can access these URLs from:")
        print("  - Mobile phones")
        print("  - Tablets") 
        print("  - Other laptops/computers")
        return 0
    else:
        print(f"WARNING: {accessible_count}/{total_count} services accessible")
        print()
        print("Some services may not be accessible from other devices.")
        print("Check Windows Firewall settings or restart the services.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
