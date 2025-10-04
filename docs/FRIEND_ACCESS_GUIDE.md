# 🌐 Friend Access Guide

## Quick Setup for Your Friend

### Step 1: Connect to the Same WiFi
- Make sure your friend is connected to the **exact same WiFi network** as you
- Check the WiFi name matches exactly (case-sensitive)

### Step 2: Test Network Access
Your friend should open this test page in their browser:
**http://10.3.35.27:8000/friend_network_test.html**

This will automatically test all services and show what's working.

### Step 3: Direct Access URLs
If the test passes, your friend can access:

- **Main Dashboard**: http://10.3.35.27:3000
- **Reports UI**: http://10.3.35.27:3001  
- **API Documentation**: http://10.3.35.27:8000/docs
- **API Test Form**: http://10.3.35.27:8000/api_test_form.html

---

## 🔧 Troubleshooting for Your Friend

### If Nothing Works:
1. **Check WiFi Connection**
   - Make sure you're on the same WiFi network
   - Try disconnecting and reconnecting to WiFi

2. **Test Basic Connectivity**
   - Open Command Prompt (Windows) or Terminal (Mac/Linux)
   - Type: `ping 10.3.35.27`
   - If this fails, you're not on the same network

3. **Try Different Browser**
   - Try Chrome, Firefox, Safari, or Edge
   - Clear browser cache and cookies

4. **Check Firewall**
   - If you have antivirus/firewall software, temporarily disable it
   - Some security software blocks local network connections

### If Some Services Work:
- The network connection is fine
- Some services might be starting up
- Try refreshing the page after a few seconds

### If You Get "Connection Refused":
- The host computer might not be running the services
- Ask the host to restart the services
- Check if the host computer is in sleep mode

---

## 📱 Mobile Device Access

### From Phone/Tablet:
1. Connect to the same WiFi
2. Open any web browser
3. Go to: http://10.3.35.27:3000
4. The dashboard should load normally

### Common Mobile Issues:
- **"This site can't be reached"**: Not on same WiFi
- **"Connection timeout"**: Host computer firewall blocking
- **"Page loads but looks broken"**: Try a different browser

---

## 🖥️ Computer Access

### From Laptop/Desktop:
1. Connect to the same WiFi network
2. Open any web browser
3. Navigate to the URLs above
4. Everything should work normally

### Windows Users:
- If Windows Defender Firewall blocks the connection, temporarily disable it
- Or add an exception for the browser

### Mac Users:
- Check System Preferences > Security & Privacy > Firewall
- Allow connections for your browser

---

## 🆘 Still Not Working?

### Quick Tests:
1. **Ping Test**: Open terminal/command prompt and run:
   ```
   ping 10.3.35.27
   ```
   If this fails, you're not on the same network.

2. **Browser Test**: Try accessing:
   ```
   http://10.3.35.27:8000/docs
   ```
   This is the API documentation page.

3. **Network Test**: Ask the host to run:
   ```
   python quick_network_test.py
   ```

### Contact the Host:
If nothing works, ask the host to:
1. Check if all services are running
2. Restart the services
3. Check Windows Firewall settings
4. Verify the IP address hasn't changed

---

## ✅ Success Indicators

You'll know it's working when:
- ✅ The test page shows "SUCCESS" for all services
- ✅ You can access http://10.3.35.27:3000 in your browser
- ✅ The dashboard loads and shows military hierarchy data
- ✅ You can send data through the API test form

---

**Need Help?** Share the test results with the host - they'll show exactly what's working and what isn't!
