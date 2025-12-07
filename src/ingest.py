import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
PDF_PATH = BASE_DIR.parent / os.getenv("PDF_PATH")

def ingest_pdf():
    
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    full_text = "\n".join(page.page_content for page in documents)
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=150, 
    )

    parts = splitter.create_documents([full_text])

    for part in parts:
        print(part.page_content)
        print("-"*30)
     


if __name__ == "__main__":
    ingest_pdf()