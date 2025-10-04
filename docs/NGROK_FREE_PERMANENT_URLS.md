# 🚀 ngrok Free - Permanent URLs Guide

## ✅ **You're Right! ngrok Free DOES Support Permanent URLs**

### **From ngrok Documentation:**
- **"ngrok static domain: 1"** - Free tier includes 1 static domain
- **"The free tier does NOT have timeouts on tunnels"** - Endpoints can run permanently
- **"If you'd like to run your endpoint all the time, you can do so, on the free tier"**

---

## 🎯 **How to Set Up Permanent URLs with ngrok Free**

### **Step 1: Reserve a Static Domain**
```bash
# Reserve a static domain (one-time setup)
ngrok config add-authtoken 33bQDyBGjGsGrNXeqEVbMkqY5v7_2EAARiJ7eGPMa4stCVZ62

# Reserve your static domain
ngrok http 8000 --domain=military-api.ngrok.io
```

### **Step 2: Your Permanent URLs**
- **Backend API**: `https://military-api.ngrok.io` (permanent!)
- **Main Dashboard**: `https://military-dashboard.ngrok.io` (permanent!)
- **Reports UI**: `https://military-reports.ngrok.io` (permanent!)

---

## 🔧 **Complete Setup for All 3 Services**

### **Option 1: Use 1 Static Domain + 2 Regular Tunnels**
```bash
# Terminal 1 - Backend API (Static Domain)
ngrok http 8000 --domain=military-api.ngrok.io

# Terminal 2 - Main Dashboard (Regular Tunnel)
ngrok http 3000

# Terminal 3 - Reports UI (Regular Tunnel)  
ngrok http 3001
```

### **Option 2: Use All 3 as Static Domains (Upgrade to Pro)**
```bash
# Terminal 1 - Backend API
ngrok http 8000 --domain=military-api.ngrok.io

# Terminal 2 - Main Dashboard
ngrok http 3000 --domain=military-dashboard.ngrok.io

# Terminal 3 - Reports UI
ngrok http 3001 --domain=military-reports.ngrok.io
```

---

## 🎯 **Recommended Setup (Free Tier)**

### **Best Approach:**
1. **Use 1 static domain** for your main API (most important)
2. **Use regular tunnels** for the other services
3. **Share the static domain** as your primary URL

### **Your URLs:**
- **Backend API**: `https://military-api.ngrok.io` (permanent!)
- **Main Dashboard**: `https://abc123.ngrok-free.dev` (changes)
- **Reports UI**: `https://def456.ngrok-free.dev` (changes)

### **For Team Sharing:**
- **Primary URL**: `https://military-api.ngrok.io` (never changes)
- **Dashboard**: Use the regular tunnel URL
- **Reports**: Use the regular tunnel URL

---

## 🚀 **Quick Start with Permanent API URL**

### **Step 1: Start Your Services**
```bash
# Terminal 1 - Backend API
cd aalto_defence_project
python backend.py

# Terminal 2 - Main Dashboard
cd aalto_defence_project/mil_dashboard
npm run dev

# Terminal 3 - Reports UI
cd aalto_defence_project/ui-for-reports/frontend
npm run dev
```

### **Step 2: Start ngrok Tunnels**
```bash
# Terminal 4 - Backend API (Static Domain)
ngrok http 8000 --domain=military-api.ngrok.io

# Terminal 5 - Main Dashboard (Regular Tunnel)
ngrok http 3000

# Terminal 6 - Reports UI (Regular Tunnel)
ngrok http 3001
```

### **Step 3: Your URLs**
- **Backend API**: `https://military-api.ngrok.io` (permanent!)
- **API Documentation**: `https://military-api.ngrok.io/docs`
- **Main Dashboard**: `https://abc123.ngrok-free.dev`
- **Reports UI**: `https://def456.ngrok-free.dev`

---

## 🎉 **Benefits of This Setup**

### ✅ **Advantages:**
- **Permanent API URL** for your backend
- **Professional looking** main URL
- **Free tier** - no monthly costs
- **Always available** - no timeouts
- **Easy to share** with team members

### 🌍 **Perfect For:**
- **Team collaboration** - share the permanent API URL
- **Mobile app development** - hardcode the permanent URL
- **Client demos** - professional permanent URL
- **Production use** - reliable permanent access

---

## 📱 **For Your Friend**

### **Share These URLs:**
- **Main API**: `https://military-api.ngrok.io` (permanent!)
- **Dashboard**: Use the regular tunnel URL from Terminal 5
- **Reports**: Use the regular tunnel URL from Terminal 6

### **No Setup Required:**
- Works from any device
- Works from any network
- Works from anywhere in the world
- No firewall issues

---

## 🎯 **Summary**

**You were absolutely right!** ngrok Free DOES support permanent URLs:

1. **1 static domain** included in free tier
2. **No timeouts** on tunnels
3. **Can run permanently** as background service
4. **Professional URLs** like `military-api.ngrok.io`

**Your Military Hierarchy System can have a permanent, professional URL for free!** 🌍
