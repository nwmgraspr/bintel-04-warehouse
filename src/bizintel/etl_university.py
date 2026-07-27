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

from bizintel.utils_logger import LOG, log_header

# === CONSTANTS ===

DATA_RAW: Final[Path] = Path("data/raw")

UNIVERSITY_DATA: Final[Path] = DATA_RAW / "university_records.csv"

DW_FILE: Final[Path] = Path("artifacts/university_records.duckdb")


# === Section 2. Define reusable functions ===


def verify_row_count(
    conn: duckdb.DuckDBPyConnection,
    table: str,
    expected: int,
) -> None:
    """Verify table row count."""

    result = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()

    actual = int(result[0]) if result else 0

    if actual == expected:
        LOG.info(f"  PASS: {table} has {actual} rows")
    else:
        LOG.warning(f"  FAIL: {table} expected {expected}, got {actual}")


# === LOAD DIMENSION TABLES ===
# === LOAD DIMENSION TABLES ===


def load_students(
    conn: duckdb.DuckDBPyConnection,
    df: pd.DataFrame,
) -> None:
    """Load students dimension."""

    LOG.info("Loading students into dim_students")

    conn.register(
        "students_df",
        df,
    )

    conn.execute("""
        INSERT INTO dim_students
        SELECT
            StudentID,
            StudentName,
            Major,
            StudentEnrollmentDate
        FROM students_df
    """)

    LOG.info(f"  Loaded {df.shape[0]} rows into dim_students")


def load_courses(
    conn: duckdb.DuckDBPyConnection,
    df: pd.DataFrame,
) -> None:
    """Load courses dimension."""

    LOG.info("Loading courses into dim_courses")

    conn.register(
        "courses_df",
        df,
    )

    conn.execute("""
        INSERT INTO dim_courses
        SELECT
            CourseID,
            CourseName,
            Department,
            CreditHours
        FROM courses_df
    """)

    LOG.info(f"  Loaded {df.shape[0]} rows into dim_courses")


def load_instructors(
    conn: duckdb.DuckDBPyConnection,
    df: pd.DataFrame,
) -> None:
    """Load instructors dimension."""

    LOG.info("Loading instructors into dim_instructors")

    conn.register(
        "instructors_df",
        df,
    )

    conn.execute("""
        INSERT INTO dim_instructors
        SELECT
            InstructorID,
            InstructorName
        FROM instructors_df
    """)

    LOG.info(f"  Loaded {df.shape[0]} rows into dim_instructors")


def load_semesters(
    conn: duckdb.DuckDBPyConnection,
    df: pd.DataFrame,
) -> None:
    """Load semesters dimension."""

    LOG.info("Loading semesters into dim_semesters")

    conn.register(
        "semesters_df",
        df,
    )

    conn.execute("""
        INSERT INTO dim_semesters
        SELECT
            SemesterID,
            Semester,
            Year
        FROM semesters_df
    """)

    LOG.info(f"  Loaded {df.shape[0]} rows into dim_semesters")


# === LOAD FACT TABLE ===


def load_enrollments(
    conn: duckdb.DuckDBPyConnection,
    df: pd.DataFrame,
) -> None:
    """Load enrollment fact table."""

    LOG.info("Loading enrollments into fact_enrollments")

    conn.register(
        "enrollments_df",
        df,
    )

    conn.execute("""
        INSERT INTO fact_enrollments
        SELECT
            EnrollmentID,
            EnrollmentDate,
            StudentID,
            CourseID,
            InstructorID,
            SemesterID,
            Grade
        FROM enrollments_df
    """)

    LOG.info(f"  Loaded {df.shape[0]} rows into fact_enrollments")


# === MAIN FUNCTION ===


def main() -> None:
    """Run university ETL process."""

    log_header(LOG, "BI")

    LOG.info("========================")
    LOG.info("START UNIVERSITY ETL")
    LOG.info("========================")

    LOG.info("Reading university source data...")

    df = pd.read_csv(UNIVERSITY_DATA)

    LOG.info("Transforming university data...")

    students = df[
        [
            "StudentID",
            "StudentName",
            "Major",
            "StudentEnrollmentDate",
        ]
    ].drop_duplicates()

    students["StudentEnrollmentDate"] = pd.to_datetime(
        students["StudentEnrollmentDate"],
        errors="coerce",
    )

    courses = df[
        [
            "CourseID",
            "CourseName",
            "Department",
            "CreditHours",
        ]
    ].drop_duplicates()

    # Instructors dimension
    instructors = df[
        [
            "InstructorID",
            "InstructorName",
        ]
    ].drop_duplicates()

    # Semesters dimension
    semesters = (
        df[
            [
                "Semester",
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    semesters["SemesterID"] = semesters.index + 1

    semesters["Year"] = semesters["Semester"].str.extract(r"(\d{4})").astype(int)

    semesters = semesters[
        [
            "SemesterID",
            "Semester",
            "Year",
        ]
    ]

    # Enrollment fact table
    enrollments = df.merge(
        semesters[
            [
                "Semester",
                "SemesterID",
            ]
        ],
        on="Semester",
        how="left",
    )

    enrollments["EnrollmentDate"] = pd.to_datetime(
        enrollments["EnrollmentDate"],
        errors="coerce",
    )

    enrollments = enrollments[
        [
            "EnrollmentID",
            "EnrollmentDate",
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

    # Connect to DuckDB warehouse

    LOG.info("Connecting to DuckDB warehouse...")

    conn = duckdb.connect(str(DW_FILE))
    # Load dimension tables first

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

    # Load fact table last

    load_enrollments(
        conn,
        enrollments,
    )
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
    LOG.info("University ETL completed successfully.")
    LOG.info("========================")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    main()
