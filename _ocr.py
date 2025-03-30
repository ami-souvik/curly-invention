from pdf2image import convert_from_path

# Replace 'input_file.pdf' with the path to your PDF file
pdf_file = 'PhonePe_Statement_Mar2025_Mar2025.pdf'
pages = convert_from_path(pdf_file)[:1]

import cv2
import numpy as np

def deskew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    coords = np.column_stack(np.where(gray > 0))
    angle = cv2.minAreaRect(coords)[-1]
    
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated

import pytesseract

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

# Create a list to store extracted text from all pages
extracted_text = []

for page in pages:
    # Step 2: Preprocess the image (deskew)
    # preprocessed_image = deskew(np.array(page))
    preprocessed_image = page

    # Step 3: Extract text using OCR
    text = extract_text_from_image(preprocessed_image)
    extracted_text.append(text)

print(extracted_text)

import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")

def extract_transaction_details(text):
    doc = nlp(text.lower())

    matcher = Matcher(nlp.vocab)

    # Add the patterns to the matcher
    expense_pattern = [{"LOWER": "expense"}, {"POS": "NOUN"}]
    income_pattern = [{"LOWER": "income"}, {"POS": "NOUN"}]
    matcher.add("SECTION_PATTERN", [expense_pattern, income_pattern])

    return doc.text

for line in extracted_text:
    print(extract_transaction_details(line))
    break