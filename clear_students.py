import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "attendance.db")

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute("DELETE FROM students")

connection.commit()
connection.close()

print("All student records deleted.")