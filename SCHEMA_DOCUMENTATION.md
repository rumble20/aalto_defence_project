# Military Hierarchy Database Schema Documentation

## Overview

The Military Hierarchy Database is designed to support real-time military communication monitoring with AI-powered report generation. The schema follows a hierarchical structure that mirrors military organization while maintaining complete audit trails of all communications.

## Database Files

- **`database_schema.sql`** - Complete SQL schema with comments and examples
- **`schema_definition.py`** - Python classes for programmatic schema access
- **`validate_schema.py`** - Validation script to ensure database integrity
- **`database_setup.py`** - Initialization script that creates tables and sample data

## Table Structure

### 1. Units Table
**Purpose**: Hierarchical military organization structure

```sql
CREATE TABLE units (
    unit_id TEXT PRIMARY KEY,           -- e.g., 'BAT_1', 'CO_A', 'PLT_1'
    name TEXT NOT NULL,                 -- e.g., '1st Infantry Battalion'
    parent_unit_id TEXT,                -- Reference to parent unit (NULL for top-level)
    level TEXT NOT NULL,                -- Battalion, Company, Platoon, Squad
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

**Hierarchy Example**:
```
1st Infantry Battalion (BAT_1)
├── Alpha Company (CO_A)
│   ├── 1st Platoon (PLT_1)
│   │   ├── 1st Squad (SQD_1)
│   │   └── 2nd Squad (SQD_2)
│   └── 2nd Platoon (PLT_2)
│       └── 3rd Squad (SQD_3)
└── Bravo Company (CO_B)
```

### 2. Soldiers Table
**Purpose**: Individual personnel records with device associations

```sql
CREATE TABLE soldiers (
    soldier_id TEXT PRIMARY KEY,        -- e.g., 'ALPHA_01'
    name TEXT NOT NULL,                 -- e.g., 'Lt. John Smith'
    rank TEXT,                          -- e.g., 'Lieutenant'
    unit_id TEXT NOT NULL,              -- Assigned unit reference
    device_id TEXT,                     -- Associated device/radio ID
    status TEXT DEFAULT 'active',       -- active, injured, missing, etc.
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    last_seen TEXT                      -- Last communication timestamp
);
```

### 3. Soldier Raw Inputs Table
**Purpose**: Complete history of all voice/text inputs from soldiers

```sql
CREATE TABLE soldier_raw_inputs (
    input_id TEXT PRIMARY KEY,          -- UUID for unique identification
    soldier_id TEXT NOT NULL,           -- Source soldier reference
    timestamp TEXT NOT NULL,            -- ISO format timestamp
    raw_text TEXT NOT NULL,             -- Transcribed voice or typed text
    raw_audio_ref TEXT,                 -- Optional reference to audio file
    input_type TEXT DEFAULT 'voice',    -- voice, text, image, sensor
    confidence REAL DEFAULT 0.0,        -- Transcription confidence (0.0-1.0)
    location_ref TEXT,                  -- Optional location reference
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

**Key Features**:
- Complete audit trail of all communications
- Supports multiple input types (voice, text, images, sensor data)
- Confidence scoring for AI transcription accuracy
- Location tracking capabilities

### 4. Reports Table
**Purpose**: AI-generated structured military reports

```sql
CREATE TABLE reports (
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
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

**Report Types**:
- **CASEVAC**: Casualty Evacuation requests
- **EOINCREP**: Enemy Order of Battle Intelligence Reports
- **SITREP**: Situation Reports
- **FRAGO**: Fragmentary Orders
- **OPORD**: Operation Orders

### 5. Device Status Table
**Purpose**: Equipment and communication device monitoring

```sql
CREATE TABLE device_status (
    device_id TEXT PRIMARY KEY,         -- Device identifier
    soldier_id TEXT,                    -- Associated soldier (nullable)
    status TEXT DEFAULT 'active',       -- active, offline, maintenance, lost
    last_heartbeat TEXT,                -- Last MQTT heartbeat
    battery_level INTEGER,              -- Battery percentage (0-100)
    signal_strength INTEGER,            -- Signal strength (0-100)
    location_lat REAL,                  -- GPS latitude
    location_lon REAL,                  -- GPS longitude
    location_accuracy REAL,             -- GPS accuracy in meters
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

### 6. Communication Log Table
**Purpose**: MQTT and network activity tracking

```sql
CREATE TABLE comm_log (
    log_id TEXT PRIMARY KEY,            -- UUID for log entry
    device_id TEXT,                     -- Source device
    soldier_id TEXT,                    -- Associated soldier
    topic TEXT NOT NULL,                -- MQTT topic
    message_type TEXT NOT NULL,         -- input, heartbeat, status, error
    message_size INTEGER,               -- Message size in bytes
    timestamp TEXT NOT NULL,            -- Message timestamp
    success BOOLEAN DEFAULT TRUE,       -- Delivery success status
    error_message TEXT,                 -- Error details if failed
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

## Indexes

The schema includes comprehensive indexing for optimal query performance:

### Units Indexes
- `idx_units_parent` - Fast parent unit lookups
- `idx_units_level` - Filter by unit level

### Soldiers Indexes
- `idx_soldiers_unit` - Find soldiers by unit
- `idx_soldiers_device` - Device-to-soldier mapping
- `idx_soldiers_status` - Filter by status

### Raw Inputs Indexes
- `idx_raw_inputs_soldier` - Soldier input history
- `idx_raw_inputs_timestamp` - Time-based queries
- `idx_raw_inputs_type` - Filter by input type

### Reports Indexes
- `idx_reports_soldier` - Soldier report history
- `idx_reports_unit` - Unit-level reports
- `idx_reports_type` - Filter by report type
- `idx_reports_timestamp` - Time-based queries
- `idx_reports_status` - Filter by status

### Device & Communication Indexes
- `idx_device_status_soldier` - Soldier device lookup
- `idx_device_status_last_heartbeat` - Device health monitoring
- `idx_comm_log_device` - Device communication history
- `idx_comm_log_soldier` - Soldier communication history
- `idx_comm_log_timestamp` - Time-based communication queries
- `idx_comm_log_topic` - MQTT topic filtering

## Views

### Soldier Details View
```sql
CREATE VIEW soldier_details AS
SELECT 
    s.soldier_id, s.name, s.rank, s.unit_id, s.device_id, s.status, s.last_seen,
    u.name as unit_name, u.level as unit_level, u.parent_unit_id,
    (SELECT name FROM units WHERE unit_id = u.parent_unit_id) as parent_unit_name
FROM soldiers s
JOIN units u ON s.unit_id = u.unit_id;
```

### Recent Activity View
```sql
CREATE VIEW recent_activity AS
SELECT 
    s.soldier_id, s.name, s.rank, u.name as unit_name,
    COUNT(r.input_id) as recent_inputs, MAX(r.timestamp) as last_input,
    COUNT(rp.report_id) as recent_reports, MAX(rp.timestamp) as last_report
FROM soldiers s
JOIN units u ON s.unit_id = u.unit_id
LEFT JOIN soldier_raw_inputs r ON s.soldier_id = r.soldier_id 
    AND r.timestamp > datetime('now', '-24 hours')
LEFT JOIN reports rp ON s.soldier_id = rp.soldier_id 
    AND rp.timestamp > datetime('now', '-24 hours')
GROUP BY s.soldier_id, s.name, s.rank, u.name;
```

### Unit Hierarchy View
```sql
CREATE VIEW unit_hierarchy AS
WITH RECURSIVE unit_tree AS (
    SELECT unit_id, name, parent_unit_id, level, 0 as depth
    FROM units WHERE parent_unit_id IS NULL
    UNION ALL
    SELECT u.unit_id, u.name, u.parent_unit_id, u.level, ut.depth + 1
    FROM units u JOIN unit_tree ut ON u.parent_unit_id = ut.unit_id
)
SELECT unit_id, name, parent_unit_id, level, depth
FROM unit_tree ORDER BY depth, name;
```

## Data Flow

1. **Soldier Device** → MQTT → **Raw Inputs Table**
2. **Raw Inputs** → AI Processing → **Reports Table**
3. **Frontend** → API Queries → **All Tables**
4. **Device Monitoring** → **Device Status Table**
5. **Communication Tracking** → **Comm Log Table**

## Schema Validation

Run the validation script to ensure database integrity:

```bash
python validate_schema.py
```

This will check:
- All expected tables exist
- Column types and constraints match
- Foreign key relationships are intact
- Required indexes are present
- Sample data integrity

## Migration Notes

### From Basic to Full Schema
If you have an existing database with the basic 4-table schema, you can migrate by:

1. Backing up existing data
2. Running the new `database_setup.py`
3. Migrating data to new columns
4. Validating with `validate_schema.py`

### Future Enhancements
The schema is designed to be extensible:
- Additional report types can be added
- New input types (sensors, images) are supported
- GPS coordinates can be expanded to full location services
- Audit trails can be enhanced with more metadata

## Performance Considerations

- **Indexes**: All frequently queried columns are indexed
- **Partitioning**: Consider partitioning by date for large datasets
- **Archiving**: Implement data archiving for old communications
- **Caching**: Use Redis for frequently accessed hierarchy data
- **Connection Pooling**: Use connection pooling for high-concurrency scenarios

## Security Considerations

- **Encryption**: Sensitive data should be encrypted at rest
- **Access Control**: Implement role-based access control
- **Audit Logging**: All data modifications should be logged
- **Data Retention**: Implement proper data retention policies
- **Network Security**: Secure MQTT communication with TLS

This schema provides a robust foundation for military communication monitoring while maintaining flexibility for future enhancements and scalability requirements.
