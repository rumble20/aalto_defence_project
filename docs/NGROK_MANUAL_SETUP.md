# 🚀 Manual ngrok Setup for Military Hierarchy System

## 📋 **Step-by-Step Instructions**

### **Step 1: Start Your Local Services**

Open **3 separate Command Prompt/PowerShell windows** and run:

**Window 1 - Backend API:**
```bash
cd C:\Users\henri\Documents\hackathon\aalto_defence_project
python backend.py
```

**Window 2 - Main Dashboard:**
```bash
cd C:\Users\henri\Documents\hackathon\aalto_defence_project\mil_dashboard
npm run dev
```

**Window 3 - Reports UI:**
```bash
cd C:\Users\henri\Documents\hackathon\aalto_defence_project\ui-for-reports\frontend
npm run dev
```

### **Step 2: Start ngrok Tunnels**

Open **3 more Command Prompt/PowerShell windows** and run:

**Window 4 - Backend API Tunnel:**
```bash
ngrok http 8000
```

**Window 5 - Main Dashboard Tunnel:**
```bash
ngrok http 3000
```

**Window 6 - Reports UI Tunnel:**
```bash
ngrok http 3001
```

### **Step 3: Get Your Public URLs**

In each ngrok window, you'll see something like:
```
Forwarding    https://abc123.ngrok-free.dev -> http://localhost:8000
Forwarding    https://def456.ngrok-free.dev -> http://localhost:3000
Forwarding    https://ghi789.ngrok-free.dev -> http://localhost:3001
```

### **Step 4: Share Your URLs**

Your Military Hierarchy System will be accessible at:
- **Backend API**: `https://abc123.ngrok-free.dev`
- **API Documentation**: `https://abc123.ngrok-free.dev/docs`
- **Main Dashboard**: `https://def456.ngrok-free.dev`
- **Reports UI**: `https://ghi789.ngrok-free.dev`

---

## 🌍 **How ngrok Works**

### **Multiple Endpoints:**
- **Each service needs its own ngrok tunnel**
- **Each tunnel gets a unique URL**
- **You need 3 separate ngrok processes running**

### **URL Permanence:**
- **Free tier**: URLs change every time you restart ngrok
- **Paid tier**: You can get permanent custom domains
- **Current session**: URLs stay the same until you restart ngrok

### **Traffic Flow:**
```
Internet → ngrok URL → ngrok servers → your local service
```

---

## 🎯 **Quick Test**

### **Test Your Services:**
1. **Backend API**: Visit `https://your-backend-url.ngrok-free.dev`
2. **Main Dashboard**: Visit `https://your-dashboard-url.ngrok-free.dev`
3. **Reports UI**: Visit `https://your-reports-url.ngrok-free.dev`

### **Test API:**
- **API Docs**: `https://your-backend-url.ngrok-free.dev/docs`
- **Soldiers**: `https://your-backend-url.ngrok-free.dev/soldiers`
- **Units**: `https://your-backend-url.ngrok-free.dev/units`

---

## 📱 **Share with Anyone**

### **For Your Friend:**
Just send them the 3 ngrok URLs:
- Main Dashboard: `https://def456.ngrok-free.dev`
- Reports UI: `https://ghi789.ngrok-free.dev`
- API Docs: `https://abc123.ngrok-free.dev/docs`

### **No Setup Required:**
- Works from any device
- Works from any network
- Works from anywhere in the world
- No firewall issues
- No network configuration needed

---

## 🔧 **Troubleshooting**

### **"ngrok not found"**
- Make sure ngrok is installed from Microsoft Store
- Try running `ngrok` from Command Prompt

### **"Services not starting"**
- Check that Python and Node.js are installed
- Make sure you're in the correct directories
- Check that ports 8000, 3000, 3001 are not already in use

### **"ngrok URLs not working"**
- Wait a few seconds for services to start
- Check that local services are running on localhost
- Verify ngrok tunnels are active

---

## 🎉 **Success!**

Once all 6 windows are running, your Military Hierarchy System is globally accessible! Share the ngrok URLs with anyone, anywhere in the world! 🌍
