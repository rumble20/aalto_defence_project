-- Create suggestions table for AI-triggered report recommendations
-- This supports Level 2 (Smart Notifications) and Level 3 (Auto-Drafts)

CREATE TABLE IF NOT EXISTS suggestions (
    suggestion_id TEXT PRIMARY KEY,
    suggestion_type TEXT NOT NULL CHECK(suggestion_type IN ('CASEVAC', 'EOINCREP', 'EOINCREP_EOD')),
    urgency TEXT NOT NULL CHECK(urgency IN ('URGENT', 'HIGH', 'MEDIUM', 'LOW')),
    reason TEXT NOT NULL,
    confidence REAL NOT NULL CHECK(confidence >= 0.0 AND confidence <= 1.0),
    source_reports TEXT NOT NULL, -- JSON array of report IDs
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'draft_created', 'approved', 'dismissed')),
    suggested_fields TEXT, -- JSON object with pre-filled field suggestions
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    dismissed_at TIMESTAMP,
    dismissed_by TEXT,
    unit_id TEXT, -- Which unit this suggestion is for
    FOREIGN KEY (unit_id) REFERENCES units(unit_id)
);

CREATE INDEX IF NOT EXISTS idx_suggestions_status ON suggestions(status);
CREATE INDEX IF NOT EXISTS idx_suggestions_created ON suggestions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_suggestions_unit ON suggestions(unit_id);
CREATE INDEX IF NOT EXISTS idx_suggestions_type ON suggestions(suggestion_type);

-- Create drafts table for Level 3 (Auto-Drafts)
-- Drafts are pre-generated reports awaiting user approval
CREATE TABLE IF NOT EXISTS report_drafts (
    draft_id TEXT PRIMARY KEY,
    suggestion_id TEXT,
    report_type TEXT NOT NULL CHECK(report_type IN ('CASEVAC', 'EOINCREP', 'EOINCREP_EOD')),
    report_number INTEGER,
    formatted_text TEXT NOT NULL,
    structured_json TEXT NOT NULL, -- JSON with all fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP,
    approved_by TEXT,
    report_id TEXT, -- ID of final report if approved
    FOREIGN KEY (suggestion_id) REFERENCES suggestions(suggestion_id),
    FOREIGN KEY (report_id) REFERENCES reports(report_id)
);

CREATE INDEX IF NOT EXISTS idx_drafts_suggestion ON report_drafts(suggestion_id);
CREATE INDEX IF NOT EXISTS idx_drafts_created ON report_drafts(created_at DESC);

-- Create report sequences for CASEVAC and EOINCREP
-- Auto-incrementing report numbers per type
CREATE TABLE IF NOT EXISTS report_sequences (
    report_type TEXT PRIMARY KEY,
    next_number INTEGER NOT NULL DEFAULT 1
);

INSERT OR IGNORE INTO report_sequences (report_type, next_number) VALUES 
    ('CASEVAC', 1),
    ('EOINCREP', 1);

-- Add trigger to update updated_at timestamp
CREATE TRIGGER IF NOT EXISTS update_suggestions_timestamp 
AFTER UPDATE ON suggestions
BEGIN
    UPDATE suggestions SET updated_at = CURRENT_TIMESTAMP WHERE suggestion_id = NEW.suggestion_id;
END;
