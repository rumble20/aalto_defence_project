# Military Hierarchy Database System

A hackathon-ready system for military communication. Starts with speech-to-text recognition, raw json text gets converted through a local run LLM into structured json text packages for easy delivering of information at low power. Packages which have arrived to base station get composed into a database, from which both backend services and a frontend system provide real-time monitoring, analytics, and AI-powered report generation.

## Features

- **Hierarchical Military Database**: Units (Battalion → Company → Platoon → Squad) with soldier management
- **Real-time MQTT Communication**: Soldier devices send voice inputs via MQTT
- **Backend AI Processing**: Local LLM converts raw JSON into structured military reports (CASEVAC, EOINCREP, SITREP)
- **AI Report Generation**: Automated military-grade reports with confidence scores
- **Modern Web Dashboard**: Next.js frontend with real-time data visualization
- **Complete History Tracking**: All raw inputs and processed reports stored permanently

## System Architecture

Soldier Device (Raspberry Pi) → MQTT → FastAPI Backend → SQLite Database
↓
Backend Services & AI Processing
↓
Next.js Frontend

markdown
Copia codice

## Backend Workflow

1. **Speech-to-Text Input**  
   - Soldier devices capture voice and convert it to raw JSON text.
   - Data sent via MQTT to the backend.

2. **Data Ingestion & Validation**  
   - FastAPI backend receives inputs from MQTT broker.
   - Pydantic schemas validate incoming JSON.

3. **AI Processing**  
   - Local LLM transforms messy JSON into structured report packages.
   - Each package tagged with metadata (time, soldier ID, unit hierarchy).

4. **Database Composition**  
   - All raw and structured data stored in SQLite.  
   - Tables link inputs, reports, soldiers, and unit hierarchy.

5. **API Layer**  
   - REST endpoints expose soldier data, hierarchy, and reports.  
   - Enables secure queries from frontend and external tools.

6. **Report Generation**  
   - AI-powered backend service produces CASEVAC, SITREP, or EOINCREP.  
   - Reports are stored and made queryable in real time.

7. **Data Delivery to Frontend**  
   - Backend streams updates (via WebSocket or polling).  
   - Frontend dashboard visualizes and organizes all incoming information.

## Quick Start

### 1. Setup Environment

bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies (already done)
pip install fastapi uvicorn pydantic paho-mqtt sqlalchemy

### 2. Initialize Database
python database_setup.py

### 3. Start Backend Server
python backend.py

# or use the startup script
python start_system.py

# Backend will be available at:

API: http://localhost:8000

Documentation: http://localhost:8000/docs

### 4. Start Frontend Dashboard
cd mil_dashboard
npm run dev

# Frontend will be available at: http://localhost:3000

### 5. (Optional) Start MQTT Broker
For full functionality, install and start Mosquitto:

Windows:

Download from https://mosquitto.org/download/

Install and start the service

Linux:

sudo apt install mosquitto mosquitto-clients
mosquitto -v

### 6. Simulate Soldier Devices
python soldier_simulator.py

# Database Schema
# Units Table
Hierarchical military units (Battalion → Company → Platoon → Squad)

Supports recursive subunit queries

# Soldiers Table
Individual soldier metadata (name, rank, unit assignment, device ID)

# Raw Inputs Table
Complete history of all voice/text inputs from soldiers

Timestamped and linked to soldier devices

# Reports Table
AI-generated structured reports

JSON format with confidence scores

Linked to both soldiers and units

# API Endpoints
GET /soldiers - List all soldiers

GET /soldiers/{id}/raw_inputs - Get soldier's voice inputs

GET /soldiers/{id}/reports - Get soldier's structured reports

GET /reports - Get all reports

GET /hierarchy - Get complete military hierarchy

POST /soldiers/{id}/reports - Create new report

# MQTT Topics
soldiers/inputs - Voice inputs from soldier devices

soldiers/heartbeat - Device status updates

# Sample Data
The system comes with sample military hierarchy data:

1st Infantry Battalion

Alpha Company

1st Platoon (Lt. John Smith)

1st Squad (Sgt. Mike Johnson, Pvt. David Wilson)

2nd Squad (Cpl. Sarah Brown)

2nd Platoon (Sgt. Lisa Garcia)

Bravo Company (Capt. Tom Davis)

## Frontend Features
Real-time Dashboard: Live monitoring of soldier communications

Soldier Selection: Browse individual soldiers and their data

Raw Input Display: View original voice transcriptions

Structured Reports: AI-generated military reports with confidence scores

Responsive Design: Works on desktop and mobile devices

## Development Notes
Built with FastAPI for high-performance backend

SQLite for rapid prototyping (easily upgradeable to PostgreSQL)

Next.js with TypeScript for modern frontend

Tailwind CSS for responsive design

Pydantic for data validation

MQTT for real-time communication

Local LLM for lightweight, offline AI processing

## Hackathon Ready
This system is designed for rapid deployment and demonstration:

Minimal setup time

Clear backend-to-frontend data flow

Real-time updates

Professional military-themed UI

Complete documentation

Sample data for immediate testing
