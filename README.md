# 🎖️ A.U.R.A : Audio Understanding and Reconnassaince Automation

A comprehensive military report management system with real-time communication, text-to-speech interpretation, LLM data encoding, web visualization of database, AI automatic reporting summary and global access capabilities.

## 📁 Project Structure

```
aalto_defence_project/
├── 📁 docs/
├── 📁 tests/                         # Test files
├── 📁 scripts/                       # Automation scripts
├── 📁 tools/                         # Utility tools
├── 📁 ngrok/                         # ngrok configuration
├── 📁 mil_dashboard/                 # Main Dashboard (Next.js)
├── 📁 ui-for-reports/               # Reports UI (Next.js)
├── 📁 venv/                         # Python virtual environment
├── 🐍 backend.py                     # FastAPI backend server
├── 🗄️ database_schema.sql            # Database schema
├── 🗄️ database_setup.py              # Database initialization
├── 🗄️ military_hierarchy.db          # SQLite database
```
For the web visualization and AI summary

```
aalto_defence_project/
├── 📁 soldier_assistant/
```
For the speech-to-text recognition, developed to be tested on a Raspberry Pi

```
aalto_defence_project/
├── 📁 Decoding_and_storing_LLM/
├── 📁 processed_data/
```
For the LLM text encoding in json format to be sent over low bandwidth capabilities

## 🚀 Quick Start

### 1. **Start the System**
```bash
# Run the organized setup script
scripts\fixed_setup.bat
```

### 2. **Check Status**
```bash
# Check if all services are running
tools\check_status.py
```

### 3. **Access Your System**
- **Local URLs:**
  - Backend API: `http://localhost:8000`
  - Main Dashboard: `http://localhost:3000`
  - Reports UI: `http://localhost:3001`

- **Global URLs:** Check ngrok windows for public URLs

## 🌍 Global Access

### **For External Users:**
1. **Check ngrok windows** for public URLs
2. **Share URLs** with team members
3. **Access from anywhere** in the world

### **Example URLs:**
- Backend API: `https://abc123.ngrok-free.dev`
- Main Dashboard: `https://def456.ngrok-free.dev`
- Reports UI: `https://ghi789.ngrok-free.dev`

## 🛠️ Development

### **Backend API (FastAPI)**
- **File:** `backend.py`
- **Port:** 8000
- **Features:** REST API, MQTT integration, real-time data

### **Main Dashboard (Next.js)**
- **Directory:** `mil_dashboard/`
- **Port:** 3000
- **Features:** Military hierarchy visualization

### **Reports UI (Next.js)**
- **Directory:** `ui-for-reports/frontend/`
- **Port:** 3001
- **Features:** Report generation and management

## 📊 Database

### **Schema**
- **File:** `database_schema.sql`
- **Database:** `military_hierarchy.db` (SQLite)

### **Setup**
```bash
# Initialize database
python database_setup.py
```

## 🌐 Network Configuration

### **Local Access**
- **Backend API:** `http://localhost:8000`
- **Main Dashboard:** `http://localhost:3000`
- **Reports UI:** `http://localhost:3001`

### **Global Access**
- **ngrok tunnels** provide global URLs
- **Check ngrok windows** for public URLs
- **Share URLs** with team members

📝 License

This project is licensed, see the `LICENSE` file for details.

---

## 🎯 **Quick Commands**

```bash
# Start everything
scripts\fixed_setup.bat

# Check status
tools\check_status.py

# Test API
tests\test_api.py

# View documentation
docs\API_DOCUMENTATION.md
```
