from sqlalchemy.orm import Session
from app.models.documentModel import Document
from sqlalchemy import desc

def create_document(db: Session, doc_url: str, user_id: int,name:str):
    new_doc = Document(
        doc_url=doc_url,
        user_id=user_id,
        name=name,
        status="processing"
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return new_doc


def fetch_docs(db:Session,user_id:int,page:int=1,limit:int=10):

    total_docs = db.query(Document).filter(Document.user_id==user_id).count()
    skip = (page-1) * limit
    docs = (
        db.query(Document).
        filter(Document.user_id == user_id)
        .order_by(desc(Document.created_at))
        .offset(skip)
        .limit(limit=limit)
        .all()
    )
    return {
        "docs":docs,
        "count":total_docs
    }

def fetch_doc(db:Session,user_id:int,doc_id:int):
    doc = db.query(Document).filter(Document.user_id==user_id,Document.id==doc_id).first()
    return doc.doc_url