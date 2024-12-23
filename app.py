import cv2
from PIL import Image
import os

def detect_faces(image_path):
    # Load the pre-trained Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Read the image using OpenCV
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 30))
    return faces

def create_passport_photo(input_path, output_path, passport_size=(900, 950), extra_space_ratio=0.3):
    faces = detect_faces(input_path)
    if len(faces) == 0:
        raise ValueError("No face detected in the image.")

    # Open the image file
    with Image.open(input_path) as img:
        for (x, y, w, h) in faces:
            # Calculate the cropping box with extra space around the face
            face_box = (x, y, x + w, y + h)
            face_area = img.crop(face_box)

            # Calculate extra space
            extra_width = int(w * extra_space_ratio)
            extra_height = int(h * extra_space_ratio)

            # Define the new box with extra space
            new_box = (
                max(x - extra_width, 0),
                max(y - extra_height, 0),
                min(x + w + extra_width, img.width),
                min(y + h + extra_height, img.height)
            )

            # Crop the image to include extra space
            cropped_img = img.crop(new_box)

            # Resize the image to passport size
            passport_img = cropped_img.resize(passport_size, Image.Resampling.LANCZOS)

            # Save the final passport-sized image
            passport_img.save(output_path)
            print(f"Passport photo saved as {output_path}")

# Example usage
input_path = "D:\\village\\Photo resize\\images\\ryan.jpg"
output_path = "D:\\village\\Photo resize\\images\\photo1.jpg"  # Full path including filename for the output

create_passport_photo(input_path, output_path)
