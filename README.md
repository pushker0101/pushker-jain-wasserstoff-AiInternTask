# pushker-jain-wasserstoff-AiInternTask

A pipeline for processing PDF documents that:

Parses PDF text.
Generates summaries using an abstractive summarization model.
Extracts domain-specific keywords.
Stores results in a MongoDB database.
This solution is optimized for concurrency and can handle either a single PDF or a folder of PDFs.

Python Libraries: 
The pipeline relies on the following libraries:

PyMuPDF: For PDF parsing
transformers: For using Hugging Face’s BART summarization model
spaCy: For text processing and cleaning
yake: For keyword extraction
pymongo: To interact with MongoDB

Step1 - clone the repositroy
ste2- In your terminal install the following dependencies by running 
    pip install pymongo[srv] transformers PyMuPDF spacy yake
    python -m spacy download en_core_web_sm
    
Step3 - Setup MongoDB
MongoDB Atlas:
Go to MongoDB Atlas and create a free account.
Set up a new cluster and create a database (e.g., pdf_summary_db) with a collection (e.g., pdf_documents).
Get the MongoDB URI in the following format and replace placeholders with your details:
    mongodb+srv://<username>:<password>@clustername.mongodb.net/pdf_summary_db?retryWrites=true&w=majority

then configure the mongodb connection in the code 
# Replace with your MongoDB Atlas connection URI
client = pymongo.MongoClient("your_mongodb_atlas_uri")
db = client["pdf_summary_db"]
collection = db["pdf_documents"]



Solution Explanation
This pipeline processes each PDF document by:

Parsing Text from PDFs:

The parsing.py script categorizes PDFs as "short," "medium," or "long" based on page count, extracts text using PyMuPDF, and stores initial metadata in MongoDB.

Generating Summaries:
The summarization.py script uses Hugging Face’s transformers library with the BART model to generate abstractive summaries.
Summaries are concise yet capture key points from the document, and the length is dynamically set based on document size.

Extracting Keywords:
The keyword.py script leverages yake for domain-specific keyword extraction, removing common or irrelevant words for better accuracy.
Keywords are stored in MongoDB for each document.

Updating MongoDB:
The docUpdation.py script updates MongoDB with summaries, keywords, and processing time, ensuring each document's information is stored and retrievable.
It also logs errors if a document fails to process.
Running the Pipeline:

main.py acts as the orchestrator, allowing you to provide either a single PDF file or a folder path to process. It handles concurrency, logs errors, and ensures MongoDB updates are completed.


Future Work

In this I can connect it to a LLM like llama or bert can can use that to ask questions from the pdf and generate answers from it.

OCR for Scanned PDFs:  I can Integrate OCR techniques to handle scanned or written documents in pdf form
