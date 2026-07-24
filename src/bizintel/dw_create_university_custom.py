"""
dw_create_university_custom.py

An example that creates a university enrollment star schema
data warehouse using DuckDB.

This project combines SQL and Python - two key skills for BI development.
It demonstrates recreating an empty star schema data warehouse.

After calling this, call the etl_university_custom.py script
to load data into the warehouse.

Author: Your Name
Date: 2026-07

Development:
    This script is intended for development and testing purposes.
    - It drops and recreates the warehouse tables.
    - This ensures a clean slate for testing.
    - This approach is suitable for development but should be
      used carefully in production environments.

Process:
    - Create the artifacts/university folder if it does not exist.
    - Connect to the DuckDB university warehouse.
    - Drop existing tables if they exist.
    - Create dimension tables:
        - dim_students
        - dim_courses
    - Create the fact table:
        - fact_enrollments
    - Verify table creation.

Output:
    artifacts/university/university_registration.duckdb

Terminal command to run this file:

uv run python -m bizintel.dw_create_university_custom
"""

# ============================================================
# Section 1. Import dependencies
# ============================================================

from pathlib import Path
from typing import Final

from datafun_toolkit.logger import log_path
import duckdb

from bizintel.utils_logger import LOG, log_header

# ============================================================
# Constants
# ============================================================

DW_FILE: Final[Path] = Path("artifacts/university_registration.duckdb")

# ============================================================
# Create Student Dimension
# ============================================================


def create_dim_students(
    conn: duckdb.DuckDBPyConnection,
) -> None:
    """
    Create the Students dimension table.
    """

    LOG.info("START create students dimension table....")

    LOG.info("Dropping existing table if necessary")

    conn.execute("""
        DROP TABLE IF EXISTS dim_students
    """)

    LOG.info("Creating dim_students table")

    conn.execute("""
        CREATE TABLE dim_students (

            StudentID INTEGER PRIMARY KEY,

            StudentName VARCHAR,

            Major VARCHAR,

            EnrollmentDate DATE

        )
    """)
    # ============================================================


# Create Course Dimension
# ============================================================


def create_dim_courses(
    conn: duckdb.DuckDBPyConnection,
) -> None:
    """
    Create the Courses dimension table.
    """

    LOG.info("START create courses dimension table....")

    LOG.info("Dropping existing table if necessary")

    conn.execute("""
        DROP TABLE IF EXISTS dim_courses
    """)

    LOG.info("Creating dim_courses table")

    conn.execute("""
        CREATE TABLE dim_courses (

            CourseID INTEGER PRIMARY KEY,

            CourseName VARCHAR,

            Department VARCHAR,

            CreditHours INTEGER

        )
    """)

    LOG.info("dim_courses created.")

    LOG.info("dim_students created.")
    # ============================================================


# Create Enrollment Fact Table
# ============================================================


def create_fact_enrollments(
    conn: duckdb.DuckDBPyConnection,
) -> None:
    """
    Create the Enrollments fact table.
    """

    LOG.info("START create enrollments fact table....")

    LOG.info("Dropping existing table if necessary")

    conn.execute("""
        DROP TABLE IF EXISTS fact_enrollments
    """)

    LOG.info("Creating fact_enrollments table")

    conn.execute("""
        CREATE TABLE fact_enrollments (

            EnrollmentID INTEGER PRIMARY KEY,

            EnrollmentDate DATE,

            StudentID INTEGER
                REFERENCES dim_students(StudentID),

            CourseID INTEGER
                REFERENCES dim_courses(CourseID),

            Semester VARCHAR,

            InstructorID INTEGER,

            Grade VARCHAR

        )
    """)

    LOG.info("fact_enrollments created.")
    # ============================================================


# Delete Existing Tables
# ============================================================


def delete_tables(
    conn: duckdb.DuckDBPyConnection,
) -> None:
    """
    Delete all warehouse tables.
    """

    LOG.info("Deleting old tables...")

    conn.execute("""
        DROP TABLE IF EXISTS fact_enrollments
    """)

    conn.execute("""
        DROP TABLE IF EXISTS dim_courses
    """)

    conn.execute("""
        DROP TABLE IF EXISTS dim_students
    """)

    LOG.info("Tables deleted.")
    # ============================================================


# Verify Warehouse
# ============================================================


def verify_schema(
    conn: duckdb.DuckDBPyConnection,
) -> None:
    """
    Verify warehouse schema.
    """

    LOG.info("Verifying schema...")

    tables = conn.execute("SHOW TABLES").fetchall()

    LOG.info(f"Tables in warehouse: {[t[0] for t in tables]}")
    # ============================================================


# Main
# ============================================================


def main() -> None:

    log_header(LOG, "BI")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    log_path(LOG, "Data warehouse:", DW_FILE)

    DW_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    LOG.info("Connecting to DuckDB...")

    conn = duckdb.connect(str(DW_FILE))

    delete_tables(conn)

    create_dim_students(conn)

    create_dim_courses(conn)

    create_fact_enrollments(conn)

    verify_schema(conn)

    conn.close()

    LOG.info("Workflow complete.")

    LOG.info("========================")
    LOG.info("Executed successfully!")
    LOG.info("========================")


if __name__ == "__main__":
    main()
