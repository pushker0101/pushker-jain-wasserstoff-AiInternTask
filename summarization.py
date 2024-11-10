from transformers import pipeline
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["pdf_summary_db"]
collection = db["pdf_documents"]

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_summary(text, max_length=150, min_length=50):
    try:
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        summary_text = summary[0]["summary_text"]
        return summary_text
    except Exception as e:
        print(f"Error generating summary: {e}")
        return None

def update_summary_in_mongo(doc_id, summary_text):
    try:
        collection.update_one({"_id": ObjectId(doc_id)}, {"$set": {"summary": summary_text}})
        print(f"Updated document {doc_id} with summary.")
    except Exception as e:
        print(f"Error updating MongoDB with summary: {e}")

def summarize_document(doc_id, text, category):
    if category == 'short':
        max_len, min_len = 60, 30
    elif category == 'medium':
        max_len, min_len = 100, 50
    else:
        max_len, min_len = 200, 100

    summary_text = generate_summary(text, max_length=max_len, min_length=min_len)
    if summary_text:
        update_summary_in_mongo(doc_id, summary_text)
    return summary_text
