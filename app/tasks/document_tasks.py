from app.core.celery_app import celery_app
from app.services.procesPdfService import ProcessDocuments
from langchain_community.document_loaders import PyMuPDFLoader
from app.db.session import SessionLocal
from app.models.documentModel import Document as DbDocument
from app.services.documentStatusService import updateDocumentStatus
from app.services.chunkService import create_document_chunks
from langchain_core.documents import Document
from app.services.createEmbeddings import embed_documents
from app.services.createVectorStore import create_vector_store
from celery import chain

@celery_app.task
def load_pdf_task(docId):
    db = SessionLocal()
    updateDocumentStatus(docId=docId,status="Processing Started",progress=10)
    try:
      pdfDoc = db.query(DbDocument).filter(DbDocument.id == docId).first()
      
      if not pdfDoc:
          return None

          
      loader = PyMuPDFLoader(pdfDoc.doc_url)
      docs = loader.load()
      response = [{
          "page_content":doc.page_content,
          "metadata":doc.metadata
          } for doc in docs]
      return {
          "docId":docId,
          "docs":response
      }
    finally:
        db.close()


@celery_app.task
def create_chunks_task(data):
    
    docId = data["docId"]
    docs = data["docs"]
    updateDocumentStatus(docId=docId,status="Chunking Started",progress=30)
    
    langchain_docs = [
       Document(
            page_content=doc["page_content"],
            metadata=doc["metadata"]
        )
        for doc in docs
    ]
    
    chunks = create_document_chunks(langchain_docs)
    serializedChunks = [
        {
            "page_content":chunk.page_content,
            "metadata":chunk.metadata
        }
        for chunk in chunks
    ]
    return {
        "docChunks":serializedChunks,
        "docId":docId
    }

@celery_app.task
def create_embeddings_task(data):
    docId = data["docId"]
    updateDocumentStatus(docId=docId,status="Embeddings Started",progress=60)
    docChunks = data["docChunks"]
    textChunks = [doc["page_content"] for doc in docChunks]
    embeddings = embed_documents(texts=textChunks)

    serialized_embeddings = [
    embedding.tolist()
    for embedding in embeddings
   ]
    
    return {
        "embeddings":serialized_embeddings,
        "docId":docId,
        "docChunks":docChunks
    }
    

@celery_app.task
def set_vector_store_task(data):
    docId = data["docId"]
    updateDocumentStatus(docId=docId,status="storing vectors....",progress=85)
    embeddings = data["embeddings"]
    docChunks = data["docChunks"]
    chunks = [
        Document(page_content=doc["page_content"],metadata=doc["metadata"])
        for doc in docChunks
    ]
    
    create_vector_store(doc_id=docId,document_chunks=chunks,embeddings=embeddings)
    updateDocumentStatus(docId=docId,status="Vectors stored successfully.",progress=100)
    return True
    

@celery_app.task
def failed_task(request, exc, traceback, doc_id):
    updateDocumentStatus(doc_id, "failed", 0)
    
    
def process_document_pipeline(doc_id):

    workflow = chain(
        load_pdf_task.s(doc_id),
        create_chunks_task.s(),
        create_embeddings_task.s(),
        set_vector_store_task.s()
    )

    workflow.apply_async()