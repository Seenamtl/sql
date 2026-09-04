import sqlite3
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

DB_PATH = DATA_DIR / "students.db"


students = pd.read_csv(DATA_DIR / "students.csv")
courses = pd.read_csv(DATA_DIR / "courses.csv")

connection = sqlite3.connect(DB_PATH)

students.to_sql("students", connection, if_exists="replace", index=False)

courses.to_sql("courses", connection, if_exists="replace", index=False)

connection.close()

print("Data has been successfully imported into the SQLite database.")


connection = sqlite3.connect(DB_PATH)

query = """
WITH ranked_courses AS (
    SELECT
        student_id,
        course,
        grade,
        ROW_NUMBER() OVER (
            PARTITION BY student_id
            ORDER BY grade
        ) AS course_rank
    FROM courses
)

SELECT
    student_id,
    course,
    grade
FROM ranked_courses
WHERE course_rank = 1
ORDER BY student_id
"""

result = pd.read_sql_query(query, connection)
# print("\nAll students:")
print(result)

connection.close()


