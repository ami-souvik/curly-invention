from pdf2image import convert_from_path

f = open("statement.txt", "w")

# Replace 'input_file.pdf' with the path to your PDF file
pdf_file = 'PhonePe_Statement_Mar2025_Mar2025.pdf'
pages = convert_from_path(pdf_file)

import pytesseract

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

# Create a list to store extracted text from all pages
extracted_text = []

for page in pages:
    preprocessed_image = page

    text = extract_text_from_image(preprocessed_image)
    extracted_text.extend(text.split('\n'))

import re

"""
Regex pattern:
(?P<date>\b(?:\d{1,2}[-/ ]\d{1,2}[-/ ]\d{2,4}|\d{4}[-/ ]\d{1,2}[-/ ]\d{1,2}|[a-zA-Z]{3,9} \d{1,2},? \d{4})\b)

- (?P<date>...) → Named capturing group called "date" (allows easier access in code).
- \b → Word boundary (ensures we match whole dates, not parts of words).
- (?: ... ) → Non-capturing group, used to match different date formats.
"""


"""
1. Matches Numeric Date Formats (MM/DD/YYYY, DD-MM-YYYY, etc.)
✅ 03-30-2025
✅ 30/03/2025
✅ 12 05 22
pattern: \d{1,2}[-/ ]\d{1,2}[-/ ]\d{2,4}

Explaination:
---------------------------------------------------------------------------------------------------------------------
- \d{1,2} → Matches 1 or 2 digits (day or month).
- [-/ ] → Matches hyphen (-), slash (/), or space ( ) as separators.
- \d{1,2} → Matches another 1 or 2 digits (month or day).
- [-/ ] → Another separator.
- \d{2,4} → Matches 2 to 4 digits (year).
"""


"""
2. Matches ISO & Year-First Formats (YYYY/MM/DD, YYYY-MM-DD)
✅ 2025-03-30
✅ 2025/03/30
✅ 2025 3 30
pattern: \d{4}[-/ ]\d{1,2}[-/ ]\d{1,2}

Explaination:
---------------------------------------------------------------------------------------------------------------------
- \d{4} → Matches 4 digits (year).
- [-/ ] → Matches separators.
- \d{1,2} → Matches 1 or 2 digits (month).
- [-/ ] → Another separator.
- \d{1,2} → Matches 1 or 2 digits (day).
"""


"""
3. Matches Month Name Formats (Mar 30, 2025 / March 30 2025)
✅ Mar 30, 2025
✅ March 30 2025
✅ July 4, 2023
✅ December 25 2024
pattern: [a-zA-Z]{3,9} \d{1,2},? \d{4}

Explaination:
---------------------------------------------------------------------------------------------------------------------
- [a-zA-Z]{3,9} → Matches month names (like "Mar" or "March").
- \s → Space.
- \d{1,2} → Matches day (1 or 2 digits).
- ,? → Matches an optional comma (,).
- \s → Space.
- \d{4} → Matches 4-digit year.
"""
# 2. 

# ✅ March 30, 2025 / Mar 30, 2025 / Mar30,2025
# ✅ 30 March 2025
date_patterns = r"(?P<date>\b(?:\d{1,2}[-/ ]\d{1,2}[-/ ]\d{2,4}|\d{4}[-/ ]\d{1,2}[-/ ]\d{1,2}|[a-zA-Z]{3,9} \d{1,2},? \d{4})\b)"

def parse_transaction(t):
    match = re.search(date_patterns, t)
    if not match:
        return ''
    date = match.group("date")
    desc = t[match.span()[1]:]
    return ",".join([date, desc]) + '\n'

for t in extracted_text:
    f.write(parse_transaction(t))

f.close()
