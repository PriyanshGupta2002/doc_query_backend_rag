from app.db.session import SessionLocal
from app.models.documentModel import Document


def updateDocumentStatus(progress: int, docId: int, status: str):
    db = SessionLocal()
    document = db.query(Document).filter(Document.id == docId).first()
    try:
        if document:
            document.status = status
            document.progress = progress
            db.commit()
    finally:
        db.close()
