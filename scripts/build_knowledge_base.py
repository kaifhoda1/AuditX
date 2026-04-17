#!/usr/bin/env python3
"""
AuditX Knowledge Base Builder
Processes framework PDFs into searchable vector database
"""

import os
import chromadb
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader

def main():
    print("=" * 50)
    print("AuditX Knowledge Base Builder")
    print("=" * 50)
    
    db_path = "../frameworks/chroma_db"
    client = chromadb.PersistentClient(path=db_path)
    
    collection_name = "grc_frameworks"
    try:
        client.delete_collection(collection_name)
        print(f"Cleared existing '{collection_name}' collection")
    except:
        pass
    
    collection = client.create_collection(collection_name)
    
    print("Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    frameworks_path = "../frameworks/"
    pdf_files = [f for f in os.listdir(frameworks_path) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found in frameworks directory.")
        return
    
    total_chunks = 0
    
    for filename in pdf_files:
        print(f"\nProcessing: {filename}")
        filepath = os.path.join(frameworks_path, filename)
        
        try:
            reader = PdfReader(filepath)
            full_text = ""
            
            for page in reader.pages:
                text = page.extract_text()
                full_text += text
            
            chunks = [c.strip() for c in full_text.split("\n\n") if len(c.strip()) > 100]
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"{filename.replace('.pdf', '')}_{i}"
                collection.add(
                    documents=[chunk],
                    metadatas=[{"source": filename, "chunk_id": i}],
                    ids=[chunk_id]
                )
            
            total_chunks += len(chunks)
            print(f"  Added {len(chunks)} chunks from {filename}")
            
        except Exception as e:
            print(f"  Error processing {filename}: {e}")
    
    print("\n" + "=" * 50)
    print(f"Knowledge base built successfully!")
    print(f"Total chunks stored: {total_chunks}")
    print("=" * 50)

if __name__ == "__main__":
    main()
