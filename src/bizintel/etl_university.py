"""
etl_university.py

Extract, transform, and load university records
into DuckDB warehouse.

Source:
    data/raw/university_records.csv

Target:
    artifacts/university_records.duckdb
"""

from pathlib import Path

import duckdb
import pandas as pd

RAW_FILE = Path("data/raw/university_records.csv")

DW_FILE = Path("artifacts/university_records.duckdb")


def extract() -> pd.DataFrame:
    """Extract raw university data."""

    return pd.read_csv(RAW_FILE)


def transform_students(df: pd.DataFrame) -> pd.DataFrame:
    """Create student dimension."""

    return df[
        [
            "StudentID",
            "StudentName",
            "Major",
            "StudentEnrollmentDate",
        ]
    ].drop_duplicates()


def transform_courses(df: pd.DataFrame) -> pd.DataFrame:
    """Create course dimension."""

    return df[
        [
            "CourseID",
            "CourseName",
            "Department",
            "CreditHours",
        ]
    ].drop_duplicates()


def transform_instructors(df: pd.DataFrame) -> pd.DataFrame:
    """Create instructor dimension."""

    return df[
        [
            "InstructorID",
            "InstructorName",
        ]
    ].drop_duplicates()


def transform_semesters(df: pd.DataFrame) -> pd.DataFrame:
    """Create semester dimension."""

    semesters = df[["Semester"]].drop_duplicates().reset_index(drop=True)

    semesters["SemesterID"] = semesters.index + 1

    semesters["Year"] = 2024

    return semesters[
        [
            "SemesterID",
            "Semester",
            "Year",
        ]
    ]


def transform_enrollments(
    df: pd.DataFrame,
    semesters: pd.DataFrame,
) -> pd.DataFrame:
    """Create enrollment fact."""

    fact = df[
        [
            "EnrollmentID",
            "EnrollmentDate",
            "StudentID",
            "CourseID",
            "InstructorID",
            "Semester",
            "Grade",
        ]
    ].copy()

    fact = fact.merge(
        semesters,
        on="Semester",
        how="left",
    )

    fact = fact.drop(columns=["Semester"])

    return fact[
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


def load(
    students,
    courses,
    instructors,
    semesters,
    enrollments,
):
    """Load warehouse tables."""

    conn = duckdb.connect(str(DW_FILE))

    students.to_sql(
        "dim_students",
        conn,
        if_exists="append",
        index=False,
    )

    courses.to_sql(
        "dim_courses",
        conn,
        if_exists="append",
        index=False,
    )

    instructors.to_sql(
        "dim_instructors",
        conn,
        if_exists="append",
        index=False,
    )

    semesters.to_sql(
        "dim_semesters",
        conn,
        if_exists="append",
        index=False,
    )

    enrollments.to_sql(
        "fact_enrollments",
        conn,
        if_exists="append",
        index=False,
    )

    conn.close()


def main():
    df = extract()

    students = transform_students(df)
    courses = transform_courses(df)
    instructors = transform_instructors(df)
    semesters = transform_semesters(df)

    enrollments = transform_enrollments(
        df,
        semesters,
    )

    load(
        students,
        courses,
        instructors,
        semesters,
        enrollments,
    )


if __name__ == "__main__":
    main()
