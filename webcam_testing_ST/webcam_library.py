import cv2
import os
import numpy as np

def detect_faces(video_source=0, scaleFactor=1.1, minNeighbors=3, minSize=(10, 10), windowHeight=200, windowWidth=200):
    """
    Function to perform real-time face detection using a webcam.
    Author: Santiago Toro - M122

    Parameters:
        video_source (int or str): The video source (default is 0 for the webcam).
        scaleFactor (float): Parameter specifying how much the image size is reduced at each image scale (default is 1.1).
        minNeighbors (int): Parameter specifying how many neighbors each candidate rectangle should have to retain it (default is 3).
        minSize (tuple): Minimum possible object size (default is (10, 10)).
        windowHeight (int): Camera Window height (default is 200).
        windowWidth (int): Camera Window width (default is 200).
    """
    # Load the Haar cascade file for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Open the video source
    vid = cv2.VideoCapture(video_source)

    # Set video frame width and height
    vid.set(3, windowWidth )  # Width
    vid.set(4, windowHeight )  # Height

    while True:
        ret, frame = vid.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Convert the frame to grayscale for better detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize)

        # Draw red rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Display the resulting frame
        cv2.imshow('Face Detection', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    vid.release()
    cv2.destroyAllWindows()

def recognize_faces(
    video_source=0, 
    scaleFactor=1.1,
    minNeighbors=3,
    minSize=(3, 3),
    windowHeight=300, 
    windowWidth=300, 
    known_faces_dir="known_faces"
):
    """
    Function to perform real-time face recognition using OpenCV.

    Parameters:
        video_source (int or str): The video source (default is 0 for the webcam).
        scaleFactor (float): Parameter specifying how much the image size is reduced at each image scale (default is 1.1).
        minNeighbors (int): Parameter specifying how many neighbors each candidate rectangle should have to retain it (default is 3).
        minSize (tuple): Minimum possible object size (default is (10, 10)).
        windowHeight (int): Camera Window height (default is 200).
        windowWidth (int): Camera Window width (default is 200).
        known_faces_dir (str): Directory containing subfolders for each person with labeled images.
    """
    # Load the Haar cascade file for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Prepare the LBPH face recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Load training data from known faces directory
    labels = {}
    faces = []
    face_labels = []
    label_id = 0

    for person_name in os.listdir(known_faces_dir):
        person_path = os.path.join(known_faces_dir, person_name)
        if not os.path.isdir(person_path):
            continue
        labels[label_id] = person_name
        for img_name in os.listdir(person_path):
            img_path = os.path.join(person_path, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                faces.append(img)
                face_labels.append(label_id)
        label_id += 1

    recognizer.train(faces, np.array(face_labels))

    # Open the video source
    vid = cv2.VideoCapture(video_source)

    # Set video frame width and height
    vid.set(3, windowWidth)  # Width
    vid.set(4, windowHeight)  # Height

    confidence_threshold = 90  # Confidence threshold for unknown faces

    while True:
        ret, frame = vid.read()
        if not ret:
            print("Failed to grab frame")
            break

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        detected_faces = face_cascade.detectMultiScale(
            gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize
        )

        recognized_labels = set()  # To track already recognized labels in this frame

        for (x, y, w, h) in detected_faces:
            face_roi = gray[y:y+h, x:x+w]
            face_roi = cv2.resize(face_roi, (200, 200))

            label_id, confidence = recognizer.predict(face_roi)

            if label_id in recognized_labels:
                # Skip if this label is already recognized
                continue

            if confidence > confidence_threshold:
                label_text = "Unknown"
                color = (0, 0, 255)  # Red for unknown
            else:
                label_text = labels.get(label_id, "Unknown")
                recognized_labels.add(label_id)  # Mark this label as recognized
                color = (0, 255, 0)  # Green for recognized

            # Draw rectangle and label
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{label_text} ({int(confidence)})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            print(label_text, confidence)
        # Display the resulting frame
        cv2.imshow('Face Recognition', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    vid.release()
    cv2.destroyAllWindows()