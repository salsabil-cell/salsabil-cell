import os
import numpy as np
from PIL import Image
import cv2

def validate_tunisian_id_photo(photo_path):
    try:
        # Open the image
        img = Image.open(photo_path)
        
        # Check if the image dimensions meet the requirement
        min_width, min_height = 300, 400  # Minimum width and height for the ID card photo
        width, height = img.size
        if width < min_width or height < min_height:
            return False, f"Image dimensions are too small. Minimum required dimensions are {min_width}x{min_height}"
        
        # Perform content verification checks
        
        # Check for plain background (Assuming plain background is white)
        if not has_plain_background(img):
            return False, "Background is not plain or not white"
        
        # Check for text or watermark overlay
        if has_text_overlay(photo_path):
            return False, "Text or watermark overlay detected"
        
        # Perform forgery detection checks
        
        # Check for potential forgery using edge detection
        if is_potential_forgery(photo_path):
            return False, "Potential photo manipulation or forgery detected"
        
        # If all checks pass, return True
        return True, "Validation successful"
    
    except Exception as e:
        return False, str(e)

def has_plain_background(image):
    # Convert the image to grayscale
    gray_img = image.convert('L')
    
    # Threshold the image to extract the background
    _, binary_img = cv2.threshold(np.array(gray_img), 240, 255, cv2.THRESH_BINARY)
    
    # Calculate the percentage of white pixels in the image
    white_pixel_percentage = np.sum(binary_img == 255) / binary_img.size
    
    # Define a threshold for the percentage of white pixels
    # You may need to adjust this threshold based on your requirements
    threshold_percentage = 0.95
    
    return white_pixel_percentage >= threshold_percentage

def has_text_overlay(photo_path):
    # Placeholder function for text overlay detection
    # For simplicity, this function uses a basic OCR approach using Tesseract OCR
    # You need to install pytesseract and Tesseract OCR on your system to use this
    try:
        import pytesseract
        
        # Load the image using OpenCV
        img = cv2.imread(photo_path)
        
        # Convert the image to grayscale
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding to extract text regions
        _, binary_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Use pytesseract to perform OCR
        text = pytesseract.image_to_string(binary_img)
        
        # Check if any text is detected
        if text.strip() != "":
            return True
        else:
            return False
        
    except Exception as e:
        # Log any exceptions (e.g., missing libraries)
        print("Error in text overlay detection:", e)
        return False

def is_potential_forgery(photo_path):
    # Placeholder function for forgery detection using edge detection
    # For simplicity, this function uses Canny edge detection
    try:
        # Load the image using OpenCV
        img = cv2.imread(photo_path, 0)  # Load image in grayscale
        
        # Apply Canny edge detection
        edges = cv2.Canny(img, 100, 200)
        
        # Check if the number of detected edges is above a threshold
        min_edge_count = 1000  # Adjust this threshold as needed
        edge_count = np.sum(edges != 0)
        
        if edge_count > min_edge_count:
            return True
        else:
            return False
        
    except Exception as e:
        # Log any exceptions (e.g., missing libraries)
        print("Error in potential forgery detection:", e)
        return False

# Example usage:
photo_path = "path/to/tunisian_id_photo.jpg"
is_valid, message = validate_tunisian_id_photo(photo_path)
print("Validation Result:", is_valid)
print("Message:", message)
