# military_database_handler.py
import sqlite3
from datetime import datetime
import json

class MilitaryDatabaseHandler:
    def __init__(self, db_path="military_reports.db"):
        self.db_path = db_path
        self.initialize_database()
    
    def initialize_database(self):
        """Create necessary tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create main reports table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS military_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_type TEXT NOT NULL,
                    action TEXT,
                    timestamp DATETIME,
                    coordinates_x FLOAT,
                    coordinates_y FLOAT,
                    timeframe TEXT,
                    priority TEXT,
                    raw_data TEXT
                )
            ''')
            
            # Create units involvement table for many-to-many relationship
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS report_units (
                    report_id INTEGER,
                    unit_name TEXT,
                    FOREIGN KEY (report_id) REFERENCES military_reports (id),
                    PRIMARY KEY (report_id, unit_name)
                )
            ''')
            
            conn.commit()

    def store_report(self, packet, report_type):
        """
        Store a military report packet in the database
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Extract data from packet
            action = packet.get("action", "UNKNOWN")
            coords = packet.get("coordinates", {})
            x = coords.get("x")
            y = coords.get("y")
            timeframe = packet.get("timeframe")
            priority = packet.get("priority")
            
            # Insert main report data
            cursor.execute('''
                INSERT INTO military_reports 
                (report_type, action, timestamp, coordinates_x, coordinates_y, 
                timeframe, priority, raw_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                report_type,
                action,
                datetime.now().isoformat(),
                x,
                y,
                timeframe,
                priority,
                json.dumps(packet)
            ))
            
            report_id = cursor.lastrowid
            
            # Store unit associations
            units = packet.get("target_units", [])
            for unit in units:
                cursor.execute('''
                    INSERT INTO report_units (report_id, unit_name)
                    VALUES (?, ?)
                ''', (report_id, unit))
            
            conn.commit()
            return report_id

    def get_report(self, report_id):
        """Retrieve a specific report by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get main report data
            cursor.execute('''
                SELECT * FROM military_reports WHERE id = ?
            ''', (report_id,))
            report = cursor.fetchone()
            
            if report:
                # Get associated units
                cursor.execute('''
                    SELECT unit_name FROM report_units WHERE report_id = ?
                ''', (report_id,))
                units = [row[0] for row in cursor.fetchall()]
                
                return {
                    "id": report[0],
                    "report_type": report[1],
                    "action": report[2],
                    "timestamp": report[3],
                    "coordinates": {"x": report[4], "y": report[5]},
                    "timeframe": report[6],
                    "priority": report[7],
                    "units": units,
                    "raw_data": json.loads(report[8])
                }
            return None

    def get_reports_by_unit(self, unit_name):
        """Retrieve all reports involving a specific unit"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DISTINCT m.* 
                FROM military_reports m
                JOIN report_units ru ON m.id = ru.report_id
                WHERE ru.unit_name = ?
            ''', (unit_name,))
            return [dict(zip([col[0] for col in cursor.description], row)) 
                   for row in cursor.fetchall()]

# Example usage:
# db_handler = MilitaryDatabaseHandler()
# packet = {
#     "action": "Advance",
#     "target_units": ["Alpha", "Bravo"],
#     "coordinates": {"x": 123, "y": 456},
#     "timeframe": "0600Z",
#     "priority": "HIGH"
# }
# report_id = db_handler.store_report(packet, "EOINCREP")
# retrieved_report = db_handler.get_report(report_id)