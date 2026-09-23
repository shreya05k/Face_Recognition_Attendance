import cv2
import os
import numpy as np

recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []

dataset_path = "dataset"

for folder in os.listdir(dataset_path):

    folder_path = os.path.join(dataset_path, folder)

    if not os.path.isdir(folder_path):
        continue

    student_id = int(folder.split("_")[0])

    for image_name in os.listdir(folder_path):

        image_path = os.path.join(folder_path, image_name)

        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if image is not None:
            faces.append(image)
            labels.append(student_id)

recognizer.train(faces, np.array(labels))

recognizer.save("trainer.yml")

print("Training completed!")
print("Students trained:", len(set(labels)))