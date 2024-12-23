# Passport Photo Generator

This project automates the creation of passport-sized photos from regular images using face detection and image processing. It ensures robust face cropping with customizable settings for passport dimensions and additional spacing around the face.

## Features
- Automatic face detection using OpenCV Haar cascades.
- Supports multiple faces with individual cropping and saving.
- Configurable passport size and extra spacing.
- Batch processing for multiple images in a folder.

## Requirements
- Python 3.7+
- Required libraries: OpenCV, Pillow

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### Single Image
```python
input_path = "path/to/image.jpg"
output_path = "path/to/output.jpg"
create_passport_photo(input_path, output_path)
```

### Batch Processing
```python
input_folder = "path/to/input/folder"
output_folder = "path/to/output/folder"
batch_process(input_folder, output_folder)
```

## License
This project is open-source and available under the [MIT License](LICENSE).

