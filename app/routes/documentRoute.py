# app/routes/documentRoute.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import SessionLocal
from app.services.documentService import create_document
from app.tasks.document_tasks import process_document_pipeline
from app.core.dependencies import get_current_user
from app.services.getDocumentStatusService import getDocumentStatus

router = APIRouter(prefix="/documents", tags=["Documents"])


class DocumentCreate(BaseModel):
    doc_url: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload")
def upload_document(
    payload: DocumentCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    doc = create_document(db, payload.doc_url, user_id)
    process_document_pipeline(doc_id=doc.id)

    return {
        "message": "Document uploaded successfully",
        "success": True,
        "data": {"id": doc.id, "status": doc.status},
    }


@router.get("/{doc_id}/status")
def get_document_status(
    doc_id: int,
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user),
):
    status = getDocumentStatus(docId=doc_id, db=db, user_id=user_id)
    return {"status": status}
