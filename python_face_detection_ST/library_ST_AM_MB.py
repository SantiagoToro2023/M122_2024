import cv2
import os

# Function for detecting front facing people in Images and exporting marked images to output folder.
def detect_faces(image_path, output_dir="output"):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # Read the input image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Could not read the image: {image_path}. Please check the file path.")
        return
    # Convert the image to grayscale (required for the classifier)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=3, minSize=(1, 1))
    # Check if faces are detected
    if len(faces) > 0:
        print(f"Detected {len(faces)} face(s) in the image: {image_path}.")
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 100, 255), 2)
    else:
        print(f"No faces detected in the image: {image_path}.")
    # Save the image with detected faces
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, os.path.basename(image_path))
    cv2.imwrite(output_path, image)
    print(f"Saved image with detected faces to: {output_path}")
