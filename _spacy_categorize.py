# python _spacy_categorize.py
import re
import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")

def extract_transaction_details(text):
    doc = nlp(text.lower())

    print()
    for token in doc:
        print(token.text, token.pos_, token.dep_)
    print()
    
    # Iterate over the predicted entities
    for ent in doc.ents:
        # Print the entity text and its label
        print(ent.text, ent.label_, spacy.explain(ent.label_))
    print()

    matcher = Matcher(nlp.vocab)

    # Add the patterns to the matcher
    expense_pattern = [{"LOWER": "expense"}, {"POS": "NOUN"}]
    income_pattern = [{"LOWER": "income"}, {"POS": "NOUN"}]
    matcher.add("SECTION_PATTERN", [expense_pattern, income_pattern])

    matches = matcher(doc)
    # Iterate over the matches
    for match_id, start, end in matches:
        # Get the matched span
        matched_span = doc[start:end]
        print(match_id, ":", matched_span.text)

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

text = "Add expense of 20 for Dinner on Swiggy, Add income of 20 to my ICICI bank"
print(extract_transaction_details(text))