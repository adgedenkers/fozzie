import sqlite3
import json
import os
import re
import pandas as pd
import numpy as np

def save_json_to_sqlite(json_data, db_path, table_name="data", primary_key=None, debug=False):
    """
    Saves a JSON object or list of objects to an SQLite database.
    - Detects schema changes and updates the table if new fields are introduced.
    - Handles nested JSON by creating separate relational tables.
    - Provides logging and debugging options.

    Parameters:
    - json_data (dict | list): JSON data (dict or list of dicts).
    - db_path (str): Path to the SQLite database file.
    - table_name (str): Table name in the SQLite database.
    - primary_key (str, optional): Field to use as primary key.
    - debug (bool, optional): If True, prints debug information.

    """
    
    def sanitize_name(name):
        """Replace spaces and hyphens with underscores for SQLite compatibility."""
        return re.sub(r'[\s\-]', '_', name)

    def infer_sqlite_type(value):
        """Infer SQLite-compatible data type from a value."""
        if isinstance(value, int):
            return "INTEGER"
        elif isinstance(value, float):
            return "REAL"
        elif isinstance(value, bool):
            return "INTEGER"  # SQLite stores booleans as integers (0/1)
        elif isinstance(value, dict) or isinstance(value, list):
            return "TEXT"  # Store JSON as text for nested structures
        else:
            return "TEXT"

    def get_existing_columns(conn, table):
        """Returns a set of existing column names for the given table."""
        sanitized_table = sanitize_name(table)
        query = f'PRAGMA table_info("{sanitized_table}")'
        cursor = conn.execute(query)
        return {row[1] for row in cursor.fetchall()}  # row[1] is column name

    def create_or_update_table(conn, table, sample_record):
        """Creates or updates a table based on a sample record."""
        sanitized_table = sanitize_name(table)
        existing_columns = get_existing_columns(conn, table)

        new_columns = []
        for key, value in sample_record.items():
            col_name = sanitize_name(key)
            col_type = infer_sqlite_type(value)
            if col_name not in existing_columns:
                new_columns.append(f'ADD COLUMN "{col_name}" {col_type}')

        if not existing_columns:
            # Create table if it doesn't exist
            columns = [f'"{sanitize_name(k)}" {infer_sqlite_type(v)}' for k, v in sample_record.items()]
            if primary_key and primary_key in sample_record:
                columns.append(f"PRIMARY KEY(\"{sanitize_name(primary_key)}\")")
            columns_def = ", ".join(columns)
            query = f'CREATE TABLE IF NOT EXISTS "{sanitized_table}" ({columns_def})'
            if debug: print(f"[DEBUG] Creating table: {query}")
            conn.execute(query)
        elif new_columns:
            # Alter table if new columns are found
            for alter_stmt in new_columns:
                query = f'ALTER TABLE "{sanitized_table}" {alter_stmt}'
                if debug: print(f"[DEBUG] Altering table: {query}")
                conn.execute(query)

    def insert_data(conn, table, record):
        """Inserts a record into the database, handling nested JSON."""
        sanitized_table = sanitize_name(table)
        keys, values = [], []

        for key, value in record.items():
            col_name = sanitize_name(key)
            if isinstance(value, dict):
                # Store nested dict in a separate table
                nested_table = f"{sanitized_table}_{col_name}"
                nested_key = f"{sanitized_table}_id"
                create_or_update_table(conn, nested_table, value)
                insert_data(conn, nested_table, {nested_key: record.get(primary_key, None), **value})
                continue
            elif isinstance(value, list):
                # Store lists in a separate table with relationships
                nested_table = f"{sanitized_table}_{col_name}"
                nested_key = f"{sanitized_table}_id"
                create_or_update_table(conn, nested_table, {nested_key: None, "value": None})
                for item in value:
                    insert_data(conn, nested_table, {nested_key: record.get(primary_key, None), "value": item})
                continue
            else:
                keys.append(col_name)
                values.append(json.dumps(value) if isinstance(value, (dict, list)) else value)

        if keys:
            columns = ", ".join(f'"{k}"' for k in keys)
            placeholders = ", ".join("?" for _ in keys)
            query = f'INSERT OR REPLACE INTO "{sanitized_table}" ({columns}) VALUES ({placeholders})'
            if debug: print(f"[DEBUG] Inserting: {query} | Values: {values}")
            conn.execute(query, values)

    # Convert JSON file path to dict if a string is passed
    if isinstance(json_data, str) and os.path.exists(json_data):
        with open(json_data, "r", encoding="utf-8") as f:
            json_data = json.load(f)

    if not isinstance(json_data, (list, dict)):
        raise ValueError("JSON data must be a dictionary or a list of dictionaries.")

    # Ensure data is a list of records
    records = json_data if isinstance(json_data, list) else [json_data]

    # Open database connection
    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")  # Enable foreign key support

        # Create or update table
        if records:
            create_or_update_table(conn, table_name, records[0])

       
