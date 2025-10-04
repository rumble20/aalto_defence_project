# 🎖️ Military Hierarchy Management System

A comprehensive military hierarchy management system with real-time communication, reporting, and global access capabilities.

## 📁 Project Structure

```
aalto_defence_project/
├── 📁 docs/                          # Documentation
│   ├── API_DOCUMENTATION.md         # Complete API reference
│   ├── NETWORK_SETUP.md             # Network configuration guide
│   ├── NGROK_SETUP_INSTRUCTIONS.md  # ngrok setup guide
│   ├── FRIEND_ACCESS_GUIDE.md       # External access guide
│   └── ...                          # Other documentation
│
├── 📁 tests/                         # Test files
│   ├── test_api.py                  # API endpoint tests
│   ├── test_network_access.py       # Network connectivity tests
│   ├── test_tunnel_access.py        # Tunnel connectivity tests
│   └── ...                          # Other test files
│
├── 📁 scripts/                       # Automation scripts
│   ├── start_all.bat                # Start all services
│   ├── fixed_setup.bat              # Fixed setup script
│   ├── setup_ngrok.bat              # ngrok setup
│   └── ...                          # Other scripts
│
├── 📁 tools/                         # Utility tools
│   ├── check_status.py              # System status checker
│   ├── validate_schema.py            # Database validation
│   ├── soldier_simulator.py         # Soldier data simulator
│   └── ...                          # Other utilities
│
├── 📁 ngrok/                         # ngrok configuration
│   ├── ngrok.exe                     # ngrok executable
│   ├── ngrok.yml                     # ngrok configuration
│   └── ngrok.zip                     # ngrok archive
│
├── 📁 mil_dashboard/                 # Main Dashboard (Next.js)
│   └── ...                          # Dashboard files
│
├── 📁 ui-for-reports/               # Reports UI (Next.js)
│   └── frontend/                    # Reports frontend
│
├── 📁 venv/                         # Python virtual environment
│
├── 🐍 backend.py                     # FastAPI backend server
├── 🗄️ database_schema.sql            # Database schema
├── 🗄️ database_setup.py              # Database initialization
├── 🗄️ military_hierarchy.db          # SQLite database
└── 📄 README.md                      # This file
```

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

## 📚 Documentation

### **API Documentation**
- **File:** `docs/API_DOCUMENTATION.md`
- **Live Docs:** `http://localhost:8000/docs`

### **Network Setup**
- **File:** `docs/NETWORK_SETUP.md`
- **Covers:** Local network access, firewall configuration

### **ngrok Setup**
- **File:** `docs/NGROK_SETUP_INSTRUCTIONS.md`
- **Covers:** Global access via ngrok tunnels

## 🧪 Testing

### **Run Tests**
```bash
# API tests
tests\test_api.py

# Network tests
tests\test_network_access.py

# Tunnel tests
tests\test_tunnel_access.py
```

### **System Status**
```bash
# Check all services
tools\check_status.py

# Validate database
tools\validate_schema.py
```

## 🔧 Scripts

### **Start Services**
```bash
# Start everything
scripts\start_all.bat

# Fixed setup (recommended)
scripts\fixed_setup.bat
```

### **ngrok Setup**
```bash
# Setup ngrok
scripts\setup_ngrok.bat

# Start with ngrok
scripts\start_with_ngrok.bat
```

## 🛠️ Tools

### **Status Monitoring**
- **`tools/check_status.py`** - System health check
- **`tools/simple_status.py`** - Quick status check

### **Data Management**
- **`tools/validate_schema.py`** - Database validation
- **`tools/soldier_simulator.py`** - Test data generation

### **API Testing**
- **`tools/api_data_examples.py`** - API usage examples
- **`tools/api_test_form.html`** - Web-based API testing

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

## 🚨 Troubleshooting

### **Services Not Starting**
```bash
# Check status
tools\check_status.py

# Restart services
scripts\fixed_setup.bat
```

### **Network Issues**
```bash
# Test network access
tests\test_network_access.py

# Troubleshoot connectivity
tests\troubleshoot_network_access.py
```

### **ngrok Issues**
```bash
# Test tunnel access
tests\test_tunnel_access.py

# Check ngrok configuration
docs\NGROK_SETUP_INSTRUCTIONS.md
```

## 📝 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

## 📞 Support

For issues and questions:
1. **Check the documentation** in `docs/`
2. **Run diagnostic tools** in `tools/`
3. **Test connectivity** with `tests/`
4. **Review setup guides** in `docs/`

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

**Your Military Hierarchy System is now organized and ready for global deployment!** 🌍
