"""dw_create_university.py

Create a University Records star schema data warehouse using DuckDB.

This project is based on the dw_create_case.py example but uses a custom
University Records dataset.

Dataset:
    data/raw/university_records.csv

Author: Ralph Massaquoi
Date: 2026-07

Development:
    - Drops and recreates warehouse tables for development testing.
    - This creates a clean warehouse each time.
    - Production systems should use migrations instead.


Process:
    - Create artifacts/ folder if needed.
    - Connect to DuckDB warehouse.
    - Drop existing tables.
    - Create dimension tables:
        - dim_students
        - dim_courses
        - dim_instructors
        - dim_semesters
    - Create fact table:
        - fact_enrollments
    - Verify schema.


Dataset Source:
    data/raw/university_records.csv
Output:
    artifacts/university_records.duckdb

Run:

    uv run python -m bizintel.dw_create_university
"""

from pathlib import Path
from typing import Final

from datafun_toolkit.logger import log_path
import duckdb

from bizintel.utils_logger import LOG, log_header

# --------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------

# DuckDB warehouse file

DW_FILE: Final[Path] = Path("artifacts/university_records.duckdb")

# ============================================================
# Section 2. Create Dimension Tables
# ============================================================

DW_FILE: Final[Path] = Path("artifacts/university_records.duckdb")

# --------------------------------------------------------------------
# Students Dimension
# --------------------------------------------------------------------


def create_dim_students(conn: duckdb.DuckDBPyConnection) -> None:
    """Create the students dimension table."""

    LOG.info("Creating dim_students...")

    conn.execute("DROP TABLE IF EXISTS dim_students")

    conn.execute("""
        CREATE TABLE dim_students (
            StudentID INTEGER PRIMARY KEY,
            StudentName VARCHAR,
            Major VARCHAR,
            StudentEnrollmentDate DATE
        )
    """)

    LOG.info("dim_students created.")


# --------------------------------------------------------------------
# Courses Dimension
# --------------------------------------------------------------------


def create_dim_courses(conn: duckdb.DuckDBPyConnection) -> None:
    """Create the courses dimension table."""

    LOG.info("Creating dim_courses...")

    conn.execute("DROP TABLE IF EXISTS dim_courses")

    conn.execute("""
        CREATE TABLE dim_courses (
            CourseID INTEGER PRIMARY KEY,
            CourseName VARCHAR,
            Department VARCHAR,
            CreditHours INTEGER
        )
    """)

    LOG.info("dim_courses created.")


# ------------------------------------------------------------
# Create dim_instructors
# ------------------------------------------------------------
# --------------------------------------------------------------------
# Instructors Dimension
# --------------------------------------------------------------------


def create_dim_instructors(conn: duckdb.DuckDBPyConnection) -> None:
    """Create the instructors dimension table."""

    LOG.info("Creating dim_instructors...")

    conn.execute("DROP TABLE IF EXISTS dim_instructors")

    conn.execute("""
        CREATE TABLE dim_instructors (
    InstructorID INTEGER PRIMARY KEY,
    InstructorName VARCHAR
)
    """)

    LOG.info("dim_instructors created.")


# --------------------------------------------------------------------
# Semesters Dimension
# --------------------------------------------------------------------


def create_dim_semesters(conn: duckdb.DuckDBPyConnection) -> None:
    """Create the semesters dimension table."""

    LOG.info("START create semesters dimension table....")

    # Drop the table in case it already exists
    conn.execute(
        """
        DROP TABLE IF EXISTS dim_semesters
        """
    )

    # Create the table
    conn.execute(
        """
        CREATE TABLE dim_semesters (
            SemesterID INTEGER PRIMARY KEY,
            Semester VARCHAR,
            Year INTEGER
        )
        """
    )

    LOG.info("dim_semesters created.")


# ============================================================
# Section 3. Create Fact Table
# ============================================================


# --------------------------------------------------------------------
# Enrollment Fact Table
# --------------------------------------------------------------------


def create_fact_enrollments(conn: duckdb.DuckDBPyConnection) -> None:
    """Create the enrollment fact table."""

    LOG.info("Creating fact_enrollments...")

    conn.execute("DROP TABLE IF EXISTS fact_enrollments")

    conn.execute("""
        CREATE TABLE fact_enrollments (

            EnrollmentID INTEGER PRIMARY KEY,

            EnrollmentDate DATE,

            StudentID INTEGER
                REFERENCES dim_students(StudentID),

            CourseID INTEGER
                REFERENCES dim_courses(CourseID),

            InstructorID INTEGER
                REFERENCES dim_instructors(InstructorID),

            SemesterID INTEGER
                REFERENCES dim_semesters(SemesterID),

            Grade VARCHAR
        )
    """)

    LOG.info("fact_enrollments created.")


# ============================================================
# Section 4. Delete Tables
# ============================================================


def delete_tables(conn: duckdb.DuckDBPyConnection) -> None:
    """Delete all warehouse tables in reverse dependency order."""

    LOG.info("Deleting existing warehouse tables...")

    conn.execute("DROP TABLE IF EXISTS fact_enrollments")
    conn.execute("DROP TABLE IF EXISTS dim_semesters")
    conn.execute("DROP TABLE IF EXISTS dim_instructors")
    conn.execute("DROP TABLE IF EXISTS dim_courses")
    conn.execute("DROP TABLE IF EXISTS dim_students")

    LOG.info("All existing tables deleted.")


# --------------------------------------------------------------------
# Verify Schema
# --------------------------------------------------------------------


def verify_schema(conn: duckdb.DuckDBPyConnection) -> None:
    """Verify warehouse tables."""

    LOG.info("Verifying warehouse schema...")

    tables = conn.execute("SHOW TABLES").fetchall()

    LOG.info(f"Tables in warehouse: {[table[0] for table in tables]}")


# ============================================================
# Section 6. Main Function
# ============================================================

# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------


def main() -> None:
    """Create the University Records data warehouse."""

    log_header(LOG, "University BI")

    LOG.info("========================")
    LOG.info("START create warehouse")
    LOG.info("========================")

    log_path(LOG, "Data warehouse:", DW_FILE)

    # Create artifacts folder if needed
    DW_FILE.parent.mkdir(parents=True, exist_ok=True)

    LOG.info("Connecting to DuckDB warehouse...")

    conn = duckdb.connect(str(DW_FILE))

    # Build warehouse
    delete_tables(conn)

    create_dim_students(conn)
    create_dim_courses(conn)
    create_dim_instructors(conn)
    create_dim_semesters(conn)

    create_fact_enrollments(conn)

    verify_schema(conn)

    conn.close()

    LOG.info("========================")
    LOG.info("University warehouse created successfully.")
    LOG.info("========================")


# --------------------------------------------------------------------
# Execution Guard
# --------------------------------------------------------------------

if __name__ == "__main__":
    main()
