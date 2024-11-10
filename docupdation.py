from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["pdf_summary_db"]
collection = db["pdf_documents"]

def update_document_in_mongo(doc_id, summary_text, keywords):
    try:
        processing_time = datetime.utcnow()
        update_data = {
            "summary": summary_text,
            "keywords": keywords,
            "processing_time": processing_time
        }
        collection.update_one({"_id": ObjectId(doc_id)}, {"$set": update_data})
        print(f"Document {doc_id} updated with summary, keywords, and processing time.")
    except Exception as e:
        print(f"Error updating MongoDB document {doc_id}: {e}")

def log_error(doc_id, error_message):
    try:
        collection.update_one({"_id": ObjectId(doc_id)}, {"$set": {"error": error_message}})
        print(f"Document {doc_id} updated with error message: {error_message}")
    except Exception as e:
        print(f"Error logging error message for document {doc_id}: {e}")
