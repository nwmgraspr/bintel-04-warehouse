"""etl_university.py - load university data warehouse.

Loads prepared university data into a DuckDB data warehouse.
This process is called ETL (Extract, Transform, Load).

Before this, run:
    uv run python -m bizintel.dw_create_university

Process:
    - Connect to the DuckDB data warehouse.
    - Extract university CSV data.
    - Transform data to match warehouse schema.
    - Load dimension tables.
    - Load fact table after dimensions.
    - Verify row counts.

Data Source:
- data/raw/university_records.csv

Output:
- artifacts/university_records.duckdb (populated)

Terminal command:

uv run python -m bizintel.etl_university
"""

# === Section 1. Import dependencies and set up constants ===

from pathlib import Path
from typing import Final

import duckdb
import pandas as pd

from datafun_toolkit.logger import log_path

from bizintel.utils_logger import LOG, log_header


# === CONSTANTS ===

DATA_RAW: Final[Path] = Path("data/raw")

UNIVERSITY_DATA: Final[Path] = (
    DATA_RAW / "university_records.csv"
)

DW_FILE: Final[Path] = (
    Path("artifacts/university_records.duckdb")
)


# === Section 2. Define reusable functions ===


def verify_row_count(
    conn: duckdb.DuckDBPyConnection,
    table: str,
    expected: int,
) -> None:
    """Verify table row count."""

    result = conn.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()

    actual = int(result[0]) if result else 0

    if actual == expected:
        LOG.info(
            f"  PASS: {table} has {actual} rows"
        )
    else:
        LOG.warning(
            f"  FAIL: {table} expected {expected}, got {actual}"
        )


# === LOAD DIMENSION TABLES ===


def load_students(
    conn: duckdb.DuckDBPyConnection,
    df: pd.DataFrame,
) -> None:
    """Load students dimension."""

    LOG.info("Loading students into dim_students")

    conn.execute("""
        INSERT INTO dim_students
        SELECT
            StudentID,
            StudentName,
            Major,
            EnrollmentYear
        FROM df
    """)

    LOG.info(
        f"  Loaded {df.shape[0]} rows into dim_students"
    )


def load_courses(
    conn: duckdb.DuckDBPyConnection,
    df: pd.DataFrame,
) -> None:
    """Load courses dimension."""

    LOG.info("Loading courses into dim_courses")

    conn.execute("""
        INSERT INTO dim_courses
        SELECT
            CourseID,
            CourseName,
            Department,
            Credits
        FROM df
    """)

    LOG.info(
        f"  Loaded {df.shape[0]} rows into dim_courses"
    )


def load_instructors(
    conn: duckdb.DuckDBPyConnection,
    df: pd.DataFrame,
) -> None:
    """Load instructors dimension."""

    LOG.info(
        "Loading instructors into dim_instructors"
    )

    conn.execute("""
        INSERT INTO dim_instructors
        SELECT
            InstructorID,
            InstructorName,
            Department
        FROM df
    """)

    LOG.info(
        f"  Loaded {df.shape[0]} rows into dim_instructors"
    )


def load_semesters(
    conn: duckdb.DuckDBPyConnection,
    df: pd.DataFrame,
) -> None:
    """Load semesters dimension."""

    LOG.info(
        "Loading semesters into dim_semesters"
    )

    conn.execute("""
        INSERT INTO dim_semesters
        SELECT
            SemesterID,
            SemesterName,
            Year
        FROM df
    """)

    LOG.info(
        f"  Loaded {df.shape[0]} rows into dim_semesters"
    )


# === LOAD FACT TABLE ===


def load_enrollments(
    conn: duckdb.DuckDBPyConnection,
    df: pd.DataFrame,
) -> None:
    """Load enrollment fact table."""

    LOG.info(
        "Loading enrollments into fact_enrollments"
    )

    conn.execute("""
        INSERT INTO fact_enrollments
        SELECT
            EnrollmentID,
            StudentID,
            CourseID,
            InstructorID,
            SemesterID,
            Grade
        FROM df
    """)

    LOG.info(
        f"  Loaded {df.shape[0]} rows into fact_enrollments"
    )


# === MAIN FUNCTION ===


def main() -> None:
    """Run university ETL process."""

    log_header(LOG, "BI")

    LOG.info("========================")
    LOG.info("START UNIVERSITY ETL")
    LOG.info("========================")

    log_path(
        LOG,
        "Input data:",
        UNIVERSITY_DATA,
    )

    log_path(
        LOG,
        "Data warehouse:",
        DW_FILE,
    )


    # Extract source data

    LOG.info(
        "Reading university source data..."
    )

    df = pd.read_csv(
        UNIVERSITY_DATA
    )


    LOG.info(
        f"Source rows: {df.shape[0]}"
    )


    # Transform

    LOG.info(
        "Transforming university data..."
    )

    students = (
        df[
            [
                "StudentID",
                "StudentName",
                "Major",
                "EnrollmentYear",
            ]
        ]
        .drop_duplicates()
    )

    courses = (
        df[
            [
                "CourseID",
                "CourseName",
                "Department",
                "Credits",
            ]
        ]
        .drop_duplicates()
    )

    instructors = (
        df[
            [
                "InstructorID",
                "InstructorName",
                "Department",
            ]
        ]
        .drop_duplicates()
    )

    semesters = (
        df[
            [
                "SemesterID",
                "SemesterName",
                "Year",
            ]
        ]
        .drop_duplicates()
    )

    enrollments = df[
        [
            "EnrollmentID",
            "StudentID",
            "CourseID",
            "InstructorID",
            "SemesterID",
            "Grade",
        ]
    ]


    LOG.info("========================")
    LOG.info("ROW COUNTS BEFORE LOAD")
    LOG.info("========================")

    LOG.info(
        f"Students: {students.shape[0]}"
    )

    LOG.info(
        f"Courses: {courses.shape[0]}"
    )

    LOG.info(
        f"Instructors: {instructors.shape[0]}"
    )

    LOG.info(
        f"Semesters: {semesters.shape[0]}"
    )

    LOG.info(
        f"Enrollments: {enrollments.shape[0]}"
    )


    # Connect

    LOG.info(
        "Connecting to DuckDB warehouse..."
    )

    conn = duckdb.connect(
        str(DW_FILE)
    )


    # Load dimensions first

    load_students(
        conn,
        students,
    )

    load_courses(
        conn,
        courses,
    )

    load_instructors(
        conn,
        instructors,
    )

    load_semesters(
        conn,
        semesters,
    )


    # Load fact last

    load_enrollments(
        conn,
        enrollments,
    )


    LOG.info("========================")
    LOG.info("ROW COUNTS AFTER LOAD")
    LOG.info("========================")


    verify_row_count(
        conn,
        "dim_students",
        students.shape[0],
    )

    verify_row_count(
        conn,
        "dim_courses",
        courses.shape[0],
    )

    verify_row_count(
        conn,
        "dim_instructors",
        instructors.shape[0],
    )

    verify_row_count(
        conn,
        "dim_semesters",
        semesters.shape[0],
    )

    verify_row_count(
        conn,
        "fact_enrollments",
        enrollments.shape[0],
    )


    conn.close()


    LOG.info("========================")
    LOG.info(
        "University ETL completed successfully."
    )
    LOG.info("========================")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    main()
