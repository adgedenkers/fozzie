import sqlite3
import os
from pathlib import Path

DEFAULT_DB_PATH = "c:/src/fozzie"

class VersionManager:
    def __init__(self, db_path=None):
        self.db_path = db_path or os.path.join(DEFAULT_DB_PATH, "fozzie.db")
        self.db_name = os.path.basename(self.db_path)
        self.conn = self._get_db_connection()

    def _get_db_connection(self):
        init_needed = not os.path.exists(self.db_path)
        conn = sqlite3.connect(self.db_path)
        if init_needed:
            self.initialize_db(conn)
        return conn

    def initialize_db(self, conn):
        conn.execute("""
            CREATE TABLE IF NOT EXISTS db (
                name TEXT NOT NULL,
                path TEXT NOT NULL,
                version REAL NOT NULL CHECK(version >= 0)
            );
        """)
        conn.execute("""
            INSERT INTO db (name, path, version)
            VALUES (?, ?, ?);
        """, (self.db_name, os.path.dirname(self.db_path), 0.7))
        conn.commit()

    def increment_minor(self):
        self.conn.execute("""
            UPDATE db
            SET version = 
                CAST(CAST(version AS INT) AS REAL) + ROUND((version - CAST(version AS INT)) + 0.1, 1)
            WHERE name = ?;
        """, (self.db_name,))
        self.conn.commit()

    def increment_major(self):
        self.conn.execute("""
            UPDATE db
            SET version = CAST(CAST(version AS INT) + 1 AS REAL)
            WHERE name = ?;
        """, (self.db_name,))
        self.conn.commit()

    def get_version(self):
        cur = self.conn.execute("SELECT version FROM db WHERE name = ?;", (self.db_name,))
        row = cur.fetchone()
        return row[0] if row else None

    def get_version_row(self):
        cur = self.conn.execute("SELECT * FROM db;")
        return cur.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()

    @staticmethod
    def create_new_database(db_path: str, initial_version: float = 0.1):
        """Creates a new SQLite DB with the version table set to a starting version (default: 0.1)."""
        if os.path.exists(db_path):
            raise FileExistsError(f"Database already exists at: {db_path}")
        
        db_name = os.path.basename(db_path)
        conn = sqlite3.connect(db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS db (
                name TEXT NOT NULL,
                path TEXT NOT NULL,
                version REAL NOT NULL CHECK(version >= 0)
            );
        """)
        conn.execute("""
            INSERT INTO db (name, path, version)
            VALUES (?, ?, ?);
        """, (db_name, os.path.dirname(db_path), initial_version))
        conn.commit()
        conn.close()




# import sqlite3
# import os
# from pathlib import Path

# DB_NAME = "fozzie.db"
# DEFAULT_DB_PATH = "c:/src/fozzie"

# class VersionManager:
#     def __init__(self, db_path=None):
#         self.db_path = db_path or os.path.join(DEFAULT_DB_PATH, DB_NAME)
#         self.conn = self._get_db_connection()

#     def _get_db_connection(self):
#         init_needed = not os.path.exists(self.db_path)
#         conn = sqlite3.connect(self.db_path)
#         if init_needed:
#             self.initialize_db(conn)
#         return conn

#     def initialize_db(self, conn):
#         conn.execute("""
#             CREATE TABLE IF NOT EXISTS db (
#                 name TEXT NOT NULL,
#                 path TEXT NOT NULL,
#                 version REAL NOT NULL CHECK(version >= 0)
#             );
#         """)
#         conn.execute("""
#             INSERT INTO db (name, path, version)
#             VALUES (?, ?, ?);
#         """, (DB_NAME, DEFAULT_DB_PATH, 0.7))
#         conn.commit()

#     def increment_minor(self):
#         self.conn.execute("""
#             UPDATE db
#             SET version = 
#                 CAST(CAST(version AS INT) AS REAL) + ROUND((version - CAST(version AS INT)) + 0.1, 1)
#             WHERE name = ?;
#         """, (DB_NAME,))
#         self.conn.commit()

#     def increment_major(self):
#         self.conn.execute("""
#             UPDATE db
#             SET version = CAST(CAST(version AS INT) + 1 AS REAL)
#             WHERE name = ?;
#         """, (DB_NAME,))
#         self.conn.commit()

#     def get_version(self):
#         cur = self.conn.execute("SELECT version FROM db WHERE name = ?;", (DB_NAME,))
#         row = cur.fetchone()
#         return row[0] if row else None

#     def close(self):
#         if self.conn:
#             self.conn.close()

#     @staticmethod
#     def create_new_database(db_path: str, initial_version: float = 0.1):
#         """Creates a new SQLite DB with the version table set to a starting version (default: 0.1)."""
#         if os.path.exists(db_path):
#             raise FileExistsError(f"Database already exists at: {db_path}")
        
#         conn = sqlite3.connect(db_path)
#         conn.execute("""
#             CREATE TABLE IF NOT EXISTS db (
#                 name TEXT NOT NULL,
#                 path TEXT NOT NULL,
#                 version REAL NOT NULL CHECK(version >= 0)
#             );
#         """)
#         conn.execute("""
#             INSERT INTO db (name, path, version)
#             VALUES (?, ?, ?);
#         """, (os.path.basename(db_path), os.path.dirname(db_path), initial_version))
#         conn.commit()
#         conn.close()
