import chromadb
import fitz
import os

FRAMEWORKS = {
    "dpdp": "frameworks/doc20251117695301.pdf",
    "gdpr": "frameworks/CELEX_32016R0679_EN_TXT.pdf",
    "eu_ai_act": "frameworks/eu_ai_act.pdf",
    "nist": "frameworks/NIST.SP.800-53r5.pdf",
    "rbi_digital": "frameworks/MD7493544C24B5FC47D0AB12798C61CDB56F.pdf",
}

CHROMA_PATH = "chroma_db"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def get_client():
    return chromadb.PersistentClient(path=CHROMA_PATH)

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start = end - overlap
    return chunks

def ingest_framework(name, pdf_path):
    print(f"Ingesting {name}...")
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    if not text.strip():
        print(f"  WARNING: No text from {pdf_path}")
        return 0
    chunks = chunk_text(text)
    print(f"  {len(chunks)} chunks created")
    client = get_client()
    collection = client.get_or_create_collection(name=name)
    ids = [f"{name}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"framework": name, "chunk_index": i} for i in range(len(chunks))]
    collection.add(documents=chunks, metadatas=metadatas, ids=ids)
    print(f"  Done. {len(chunks)} chunks stored.")
    return len(chunks)

def ingest_all():
    print("=== AuditX Framework Ingestion ===")
    total = 0
    for name, path in FRAMEWORKS.items():
        if os.path.exists(path):
            count = ingest_framework(name, path)
            total += count
        else:
            print(f"SKIPPED {name}: not found at {path}")
    print(f"Total chunks stored: {total}")
    print("Ingestion complete.")

if __name__ == "__main__":
    ingest_all()
