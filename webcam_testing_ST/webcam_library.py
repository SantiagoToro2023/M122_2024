import cv2
import os
import numpy as np
from collections import defaultdict

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
    scaleFactor=1.2,
    minNeighbors=4,
    minSize=(5, 5),
    windowHeight=750,
    windowWidth=750,
    known_faces_dir="known_faces",
    consistency_threshold=45  # Number of frames required for consistent identification
):
    """
    Parameters:
        video_source (int or str): The video source (default is 0 for the webcam).
        scaleFactor (float): Parameter specifying how much the image size is reduced at each image scale (default is 1.1).
        minNeighbors (int): Parameter specifying how many neighbors are required. (default is 3).
        minSize (tuple): Minimum possible object size (default is (10, 10)).
        windowHeight (int): Camera Window height (default is 200).
        windowWidth (int): Camera Window width (default is 200).
        known_faces_dir (str): Directory containing subfolders for each person with labeled images.
        consistency_threshold (int): Number of frames needed to validate identity.
    """
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
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

    vid = cv2.VideoCapture(video_source)
    vid.set(3, windowWidth)
    vid.set(4, windowHeight)

    tracked_faces = defaultdict(lambda: {"label_id": -1, "count": 0, "frames_since_last_seen": 0})
    max_frames_missed = 10
    active_labels = set()

    while True:
        ret, frame = vid.read()
        if not ret:
            print("Failed to grab frame")
            break

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        detected_faces = face_cascade.detectMultiScale(
            gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize
        )

        current_tracked_ids = set()
        active_labels.clear()

        for (x, y, w, h) in detected_faces:
            face_roi = gray[y:y+h, x:x+w]
            face_roi = cv2.resize(face_roi, (200, 200))

            label_id, confidence = recognizer.predict(face_roi)
            face_center = (x + w // 2, y + h // 2)

            # Find the closest tracked face to associate with this detection
            matched_id = None
            for track_id, data in tracked_faces.items():
                tracked_center = data["position"]
                if np.linalg.norm(np.array(tracked_center) - np.array(face_center)) < max(w, h):
                    matched_id = track_id
                    break

            if matched_id is None:
                matched_id = len(tracked_faces) + 1
                tracked_faces[matched_id]["position"] = face_center

            tracked_faces[matched_id]["position"] = face_center
            tracked_faces[matched_id]["frames_since_last_seen"] = 0

            if tracked_faces[matched_id]["label_id"] == label_id:
                # Increment the consistency count if the label remains the same
                tracked_faces[matched_id]["count"] += 1
            else:
                # Reset the count if the label changes
                tracked_faces[matched_id]["label_id"] = label_id
                tracked_faces[matched_id]["count"] = 1

            # Draw the face bounding box and label if consistent enough and not already active
            if (
                tracked_faces[matched_id]["count"] >= consistency_threshold
                and label_id not in active_labels
            ):
                final_label = labels.get(label_id, "Unknown")
                color = (0, 255, 0) if final_label != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(
                    frame, f"{final_label} ({int(confidence)})", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1
                )
                active_labels.add(label_id)  # Mark this label as active
                print(final_label, confidence)

            current_tracked_ids.add(matched_id)

        # Update frames since last seen for all tracked faces
        for track_id in list(tracked_faces.keys()):
            if track_id not in current_tracked_ids:
                tracked_faces[track_id]["frames_since_last_seen"] += 1

                # Remove faces that haven't been seen for a while
                if tracked_faces[track_id]["frames_since_last_seen"] > max_frames_missed:
                    del tracked_faces[track_id]

        # Display the resulting frame
        cv2.imshow('Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()