"""dw_create_university.py - custom project.

Creates a University Records star schema data warehouse using DuckDB.

This project combines SQL and Python - two key skills for BI development.
It demonstrates recreating an empty star schema data warehouse.

After calling this file, run:
    etl_university.py

to load data from:
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


Run from project root:

    uv run python -m bizintel.dw_create_university
"""


# ============================================================
# Section 1. Imports and Constants
# ============================================================


from pathlib import Path
from typing import Final

import duckdb

from datafun_toolkit.logger import log_path
from bizintel.utils_logger import LOG, log_header


# DuckDB warehouse file

DW_FILE: Final[Path] = Path(
    "artifacts/university_records.duckdb"
)

# ============================================================
# Section 2. Create Dimension Tables
# ============================================================


# ------------------------------------------------------------
# Create dim_students
# ------------------------------------------------------------

def create_dim_students(conn: duckdb.DuckDBPyConnection) -> None:
    """Create the students dimension table.

    WHY:
        The student dimension stores descriptive information
        about university students.

    Source columns:
        StudentID
        StudentName
        Major
        StudentEnrollmentDate

    Args:
        conn:
            Active DuckDB connection.

    Returns:
        None
    """

    LOG.info("START create students dimension table....")

    LOG.info("DROP dim_students if it already exists")

    conn.execute("""
        DROP TABLE IF EXISTS dim_students
    """)

    LOG.info("CREATE dim_students table")

    conn.execute("""
        CREATE TABLE dim_students (
            StudentID INTEGER PRIMARY KEY,
            StudentName VARCHAR,
            Major VARCHAR,
            StudentEnrollmentDate DATE
        )
    """)

    LOG.info("dim_students created.")



# ------------------------------------------------------------
# Create dim_courses
# ------------------------------------------------------------

def create_dim_courses(conn: duckdb.DuckDBPyConnection) -> None:
    """Create the courses dimension table.

    WHY:
        The course dimension stores descriptive information
        about university courses.

    Source columns:
        CourseID
        CourseName
        Department
        CreditHours

    Args:
        conn:
            Active DuckDB connection.

    Returns:
        None
    """

    LOG.info("START create courses dimension table....")

    LOG.info("DROP dim_courses if it already exists")

    conn.execute("""
        DROP TABLE IF EXISTS dim_courses
    """)

    LOG.info("CREATE dim_courses table")

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

def create_dim_instructors(conn: duckdb.DuckDBPyConnection) -> None:
    """Create the instructors dimension table.

    WHY:
        The instructor dimension stores instructor identifiers
        associated with course enrollments.

    Source columns:
        InstructorID

    Args:
        conn:
            Active DuckDB connection.

    Returns:
        None
    """

    LOG.info("START create instructors dimension table....")

    LOG.info("DROP dim_instructors if it already exists")

    conn.execute("""
        DROP TABLE IF EXISTS dim_instructors
    """)

    LOG.info("CREATE dim_instructors table")

    conn.execute("""
        CREATE TABLE dim_instructors (
            InstructorID INTEGER PRIMARY KEY
        )
    """)

    LOG.info("dim_instructors created.")



# ------------------------------------------------------------
# Create dim_semesters
# ------------------------------------------------------------

def create_dim_semesters(conn: duckdb.DuckDBPyConnection) -> None:
    """Create the semesters dimension table.

    WHY:
        The semester dimension allows analysis by academic term.

    The raw dataset contains values such as:
        Spring 2025
        Summer 2024
        Fall 2024

    These are separated into:
        Semester
        Year

    Args:
        conn:
            Active DuckDB connection.

    Returns:
        None
    """

    LOG.info("START create semesters dimension table....")

    LOG.info("DROP dim_semesters if it already exists")

    conn.execute("""
        DROP TABLE IF EXISTS dim_semesters
    """)

    LOG.info("CREATE dim_semesters table")

    conn.execute("""
        CREATE TABLE dim_semesters (
            SemesterID INTEGER PRIMARY KEY,
            Semester VARCHAR,
            Year INTEGER
        )
    """)

    LOG.info("dim_semesters created.")

# ============================================================
# Section 3. Create Fact Table
# ============================================================


def create_fact_enrollments(conn: duckdb.DuckDBPyConnection) -> None:
    """Create the enrollment fact table.

    WHY:
        The fact table is the center of the university
        star schema.

        Each row represents one student enrollment
        in one course during one semester.

    Source columns:
        EnrollmentID
        EnrollmentDate
        StudentID
        CourseID
        InstructorID
        Semester
        Grade

    Args:
        conn:
            Active DuckDB connection.

    Returns:
        None
    """

    LOG.info("START create enrollments fact table....")

    LOG.info("DROP fact_enrollments if it already exists")

    conn.execute("""
        DROP TABLE IF EXISTS fact_enrollments
    """)

    LOG.info("CREATE fact_enrollments table")

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
    """Delete all warehouse tables.

    WHY:
        Drops tables in reverse dependency order.
        Fact tables are removed before dimensions
        because they contain foreign keys.

    Args:
        conn:
            Active DuckDB connection.

    Returns:
        None
    """

    LOG.info("START delete tables....")

    LOG.info("DROP fact_enrollments")

    conn.execute("""
        DROP TABLE IF EXISTS fact_enrollments
    """)


    LOG.info("DROP dim_semesters")

    conn.execute("""
        DROP TABLE IF EXISTS dim_semesters
    """)


    LOG.info("DROP dim_instructors")

    conn.execute("""
        DROP TABLE IF EXISTS dim_instructors
    """)


    LOG.info("DROP dim_courses")

    conn.execute("""
        DROP TABLE IF EXISTS dim_courses
    """)


    LOG.info("DROP dim_students")

    conn.execute("""
        DROP TABLE IF EXISTS dim_students
    """)


    LOG.info("All tables deleted.")



# ============================================================
# Section 5. Verify Schema
# ============================================================


def verify_schema(conn: duckdb.DuckDBPyConnection) -> None:
    """Verify warehouse tables were created.

    WHY:
        Confirms that the schema creation completed
        successfully.

    Args:
        conn:
            Active DuckDB connection.

    Returns:
        None
    """

    LOG.info("START verify warehouse schema....")


    tables = conn.execute(
        "SHOW TABLES"
    ).fetchall()


    LOG.info(
        f"Tables in warehouse: {[table[0] for table in tables]}"
    )

# ============================================================
# Section 6. Main Function
# ============================================================


def main() -> None:
    """Main function to create the University Records warehouse."""

    log_header(LOG, "BI")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")


    log_path(
        LOG,
        "Data warehouse:",
        DW_FILE
    )


    LOG.info(
        "Create artifacts folder if it does not exist"
    )

    DW_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    LOG.info(
        "Connect to DuckDB warehouse"
    )

    conn: duckdb.DuckDBPyConnection = duckdb.connect(
        str(DW_FILE)
    )


    LOG.info(
        "Delete existing tables"
    )

    delete_tables(conn)


    LOG.info(
        "Create dim_students"
    )

    create_dim_students(conn)


    LOG.info(
        "Create dim_courses"
    )

    create_dim_courses(conn)


    LOG.info(
        "Create dim_instructors"
    )

    create_dim_instructors(conn)


    LOG.info(
        "Create dim_semesters"
    )

    create_dim_semesters(conn)


    LOG.info(
        "Create fact_enrollments"
    )

    create_fact_enrollments(conn)


    LOG.info(
        "Verify warehouse schema"
    )

    verify_schema(conn)


    conn.close()


    LOG.info("========================")
    LOG.info(
        "University warehouse creation complete"
    )
    LOG.info("========================")



# ============================================================
# Conditional Execution Guard
# ============================================================


if __name__ == "__main__":
    main()
