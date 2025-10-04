-- Military Hierarchy Database Schema
-- This file contains the complete database schema for the military communication system
-- Compatible with SQLite, easily adaptable to PostgreSQL

-- =====================================================
-- UNITS TABLE - Hierarchical Military Organization
-- =====================================================
CREATE TABLE IF NOT EXISTS units (
    unit_id TEXT PRIMARY KEY,           -- Unique identifier (e.g., 'BAT_1', 'CO_A', 'PLT_1')
    name TEXT NOT NULL,                 -- Display name (e.g., '1st Infantry Battalion')
    parent_unit_id TEXT,                -- Reference to parent unit (NULL for top-level)
    level TEXT NOT NULL,                -- Unit level: Battalion, Company, Platoon, Squad
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(parent_unit_id) REFERENCES units(unit_id)
);

-- =====================================================
-- SOLDIERS TABLE - Individual Personnel Records
-- =====================================================
CREATE TABLE IF NOT EXISTS soldiers (
    soldier_id TEXT PRIMARY KEY,        -- Unique identifier (e.g., 'ALPHA_01')
    name TEXT NOT NULL,                 -- Full name (e.g., 'Lt. John Smith')
    rank TEXT,                          -- Military rank (e.g., 'Lieutenant')
    unit_id TEXT NOT NULL,              -- Assigned unit reference
    device_id TEXT,                     -- Associated device/radio ID
    status TEXT DEFAULT 'active',       -- Status: active, injured, missing, etc.
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    last_seen TEXT,                     -- Last communication timestamp
    FOREIGN KEY(unit_id) REFERENCES units(unit_id)
);

-- =====================================================
-- RAW INPUTS TABLE - Complete Voice/Text Input History
-- =====================================================
CREATE TABLE IF NOT EXISTS soldier_raw_inputs (
    input_id TEXT PRIMARY KEY,          -- UUID for unique identification
    soldier_id TEXT NOT NULL,           -- Source soldier reference
    timestamp TEXT NOT NULL,            -- ISO format timestamp
    raw_text TEXT NOT NULL,             -- Transcribed voice or typed text
    raw_audio_ref TEXT,                 -- Optional reference to audio file
    input_type TEXT DEFAULT 'voice',    -- voice, text, image, sensor
    confidence REAL DEFAULT 0.0,        -- Transcription confidence (0.0-1.0)
    location_ref TEXT,                  -- Optional location reference
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(soldier_id) REFERENCES soldiers(soldier_id)
);

-- =====================================================
-- REPORTS TABLE - AI-Generated Structured Reports
-- =====================================================
CREATE TABLE IF NOT EXISTS reports (
    report_id TEXT PRIMARY KEY,         -- UUID for unique identification
    soldier_id TEXT NOT NULL,           -- Source soldier reference
    unit_id TEXT NOT NULL,              -- Unit context reference
    timestamp TEXT NOT NULL,            -- Report generation timestamp
    report_type TEXT NOT NULL,          -- CASEVAC, EOINCREP, SITREP, FRAGO, OPORD
    structured_json TEXT NOT NULL,      -- JSON-formatted structured data
    confidence REAL NOT NULL,           -- AI confidence score (0.0-1.0)
    source_input_id TEXT,               -- Reference to original raw input
    status TEXT DEFAULT 'generated',    -- generated, reviewed, approved, rejected
    reviewed_by TEXT,                   -- Reviewing officer
    reviewed_at TEXT,                   -- Review timestamp
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(soldier_id) REFERENCES soldiers(soldier_id),
    FOREIGN KEY(unit_id) REFERENCES units(unit_id),
    FOREIGN KEY(source_input_id) REFERENCES soldier_raw_inputs(input_id)
);

-- =====================================================
-- DEVICE STATUS TABLE - Equipment and Communication Status
-- =====================================================
CREATE TABLE IF NOT EXISTS device_status (
    device_id TEXT PRIMARY KEY,         -- Device identifier
    soldier_id TEXT,                    -- Associated soldier (nullable for standalone devices)
    status TEXT DEFAULT 'active',       -- active, offline, maintenance, lost
    last_heartbeat TEXT,                -- Last MQTT heartbeat
    battery_level INTEGER,              -- Battery percentage (0-100)
    signal_strength INTEGER,            -- Signal strength (0-100)
    location_lat REAL,                  -- GPS latitude
    location_lon REAL,                  -- GPS longitude
    location_accuracy REAL,             -- GPS accuracy in meters
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(soldier_id) REFERENCES soldiers(soldier_id)
);

-- =====================================================
-- COMMUNICATION LOG TABLE - MQTT and Network Activity
-- =====================================================
CREATE TABLE IF NOT EXISTS comm_log (
    log_id TEXT PRIMARY KEY,            -- UUID for log entry
    device_id TEXT,                     -- Source device
    soldier_id TEXT,                    -- Associated soldier
    topic TEXT NOT NULL,                -- MQTT topic (e.g., 'soldiers/inputs')
    message_type TEXT NOT NULL,         -- input, heartbeat, status, error
    message_size INTEGER,               -- Message size in bytes
    timestamp TEXT NOT NULL,            -- Message timestamp
    success BOOLEAN DEFAULT TRUE,       -- Delivery success status
    error_message TEXT,                 -- Error details if failed
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(soldier_id) REFERENCES soldiers(soldier_id)
);

-- =====================================================
-- INDEXES FOR PERFORMANCE OPTIMIZATION
-- =====================================================

-- Units hierarchy queries
CREATE INDEX IF NOT EXISTS idx_units_parent ON units(parent_unit_id);
CREATE INDEX IF NOT EXISTS idx_units_level ON units(level);

-- Soldier lookups
CREATE INDEX IF NOT EXISTS idx_soldiers_unit ON soldiers(unit_id);
CREATE INDEX IF NOT EXISTS idx_soldiers_device ON soldiers(device_id);
CREATE INDEX IF NOT EXISTS idx_soldiers_status ON soldiers(status);

-- Raw inputs queries
CREATE INDEX IF NOT EXISTS idx_raw_inputs_soldier ON soldier_raw_inputs(soldier_id);
CREATE INDEX IF NOT EXISTS idx_raw_inputs_timestamp ON soldier_raw_inputs(timestamp);
CREATE INDEX IF NOT EXISTS idx_raw_inputs_type ON soldier_raw_inputs(input_type);

-- Reports queries
CREATE INDEX IF NOT EXISTS idx_reports_soldier ON reports(soldier_id);
CREATE INDEX IF NOT EXISTS idx_reports_unit ON reports(unit_id);
CREATE INDEX IF NOT EXISTS idx_reports_type ON reports(report_type);
CREATE INDEX IF NOT EXISTS idx_reports_timestamp ON reports(timestamp);
CREATE INDEX IF NOT EXISTS idx_reports_status ON reports(status);

-- Device status queries
CREATE INDEX IF NOT EXISTS idx_device_status_soldier ON device_status(soldier_id);
CREATE INDEX IF NOT EXISTS idx_device_status_last_heartbeat ON device_status(last_heartbeat);

-- Communication log queries
CREATE INDEX IF NOT EXISTS idx_comm_log_device ON comm_log(device_id);
CREATE INDEX IF NOT EXISTS idx_comm_log_soldier ON comm_log(soldier_id);
CREATE INDEX IF NOT EXISTS idx_comm_log_timestamp ON comm_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_comm_log_topic ON comm_log(topic);

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- Complete soldier information with unit details
CREATE VIEW IF NOT EXISTS soldier_details AS
SELECT 
    s.soldier_id,
    s.name,
    s.rank,
    s.unit_id,
    s.device_id,
    s.status,
    s.last_seen,
    u.name as unit_name,
    u.level as unit_level,
    u.parent_unit_id,
    (SELECT name FROM units WHERE unit_id = u.parent_unit_id) as parent_unit_name
FROM soldiers s
JOIN units u ON s.unit_id = u.unit_id;

-- Recent activity summary
CREATE VIEW IF NOT EXISTS recent_activity AS
SELECT 
    s.soldier_id,
    s.name,
    s.rank,
    u.name as unit_name,
    COUNT(r.input_id) as recent_inputs,
    MAX(r.timestamp) as last_input,
    COUNT(rp.report_id) as recent_reports,
    MAX(rp.timestamp) as last_report
FROM soldiers s
JOIN units u ON s.unit_id = u.unit_id
LEFT JOIN soldier_raw_inputs r ON s.soldier_id = r.soldier_id 
    AND r.timestamp > datetime('now', '-24 hours')
LEFT JOIN reports rp ON s.soldier_id = rp.soldier_id 
    AND rp.timestamp > datetime('now', '-24 hours')
GROUP BY s.soldier_id, s.name, s.rank, u.name;

-- Unit hierarchy tree
CREATE VIEW IF NOT EXISTS unit_hierarchy AS
WITH RECURSIVE unit_tree AS (
    -- Base case: top-level units (no parent)
    SELECT unit_id, name, parent_unit_id, level, 0 as depth
    FROM units 
    WHERE parent_unit_id IS NULL
    
    UNION ALL
    
    -- Recursive case: child units
    SELECT u.unit_id, u.name, u.parent_unit_id, u.level, ut.depth + 1
    FROM units u
    JOIN unit_tree ut ON u.parent_unit_id = ut.unit_id
)
SELECT unit_id, name, parent_unit_id, level, depth
FROM unit_tree
ORDER BY depth, name;

-- =====================================================
-- SAMPLE DATA INSERTION (OPTIONAL)
-- =====================================================

-- Uncomment the following section to include sample data
-- This creates a realistic military hierarchy for testing

/*
-- Sample Units
INSERT OR IGNORE INTO units VALUES 
('BAT_1', '1st Infantry Battalion', NULL, 'Battalion'),
('CO_A', 'Alpha Company', 'BAT_1', 'Company'),
('CO_B', 'Bravo Company', 'BAT_1', 'Company'),
('PLT_1', '1st Platoon', 'CO_A', 'Platoon'),
('PLT_2', '2nd Platoon', 'CO_A', 'Platoon'),
('PLT_3', '3rd Platoon', 'CO_B', 'Platoon'),
('SQD_1', '1st Squad', 'PLT_1', 'Squad'),
('SQD_2', '2nd Squad', 'PLT_1', 'Squad'),
('SQD_3', '3rd Squad', 'PLT_2', 'Squad');

-- Sample Soldiers
INSERT OR IGNORE INTO soldiers VALUES 
('ALPHA_01', 'Lt. John Smith', 'Lieutenant', 'PLT_1', 'DEVICE_001', 'active'),
('ALPHA_02', 'Sgt. Mike Johnson', 'Sergeant', 'SQD_1', 'DEVICE_002', 'active'),
('ALPHA_03', 'Pvt. David Wilson', 'Private', 'SQD_1', 'DEVICE_003', 'active'),
('ALPHA_04', 'Cpl. Sarah Brown', 'Corporal', 'SQD_2', 'DEVICE_004', 'active'),
('BRAVO_01', 'Capt. Tom Davis', 'Captain', 'CO_B', 'DEVICE_005', 'active');
*/

-- =====================================================
-- SCHEMA VALIDATION QUERIES
-- =====================================================

-- These queries can be used to validate the schema integrity

-- Check for orphaned soldiers (soldiers without valid units)
-- SELECT * FROM soldiers WHERE unit_id NOT IN (SELECT unit_id FROM units);

-- Check for circular unit references
-- WITH RECURSIVE unit_check AS (
--     SELECT unit_id, parent_unit_id, 1 as depth FROM units WHERE parent_unit_id IS NOT NULL
--     UNION ALL
--     SELECT u.unit_id, u.parent_unit_id, uc.depth + 1 
--     FROM units u JOIN unit_check uc ON u.unit_id = uc.parent_unit_id
--     WHERE uc.depth < 10  -- Prevent infinite recursion
-- )
-- SELECT * FROM unit_check WHERE depth > 5;  -- Flag suspicious depths

-- Check for reports without valid source inputs
-- SELECT * FROM reports WHERE source_input_id IS NOT NULL 
-- AND source_input_id NOT IN (SELECT input_id FROM soldier_raw_inputs);
