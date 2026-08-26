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
WITH student_average AS (
    SELECT
        student_id,
        ROUND(AVG(grade), 2) AS avg_grade
    FROM courses
    GROUP BY student_id
)

SELECT
    s.student_id,
    s.name,
    s.city,
    a.avg_grade
FROM students AS s
LEFT JOIN student_average AS a
    ON s.student_id = a.student_id
ORDER BY a.avg_grade
"""

result = pd.read_sql_query(query, connection)
# print("\nAll students:")
print(result)

connection.close()


