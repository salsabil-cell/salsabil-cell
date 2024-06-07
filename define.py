import cv2
import pytesseract
import numpy as np
import re

# Load the image of the ID card
image_path = r'assets\OIP (1).jpg'
image = cv2.imread(image_path)

# Preprocess the image to enhance the quality
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Use Tesseract OCR to extract text from the image
config = '--oem 3 --psm 6 -l ara+fra'
text = pytesseract.image_to_string(thresh, config=config)

# Extract specific information from the text
id_number_pattern = r'\b\d{8}\b'
name_pattern = r'[A-Za-z ]+'
date_pattern = r'\d{2}/\d{2}/\d{4}'

id_number_match = re.search(id_number_pattern, text)
name_match = re.search(name_pattern, text)
date_match = re.search(date_pattern, text)

if id_number_match:
    id_number = id_number_match.group()
    print(f'ID Number: {id_number}')
else:
    print('ID Number not found')

if name_match:
    name = name_match.group()
    print(f'Name: {name}')
else:
    print('Name not found')

if date_match:
    date = date_match.group()
    print(f'Date: {date}')
else:
    print('Date not found')

# Crop and save the extracted information
def save_cropped_lines(image, lines):
    for i, (text, x, y, w, h) in enumerate(lines):
        cropped_line = image[y:y+h, x:x+w]
        line_image_path = f'cropped_line_{i}.png'
        cv2.imwrite(line_image_path, cropped_line)
        print(f'Line {i}: {text}')

lines = [(id_number, 0, 0, 100, 20), (name, 0, 20, 100, 20), (date, 0, 40, 100, 20)]
save_cropped_lines(image, lines)