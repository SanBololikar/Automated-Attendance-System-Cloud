import face_recognition
import os

def load_known_faces(images_path="images"):
    """
    Scans the images folder and encodes faces into mathematical vectors.
    """
    known_encodings = []
    known_names = []

    # Loop through every file in the images folder
    for filename in os.listdir(images_path):
        if filename.endswith((".jpg", ".png", ".jpeg")):
            # 1. Load the image file
            img = face_recognition.load_image_file(f"{images_path}/{filename}")
            
            # 2. Find face encodings (the 128-dimension math vector)
            # We take index [0] assuming there is only one face in the photo
            encodings = face_recognition.face_encodings(img)
            
            if len(encodings) > 0:
                known_encodings.append(encodings[0])
                # Use the filename (without .jpg) as the person's name
                name = os.path.splitext(filename)[0]
                known_names.append(name)
                print(f"Learned face for: {name}")
            else:
                print(f"Warning: No face found in {filename}")
            
    return known_encodings, known_names