#!/usr/bin/env python3
"""
Clear all reports from the database
"""

import sqlite3

DB_PATH = "military_hierarchy.db"

def clear_reports():
    """Delete all reports from the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Get count before deletion
        c.execute("SELECT COUNT(*) FROM reports")
        count_before = c.fetchone()[0]
        
        # Delete all reports
        c.execute("DELETE FROM reports")
        
        conn.commit()
        
        # Get count after deletion
        c.execute("SELECT COUNT(*) FROM reports")
        count_after = c.fetchone()[0]
        
        conn.close()
        
        print(f"✅ Cleared {count_before} reports from database")
        print(f"📊 Reports remaining: {count_after}")
        
    except Exception as e:
        print(f"❌ Error clearing reports: {e}")

if __name__ == "__main__":
    print("🗑️  Clearing all reports from database...")
    clear_reports()
    print("✅ Done!")
