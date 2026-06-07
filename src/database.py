import sqlite3
import os


class CompressionDatabase:

    DB_PATH = (
        "database/compression.db"
    )

    # ==================================================
    # Initialize Database
    # ==================================================

    @staticmethod
    def initialize():

        os.makedirs(
            "database",
            exist_ok=True
        )

        connection = sqlite3.connect(
            CompressionDatabase.DB_PATH
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS
            compression_history (

                id INTEGER PRIMARY KEY
                AUTOINCREMENT,

                operation TEXT,

                filename TEXT,

                original_size INTEGER,

                compressed_size INTEGER,

                ratio REAL,

                execution_time REAL
            )
            """
        )

        connection.commit()
        connection.close()

    # ==================================================
    # Save Record
    # ==================================================

    @staticmethod
    def save_record(
        operation,
        filename,
        original_size,
        compressed_size,
        ratio,
        execution_time
    ):

        connection = sqlite3.connect(
            CompressionDatabase.DB_PATH
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO
            compression_history (

                operation,
                filename,
                original_size,
                compressed_size,
                ratio,
                execution_time

            )

            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                operation,
                filename,
                original_size,
                compressed_size,
                ratio,
                execution_time
            )
        )

        connection.commit()
        connection.close()

    # ==================================================
    # Count Operations
    # ==================================================

    @staticmethod
    def compression_count():

        connection = sqlite3.connect(
            CompressionDatabase.DB_PATH
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM compression_history
            WHERE operation='Compression'
            """
        )

        count = cursor.fetchone()[0]

        connection.close()

        return count

    @staticmethod
    def decompression_count():

        connection = sqlite3.connect(
            CompressionDatabase.DB_PATH
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM compression_history
            WHERE operation='Decompression'
            """
        )

        count = cursor.fetchone()[0]

        connection.close()

        return count

    # ==================================================
    # Get All Records
    # ==================================================

    @staticmethod
    def get_all():

        connection = sqlite3.connect(
            CompressionDatabase.DB_PATH
        )

        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM compression_history
            ORDER BY id ASC
            """
        )

        rows = cursor.fetchall()

        connection.close()

        return [
            dict(row)
            for row in rows
        ]

    # ==================================================
    # Get Record By ID
    # ==================================================

    @staticmethod
    def get_by_id(record_id):

        connection = sqlite3.connect(
            CompressionDatabase.DB_PATH
        )

        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM compression_history
            WHERE id = ?
            """,
            (record_id,)
        )

        row = cursor.fetchone()

        connection.close()

        if row:

            return dict(row)

        return None

    # ==================================================
    # Delete Record
    # ==================================================

    @staticmethod
    def delete_record(record_id):

        connection = sqlite3.connect(
            CompressionDatabase.DB_PATH
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM
            compression_history
            WHERE id = ?
            """,
            (record_id,)
        )

        connection.commit()

        deleted = (
            cursor.rowcount > 0
        )

        connection.close()

        return deleted

    # ==================================================
    # Clear Entire History
    # ==================================================

    @staticmethod
    def clear_all():

        connection = sqlite3.connect(
            CompressionDatabase.DB_PATH
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM compression_history
            """
        )

        cursor.execute(
            """
            DELETE FROM sqlite_sequence
            WHERE name='compression_history'
            """
        )

        connection.commit()
        connection.close()

        return True

    # ==================================================
    # Statistics
    # ==================================================

    @staticmethod
    def statistics():

        connection = sqlite3.connect(
            CompressionDatabase.DB_PATH
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                COUNT(*),
                AVG(ratio),
                AVG(execution_time)
            FROM compression_history
            """
        )

        row = cursor.fetchone()

        connection.close()

        return {

            "total_compressions":
                CompressionDatabase.compression_count(),

            "total_decompressions":
                CompressionDatabase.decompression_count(),

            "average_ratio":
                round(
                    row[1] or 0,
                    2
                ),

            "average_execution_time":
                round(
                    row[2] or 0,
                    6
                )
        }

    # ==================================================
    # Top Compressions
    # ==================================================

    @staticmethod
    def top_compressions(limit=5):

        connection = sqlite3.connect(
            CompressionDatabase.DB_PATH
        )

        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM compression_history
            ORDER BY ratio DESC
            LIMIT ?
            """,
            (limit,)
        )

        rows = cursor.fetchall()

        connection.close()

        return [
            dict(row)
            for row in rows
        ]

    # ==================================================
    # Recent Compressions
    # ==================================================

    @staticmethod
    def recent(limit=5):

        connection = sqlite3.connect(
            CompressionDatabase.DB_PATH
        )

        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM compression_history
            ORDER BY id ASC
            LIMIT ?
            """,
            (limit,)
        )

        rows = cursor.fetchall()

        connection.close()

        return [
            dict(row)
            for row in rows
        ]

    # ==================================================
    # Search Records
    # ==================================================

    @staticmethod
    def search(filename):

        connection = sqlite3.connect(
            CompressionDatabase.DB_PATH
        )

        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM compression_history
            WHERE filename
            LIKE ?
            ORDER BY id DESC
            """,
            (f"%{filename}%",)
        )

        rows = cursor.fetchall()

        connection.close()

        return [
            dict(row)
            for row in rows
        ]

    # ==================================================
    # Dashboard Summary
    # ==================================================

    @staticmethod
    def dashboard():

        stats = (
            CompressionDatabase
            .statistics()
        )

        top = (
            CompressionDatabase
            .top_compressions(3)
        )

        recent = (
            CompressionDatabase
            .recent(3)
        )

        return {

            "statistics":
                stats,

            "top":
                top,

            "recent":
                recent
        }