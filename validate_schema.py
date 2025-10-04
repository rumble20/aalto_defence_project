#!/usr/bin/env python3
"""
Schema Validation Script for Military Hierarchy Database
Validates that the actual database matches the defined schema.
"""

import sqlite3
import sys
from schema_definition import MilitaryHierarchySchema

class SchemaValidator:
    """Validates database schema against the defined schema."""
    
    def __init__(self, db_path: str = "military_hierarchy.db"):
        self.db_path = db_path
        self.schema = MilitaryHierarchySchema()
        self.errors = []
        self.warnings = []
    
    def validate(self) -> bool:
        """Run complete schema validation."""
        print("🔍 Validating Military Hierarchy Database Schema...")
        print(f"Database: {self.db_path}")
        print()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if database exists and is accessible
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            existing_tables = [row[0] for row in cursor.fetchall()]
            
            print(f"Found {len(existing_tables)} tables in database:")
            for table in existing_tables:
                print(f"  ✓ {table}")
            print()
            
            # Validate each expected table
            expected_tables = self.schema.get_table_names()
            missing_tables = set(expected_tables) - set(existing_tables)
            extra_tables = set(existing_tables) - set(expected_tables)
            
            if missing_tables:
                self.errors.append(f"Missing tables: {', '.join(missing_tables)}")
            
            if extra_tables:
                self.warnings.append(f"Extra tables found: {', '.join(extra_tables)}")
            
            # Validate each table structure
            for table_name in expected_tables:
                if table_name in existing_tables:
                    self._validate_table_structure(cursor, table_name)
            
            # Validate foreign key constraints
            self._validate_foreign_keys(cursor)
            
            # Validate indexes
            self._validate_indexes(cursor)
            
            conn.close()
            
            # Report results
            self._report_results()
            
            return len(self.errors) == 0
            
        except sqlite3.Error as e:
            self.errors.append(f"Database error: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Validation error: {e}")
            return False
    
    def _validate_table_structure(self, cursor, table_name: str):
        """Validate the structure of a specific table."""
        table_schema = self.schema.get_table_schema(table_name)
        if not table_schema:
            return
        
        # Get actual table info
        cursor.execute(f"PRAGMA table_info({table_name});")
        actual_columns = {row[1]: row for row in cursor.fetchall()}  # name: (cid, name, type, notnull, dflt_value, pk)
        
        expected_columns = {col['name']: col for col in table_schema.columns}
        
        # Check for missing columns
        missing_columns = set(expected_columns.keys()) - set(actual_columns.keys())
        if missing_columns:
            self.errors.append(f"Table {table_name}: Missing columns {', '.join(missing_columns)}")
        
        # Check for extra columns
        extra_columns = set(actual_columns.keys()) - set(expected_columns.keys())
        if extra_columns:
            self.warnings.append(f"Table {table_name}: Extra columns {', '.join(extra_columns)}")
        
        # Validate existing columns
        for col_name in set(expected_columns.keys()) & set(actual_columns.keys()):
            expected = expected_columns[col_name]
            actual = actual_columns[col_name]
            
            # Check data type (SQLite is flexible, so we'll be lenient)
            expected_type = expected['type'].upper()
            actual_type = actual[2].upper()
            
            if expected_type not in actual_type and actual_type not in expected_type:
                self.warnings.append(f"Table {table_name}.{col_name}: Type mismatch (expected {expected_type}, got {actual_type})")
            
            # Check NOT NULL constraint
            expected_nullable = expected.get('nullable', True)
            actual_nullable = actual[3] == 0  # SQLite: 0 = nullable, 1 = not null
            
            if expected_nullable != actual_nullable:
                self.errors.append(f"Table {table_name}.{col_name}: NULL constraint mismatch")
            
            # Check primary key
            expected_pk = expected.get('primary_key', False)
            actual_pk = actual[5] == 1  # SQLite: 1 = primary key
            
            if expected_pk != actual_pk:
                self.errors.append(f"Table {table_name}.{col_name}: Primary key mismatch")
    
    def _validate_foreign_keys(self, cursor):
        """Validate foreign key constraints."""
        cursor.execute("PRAGMA foreign_key_check;")
        fk_violations = cursor.fetchall()
        
        if fk_violations:
            for violation in fk_violations:
                self.errors.append(f"Foreign key violation: {violation}")
        
        # Check if foreign keys are enabled
        cursor.execute("PRAGMA foreign_keys;")
        fk_enabled = cursor.fetchone()[0]
        if not fk_enabled:
            self.warnings.append("Foreign key constraints are disabled")
    
    def _validate_indexes(self, cursor):
        """Validate that expected indexes exist."""
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%';")
        existing_indexes = {row[0] for row in cursor.fetchall()}
        
        expected_indexes = set()
        for table_schema in self.schema.tables.values():
            expected_indexes.update(table_schema.indexes)
        
        missing_indexes = expected_indexes - existing_indexes
        if missing_indexes:
            self.warnings.append(f"Missing indexes: {', '.join(missing_indexes)}")
    
    def _report_results(self):
        """Report validation results."""
        print("📊 Validation Results:")
        print("=" * 30)
        
        if not self.errors and not self.warnings:
            print("✅ Schema validation passed! Database structure is correct.")
            return
        
        if self.errors:
            print("❌ Errors found:")
            for error in self.errors:
                print(f"  • {error}")
            print()
        
        if self.warnings:
            print("⚠️  Warnings:")
            for warning in self.warnings:
                print(f"  • {warning}")
            print()
        
        if self.errors:
            print("🔧 Action required: Fix errors before proceeding.")
        elif self.warnings:
            print("💡 Consider addressing warnings for optimal performance.")

def main():
    """Main validation function."""
    db_path = sys.argv[1] if len(sys.argv) > 1 else "military_hierarchy.db"
    
    validator = SchemaValidator(db_path)
    success = validator.validate()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
