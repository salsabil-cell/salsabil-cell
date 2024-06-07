# information_extraction.py
import spacy
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Load English language model for spaCy
nlp = spacy.load('xx_ent_wiki_sm')


# Function for text preprocessing
def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('arabic'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    
    return lemmatized_tokens

# Function for named entity recognition (NER)
def extract_named_entities(text):
    doc = nlp(text)
    named_entities = [(ent.text, ent.label_) for ent in doc.ents]
    return named_entities

# Function for regular expression-based extraction
def extract_using_regex(text):
    # Example: Extract date of birth using regex
    dob_pattern = r'\b\d{1,2}/\d{1,2}/\d{4}\b'  # Example date format: dd/mm/yyyy
    dob_matches = re.findall(dob_pattern, text)
    return dob_matches
# Function for rule-based extraction
def extract_using_rules(text):
    # Define patterns for ID number, name, prename, date of birth, and place of birth using regex
    id_pattern = r'\b\d{9}\b'  # Assuming ID number is a 9-digit number
    name_pattern = r'اسم:(.*)'
    prename_pattern = r'الاسم الاخير:(.*)'
    dob_pattern = r'\b\d{1,2}/\d{1,2}/\d{4}\b'  # Example date format: dd/mm/yyyy
    place_of_birth_pattern = r'مكان الولادة:(.*)'  # Pattern for place of birth
    
    # Extract information using regex
    id_matches = re.findall(id_pattern, text)
    name_matches = re.findall(name_pattern, text)
    prename_matches = re.findall(prename_pattern, text)
    dob_matches = re.findall(dob_pattern, text)
    place_of_birth_matches = re.findall(place_of_birth_pattern, text)
    
    return id_matches, name_matches, prename_matches, dob_matches, place_of_birth_matches

# Main function for information extraction
def extract_information(text):
    named_entities = extract_named_entities(text)  # Extract named entities using spaCy
    id_number, name, prename, dob, place_of_birth = extract_using_rules(text)  # Extract information using rules
    
    extracted_info = {
        'named_entities': named_entities,
        'identification_number': id_number,
        'name': name,
        'prename': prename,
        'date_of_birth': dob,
        'place_of_birth': place_of_birth
    }
    return extracted_info

