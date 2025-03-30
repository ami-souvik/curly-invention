import spacy
import re

nlp = spacy.load("en_core_web_sm")
# print(nlp._path)

# doc = nlp("Add expense of 20 for Dinner on Swiggy")
# for token in doc:
#     print(token.text, token.pos_, token.dep_)

def extract_transaction_details(text):
    doc = nlp(text.lower())

    # Extract amount using regex
    amount_match = re.search(r'\b\d+\b', text)
    amount = float(amount_match.group()) if amount_match else None

    # Extract category (assumes category is a noun)
    categories = [token.text for token in doc if token.pos_ == "NOUN"]
    category = categories[0] if categories else "Unknown"

    return {
        "section": "EXPENSE",
        "amount": amount,
        "category": category,
        "note": text
    }

text = "Add expense of 20 for Dinner on Swiggy"
print(extract_transaction_details(text))