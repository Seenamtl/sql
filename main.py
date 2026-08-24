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
SELECT
    students.student_id,
    students.name,
    COUNT(courses.course_id) AS course_count,
    ROUND(AVG(courses.grade), 2) AS average_grade
FROM students
LEFT JOIN courses
    ON students.student_id = courses.student_id
GROUP BY
    students.student_id,
    students.name
HAVING COUNT(courses.course_id) >= 2
ORDER BY course_count DESC
"""

result = pd.read_sql_query(query, connection)
# print("\nAll students:")
print(result)

connection.close()


