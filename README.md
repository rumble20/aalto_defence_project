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

Soldier Device (Raspberry Pi) → Speech_to_text -> convert into formatted JSON through AI interpreting -> MQTT → FastAPI Backend ->
→ SQLite Database -> Backend Services & AI Processing -> Next.js Frontend

## Backend Workflow

1. **Speech-to-Text Input**  
   - Soldier devices capture voice and convert it to raw JSON text.

2. **JSON text into JSON structured table**
   - locally run LLM converts it into more easy-to-transmit data
   - sent to MQTT server

3. **Data Ingestion & Validation**  
   - FastAPI backend receives inputs from MQTT broker.
   - Pydantic schemas validate incoming JSON.

4. **AI Processing**  
   - Local LLM transforms messy JSON into structured report packages.
   - Each package tagged with metadata (time, soldier ID, unit hierarchy).

5. **Database Composition**  
   - All raw and structured data stored in SQLite.  
   - Tables link inputs, reports, soldiers, and unit hierarchy.

6. **API Layer**  
   - REST endpoints expose soldier data, hierarchy, and reports.  
   - Enables secure queries from frontend and external tools.

7. **Report Generation**  
   - AI-powered backend service produces CASEVAC, SITREP, or EOINCREP.  
   - Reports are stored and made queryable in real time.

8. **Data Delivery to Frontend**  
   - Backend streams updates (via WebSocket or polling).  
   - Frontend dashboard visualizes and organizes all incoming information.

## Quick Start

### 1. Setup Environment

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

# Frontend will be available at: 

http://localhost:3000

## Database Schema
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

### Development Notes

VOSK for speech-to-text recognition (tested on Raspberry 4)

Local LLM for lightweight, offline AI processing of JSON data

Built with FastAPI for high-performance backend

SQLite for rapid prototyping (easily upgradeable to PostgreSQL)

Next.js with TypeScript for modern frontend

Tailwind CSS for responsive design

Pydantic for data validation

MQTT for real-time communication

