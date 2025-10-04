# 🌐 Free Permanent URL Solutions

## 🚀 **Option 1: LocalTunnel (Free, Custom Subdomains)**

### **Setup:**
```bash
# Install LocalTunnel
npm install -g localtunnel

# Start with custom subdomains
lt --port 8000 --subdomain military-api
lt --port 3000 --subdomain military-dashboard  
lt --port 3001 --subdomain military-reports
```

### **Your Permanent URLs:**
- **Backend API**: `https://military-api.loca.lt`
- **Main Dashboard**: `https://military-dashboard.loca.lt`
- **Reports UI**: `https://military-reports.loca.lt`

**✅ Benefits:** Free, custom subdomains, URLs stay the same
**❌ Limitations:** URLs change if subdomain is taken

---

## 🌐 **Option 2: Serveo (Free, SSH-based)**

### **Setup:**
```bash
# No installation needed - uses SSH
ssh -R 80:localhost:8000 serveo.net
ssh -R 80:localhost:3000 serveo.net
ssh -R 80:localhost:3001 serveo.net
```

### **Your URLs:**
- **Backend API**: `https://abc123.serveo.net`
- **Main Dashboard**: `https://def456.serveo.net`
- **Reports UI**: `https://ghi789.serveo.net`

**✅ Benefits:** Free, no installation, works anywhere
**❌ Limitations:** URLs are random, change each time

---

## 🏠 **Option 3: Deploy to Free Cloud Platforms**

### **Railway (Free Tier):**
```bash
# Deploy your services to Railway
# Get permanent URLs like:
# https://military-api-production.up.railway.app
# https://military-dashboard-production.up.railway.app
```

### **Heroku (Free Tier):**
```bash
# Deploy to Heroku
# Get permanent URLs like:
# https://military-api.herokuapp.com
# https://military-dashboard.herokuapp.com
```

### **Vercel (Free Tier):**
```bash
# Deploy frontend to Vercel
# Get permanent URLs like:
# https://military-dashboard.vercel.app
# https://military-reports.vercel.app
```

---

## 🔧 **Option 4: Use Your Own Domain (Free)**

### **If you have a domain:**
```bash
# Use Cloudflare Tunnel with your domain
cloudflared tunnel create military-system
cloudflared tunnel route dns military-system api.yourdomain.com
cloudflared tunnel route dns military-system dashboard.yourdomain.com
cloudflared tunnel route dns military-system reports.yourdomain.com
```

### **Your Permanent URLs:**
- **Backend API**: `https://api.yourdomain.com`
- **Main Dashboard**: `https://dashboard.yourdomain.com`
- **Reports UI**: `https://reports.yourdomain.com`

---

## 🎯 **Recommended Free Solution: LocalTunnel**

### **Why LocalTunnel:**
- **Completely free**
- **Custom subdomains** (military-api, military-dashboard, etc.)
- **URLs stay the same** as long as you use the same subdomain
- **Easy setup** - just install and run

### **Quick Setup:**
```bash
# Install LocalTunnel
npm install -g localtunnel

# Start your local services first
python backend.py                    # Terminal 1
npm run dev                          # Terminal 2 (mil_dashboard)
npm run dev                          # Terminal 3 (ui-for-reports/frontend)

# Start LocalTunnel tunnels
lt --port 8000 --subdomain military-api      # Terminal 4
lt --port 3000 --subdomain military-dashboard # Terminal 5
lt --port 3001 --subdomain military-reports  # Terminal 6
```

### **Your Permanent URLs:**
- **Backend API**: `https://military-api.loca.lt`
- **Main Dashboard**: `https://military-dashboard.loca.lt`
- **Reports UI**: `https://military-reports.loca.lt`

---

## 🚀 **Alternative: Deploy to Free Cloud**

### **Railway (Recommended):**
1. **Sign up** at railway.app
2. **Connect GitHub** repository
3. **Deploy** your services
4. **Get permanent URLs** automatically

### **Benefits:**
- **Completely free** for small projects
- **Permanent URLs** that never change
- **Professional** looking URLs
- **No local computer** needed to run services

---

## 📱 **Quick Start with LocalTunnel**

### **Step 1: Install LocalTunnel**
```bash
npm install -g localtunnel
```

### **Step 2: Start Your Services**
```bash
# Terminal 1
cd aalto_defence_project
python backend.py

# Terminal 2  
cd aalto_defence_project/mil_dashboard
npm run dev

# Terminal 3
cd aalto_defence_project/ui-for-reports/frontend
npm run dev
```

### **Step 3: Start LocalTunnel**
```bash
# Terminal 4
lt --port 8000 --subdomain military-api

# Terminal 5
lt --port 3000 --subdomain military-dashboard

# Terminal 6
lt --port 3001 --subdomain military-reports
```

### **Step 4: Share Your URLs**
- **Backend API**: `https://military-api.loca.lt`
- **Main Dashboard**: `https://military-dashboard.loca.lt`
- **Reports UI**: `https://military-reports.loca.lt`

---

## 🎉 **Benefits of These Solutions**

### ✅ **Advantages:**
- **Completely free**
- **Permanent URLs** (with LocalTunnel)
- **Professional** looking URLs
- **Easy setup**
- **No monthly costs**

### 🌍 **Perfect For:**
- **Team collaboration**
- **Client demos**
- **Mobile app development**
- **Production use**

**Your Military Hierarchy System will have permanent, professional URLs for free!** 🌍

