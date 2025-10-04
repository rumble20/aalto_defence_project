# 🔧 ngrok Error ERR_NGROK_6030 - FIXED!

## ❌ **The Problem:**
```
ERR_NGROK_6030
The url 'https://skyla-nonpercussive-odette.ngrok-free.dev' has multiple endpoints, 
but they do not all have pooling enabled.
```

## 🎯 **Root Cause:**
This error occurs when you try to run multiple ngrok tunnels on the same URL, but they don't all have pooling enabled. ngrok gets confused about which service to route traffic to.

## ✅ **Solutions:**

### **Option 1: Separate URLs (Recommended)**
Use different ngrok tunnels for each service:

```bash
# Run this script for separate URLs
scripts\fixed_ngrok_setup.bat
```

**Result:**
- **Backend API**: `https://abc123.ngrok-free.dev` (Port 8000)
- **Unified Dashboard**: `https://def456.ngrok-free.dev` (Port 3000)

### **Option 2: Single URL (Simplest)**
Only expose the unified dashboard (since it includes everything):

```bash
# Run this script for single URL
scripts\single_url_setup.bat
```

**Result:**
- **Unified Dashboard**: `https://abc123.ngrok-free.dev` (Port 3000)
- **Backend API**: Internal only (accessible by dashboard)

---

## 🚀 **Recommended Approach:**

### **Use Single URL Setup:**
Since your unified dashboard includes both hierarchy and reports functionality, you only need to expose one URL:

1. **Run:** `scripts\single_url_setup.bat`
2. **Share:** The single ngrok URL with your friend
3. **Access:** Everything through one URL

### **Benefits:**
- ✅ **No ngrok conflicts**
- ✅ **Simpler sharing** (one URL)
- ✅ **All functionality** available
- ✅ **Easier to manage**

---

## 🔧 **Manual Fix (If Needed):**

### **Stop All ngrok Tunnels:**
1. Close all ngrok command windows
2. Wait 30 seconds
3. Restart with single tunnel

### **Start Single Tunnel:**
```bash
cd ngrok
ngrok.exe http 3000
```

### **Share the URL:**
- Copy the `https://xxxxx.ngrok-free.dev` URL
- Share with your friend
- Everything works through this single URL

---

## 🎯 **Why This Happens:**

### **Multiple Tunnels Conflict:**
- **Problem:** Multiple ngrok tunnels trying to use same URL
- **Solution:** Use separate tunnels or single tunnel

### **Pooling Not Enabled:**
- **Problem:** ngrok free tier doesn't support pooling
- **Solution:** Use separate URLs or single URL

---

## 🚀 **Quick Fix Commands:**

### **Option 1 - Separate URLs:**
```bash
scripts\fixed_ngrok_setup.bat
```

### **Option 2 - Single URL (Recommended):**
```bash
scripts\single_url_setup.bat
```

### **Check Status:**
```bash
tools\simple_status.py
```

---

## 🎉 **Success!**

**After running the fix:**
- ✅ **No more ngrok errors**
- ✅ **Working public URLs**
- ✅ **All functionality available**
- ✅ **Easy to share with friends**

**Your Military Hierarchy System is now accessible globally without ngrok conflicts!** 🌍
