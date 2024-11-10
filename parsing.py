import os
import fitz  # PyMuPDF
import pymongo
from datetime import datetime
import concurrent.futures

# MongoDB configuration
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["pdf_summary_db"]
collection = db["pdf_documents"]

# Define document length categories
SHORT_LIMIT = 5    # Pages for short documents
MEDIUM_LIMIT = 20  # Pages for medium documents

def categorize_document(pdf_path):
    doc = fitz.open(pdf_path)
    num_pages = doc.page_count
    if num_pages <= SHORT_LIMIT:
        category = 'short'
    elif num_pages <= MEDIUM_LIMIT:
        category = 'medium'
    else:
        category = 'long'
    doc.close()
    return category

def parse_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text("text")
    doc.close()
    return text

def store_metadata(pdf_path, category):
    doc_name = os.path.basename(pdf_path)
    doc_size = os.path.getsize(pdf_path)
    ingestion_time = datetime.utcnow()
    metadata = {
        "document_name": doc_name,
        "document_size": doc_size,
        "ingestion_time": ingestion_time,
        "category": category,
        "summary": None,
        "keywords": None
    }
    result = collection.insert_one(metadata)
    return result.inserted_id

def process_pdf(pdf_path):
    try:
        category = categorize_document(pdf_path)
        text = parse_pdf_text(pdf_path)
        doc_id = store_metadata(pdf_path, category)
        print(f"Processed {pdf_path} | Category: {category} | MongoDB ID: {doc_id}")
        return doc_id, text
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None, None

def parse_folder(folder_path):
    pdf_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_pdf, pdf_path): pdf_path for pdf_path in pdf_paths}
        for future in concurrent.futures.as_completed(futures):
            pdf_path = futures[future]
            try:
                doc_id, text = future.result()
                if doc_id and text:
                    results.append((doc_id, text))
            except Exception as e:
                print(f"Error with {pdf_path}: {e}")
    return results
