from datetime import datetime
from flask import Flask, render_template, request
import sqlite3
import sys
import subprocess
import os

app = Flask(__name__)

# ---------- Database Path ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "attendance.db")


# ---------- Home ----------
@app.route("/")
def home():
    return render_template("index.html")


# ---------- Start Face Recognition ----------
@app.route("/recognize")
def recognize():

    script_path = os.path.join(
        BASE_DIR,
        "recognize.py"
    )

    subprocess.Popen([
        sys.executable,
        script_path
    ])

    return """
    <h2>Face Recognition Started</h2>
    <p>Camera is opening...</p>
    <a href="/">Back to Home</a>
    """

#-----------Train Model-------------
@app.route("/train")
def train():

    train_script = os.path.join(
        BASE_DIR,
        "train.py"
    )

    subprocess.Popen([
        sys.executable,
        train_script
    ])

    return """
    <h2>Training Started</h2>
    <p>The face recognition model is being trained.</p>
    <p>Now you are able</p>

    <br>

    <a href="/">
        <button>Back to Home</button>
    </a>
    """

# ---------- View Attendance ----------
@app.route("/attendance")
def attendance():

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
        WHERE attendance.date = (
            SELECT MAX(date)
            FROM attendance
        )
        ORDER BY attendance.time DESC
    """)

    records = cursor.fetchall()

    connection.close()

    return render_template(
        "attendance.html",
        records=records
    )


# ---------- Register Student ----------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        student_id = request.form["student_id"]
        name = request.form["name"]

        # Save student in database
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO students
            (student_id, name)
            VALUES (?, ?)
        """, (student_id, name))

        connection.commit()
        connection.close()

        # Start register.py
        register_script = os.path.join(
            BASE_DIR,
            "register.py"
        )

        subprocess.Popen([
            sys.executable,
            register_script,
            str(student_id),
            name
        ])

        return """
        <h2>Student Registered Successfully!</h2>

        <p>Student ID and Name saved.</p>
        <p>Camera is opening...</p>
        <p>Please capture 5 face images.</p>

        <br>

        <a href="/">Back to Home</a>
        """

    return render_template("register.html")


# ---------- Run Flask ----------
if __name__ == "__main__":
    app.run(debug=True)