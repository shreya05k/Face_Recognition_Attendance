import cv2
import os
import sqlite3
import sys

# ---------- Get student details ----------
if len(sys.argv) >= 3:
    student_id = int(sys.argv[1])
    student_name = sys.argv[2]
else:
    student_id = int(input("Enter student ID: "))
    student_name = input("Enter student name: ")


# ---------- Database ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "attendance.db")

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

cursor.execute("""
    INSERT OR REPLACE INTO students
    (student_id, name)
    VALUES (?, ?)
""", (student_id, student_name))

connection.commit()
connection.close()

print("Student saved in database!")


# ---------- Dataset folder ----------
folder = os.path.join(
    BASE_DIR,
    f"dataset/{student_id}_{student_name}"
)

os.makedirs(folder, exist_ok=True)


# ---------- Face detector ----------
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


# ---------- Camera ----------
camera = cv2.VideoCapture(0)

count = 0

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

        if count >= 5:
            break

        count += 1

        face = gray[y:y+h, x:x+w]

        filename = os.path.join(
            folder,
            f"face_{count}.jpg"
        )

        cv2.imwrite(filename, face)

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Image: {count}/5",
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    cv2.imshow(
        "Student Registration",
        frame
    )

    if (
        cv2.waitKey(1) & 0xFF == ord("q")
        or count >= 5
    ):
        break


camera.release()
cv2.destroyAllWindows()

print("Registration completed!")
print(f"Saved {count} face images.")