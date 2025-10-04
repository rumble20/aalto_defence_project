# 🚀 ngrok Setup Instructions

## Quick Start Guide

### **Step 1: Configure ngrok (One-time setup)**
Open Command Prompt or PowerShell and run:
```bash
ngrok config add-authtoken 33bQDyBGjGsGrNXeqEVbMkqY5v7_2EAARiJ7eGPMa4stCVZ62
```

### **Step 2: Start Everything**
Run the batch file:
```bash
start_with_ngrok.bat
```

This will:
1. ✅ Start your Backend API (port 8000)
2. ✅ Start your Main Dashboard (port 3000) 
3. ✅ Start your Reports UI (port 3001)
4. ✅ Start 3 ngrok tunnels for each service

### **Step 3: Get Your Public URLs**
Look at the ngrok windows that opened. You'll see URLs like:
- **Backend API**: `https://abc123.ngrok-free.dev`
- **Main Dashboard**: `https://def456.ngrok-free.dev`
- **Reports UI**: `https://ghi789.ngrok-free.dev`

### **Step 4: Share with Anyone!**
Copy these URLs and share them with anyone, anywhere in the world!

---

## 🌍 **Your Global URLs**

Once running, your Military Hierarchy System will be accessible at:

- **Backend API**: `https://[your-ngrok-url].ngrok-free.dev`
- **API Documentation**: `https://[your-ngrok-url].ngrok-free.dev/docs`
- **Main Dashboard**: `https://[your-ngrok-url].ngrok-free.dev`
- **Reports UI**: `https://[your-ngrok-url].ngrok-free.dev`

---

## 📱 **Testing**

### **From Your Computer:**
1. Open the ngrok URLs in your browser
2. Test all services work correctly

### **From Mobile/Other Devices:**
1. Connect to any internet connection
2. Open the ngrok URLs
3. Everything should work perfectly!

### **Share with Friends:**
Just send them the ngrok URLs - no setup needed on their end!

---

## 🔧 **Manual Setup (Alternative)**

If the batch file doesn't work, you can start everything manually:

### **Terminal 1 - Backend API:**
```bash
cd aalto_defence_project
python backend.py
```

### **Terminal 2 - Main Dashboard:**
```bash
cd aalto_defence_project\mil_dashboard
npm run dev
```

### **Terminal 3 - Reports UI:**
```bash
cd aalto_defence_project\ui-for-reports\frontend
npm run dev
```

### **Terminal 4 - ngrok Backend:**
```bash
ngrok http 8000
```

### **Terminal 5 - ngrok Dashboard:**
```bash
ngrok http 3000
```

### **Terminal 6 - ngrok Reports:**
```bash
ngrok http 3001
```

---

## ✅ **Success Indicators**

You'll know it's working when:
- ✅ All 6 terminal windows are open
- ✅ ngrok shows "Forwarding" URLs
- ✅ You can access the URLs in your browser
- ✅ Services load normally via ngrok URLs

---

## 🆘 **Troubleshooting**

### **"ngrok not found"**
- Make sure ngrok is installed from Microsoft Store
- Try running `ngrok` from Command Prompt

### **"Services not starting"**
- Check that Python and Node.js are installed
- Make sure you're in the correct directory

### **"ngrok URLs not working"**
- Wait a few seconds for services to start
- Check that local services are running on localhost:8000, localhost:3000, localhost:3001

---

## 🎉 **You're Ready!**

Once everything is running, your Military Hierarchy System is globally accessible! Share the ngrok URLs with anyone, anywhere in the world! 🌍
