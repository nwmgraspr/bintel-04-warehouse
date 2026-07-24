"""
dw_create_university_custom.py

Creates a University Enrollment data warehouse using DuckDB.

This project combines SQL and Python to build a star schema data warehouse.
It recreates an empty warehouse for development and testing purposes.
Run this script before loading data with an ETL process.

Author: Ralph Massaquoi
Date: 2026

Development:
    - Drops existing warehouse tables.
    - Recreates all dimension and fact tables.
    - Verifies the schema after creation.

Star Schema:
    Dimension Tables
        - dim_students
        - dim_courses
        - dim_instructors

    Fact Table
        - fact_enrollments

Output:
    artifacts/university_dw.duckdb

Terminal command:

uv run python -m bizintel.dw_create_university_custom
"""
# ==========================
# IMPORTS
# ==========================

from pathlib import Path
from typing import Final

import duckdb
from datafun_toolkit.logger import log_path

from bizintel.utils_logger import LOG, log_header

# ==========================
# CONSTANTS
# ==========================

DW_FILE: Final[Path] = Path("artifacts/university_dw.duckdb")


# ==========================
# CREATE DIMENSION TABLES
# ==========================

def create_dim_students(conn: duckdb.DuckDBPyConnection) -> None:
    """Create student dimension table."""

    LOG.info("Creating dim_students...")

    conn.execute("DROP TABLE IF EXISTS dim_students")

    conn.execute("""
        CREATE TABLE dim_students (
            StudentID      INTEGER PRIMARY KEY,
            StudentName    VARCHAR,
            Major          VARCHAR,
            EnrollmentYear INTEGER
        )
    """)

    LOG.info("dim_students created.")


def create_dim_courses(conn: duckdb.DuckDBPyConnection) -> None:
    """Create course dimension table."""

    LOG.info("Creating dim_courses...")

    conn.execute("DROP TABLE IF EXISTS dim_courses")

    conn.execute("""
        CREATE TABLE dim_courses (
            CourseID      INTEGER PRIMARY KEY,
            CourseName    VARCHAR,
            Department    VARCHAR,
            CreditHours   INTEGER
        )
    """)

    LOG.info("dim_courses created.")


def create_dim_instructors(conn: duckdb.DuckDBPyConnection) -> None:
    """Create instructor dimension table."""

    LOG.info("Creating dim_instructors...")

    conn.execute("DROP TABLE IF EXISTS dim_instructors")

    conn.execute("""
        CREATE TABLE dim_instructors (
            InstructorID   INTEGER PRIMARY KEY,
            InstructorName VARCHAR,
            Department     VARCHAR,
            Rank           VARCHAR
        )
    """)

    LOG.info("dim_instructors created.")


# ==========================
# CREATE FACT TABLE
# ==========================

def create_fact_enrollments(conn: duckdb.DuckDBPyConnection) -> None:
    """Create enrollment fact table."""

    LOG.info("Creating fact_enrollments...")

    conn.execute("DROP TABLE IF EXISTS fact_enrollments")

    conn.execute("""
        CREATE TABLE fact_enrollments (
            EnrollmentID   INTEGER PRIMARY KEY,
            StudentID      INTEGER REFERENCES dim_students(StudentID),
            CourseID       INTEGER REFERENCES dim_courses(CourseID),
            InstructorID   INTEGER REFERENCES dim_instructors(InstructorID),
            Semester       VARCHAR,
            EnrollmentDate DATE,
            Grade          VARCHAR
        )
    """)

    LOG.info("fact_enrollments created.")


# ==========================
# DELETE TABLES
# ==========================

def delete_tables(conn: duckdb.DuckDBPyConnection) -> None:
    """Delete tables before recreating."""

    LOG.info("Deleting existing tables...")

    conn.execute("DROP TABLE IF EXISTS fact_enrollments")
    conn.execute("DROP TABLE IF EXISTS dim_instructors")
    conn.execute("DROP TABLE IF EXISTS dim_courses")
    conn.execute("DROP TABLE IF EXISTS dim_students")


# ==========================
# VERIFY SCHEMA
# ==========================

def verify_schema(conn: duckdb.DuckDBPyConnection) -> None:
    """Display warehouse tables."""

    tables = conn.execute("SHOW TABLES").fetchall()

    LOG.info("Warehouse Tables:")
    LOG.info([table[0] for table in tables])


# ==========================
# MAIN
# ==========================

def main() -> None:
    """Build University data warehouse."""

    log_header(LOG, "University BI")

    log_path(LOG, "Warehouse:", DW_FILE)

    DW_FILE.parent.mkdir(parents=True, exist_ok=True)

    conn = duckdb.connect(str(DW_FILE))

    delete_tables(conn)

    create_dim_students(conn)
    create_dim_courses(conn)
    create_dim_instructors(conn)
    create_fact_enrollments(conn)

    verify_schema(conn)

    conn.close()

    LOG.info("University data warehouse created successfully.")


# ==========================
# RUN PROGRAM
# ==========================

if __name__ == "__main__":
    main()
