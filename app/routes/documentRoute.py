# app/routes/documentRoute.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import SessionLocal
from app.services.documentService import create_document
from app.services.procesPdfService import ProcessDocuments
from app.core.dependencies import get_current_user
from fastapi import BackgroundTasks
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
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    doc = create_document(db, payload.doc_url, user_id)
    background_tasks.add_task(ProcessDocuments,doc.id)

    return {
        "message": "Document uploaded successfully",
        "success": True,
        "data": {
            "id": doc.id,
            "status": doc.status
        }
    }