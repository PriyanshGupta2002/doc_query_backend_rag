from langchain_community.document_loaders import PyMuPDFLoader
from app.db.session import SessionLocal
from app.models.documentModel import Document
from app.services.chunkService import create_document_chunks
from app.services.createVectorStore import create_vector_store
from app.services.createEmbeddings import embed_documents

def ProcessDocuments(docId:int):
    db = SessionLocal()
    try:
        doc = db.query(Document).filter(Document.id==docId).first()
        if not doc:
            return
        print(f"Doc id {docId} loader is started....")
        loader = PyMuPDFLoader(doc.doc_url)
        docs = loader.load()
        print(f"Doc id {docId} loading is finished....")
        
        print(f"Chunking of document started")
        docChunks = create_document_chunks(docs)
        
        texts = [doc.page_content for doc in docChunks]
        embeddings = embed_documents(texts)
        create_vector_store(doc_id=docId,document_chunks=docChunks,embeddings=embeddings)
        doc.status="Completed"
        db.commit()
    except Exception as e:
        print("Error:", e)
        doc.status = "failed"
        db.commit()
    finally:
        db.close()
    