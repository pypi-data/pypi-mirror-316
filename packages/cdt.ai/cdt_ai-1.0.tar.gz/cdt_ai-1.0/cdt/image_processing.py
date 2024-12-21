import easyocr
import cv2
import pytesseract
from PIL import Image
import numpy as np
import magic  # To detect MIME type

# Initialize EasyOCR reader
ocr_reader = easyocr.Reader(['en'])

def get_mimetype(image_path):
    """
    Detects the MIME type of an image using python-magic.
    """
    mime = magic.Magic(mime=True)
    mimetype = mime.from_file(image_path)
    return mimetype

def extract_text_from_image_easyocr(image_path):
    """
    Extracts text from an image using EasyOCR.
    """
    try:
        result = ocr_reader.readtext(image_path)
        text = " ".join([item[1] for item in result])
        return text
    except Exception as e:
        return f"Error with EasyOCR: {str(e)}"

def process_image_with_pytesseract(image_path):
    """
    Extracts text from an image using Pytesseract.
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image file could not be read")
        
        # Convert to grayscale for better OCR results
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding (optional, to improve results in certain cases)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        
        # Use pytesseract to extract text
        text = pytesseract.image_to_string(thresh)
        return text
    except Exception as e:
        return f"Error with Pytesseract: {str(e)}"

def process_image(image_path):
    """
    Processes the image and applies both EasyOCR and Pytesseract.
    """
    mimetype = get_mimetype(image_path)
    print(f"Detected MIME type: {mimetype}")

    easyocr_text = extract_text_from_image_easyocr(image_path)
    pytesseract_text = process_image_with_pytesseract(image_path)

    return {
        "mimetype": mimetype,
        "easyocr_text": easyocr_text,
        "pytesseract_text": pytesseract_text
    }

# Example usage
image_path = "path_to_your_image_file.jpg"
result = process_image(image_path)
print(result)
