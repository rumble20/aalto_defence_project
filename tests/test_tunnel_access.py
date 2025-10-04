#!/usr/bin/env python3
"""
Tunnel Access Test for Military Hierarchy System
This script helps test any tunneling solution (ngrok, localtunnel, etc.)
"""

import requests
import sys
import time
from datetime import datetime

def test_tunnel_url(url, name, timeout=10):
    """Test if a tunnel URL is accessible."""
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

def test_api_functionality(base_url):
    """Test API functionality through tunnel."""
    print(f"\n{'='*60}")
    print("TESTING API FUNCTIONALITY THROUGH TUNNEL")
    print(f"{'='*60}")
    
    # Test 1: System status
    try:
        response = requests.get(f"{base_url}/", timeout=10)
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
        response = requests.get(f"{base_url}/soldiers", timeout=10)
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
        response = requests.get(f"{base_url}/units", timeout=10)
        if response.status_code == 200:
            data = response.json()
            unit_count = len(data.get('units', []))
            print(f"✅ Units: {unit_count} found")
        else:
            print(f"❌ Units: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Units: {e}")

def main():
    """Run tunnel access tests."""
    print("=" * 70)
    print("🌐 TUNNEL ACCESS TEST FOR MILITARY HIERARCHY SYSTEM")
    print("=" * 70)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("Please enter your tunnel URLs:")
    print("(Get these from your ngrok/localtunnel/serveo windows)")
    print()
    
    # Get URLs from user
    backend_url = input("Backend API URL (e.g., https://abc123.ngrok.io): ").strip()
    if not backend_url:
        print("❌ No backend URL provided. Exiting.")
        return 1
    
    dashboard_url = input("Main Dashboard URL (e.g., https://def456.ngrok.io): ").strip()
    reports_url = input("Reports UI URL (e.g., https://ghi789.ngrok.io): ").strip()
    
    print()
    print("Testing tunnel accessibility...")
    print()
    
    # Test URLs
    urls_to_test = [
        (backend_url, "Backend API"),
        (f"{backend_url}/docs", "API Documentation")
    ]
    
    if dashboard_url:
        urls_to_test.append((dashboard_url, "Main Dashboard"))
    
    if reports_url:
        urls_to_test.append((reports_url, "Reports UI"))
    
    # Test all URLs
    results = {}
    for url, name in urls_to_test:
        results[name] = test_tunnel_url(url, name)
        print()
    
    # Test API functionality if backend is accessible
    if results.get("Backend API", False):
        test_api_functionality(backend_url)
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TUNNEL ACCESS TEST SUMMARY")
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
        print("🎉 ALL SERVICES ARE ACCESSIBLE VIA TUNNEL!")
        print()
        print("🌍 Your Military Hierarchy System is now globally accessible:")
        for name, url in zip([name for name, _ in urls_to_test], [url for url, _ in urls_to_test]):
            print(f"  • {name}: {url}")
        print()
        print("📱 Share these URLs with anyone, anywhere!")
        print("🔗 No network configuration needed - works from any device!")
    elif accessible_count > 0:
        print("⚠️  PARTIAL SUCCESS: Some services are accessible")
        print("Check the error messages above for troubleshooting")
    else:
        print("❌ NO SERVICES ACCESSIBLE VIA TUNNEL")
        print()
        print("Troubleshooting steps:")
        print("1. Make sure your local services are running")
        print("2. Check that your tunnel is active")
        print("3. Verify the tunnel URLs are correct")
        print("4. Test localhost access first")
    
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
