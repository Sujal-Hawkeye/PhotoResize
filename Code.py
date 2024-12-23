import cv2
from PIL import Image
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def detect_faces(image_path):
    # Load Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 30))
    return faces

def resize_with_aspect_ratio(image, target_size):
    # Maintain aspect ratio while resizing
    image.thumbnail(target_size, Image.Resampling.LANCZOS)
    return image

def resize_image_for_detection(image, max_dimension=1000):
    # Resize image to a manageable size for faster face detection
    width, height = image.size
    if max(width, height) > max_dimension:
        scaling_factor = max_dimension / max(width, height)
        new_size = (int(width * scaling_factor), int(height * scaling_factor))
        return image.resize(new_size, Image.Resampling.LANCZOS)
    return image

def create_passport_photo(input_path, output_path, passport_size=(900, 950), extra_space_ratio=0.3):
    faces = detect_faces(input_path)
    if len(faces) == 0:
        raise ValueError("No face detected in the image.")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Ensure the output directory exists

    with Image.open(input_path) as img:
        img = resize_image_for_detection(img)  # Optimize image size for processing

        for i, (x, y, w, h) in enumerate(faces):
            # Calculate extra space around the face
            extra_width = int(w * extra_space_ratio)
            extra_height = int(h * extra_space_ratio)
            new_box = (
                max(x - extra_width, 0),
                max(y - extra_height, 0),
                min(x + w + extra_width, img.width),
                min(y + h + extra_height, img.height)
            )

            # Crop the image to include extra space
            cropped_img = img.crop(new_box)

            # Resize the image to passport size while maintaining aspect ratio
            passport_img = resize_with_aspect_ratio(cropped_img, passport_size)

            # Generate unique filename for multiple faces
            face_output_path = output_path if len(faces) == 1 else output_path.replace(".jpg", f"_{i+1}.jpg")

            # Save the final passport-sized image
            passport_img.save(face_output_path)
            logging.info(f"Passport photo saved as {face_output_path}")

def batch_process(input_folder, output_folder, passport_size=(900, 950), extra_space_ratio=0.3):
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"passport_{filename}")
        try:
            create_passport_photo(input_path, output_path, passport_size, extra_space_ratio)
        except Exception as e:
            logging.error(f"Failed to process {filename}: {e}")

# Example usage
if __name__ == "__main__":
    input_path = "D:\\village\\Photo resize\\images\\sujal.jpg"
    output_path = "D:\\village\\Photo resize\\images\\photo3.jpg"

    try:
        create_passport_photo(input_path, output_path)
    except Exception as e:
        logging.error(f"Error: {e}")

    # Batch processing example
    input_folder = "D:\\village\\Photo resize\\images"
    output_folder = "D:\\village\\Photo resize\\output"

    batch_process(input_folder, output_folder)