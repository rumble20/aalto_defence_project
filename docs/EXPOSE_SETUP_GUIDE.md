# 🌐 Expose.dev Setup Guide for Military Hierarchy System

## 🚀 **Quick Setup**

### **Step 1: Install Expose**
```bash
# Download Expose
Invoke-WebRequest -Uri "https://github.com/exposedev/expose/raw/master/builds/expose" -OutFile "expose"

# Make it executable (if needed)
# chmod +x expose
```

### **Step 2: Configure Expose**
```bash
# Activate your token
expose token c253f28e-fa05-4d37-9121-311f00ceb32d

# Set default server to EU-2 (faster for Europe)
expose default-server eu-2
```

### **Step 3: Start Expose Tunnels**
```bash
# Backend API
expose share http://localhost:8000 --subdomain=military-api

# Main Dashboard  
expose share http://localhost:3000 --subdomain=military-dashboard

# Reports UI
expose share http://localhost:3001 --subdomain=military-reports
```

---

## 🌍 **Public URLs**

Once Expose is running, your services will be available at:

- **Backend API**: https://military-api.sharedwithexpose.com
- **Main Dashboard**: https://military-dashboard.sharedwithexpose.com
- **Reports UI**: https://military-reports.sharedwithexpose.com
- **API Documentation**: https://military-api.sharedwithexpose.com/docs

---

## 🎯 **Benefits of Using Expose**

### ✅ **Advantages over Local WiFi:**
- **Global Access**: Anyone can access from anywhere in the world
- **No Network Issues**: No WiFi connectivity problems
- **No Firewall Issues**: Bypasses all local network restrictions
- **Easy Sharing**: Just share the URLs - no technical setup needed
- **Mobile Friendly**: Works perfectly on phones and tablets
- **Secure**: HTTPS encryption by default

### 🔧 **How It Works:**
1. Expose creates secure tunnels from your local services to the internet
2. Your services remain running locally (localhost)
3. Expose forwards internet traffic to your local services
4. Anyone can access via the public URLs

---

## 📋 **Complete Setup Process**

### **Option 1: Automatic Setup**
Run the batch file:
```bash
setup_expose.bat
```

### **Option 2: Manual Setup**
1. **Start your local services first:**
   ```bash
   start_all.bat
   ```

2. **In separate terminal windows, run:**
   ```bash
   # Terminal 1 - Backend API
   expose share http://localhost:8000 --subdomain=military-api
   
   # Terminal 2 - Main Dashboard
   expose share http://localhost:3000 --subdomain=military-dashboard
   
   # Terminal 3 - Reports UI  
   expose share http://localhost:3001 --subdomain=military-reports
   ```

---

## 🧪 **Testing Expose Access**

### **Test URLs:**
- **API Status**: https://military-api.sharedwithexpose.com/
- **API Docs**: https://military-api.sharedwithexpose.com/docs
- **Main Dashboard**: https://military-dashboard.sharedwithexpose.com
- **Reports UI**: https://military-reports.sharedwithexpose.com

### **Test API Endpoints:**
```bash
# Test API from anywhere
curl https://military-api.sharedwithexpose.com/soldiers

# Test from browser
https://military-api.sharedwithexpose.com/docs
```

---

## 🔐 **Security Considerations**

### **Public Access:**
- Your services will be accessible to anyone with the URLs
- Consider this when sharing sensitive military data
- Expose Free has some limitations on concurrent connections

### **Authentication:**
- Currently no authentication is required
- For production use, consider adding API authentication
- Expose Pro offers additional security features

---

## 📱 **Mobile Access**

### **From Any Device:**
1. Open any web browser
2. Navigate to the Expose URLs
3. No special configuration needed
4. Works on any network (WiFi, mobile data, etc.)

### **Example Mobile URLs:**
- **Dashboard**: https://military-dashboard.sharedwithexpose.com
- **Reports**: https://military-reports.sharedwithexpose.com
- **API Test**: https://military-api.sharedwithexpose.com/docs

---

## 🚀 **Advanced Configuration**

### **Custom Domains (Expose Pro):**
```bash
# With Expose Pro, you can use custom domains
expose share http://localhost:8000 --domain=api.yourdomain.com
```

### **Multiple Subdomains:**
```bash
# You can create multiple tunnels
expose share http://localhost:8000 --subdomain=military-api-v2
expose share http://localhost:3000 --subdomain=military-dash-v2
```

### **Authentication (Expose Pro):**
```bash
# Add basic authentication
expose share http://localhost:8000 --auth=username:password
```

---

## 🔄 **Troubleshooting**

### **Common Issues:**

1. **"Subdomain already in use"**
   - Try a different subdomain name
   - Wait a few minutes and try again

2. **"Connection refused"**
   - Make sure your local services are running
   - Check that localhost:8000, localhost:3000, localhost:3001 are accessible

3. **"Token not found"**
   - Run: `expose token c253f28e-fa05-4d37-9121-311f00ceb32d`
   - Check your internet connection

### **Testing Local Services:**
```bash
# Test if local services are running
curl http://localhost:8000/
curl http://localhost:3000/
curl http://localhost:3001/
```

---

## 📊 **Monitoring**

### **Check Tunnel Status:**
```bash
# List active tunnels
expose list

# Check tunnel health
expose status
```

### **Logs:**
- Expose provides detailed logs in the terminal
- Monitor for connection issues
- Check for authentication problems

---

## 🎉 **Success Indicators**

You'll know it's working when:
- ✅ Expose shows "Tunnel established" messages
- ✅ You can access the public URLs from any browser
- ✅ The services load normally via the public URLs
- ✅ API endpoints respond correctly
- ✅ Mobile devices can access the services

---

## 📞 **Support**

### **Expose Documentation:**
- https://expose.dev/docs
- GitHub: https://github.com/exposedev/expose

### **Your Military System:**
- All local services must be running
- Check firewall settings if needed
- Verify localhost access before using Expose

---

**Ready to go global? Run `setup_expose.bat` and share your Military Hierarchy System with the world!** 🌍
