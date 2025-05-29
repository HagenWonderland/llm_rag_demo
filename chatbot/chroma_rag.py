import chromadb
from chromadb.utils import embedding_functions
from PyPDF2 import PdfReader
import os
#import API_key
#OPENAI_API_KEY = API_key.OPENAI_API_KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def load_pdf_chunks(pdf_path):
    reader = PdfReader(pdf_path)
    chunks = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            for i in range(0, len(text), 600):
                chunk = text[i:i+600]
                chunks.append(chunk)
    return chunks

def build_or_load_chroma():
    chroma_dir = "chroma_store"
    os.makedirs(chroma_dir, exist_ok=True)
    client = chromadb.PersistentClient(chroma_dir)
    collection = client.get_or_create_collection(
        name="labor_regulations",
        embedding_function=embedding_functions.OpenAIEmbeddingFunction(
            api_key=OPENAI_API_KEY, model_name="text-embedding-3-small"
        )
    )
    if collection.count() == 0:
        chunks = load_pdf_chunks("Labor_regulations.pdf")
        collection.add(
            documents=chunks,
            ids=[f"doc{i}" for i in range(len(chunks))]
        )
    return collection

def rag_retrieve(query):
    collection = build_or_load_chroma()
    results = collection.query(query_texts=[query], n_results=3)
    docs = [d for d in results["documents"][0]]
    return docs
