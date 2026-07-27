"""
generate_university_dataset.py

Generate a raw university enrollment dataset for a Business Intelligence
data warehouse project.

Creates a denormalized operational dataset used as the source
for an ETLV process.

Output:
    data/raw/university_records.csv

Run:
    uv run python -m bizintel.generate_university_dataset
"""

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
# HELPER FUNCTIONS
# ==========================================================


def create_date(
    start_year: int = 2024,
    end_year: int = 2025,
) -> str:
    """
    Create a random date.
    """

    start = datetime(start_year, 1, 1)

    end = datetime(end_year, 12, 31)

    days = (end - start).days

    result = start + timedelta(days=random.randint(0, days))

    return result.strftime("%Y-%m-%d")


def create_students() -> dict:
    """
    Create student records.
        Create student records.
    """

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
    """

    courses = {}

    for course_id, name, department, credits in COURSES:
        courses[course_id] = {
            "CourseID": course_id,
            "CourseName": name,
            "Department": department,
            "CreditHours": credits,
        }

    return courses


def create_instructors() -> dict:
    """
    Create instructor records.
    """

    instructors = {}

    for instructor_id, name in INSTRUCTORS:
        instructors[instructor_id] = {
            "InstructorID": instructor_id,
            "InstructorName": name,
        }

    return instructors


def create_semesters() -> dict:
    """
    Create semester records.
    """

    semesters = {}

    for semester_id, semester_name in SEMESTERS:
        semesters[semester_id] = {
            "SemesterID": semester_id,
            "SemesterName": semester_name,
        }

    return semesters


def create_enrollment_date() -> str:
    """
    Create enrollment transaction date.
    """

    return create_date(
        2024,
        2025,
    )


# ==========================================================
# DATA GENERATION
# ==========================================================


def create_raw_records(
    number_of_records: int,
) -> list[dict]:
    """
    Create raw university enrollment records.
    """

    records = []

    students = create_students()

    courses = create_courses()

    instructors = create_instructors()

    semesters = create_semesters()

    for enrollment_id in range(
        1001,
        1001 + number_of_records,
    ):
        student = random.choice(list(students.values()))

        course = random.choice(list(courses.values()))

        instructor = random.choice(list(instructors.values()))

        semester = random.choice(list(semesters.values()))

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
            "Semester": semester["SemesterName"],
            "InstructorID": instructor["InstructorID"],
            "InstructorName": instructor["InstructorName"],
            "Grade": random.choice(GRADES),
        }

        records.append(record)

    return records


# ==========================================================
# CSV OUTPUT
# ==========================================================


def write_csv(
    records: list[dict],
) -> None:
    """
    Write records to CSV.
    """

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    headers = [
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
        "InstructorName",
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
            fieldnames=headers,
        )

        writer.writeheader()

        writer.writerows(records)

    print(f"Created dataset: {OUTPUT_FILE}")

    print(f"Rows created: {len(records)}")


# ==========================================================
# MAIN
# ==========================================================


def main() -> None:
    """
    Generate university dataset.
    """

    print("========================")

    print("START university dataset generation")

    print("========================")

    records = create_raw_records(NUMBER_OF_RECORDS)

    write_csv(records)

    print("========================")

    print("Dataset generation complete")

    print("========================")


if __name__ == "__main__":
    main()
