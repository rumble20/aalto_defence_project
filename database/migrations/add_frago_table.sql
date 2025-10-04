-- Add FRAGO table to track generated fragmentary orders
CREATE TABLE IF NOT EXISTS fragos (
    frago_id TEXT PRIMARY KEY,
    frago_number INTEGER NOT NULL,
    unit_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    created_by TEXT,
    suggested_fields TEXT NOT NULL,  -- JSON with AI-suggested FRAGO fields
    final_fields TEXT NOT NULL,      -- JSON with user-edited final fields
    formatted_document TEXT NOT NULL, -- Final formatted FRAGO text
    source_reports TEXT NOT NULL,     -- JSON array of report IDs used for analysis
    FOREIGN KEY (unit_id) REFERENCES units (unit_id)
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_fragos_unit_id ON fragos(unit_id);
CREATE INDEX IF NOT EXISTS idx_fragos_created_at ON fragos(created_at);

-- Create sequence table for auto-incrementing FRAGO numbers
CREATE TABLE IF NOT EXISTS frago_sequence (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    next_number INTEGER NOT NULL DEFAULT 1
);

-- Initialize sequence
INSERT OR IGNORE INTO frago_sequence (id, next_number) VALUES (1, 1);
