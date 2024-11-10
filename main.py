import os
from parsing import parse_folder, process_pdf
from summarization import summarize_document
from keyword import process_keywords
from docUpdation import update_document_in_mongo, log_error

def process_single_pdf(pdf_path):
    try:
        doc_id, text = process_pdf(pdf_path)
        doc_info = db["pdf_documents"].find_one({"_id": doc_id})
        category = doc_info.get("category")
        summary_text = summarize_document(doc_id, text, category)
        keywords = process_keywords(doc_id, text)
        update_document_in_mongo(doc_id, summary_text, keywords)
    except Exception as e:
        log_error(doc_id, str(e))
        print(f"Error processing document {pdf_path}: {e}")

def process_pdf_pipeline(path):
    if os.path.isdir(path):
        parsed_documents = parse_folder(path)
        for doc_id, text in parsed_documents:
            try:
                doc_info = db["pdf_documents"].find_one({"_id": doc_id})
                category = doc_info.get("category")
                summary_text = summarize_document(doc_id, text, category)
                keywords = process_keywords(doc_id, text)
                update_document_in_mongo(doc_id, summary_text, keywords)
            except Exception as e:
                log_error(doc_id, str(e))
                print(f"Error processing document {doc_id}: {e}")
    elif os.path.isfile(path) and path.endswith('.pdf'):
        process_single_pdf(path)
    else:
        print("Invalid path provided. Please provide a valid PDF file or folder path.")

if __name__ == "__main__":
    path = "/path/to/pdf/or/folder"  # Replace with the actual path
    process_pdf_pipeline(path)
