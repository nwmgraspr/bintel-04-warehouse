"""
generate_university_dataset.py

Generate a raw university enrollment dataset for a Business Intelligence
data warehouse project.

This script creates a denormalized operational dataset that will later
be transformed into a star schema consisting of:

    • dim_students
    • dim_courses
    • fact_enrollments

The generated dataset serves as the source for the ETLV process.

Author: Your Name
Date: 2026-07

Development

    This script creates realistic sample university enrollment data.

    The output is written to

        data/raw/university_records.csv

    The generated file is later used by

        prepare_university_data.py

Output

    data/raw/university_records.csv

Terminal Command

uv run python -m bizintel.generate_university_dataset
"""

# ==========================================================
# SECTION 1
# Import libraries
# ==========================================================

import csv
from datetime import datetime, timedelta
from pathlib import Path
import random
from typing import Final

# ==========================================================
# CONSTANTS
# ==========================================================

OUTPUT_DIR: Final = Path("data/raw")

OUTPUT_FILE: Final = OUTPUT_DIR / "university_records.csv"

NUMBER_OF_RECORDS: Final = 100

random.seed(42)

# ==========================================================
# REFERENCE DATA
# ==========================================================

STUDENTS = [
    (1001, "Alice Johnson", "Computer Science"),
    (1002, "Bob Smith", "Business"),
    (1003, "Carol Davis", "Mathematics"),
    (1004, "David Wilson", "Engineering"),
    (1005, "Emma Thomas", "Biology"),
    (1006, "Frank Garcia", "Accounting"),
    (1007, "Grace Miller", "Economics"),
    (1008, "Henry Walker", "Nursing"),
    (1009, "Isabella Moore", "Psychology"),
    (1010, "Jack Anderson", "Computer Science"),
]

COURSES = [
    (101, "Database Systems", "Computer Science", 3),
    (102, "Programming I", "Computer Science", 4),
    (103, "Business Analytics", "Business", 3),
    (104, "Marketing Principles", "Business", 3),
    (105, "Calculus I", "Mathematics", 4),
    (106, "Linear Algebra", "Mathematics", 3),
    (107, "General Biology", "Biology", 4),
    (108, "Organic Chemistry", "Chemistry", 4),
    (109, "Engineering Mechanics", "Engineering", 4),
    (110, "Financial Accounting", "Accounting", 3),
]

INSTRUCTORS = [
    (501, "Dr. Adams"),
    (502, "Dr. Baker"),
    (503, "Dr. Carter"),
    (504, "Dr. Davis"),
    (505, "Dr. Evans"),
]

SEMESTERS = [
    (1, "Spring 2024"),
    (2, "Summer 2024"),
    (3, "Fall 2024"),
    (4, "Spring 2025"),
]

GRADES = [
    "A",
    "A-",
    "B+",
    "B",
    "B-",
    "C+",
    "C",
]

# ==========================================================
# SECTION 2
# Helper Functions
# ==========================================================

def create_students() -> dict:
    """ Create student records.

    students = {}

    for student_id, name, major in STUDENTS:
        students[student_id] = {
            "StudentID": student_id,
            "StudentName": name,
            "Major": major,
            "StudentEnrollmentDate": create_date(),
        }

    return students


def create_courses() -> dict:
    """
    Create course records.

    Returns:
        Dictionary containing courses.
    """

    courses = {}

    for course in COURSES:
        courses[course[0]] = {
            "CourseID": course[0],
            "CourseName": course[1],
            "Department": course[2],
            "CreditHours": course[3],
        }

    return courses

def create_instructors() -> dict:
    """Create instructor records.

    instructors = {}

    for instructor_id, instructor_name in INSTRUCTORS:
        instructors[instructor_id] = {
            "InstructorID": instructor_id,
            "InstructorName": instructor_name,
        }

    return instructors
    
def create_semesters() -> dict:
    """ Create semester records.

    semesters = {}

    for semester_id, semester_name in SEMESTERS:
        semesters[semester_id] = {
            "SemesterID": semester_id,
            "SemesterName": semester_name,
        }

    return semesters

def create_enrollment_date() -> str:
    """
    Create enrollment transaction date.def create_semesters() -> dict:
    """ Create semester records.

        semesters = {}

    for semester_id, semester_name in SEMESTERS:
        semesters[semester_id] = {
            "SemesterID": semester_id,
            "SemesterName": semester_name,
        }

    return semesters

 

    return create_date(
        2024,
        2025,
    )


# ==========================================================
# SECTION 3
# Generate Raw Enrollment Dataset
# ==========================================================


def create_raw_records(
    number_of_records: int,
) -> list[dict]:
    """
    Create raw university enrollment records.

    The raw dataset is intentionally denormalized.
    It combines student, course, and enrollment information
    into one operational-style table.

    This file will later be transformed into:

        dim_students
        dim_courses
        fact_enrollments

    Args:
        number_of_records:
            Number of enrollment records to create.

    Returns:
        List of raw enrollment dictionaries.
    """

    records = []

    students = create_students()

    courses = create_courses()

    instructors = create_instructors()

    semesters = create_semesters()

    for enrollment_id in range(
        1001,
        1001 + number_of_records,
    ):# Select random student

student = random.choice(
    list(students.values())
)


# Select random course

course = random.choice(
    list(courses.values())
)


# Select random instructor

instructor = random.choice(
    list(instructors.values())
)


# Select random semester

semester = random.choice(
    list(semesters.values())
)

        record = {
            "EnrollmentID": enrollment_id,
            "EnrollmentDate": create_enrollment_date(),
            "StudentID": student["StudentID"],
            "StudentName": student["StudentName"],
            "Major": student["Major"],
            "StudentEnrollmentDate": student["StudentEnrollmentDate"],
            "CourseID": course["CourseID"],
            "CourseName": course["CourseName"],
            "Department": course["Department"],
            "CreditHours": course["CreditHours"],
            "Semester": random.choice(SEMESTERS),
            "InstructorID": create_instructor_id(),
            "Grade": random.choice(GRADES),
        }

        records.append(record)

    return records


def write_csv(
    records: list[dict],
) -> None:
    """
    Write raw records to CSV.

    Args:
        records:
            Raw enrollment records.

    Returns:
        None
    """

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    LOG_HEADER = [
        "EnrollmentID",
        "EnrollmentDate",
        "StudentID",
        "StudentName",
        "Major",
        "StudentEnrollmentDate",
        "CourseID",
        "CourseName",
        "Department",
        "CreditHours",
        "Semester",
        "InstructorID",
        "Grade",
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=LOG_HEADER,
        )

        writer.writeheader()

        writer.writerows(records)

    print(f"Created dataset: {OUTPUT_FILE}")

    print(f"Rows created: {len(records)}")


# ==========================================================
# SECTION 4
# Main Function
# ==========================================================


def main() -> None:
    """
    Main function to generate raw university data.

    Workflow:

        1. Create raw enrollment records.
        2. Create output directory.
        3. Write records to CSV.
        4. Display completion message.
    """

    print("========================")
    print("START university dataset generation")
    print("========================")

    print("Creating raw enrollment records...")

    records = create_raw_records(NUMBER_OF_RECORDS)

    print("Writing CSV file...")

    write_csv(records)

    print("========================")
    print("Dataset generation complete")
    print("========================")


# ==========================================================
# Conditional Execution Guard
# ==========================================================


if __name__ == "__main__":
    main()
