# Military Hierarchy Database System

A hackathon-ready system for military communication monitoring with AI-powered report generation.

## Features

- **Hierarchical Military Database**: Units (Battalion → Company → Platoon → Squad) with soldier management
- **Real-time MQTT Communication**: Soldier devices send voice inputs via MQTT
- **AI Report Generation**: Converts raw voice inputs to structured military reports (CASEVAC, EOINCREP, SITREP)
- **Modern Web Dashboard**: Next.js frontend with real-time data visualization
- **Complete History Tracking**: All raw inputs and processed reports stored permanently

## System Architecture

```
Soldier Device (Raspberry Pi) → MQTT → FastAPI Backend → SQLite Database
                                                    ↓
                                              Next.js Frontend
```

## Quick Start

### 1. Setup Environment

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies (already done)
pip install fastapi uvicorn pydantic paho-mqtt sqlalchemy
```

### 2. Initialize Database

```bash
python database_setup.py
```

### 3. Start Backend Server

```bash
python backend.py
# or use the startup script
python start_system.py
```

Backend will be available at:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs

### 4. Start Frontend Dashboard

```bash
cd mil_dashboard
npm run dev
```

Frontend will be available at: http://localhost:3000

### 5. (Optional) Start MQTT Broker

For full functionality, install and start Mosquitto:

**Windows:**
- Download from https://mosquitto.org/download/
- Install and start the service

**Linux:**
```bash
sudo apt install mosquitto mosquitto-clients
mosquitto -v
```

### 6. Simulate Soldier Devices

```bash
python soldier_simulator.py
```

## Database Schema

### Units Table
- Hierarchical military units (Battalion → Company → Platoon → Squad)
- Supports recursive subunit queries

### Soldiers Table
- Individual soldier metadata (name, rank, unit assignment, device ID)

### Raw Inputs Table
- Complete history of all voice/text inputs from soldiers
- Timestamped and linked to soldier devices

### Reports Table
- AI-generated structured reports
- JSON format with confidence scores
- Linked to both soldiers and units

## API Endpoints

- `GET /soldiers` - List all soldiers
- `GET /soldiers/{id}/raw_inputs` - Get soldier's voice inputs
- `GET /soldiers/{id}/reports` - Get soldier's structured reports
- `GET /reports` - Get all reports
- `GET /hierarchy` - Get complete military hierarchy
- `POST /soldiers/{id}/reports` - Create new report

## MQTT Topics

- `soldiers/inputs` - Voice inputs from soldier devices
- `soldiers/heartbeat` - Device status updates

## Sample Data

The system comes with sample military hierarchy data:
- 1st Infantry Battalion
  - Alpha Company
    - 1st Platoon (Lt. John Smith)
      - 1st Squad (Sgt. Mike Johnson, Pvt. David Wilson)
      - 2nd Squad (Cpl. Sarah Brown)
    - 2nd Platoon (Sgt. Lisa Garcia)
  - Bravo Company (Capt. Tom Davis)

## Frontend Features

- **Real-time Dashboard**: Live monitoring of soldier communications
- **Soldier Selection**: Browse individual soldiers and their data
- **Raw Input Display**: View original voice transcriptions
- **Structured Reports**: AI-generated military reports with confidence scores
- **Responsive Design**: Works on desktop and mobile devices

## Development Notes

- Built with FastAPI for high-performance backend
- SQLite for rapid prototyping (easily upgradeable to PostgreSQL)
- Next.js with TypeScript for modern frontend
- Tailwind CSS for responsive design
- Pydantic for data validation
- MQTT for real-time communication

## Hackathon Ready

This system is designed for rapid deployment and demonstration:
- Minimal setup time
- Clear data flow visualization
- Real-time updates
- Professional military-themed UI
- Complete documentation
- Sample data for immediate testing

## Next Steps for Production

1. **AI Integration**: Add LangChain + LLM for report generation
2. **Security**: Implement authentication and encryption
3. **Scalability**: Migrate to PostgreSQL and Redis
4. **Mobile App**: Native mobile app for soldier devices
5. **Advanced Analytics**: Command center with maps and analytics