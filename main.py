import cv2
import face_recognition
import numpy as np
import sys
from database import log_attendance
from recognition import load_known_faces

def main():
    # 1. System Initialization
    print("="*50)
    print("      AUTOMATED AI ATTENDANCE SYSTEM v1.0")
    print("="*50)
    print("[1/3] Loading AI Models and Encodings...")
    
    try:
        known_encodings, known_names = load_known_faces()
        if not known_encodings:
            print("Error: No images found in 'images' folder. Add a photo first!")
            return
        print(f"Successfully loaded {len(known_names)} authorized users.")
    except Exception as e:
        print(f"Setup Error: {e}")
        return

    # 2. Camera Setup
    print("[2/3] Initializing Camera Interface...")
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not access the webcam.")
        return

    print("[3/3] Connecting to Supabase Cloud...")
    print("\nSYSTEM STATUS: ACTIVE")
    print("-> Press 'q' on the camera window to exit.")
    print("-" * 50)

    # Local memory to prevent multiple rapid-fire requests to Supabase
    logged_today = set()

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Convert the image from BGR (OpenCV) to RGB (Face Recognition)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect all faces in the current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Check for matches
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
            name = "Unknown"

            # Use the closest match (smallest distance)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]

                    # --- CLOUD LOGGING LOGIC ---
                    # Only attempt to log if we haven't already logged them in this session
                    if name not in logged_today:
                        status_result = log_attendance(name)
                        
                        if status_result == "SUCCESS":
                            print(f" [LOG] {name} marked 'Present' in Cloud.")
                            logged_today.add(name) # Update local memory immediately
                        
                        elif status_result == "ALREADY_LOGGED":
                            print(f" [INFO] {name} was already recorded in DB today.")
                            logged_today.add(name) # Mark locally so we stop checking
                        
                        elif status_result == "ERROR":
                            print(f" [!] Failed to sync {name} with Supabase.")

            # 4. User Interface - Draw Graphics
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            
            # Draw frame around face
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # Draw label background
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), 
                        cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)

        # Show the live feed
        cv2.imshow('Automated Attendance System', frame)

        # Keyboard interrupt (q to quit)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\nShutting down system gracefully...")
            break

    # Cleanup
    video_capture.release()
    cv2.destroyAllWindows()
    print("System Offline.")

if __name__ == "__main__":
    main()