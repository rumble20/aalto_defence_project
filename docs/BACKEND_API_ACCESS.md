# 🚀 Backend API - Public Access Guide

## ✅ **Backend API is Now Publicly Accessible!**

Your backend API is now exposed to the internet so people can POST data directly to it.

---

## 🌍 **Public URLs:**

### **Backend API (for POST requests):**
```
https://your-backend-url.ngrok-free.dev
```

### **Dashboard (for UI):**
```
https://your-dashboard-url.ngrok-free.dev
```

**Note:** Check the ngrok windows for the actual URLs.

---

## 📡 **API Endpoints:**

### **Base URL:**
```
https://your-backend-url.ngrok-free.dev
```

### **Available Endpoints:**

#### **1. System Status:**
```
GET https://your-backend-url.ngrok-free.dev/
```

#### **2. Get All Soldiers:**
```
GET https://your-backend-url.ngrok-free.dev/soldiers
```

#### **3. Get All Units:**
```
GET https://your-backend-url.ngrok-free.dev/units
```

#### **4. Get Hierarchy:**
```
GET https://your-backend-url.ngrok-free.dev/hierarchy
```

#### **5. Create Soldier:**
```
POST https://your-backend-url.ngrok-free.dev/soldiers
Content-Type: application/json

{
  "soldier_id": "SOL001",
  "name": "John Doe",
  "rank": "Sergeant",
  "unit_id": "UNIT001",
  "status": "active"
}
```

#### **6. Send Raw Input:**
```
POST https://your-backend-url.ngrok-free.dev/soldiers/{soldier_id}/raw_inputs
Content-Type: application/json

{
  "raw_text": "Enemy spotted at coordinates 38.8977, 77.0365",
  "input_type": "voice",
  "confidence": 0.95,
  "location_ref": "38.8977,77.0365"
}
```

#### **7. Create Report:**
```
POST https://your-backend-url.ngrok-free.dev/reports
Content-Type: application/json

{
  "report_type": "SITREP",
  "content": "Perimeter secure, all checkpoints manned",
  "soldier_id": "SOL001",
  "priority": "ROUTINE"
}
```

#### **8. Update Soldier Status:**
```
PUT https://your-backend-url.ngrok-free.dev/soldiers/{soldier_id}/status
Content-Type: application/json

{
  "status": "active",
  "last_seen": "2024-10-04T14:30:00Z"
}
```

---

## 🧪 **Testing the API:**

### **Using cURL:**
```bash
# Test if API is accessible
curl https://your-backend-url.ngrok-free.dev/

# Get all soldiers
curl https://your-backend-url.ngrok-free.dev/soldiers

# Create a soldier
curl -X POST https://your-backend-url.ngrok-free.dev/soldiers \
  -H "Content-Type: application/json" \
  -d '{"soldier_id":"SOL001","name":"John Doe","rank":"Sergeant","unit_id":"UNIT001","status":"active"}'
```

### **Using Python:**
```python
import requests

# Base URL
base_url = "https://your-backend-url.ngrok-free.dev"

# Test connection
response = requests.get(f"{base_url}/")
print(response.json())

# Get soldiers
soldiers = requests.get(f"{base_url}/soldiers")
print(soldiers.json())

# Create soldier
new_soldier = {
    "soldier_id": "SOL001",
    "name": "John Doe",
    "rank": "Sergeant",
    "unit_id": "UNIT001",
    "status": "active"
}
response = requests.post(f"{base_url}/soldiers", json=new_soldier)
print(response.json())
```

### **Using JavaScript:**
```javascript
// Base URL
const baseUrl = "https://your-backend-url.ngrok-free.dev";

// Test connection
fetch(`${baseUrl}/`)
  .then(response => response.json())
  .then(data => console.log(data));

// Get soldiers
fetch(`${baseUrl}/soldiers`)
  .then(response => response.json())
  .then(soldiers => console.log(soldiers));

// Create soldier
const newSoldier = {
  soldier_id: "SOL001",
  name: "John Doe",
  rank: "Sergeant",
  unit_id: "UNIT001",
  status: "active"
};

fetch(`${baseUrl}/soldiers`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(newSoldier)
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## 📚 **API Documentation:**

### **Interactive Docs:**
```
https://your-backend-url.ngrok-free.dev/docs
```

### **OpenAPI Schema:**
```
https://your-backend-url.ngrok-free.dev/openapi.json
```

---

## 🎯 **For Your Friends:**

### **Share These URLs:**
1. **Backend API URL** - For POST requests and data access
2. **Dashboard URL** - For the web interface
3. **API Docs URL** - For interactive testing

### **What They Can Do:**
- ✅ **POST data** to create soldiers, reports, inputs
- ✅ **GET data** to retrieve soldiers, units, hierarchy
- ✅ **PUT data** to update soldier status
- ✅ **Use the web interface** for visualization
- ✅ **Test with API docs** for interactive exploration

---

## 🚀 **Quick Start for Friends:**

1. **Get the Backend API URL** from your ngrok window
2. **Test connection:** `GET https://your-url.ngrok-free.dev/`
3. **View API docs:** `https://your-url.ngrok-free.dev/docs`
4. **Start POSTing data** to create soldiers and reports!

**Your Backend API is now globally accessible for POST requests!** 🌍
