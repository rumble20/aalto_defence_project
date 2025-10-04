"""
Database Schema Definition for Military Hierarchy System
This file provides programmatic access to the database schema for validation,
documentation, and migration purposes.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum

class UnitLevel(Enum):
    """Military unit hierarchy levels."""
    BATTALION = "Battalion"
    COMPANY = "Company"
    PLATOON = "Platoon"
    SQUAD = "Squad"

class ReportType(Enum):
    """Standard military report types."""
    CASEVAC = "CASEVAC"      # Casualty Evacuation
    EOINCREP = "EOINCREP"    # Enemy Order of Battle Intelligence Report
    SITREP = "SITREP"        # Situation Report
    FRAGO = "FRAGO"          # Fragmentary Order
    OPORD = "OPORD"          # Operation Order

class InputType(Enum):
    """Types of input from soldier devices."""
    VOICE = "voice"
    TEXT = "text"
    IMAGE = "image"
    SENSOR = "sensor"

class Status(Enum):
    """Common status values across tables."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    INJURED = "injured"
    MISSING = "missing"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"
    LOST = "lost"

@dataclass
class TableSchema:
    """Represents a database table schema."""
    name: str
    columns: List[Dict[str, Any]]
    indexes: List[str]
    foreign_keys: List[Dict[str, str]]

class MilitaryHierarchySchema:
    """Complete database schema definition for the military hierarchy system."""
    
    def __init__(self):
        self.tables = self._define_tables()
    
    def _define_tables(self) -> Dict[str, TableSchema]:
        """Define all database tables with their schemas."""
        return {
            'units': TableSchema(
                name='units',
                columns=[
                    {'name': 'unit_id', 'type': 'TEXT', 'primary_key': True, 'nullable': False},
                    {'name': 'name', 'type': 'TEXT', 'primary_key': False, 'nullable': False},
                    {'name': 'parent_unit_id', 'type': 'TEXT', 'primary_key': False, 'nullable': True},
                    {'name': 'level', 'type': 'TEXT', 'primary_key': False, 'nullable': False},
                    {'name': 'created_at', 'type': 'TEXT', 'primary_key': False, 'nullable': True, 'default': 'CURRENT_TIMESTAMP'}
                ],
                indexes=[
                    'idx_units_parent',
                    'idx_units_level'
                ],
                foreign_keys=[
                    {'column': 'parent_unit_id', 'references_table': 'units', 'references_column': 'unit_id'}
                ]
            ),
            
            'soldiers': TableSchema(
                name='soldiers',
                columns=[
                    {'name': 'soldier_id', 'type': 'TEXT', 'primary_key': True, 'nullable': False},
                    {'name': 'name', 'type': 'TEXT', 'primary_key': False, 'nullable': False},
                    {'name': 'rank', 'type': 'TEXT', 'primary_key': False, 'nullable': True},
                    {'name': 'unit_id', 'type': 'TEXT', 'primary_key': False, 'nullable': False},
                    {'name': 'device_id', 'type': 'TEXT', 'primary_key': False, 'nullable': True},
                    {'name': 'status', 'type': 'TEXT', 'primary_key': False, 'nullable': True, 'default': "'active'"},
                    {'name': 'created_at', 'type': 'TEXT', 'primary_key': False, 'nullable': True, 'default': 'CURRENT_TIMESTAMP'},
                    {'name': 'last_seen', 'type': 'TEXT', 'primary_key': False, 'nullable': True}
                ],
                indexes=[
                    'idx_soldiers_unit',
                    'idx_soldiers_device',
                    'idx_soldiers_status'
                ],
                foreign_keys=[
                    {'column': 'unit_id', 'references_table': 'units', 'references_column': 'unit_id'}
                ]
            ),
            
            'soldier_raw_inputs': TableSchema(
                name='soldier_raw_inputs',
                columns=[
                    {'name': 'input_id', 'type': 'TEXT', 'primary_key': True, 'nullable': False},
                    {'name': 'soldier_id', 'type': 'TEXT', 'primary_key': False, 'nullable': False},
                    {'name': 'timestamp', 'type': 'TEXT', 'primary_key': False, 'nullable': False},
                    {'name': 'raw_text', 'type': 'TEXT', 'primary_key': False, 'nullable': False},
                    {'name': 'raw_audio_ref', 'type': 'TEXT', 'primary_key': False, 'nullable': True},
                    {'name': 'input_type', 'type': 'TEXT', 'primary_key': False, 'nullable': True, 'default': "'voice'"},
                    {'name': 'confidence', 'type': 'REAL', 'primary_key': False, 'nullable': True, 'default': '0.0'},
                    {'name': 'location_ref', 'type': 'TEXT', 'primary_key': False, 'nullable': True},
                    {'name': 'created_at', 'type': 'TEXT', 'primary_key': False, 'nullable': True, 'default': 'CURRENT_TIMESTAMP'}
                ],
                indexes=[
                    'idx_raw_inputs_soldier',
                    'idx_raw_inputs_timestamp',
                    'idx_raw_inputs_type'
                ],
                foreign_keys=[
                    {'column': 'soldier_id', 'references_table': 'soldiers', 'references_column': 'soldier_id'}
                ]
            ),
            
            'reports': TableSchema(
                name='reports',
                columns=[
                    {'name': 'report_id', 'type': 'TEXT', 'primary_key': True, 'nullable': False},
                    {'name': 'soldier_id', 'type': 'TEXT', 'primary_key': False, 'nullable': False},
                    {'name': 'unit_id', 'type': 'TEXT', 'primary_key': False, 'nullable': False},
                    {'name': 'timestamp', 'type': 'TEXT', 'primary_key': False, 'nullable': False},
                    {'name': 'report_type', 'type': 'TEXT', 'primary_key': False, 'nullable': False},
                    {'name': 'structured_json', 'type': 'TEXT', 'primary_key': False, 'nullable': False},
                    {'name': 'confidence', 'type': 'REAL', 'primary_key': False, 'nullable': False},
                    {'name': 'source_input_id', 'type': 'TEXT', 'primary_key': False, 'nullable': True},
                    {'name': 'status', 'type': 'TEXT', 'primary_key': False, 'nullable': True, 'default': "'generated'"},
                    {'name': 'reviewed_by', 'type': 'TEXT', 'primary_key': False, 'nullable': True},
                    {'name': 'reviewed_at', 'type': 'TEXT', 'primary_key': False, 'nullable': True},
                    {'name': 'created_at', 'type': 'TEXT', 'primary_key': False, 'nullable': True, 'default': 'CURRENT_TIMESTAMP'}
                ],
                indexes=[
                    'idx_reports_soldier',
                    'idx_reports_unit',
                    'idx_reports_type',
                    'idx_reports_timestamp',
                    'idx_reports_status'
                ],
                foreign_keys=[
                    {'column': 'soldier_id', 'references_table': 'soldiers', 'references_column': 'soldier_id'},
                    {'column': 'unit_id', 'references_table': 'units', 'references_column': 'unit_id'},
                    {'column': 'source_input_id', 'references_table': 'soldier_raw_inputs', 'references_column': 'input_id'}
                ]
            ),
            
            'device_status': TableSchema(
                name='device_status',
                columns=[
                    {'name': 'device_id', 'type': 'TEXT', 'primary_key': True, 'nullable': False},
                    {'name': 'soldier_id', 'type': 'TEXT', 'primary_key': False, 'nullable': True},
                    {'name': 'status', 'type': 'TEXT', 'primary_key': False, 'nullable': True, 'default': "'active'"},
                    {'name': 'last_heartbeat', 'type': 'TEXT', 'primary_key': False, 'nullable': True},
                    {'name': 'battery_level', 'type': 'INTEGER', 'primary_key': False, 'nullable': True},
                    {'name': 'signal_strength', 'type': 'INTEGER', 'primary_key': False, 'nullable': True},
                    {'name': 'location_lat', 'type': 'REAL', 'primary_key': False, 'nullable': True},
                    {'name': 'location_lon', 'type': 'REAL', 'primary_key': False, 'nullable': True},
                    {'name': 'location_accuracy', 'type': 'REAL', 'primary_key': False, 'nullable': True},
                    {'name': 'created_at', 'type': 'TEXT', 'primary_key': False, 'nullable': True, 'default': 'CURRENT_TIMESTAMP'},
                    {'name': 'updated_at', 'type': 'TEXT', 'primary_key': False, 'nullable': True, 'default': 'CURRENT_TIMESTAMP'}
                ],
                indexes=[
                    'idx_device_status_soldier',
                    'idx_device_status_last_heartbeat'
                ],
                foreign_keys=[
                    {'column': 'soldier_id', 'references_table': 'soldiers', 'references_column': 'soldier_id'}
                ]
            ),
            
            'comm_log': TableSchema(
                name='comm_log',
                columns=[
                    {'name': 'log_id', 'type': 'TEXT', 'primary_key': True, 'nullable': False},
                    {'name': 'device_id', 'type': 'TEXT', 'primary_key': False, 'nullable': True},
                    {'name': 'soldier_id', 'type': 'TEXT', 'primary_key': False, 'nullable': True},
                    {'name': 'topic', 'type': 'TEXT', 'primary_key': False, 'nullable': False},
                    {'name': 'message_type', 'type': 'TEXT', 'primary_key': False, 'nullable': False},
                    {'name': 'message_size', 'type': 'INTEGER', 'primary_key': False, 'nullable': True},
                    {'name': 'timestamp', 'type': 'TEXT', 'primary_key': False, 'nullable': False},
                    {'name': 'success', 'type': 'BOOLEAN', 'primary_key': False, 'nullable': True, 'default': 'TRUE'},
                    {'name': 'error_message', 'type': 'TEXT', 'primary_key': False, 'nullable': True},
                    {'name': 'created_at', 'type': 'TEXT', 'primary_key': False, 'nullable': True, 'default': 'CURRENT_TIMESTAMP'}
                ],
                indexes=[
                    'idx_comm_log_device',
                    'idx_comm_log_soldier',
                    'idx_comm_log_timestamp',
                    'idx_comm_log_topic'
                ],
                foreign_keys=[
                    {'column': 'soldier_id', 'references_table': 'soldiers', 'references_column': 'soldier_id'}
                ]
            )
        }
    
    def get_table_names(self) -> List[str]:
        """Get list of all table names."""
        return list(self.tables.keys())
    
    def get_table_schema(self, table_name: str) -> Optional[TableSchema]:
        """Get schema for a specific table."""
        return self.tables.get(table_name)
    
    def get_column_info(self, table_name: str, column_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific column."""
        table = self.get_table_schema(table_name)
        if not table:
            return None
        
        for column in table.columns:
            if column['name'] == column_name:
                return column
        return None
    
    def validate_table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the schema."""
        return table_name in self.tables
    
    def get_foreign_key_relationships(self) -> Dict[str, List[Dict[str, str]]]:
        """Get all foreign key relationships in the database."""
        relationships = {}
        for table_name, table_schema in self.tables.items():
            if table_schema.foreign_keys:
                relationships[table_name] = table_schema.foreign_keys
        return relationships
    
    def generate_create_table_sql(self, table_name: str) -> str:
        """Generate CREATE TABLE SQL for a specific table."""
        table = self.get_table_schema(table_name)
        if not table:
            raise ValueError(f"Table {table_name} not found in schema")
        
        columns = []
        for col in table.columns:
            col_def = f"{col['name']} {col['type']}"
            if col.get('primary_key'):
                col_def += " PRIMARY KEY"
            if not col.get('nullable', True):
                col_def += " NOT NULL"
            if col.get('default'):
                col_def += f" DEFAULT {col['default']}"
            columns.append(col_def)
        
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
        sql += "    " + ",\n    ".join(columns)
        
        if table.foreign_keys:
            sql += ",\n    "
            fk_definitions = []
            for fk in table.foreign_keys:
                fk_def = f"FOREIGN KEY({fk['column']}) REFERENCES {fk['references_table']}({fk['references_column']})"
                fk_definitions.append(fk_def)
            sql += ",\n    ".join(fk_definitions)
        
        sql += "\n);"
        return sql
    
    def generate_all_create_statements(self) -> str:
        """Generate CREATE TABLE statements for all tables."""
        statements = []
        statements.append("-- Military Hierarchy Database Schema")
        statements.append("-- Generated from schema_definition.py")
        statements.append("")
        
        for table_name in self.get_table_names():
            statements.append(self.generate_create_table_sql(table_name))
            statements.append("")
        
        return "\n".join(statements)
    
    def get_enum_values(self) -> Dict[str, List[str]]:
        """Get all enum values for documentation."""
        return {
            'UnitLevel': [level.value for level in UnitLevel],
            'ReportType': [report_type.value for report_type in ReportType],
            'InputType': [input_type.value for input_type in InputType],
            'Status': [status.value for status in Status]
        }

def main():
    """Example usage of the schema definition."""
    schema = MilitaryHierarchySchema()
    
    print("Military Hierarchy Database Schema")
    print("=" * 40)
    print()
    
    print("Available Tables:")
    for table_name in schema.get_table_names():
        print(f"  - {table_name}")
    print()
    
    print("Enum Values:")
    for enum_name, values in schema.get_enum_values().items():
        print(f"  {enum_name}: {', '.join(values)}")
    print()
    
    print("Foreign Key Relationships:")
    for table, fks in schema.get_foreign_key_relationships().items():
        print(f"  {table}:")
        for fk in fks:
            print(f"    {fk['column']} -> {fk['references_table']}.{fk['references_column']}")
    print()
    
    print("Sample CREATE TABLE statement for 'units':")
    print(schema.generate_create_table_sql('units'))

if __name__ == "__main__":
    main()
