import spacy
from pymongo import MongoClient
from bson import ObjectId
from yake import KeywordExtractor

client = MongoClient("mongodb://localhost:27017/")
db = client["pdf_summary_db"]
collection = db["pdf_documents"]

nlp = spacy.load("en_core_web_sm")
yake_extractor = KeywordExtractor(lan="en", n=1, top=10)

def clean_text(text):
    doc = nlp(text)
    cleaned_tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
    return " ".join(cleaned_tokens)

def extract_keywords(text):
    cleaned_text = clean_text(text)
    keywords = yake_extractor.extract_keywords(cleaned_text)
    keywords = [kw[0] for kw in keywords]
    return keywords

def update_keywords_in_mongo(doc_id, keywords):
    try:
        collection.update_one({"_id": ObjectId(doc_id)}, {"$set": {"keywords": keywords}})
        print(f"Updated document {doc_id} with keywords.")
    except Exception as e:
        print(f"Error updating MongoDB with keywords: {e}")

def process_keywords(doc_id, text):
    keywords = extract_keywords(text)
    update_keywords_in_mongo(doc_id, keywords)
    return keywords
