#!/usr/bin/env python3
"""
PostgreSQL Database Initialization Script for Render Deployment
Converts SQLite schema to PostgreSQL and initializes the database.
"""

import os
import sys
import psycopg2
from psycopg2 import sql
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# PostgreSQL schema - adapted from SQLite schema
POSTGRES_SCHEMA = """
-- Military Hierarchy Database Schema (PostgreSQL)

-- UNITS TABLE - Hierarchical Military Organization
CREATE TABLE IF NOT EXISTS units (
    unit_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    parent_unit_id TEXT,
    level TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(parent_unit_id) REFERENCES units(unit_id)
);

-- SOLDIERS TABLE - Individual Personnel Records
CREATE TABLE IF NOT EXISTS soldiers (
    soldier_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    rank TEXT,
    unit_id TEXT NOT NULL,
    device_id TEXT,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP,
    FOREIGN KEY(unit_id) REFERENCES units(unit_id)
);

-- RAW INPUTS TABLE - Complete Voice/Text Input History
CREATE TABLE IF NOT EXISTS soldier_raw_inputs (
    input_id TEXT PRIMARY KEY,
    soldier_id TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    raw_text TEXT NOT NULL,
    raw_audio_ref TEXT,
    input_type TEXT DEFAULT 'voice',
    confidence REAL DEFAULT 0.0,
    location_ref TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(soldier_id) REFERENCES soldiers(soldier_id)
);

-- REPORTS TABLE - AI-Generated Structured Reports
CREATE TABLE IF NOT EXISTS reports (
    report_id TEXT PRIMARY KEY,
    soldier_id TEXT NOT NULL,
    unit_id TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    report_type TEXT NOT NULL,
    structured_json TEXT NOT NULL,
    confidence REAL NOT NULL,
    source_input_id TEXT,
    status TEXT DEFAULT 'generated',
    reviewed_by TEXT,
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(soldier_id) REFERENCES soldiers(soldier_id),
    FOREIGN KEY(unit_id) REFERENCES units(unit_id),
    FOREIGN KEY(source_input_id) REFERENCES soldier_raw_inputs(input_id)
);

-- DEVICE STATUS TABLE
CREATE TABLE IF NOT EXISTS device_status (
    device_id TEXT PRIMARY KEY,
    soldier_id TEXT,
    status TEXT DEFAULT 'active',
    last_heartbeat TIMESTAMP,
    battery_level INTEGER,
    signal_strength INTEGER,
    location_lat REAL,
    location_lon REAL,
    location_accuracy REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(soldier_id) REFERENCES soldiers(soldier_id)
);

-- COMMUNICATION LOG TABLE
CREATE TABLE IF NOT EXISTS comm_log (
    log_id TEXT PRIMARY KEY,
    device_id TEXT,
    soldier_id TEXT,
    topic TEXT NOT NULL,
    message_type TEXT NOT NULL,
    message_size INTEGER,
    timestamp TIMESTAMP NOT NULL,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(soldier_id) REFERENCES soldiers(soldier_id)
);

-- FRAGOS TABLE (Fragmentary Orders)
CREATE TABLE IF NOT EXISTS fragos (
    frago_id TEXT PRIMARY KEY,
    unit_id TEXT NOT NULL,
    task TEXT NOT NULL,
    assigned_by TEXT NOT NULL,
    assigned_at TIMESTAMP NOT NULL,
    status TEXT DEFAULT 'pending',
    priority TEXT DEFAULT 'medium',
    deadline TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(unit_id) REFERENCES units(unit_id)
);

-- SUGGESTIONS TABLE (AI-Generated Suggestions)
CREATE TABLE IF NOT EXISTS suggestions (
    suggestion_id TEXT PRIMARY KEY,
    report_id TEXT NOT NULL,
    unit_id TEXT,
    suggestion_type TEXT NOT NULL,
    suggestion_text TEXT NOT NULL,
    priority TEXT DEFAULT 'medium',
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP,
    reviewed_by TEXT,
    FOREIGN KEY(report_id) REFERENCES reports(report_id),
    FOREIGN KEY(unit_id) REFERENCES units(unit_id)
);

-- INDEXES FOR PERFORMANCE
CREATE INDEX IF NOT EXISTS idx_units_parent ON units(parent_unit_id);
CREATE INDEX IF NOT EXISTS idx_units_level ON units(level);
CREATE INDEX IF NOT EXISTS idx_soldiers_unit ON soldiers(unit_id);
CREATE INDEX IF NOT EXISTS idx_soldiers_device ON soldiers(device_id);
CREATE INDEX IF NOT EXISTS idx_soldiers_status ON soldiers(status);
CREATE INDEX IF NOT EXISTS idx_raw_inputs_soldier ON soldier_raw_inputs(soldier_id);
CREATE INDEX IF NOT EXISTS idx_raw_inputs_timestamp ON soldier_raw_inputs(timestamp);
CREATE INDEX IF NOT EXISTS idx_reports_soldier ON reports(soldier_id);
CREATE INDEX IF NOT EXISTS idx_reports_unit ON reports(unit_id);
CREATE INDEX IF NOT EXISTS idx_reports_type ON reports(report_type);
CREATE INDEX IF NOT EXISTS idx_reports_timestamp ON reports(timestamp);
CREATE INDEX IF NOT EXISTS idx_device_status_soldier ON device_status(soldier_id);
CREATE INDEX IF NOT EXISTS idx_comm_log_timestamp ON comm_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_fragos_unit ON fragos(unit_id);
CREATE INDEX IF NOT EXISTS idx_fragos_status ON fragos(status);
CREATE INDEX IF NOT EXISTS idx_suggestions_report ON suggestions(report_id);
CREATE INDEX IF NOT EXISTS idx_suggestions_unit ON suggestions(unit_id);
CREATE INDEX IF NOT EXISTS idx_suggestions_status ON suggestions(status);
"""

# Sample data for testing
SAMPLE_DATA = """
-- Sample Units
INSERT INTO units (unit_id, name, parent_unit_id, level) VALUES 
('BAT_1', '1st Infantry Battalion', NULL, 'Battalion'),
('CO_A', 'Alpha Company', 'BAT_1', 'Company'),
('CO_B', 'Bravo Company', 'BAT_1', 'Company'),
('PLT_1', '1st Platoon', 'CO_A', 'Platoon'),
('PLT_2', '2nd Platoon', 'CO_A', 'Platoon'),
('PLT_3', '3rd Platoon', 'CO_B', 'Platoon'),
('SQD_1', '1st Squad', 'PLT_1', 'Squad'),
('SQD_2', '2nd Squad', 'PLT_1', 'Squad'),
('SQD_3', '3rd Squad', 'PLT_2', 'Squad')
ON CONFLICT (unit_id) DO NOTHING;

-- Sample Soldiers
INSERT INTO soldiers (soldier_id, name, rank, unit_id, device_id, status) VALUES 
('ALPHA_01', 'Lt. John Smith', 'Lieutenant', 'PLT_1', 'DEVICE_001', 'active'),
('ALPHA_02', 'Sgt. Mike Johnson', 'Sergeant', 'SQD_1', 'DEVICE_002', 'active'),
('ALPHA_03', 'Pvt. David Wilson', 'Private', 'SQD_1', 'DEVICE_003', 'active'),
('ALPHA_04', 'Cpl. Sarah Brown', 'Corporal', 'SQD_2', 'DEVICE_004', 'active'),
('BRAVO_01', 'Capt. Tom Davis', 'Captain', 'CO_B', 'DEVICE_005', 'active')
ON CONFLICT (soldier_id) DO NOTHING;
"""


def initialize_database():
    """Initialize PostgreSQL database with schema and sample data."""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        logger.error("DATABASE_URL environment variable not set!")
        sys.exit(1)
    
    try:
        logger.info("Connecting to PostgreSQL database...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        logger.info("Creating database schema...")
        cursor.execute(POSTGRES_SCHEMA)
        
        logger.info("Inserting sample data...")
        cursor.execute(SAMPLE_DATA)
        
        conn.commit()
        logger.info("✅ Database initialized successfully!")
        
        # Verify tables were created
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        logger.info(f"Created tables: {[t[0] for t in tables]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    initialize_database()
