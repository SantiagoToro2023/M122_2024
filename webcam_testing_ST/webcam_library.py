import cv2

def detect_faces(video_source=0, scaleFactor=1.1, minNeighbors=3, minSize=(10, 10)):
    """
    Function to perform real-time face detection using a webcam.
    Author: Santiago Toro - M122

    Parameters:
        video_source (int or str): The video source (default is 0 for the webcam).
        scaleFactor (float): Parameter specifying how much the image size is reduced at each image scale (default is 1.1).
        minNeighbors (int): Parameter specifying how many neighbors each candidate rectangle should have to retain it (default is 3).
        minSize (tuple): Minimum possible object size (default is (10, 10)).
    """
    # Load the Haar cascade file for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Open the video source
    vid = cv2.VideoCapture(video_source)

    # Set video frame width and height
    vid.set(3, 200)  # Width
    vid.set(4, 200)  # Height

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
