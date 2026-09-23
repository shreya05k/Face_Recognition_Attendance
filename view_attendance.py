import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "attendance.db")
print("VIEW DATABASE:", DB_PATH)

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute("""
SELECT
    attendance.attendance_id,
    students.student_id,
    students.name,
    attendance.date,
    attendance.time,
    attendance.status
FROM attendance
JOIN students
ON attendance.student_id = students.student_id
ORDER BY attendance.date DESC, attendance.time DESC
""")

records = cursor.fetchall()

if records:
    print("\n===== ATTENDANCE RECORDS =====\n")

    for record in records:
        print(
            f"Attendance ID: {record[0]}"
        )
        print(
            f"Student ID: {record[1]}"
        )
        print(
            f"Name: {record[2]}"
        )
        print(
            f"Date: {record[3]}"
        )
        print(
            f"Time: {record[4]}"
        )
        print(
            f"Status: {record[5]}"
        )
        print("-----------------------------")

else:
    print("No attendance records found.")

connection.close()