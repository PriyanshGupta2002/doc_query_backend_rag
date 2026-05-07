from sqlalchemy.orm import Session
from app.models.documentModel import Document


def getDocumentStatus(docId: int, db: Session, user_id: int):
    try:
        document = (
            db.query(Document)
            .filter(Document.id == docId, Document.user_id == user_id)
            .first()
        )
        return document.status
    finally:
        db.close()
