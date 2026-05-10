# app/routes/documentRoute.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import SessionLocal
from app.services.documentService import create_document,fetch_docs,fetch_doc
from app.tasks.document_tasks import process_document_pipeline
from app.core.dependencies import get_current_user
from app.services.getDocumentStatusService import getDocumentStatus
from app.schemas.responseSchema import responseModel
from app.schemas.documentResponseSchema import ApiResponse

router = APIRouter(prefix="/documents", tags=["Documents"])


class DocumentCreate(BaseModel):
    doc_url: str
    name:str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload", response_model=responseModel)
def upload_document(
    payload: DocumentCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),
):
    doc = create_document(db, payload.doc_url, user_id,payload.name)
    process_document_pipeline(doc_id=doc.id)

    return responseModel(
        message="Document uploaded successfully",
        success=True,
        data={"id": doc.id, "status": doc.status,"name":doc.name},
    )


@router.get("/{doc_id}/status")
def get_document_status(
    doc_id: int,
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user),
):
    status = getDocumentStatus(docId=doc_id, db=db, user_id=user_id)

    return responseModel(
        message="Document status fetched successfully",
        success=True,
        data={"status": status},
    )

@router.get("/",response_model=ApiResponse)
def fetch_documents(
        user_id=Depends(get_current_user),
        db:Session=Depends(get_db),
        page:int=1,
        limit:int=10
):
    docs = fetch_docs(user_id=user_id,db=db,limit=limit,page=page)
    return ApiResponse(
        message="Documents fetched successfully",
        success=True,
        data=docs
    )

@router.get("/{doc_id}",response_model=responseModel)
def fetch_doc_url(
    doc_id:int,
    user_id=Depends(get_current_user),
    db:Session=Depends(get_db)
    
):
    url = fetch_doc(db=db,doc_id=doc_id,user_id=user_id)
    return responseModel(
        message="Doc fetched successfully",
        data={
            "url":url
        },
        success=True
    )

