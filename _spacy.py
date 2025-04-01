import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_lg")

def extract_transaction_details(text):
    doc = nlp(text.lower())
    print("TEXT", "LEMMA", "POS", "TAG", "DEP", "SHAPE", "IS_ALPHA", "IS_STOP")
    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)
    
    matcher = Matcher(nlp.vocab)

    # Add the patterns to the matcher
    datetime_pattern = [{"SHAPE": "dd,dddd"}]
    matcher.add("DATETIME_PATTERN", [datetime_pattern])

    matches = matcher(doc)
    # Iterate over the matches
    for match_id, start, end in matches:
        # Get the matched span
        matched_span = doc[start:end]
        print(match_id, ":", matched_span.text)

# text = "mar30,2025 __ paid to zepto debit %436"
text = "mar 30,2025 __ paid to zepto debit %436"
extract_transaction_details(text)