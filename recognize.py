import cv2
import os
import sqlite3
from datetime import datetime


# ---------- Database function ----------
def mark_attendance(student_id):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "attendance.db")

    print("RECOGNIZE DATABASE:", DB_PATH)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    cursor.execute("""
        SELECT * FROM attendance
        WHERE student_id = ? AND date = ?
    """, (student_id, date))

    record = cursor.fetchone()

    if record:
        print("Attendance already marked today!")

    else:
        cursor.execute("""
            INSERT INTO attendance
            (student_id, date, time, status)
            VALUES (?, ?, ?, ?)
        """, (
            student_id,
            date,
            time,
            "Present"
        ))

        connection.commit()

        print("Attendance marked successfully!")

    connection.close()


# ---------- Load trained model ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read(
    os.path.join(BASE_DIR, "trainer.yml")
)


# ---------- Face detector ----------
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


# ---------- Load student names ----------
students = {}

dataset_path = os.path.join(
    BASE_DIR,
    "dataset"
)

for folder in os.listdir(dataset_path):

    if "_" in folder:

        student_id, student_name = folder.split("_", 1)

        students[int(student_id)] = student_name


print("Students:", students)


# ---------- Open camera ----------
camera = cv2.VideoCapture(0)

attendance_done = set()


while True:

    success, frame = camera.read()

    if not success:
        print("Camera not found")
        break

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )

    for x, y, w, h in faces:

        face = gray[y:y+h, x:x+w]

        student_id, confidence = recognizer.predict(face)

        # ---------- Recognized ----------
        if confidence < 70:

            name = students.get(
                student_id,
                "Unknown"
            )

            text = name

            # Mark attendance only once
            if student_id not in attendance_done:

                mark_attendance(student_id)

                attendance_done.add(student_id)

        # ---------- Unknown ----------
        else:

            name = "Unknown"
            text = name


        # ---------- Face rectangle ----------
        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0, 255, 0),
            2
        )


        # ---------- Display name ----------
        cv2.putText(
            frame,
            text,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )


    # ---------- Q instruction ----------
    cv2.putText(
        frame,
        "Press Q to close",
        (frame.shape[1] - 220, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )


    cv2.imshow(
        "Face Recognition Attendance",
        frame
    )


    # ---------- Press Q ----------
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()