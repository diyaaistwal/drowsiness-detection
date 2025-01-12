import cv2
import numpy as np
import time

def detect_drowsiness():
    # Load the pre-trained classifiers
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

    # Initialize camera with increased resolution
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("Error: Could not open camera")
        return

    # Initialize variables
    frame_counter = 0
    blink_counter = 0
    start_time = time.time()
    eye_closed_time = None
    status = "Active"
    color = (0, 255, 0)
    blink_rate = 0
    last_blink_time = time.time()

    # Constants
    DROWSY_TIME_THRESHOLD = 1.5  # Seconds
    MIN_EYE_AREA = 100  # Minimum eye area to be considered open

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Calculate FPS
        frame_counter += 1
        current_time = time.time()
        if frame_counter >= 30:
            fps = frame_counter / (current_time - start_time)
            frame_counter = 0
            start_time = current_time

        # Enhance frame quality
        frame = cv2.resize(frame, (1280, 720))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        # Detect faces with improved parameters
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

                # Define region of interest (ROI) for eyes
                roi_gray = gray[y:y+h//2, x:x+w]  # Upper half of face
                roi_color = frame[y:y+h//2, x:x+w]

                # Detect eyes with improved parameters
                eyes = eye_cascade.detectMultiScale(
                    roi_gray,
                    scaleFactor=1.1,
                    minNeighbors=4,
                    minSize=(25, 25),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )

                # Calculate total eye area
                total_eye_area = sum([w*h for (ex,ey,w,h) in eyes]) if len(eyes) > 0 else 0

                if len(eyes) >= 2 and total_eye_area > MIN_EYE_AREA:
                    if eye_closed_time is not None:
                        # Check if it was a blink
                        if (current_time - eye_closed_time) < 0.3:  # Normal blink duration
                            blink_counter += 1
                            if current_time - last_blink_time >= 60:
                                blink_rate = blink_counter
                                blink_counter = 0
                                last_blink_time = current_time

                    eye_closed_time = None
                    status = "Active"
                    color = (0, 255, 0)

                    # Draw rectangles around eyes
                    for (ex, ey, ew, eh) in eyes:
                        cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                else:
                    if eye_closed_time is None:
                        eye_closed_time = current_time

                    eyes_closed_duration = current_time - eye_closed_time

                    if eyes_closed_duration >= DROWSY_TIME_THRESHOLD:
                        status = "DROWSY!"
                        color = (0, 0, 255)
                        cv2.putText(frame, "DROWSY ALERT!", (10, 90),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    else:
                        status = "Eyes Closing..."
                        color = (0, 255, 255)
        else:
            status = "No Face Detected"
            color = (0, 0, 255)

        # Display metrics
        cv2.putText(frame, f"Status: {status}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.putText(frame, f"Blink Rate: {blink_rate} blinks/min", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        if eye_closed_time is not None:
            cv2.putText(frame, f"Eyes Closed: {current_time - eye_closed_time:.1f}s",
                       (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        # Display the frame
        cv2.imshow("Drowsiness Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_drowsiness()
