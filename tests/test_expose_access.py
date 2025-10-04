#!/usr/bin/env python3
"""
Expose.dev Access Test for Military Hierarchy System
This script tests if the Expose tunnels are working correctly.
"""

import requests
import sys
import time
from datetime import datetime

# Expose URLs
EXPOSE_URLS = {
    "Backend API": "https://military-api.sharedwithexpose.com",
    "Main Dashboard": "https://military-dashboard.sharedwithexpose.com", 
    "Reports UI": "https://military-reports.sharedwithexpose.com",
    "API Documentation": "https://military-api.sharedwithexpose.com/docs"
}

def test_expose_url(url, name, timeout=10):
    """Test if an Expose URL is accessible."""
    try:
        print(f"Testing {name}...")
        print(f"URL: {url}")
        
        response = requests.get(url, timeout=timeout)
        
        if response.status_code == 200:
            print(f"✅ SUCCESS: {name} is accessible!")
            return True
        else:
            print(f"❌ ERROR: {name} returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ CONNECTION FAILED: {name} - Cannot reach server")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ TIMEOUT: {name} - Request timed out after {timeout}s")
        return False
    except Exception as e:
        print(f"❌ ERROR: {name} - {e}")
        return False

def test_api_functionality():
    """Test API functionality through Expose."""
    print(f"\n{'='*60}")
    print("TESTING API FUNCTIONALITY THROUGH EXPOSE")
    print(f"{'='*60}")
    
    api_base = "https://military-api.sharedwithexpose.com"
    
    # Test 1: System status
    try:
        response = requests.get(f"{api_base}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ System Status: {data.get('status', 'unknown')}")
            print(f"   MQTT Connected: {data.get('mqtt_connected', False)}")
        else:
            print(f"❌ System Status: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ System Status: {e}")
    
    # Test 2: Get soldiers
    try:
        response = requests.get(f"{api_base}/soldiers", timeout=10)
        if response.status_code == 200:
            data = response.json()
            soldier_count = len(data.get('soldiers', []))
            print(f"✅ Soldiers: {soldier_count} found")
        else:
            print(f"❌ Soldiers: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Soldiers: {e}")
    
    # Test 3: Get units
    try:
        response = requests.get(f"{api_base}/units", timeout=10)
        if response.status_code == 200:
            data = response.json()
            unit_count = len(data.get('units', []))
            print(f"✅ Units: {unit_count} found")
        else:
            print(f"❌ Units: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Units: {e}")

def test_data_sending():
    """Test sending data through Expose API."""
    print(f"\n{'='*60}")
    print("TESTING DATA SENDING THROUGH EXPOSE")
    print(f"{'='*60}")
    
    api_base = "https://military-api.sharedwithexpose.com"
    
    # Test sending raw input
    try:
        test_data = {
            "raw_text": "Test message from Expose tunnel",
            "input_type": "voice",
            "confidence": 0.95,
            "location_ref": "EXPOSE_TEST"
        }
        
        # Use the first available soldier ID
        response = requests.post(f"{api_base}/soldiers/ALPHA_01/raw_inputs", 
                               json=test_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Raw Input: Successfully sent test data")
            print(f"   Input ID: {result.get('input_id', 'unknown')}")
        else:
            print(f"❌ Raw Input: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Raw Input: {e}")

def main():
    """Run comprehensive Expose access tests."""
    print("=" * 70)
    print("🌐 EXPOSE.DEV ACCESS TEST FOR MILITARY HIERARCHY SYSTEM")
    print("=" * 70)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("Testing Expose tunnel accessibility...")
    print("Make sure your local services are running and Expose tunnels are active!")
    print()
    
    # Test all Expose URLs
    results = {}
    for name, url in EXPOSE_URLS.items():
        results[name] = test_expose_url(url, name)
        print()
    
    # Test API functionality if backend is accessible
    if results.get("Backend API", False):
        test_api_functionality()
        test_data_sending()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 EXPOSE ACCESS TEST SUMMARY")
    print("=" * 70)
    
    accessible_count = sum(1 for accessible in results.values() if accessible)
    total_count = len(results)
    
    print(f"Accessible Services: {accessible_count}/{total_count}")
    print()
    
    for name, accessible in results.items():
        status = "✅ ACCESSIBLE" if accessible else "❌ NOT ACCESSIBLE"
        print(f"{name}: {status}")
    
    print()
    if accessible_count == total_count:
        print("🎉 ALL SERVICES ARE ACCESSIBLE VIA EXPOSE!")
        print()
        print("🌍 Your Military Hierarchy System is now globally accessible:")
        for name, url in EXPOSE_URLS.items():
            print(f"  • {name}: {url}")
        print()
        print("📱 Share these URLs with anyone, anywhere!")
        print("🔗 No network configuration needed - works from any device!")
    elif accessible_count > 0:
        print("⚠️  PARTIAL SUCCESS: Some services are accessible")
        print("Check the error messages above for troubleshooting")
    else:
        print("❌ NO SERVICES ACCESSIBLE VIA EXPOSE")
        print()
        print("Troubleshooting steps:")
        print("1. Make sure your local services are running")
        print("2. Check that Expose tunnels are active")
        print("3. Verify your internet connection")
        print("4. Check Expose token configuration")
    
    print()
    return 0 if accessible_count == total_count else 1

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
