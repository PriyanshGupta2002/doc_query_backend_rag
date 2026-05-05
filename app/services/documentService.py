from sqlalchemy.orm import Session
from app.models.documentModel import Document

def create_document(db: Session, doc_url: str, user_id: int):
    new_doc = Document(
        doc_url=doc_url,
        user_id=user_id,
        status="processing"
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return new_doc