from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.chatSchema import ChatCreate
from app.services.chatService import save_chat
from app.services.search import search
from app.db.session import SessionLocal
from app.models.conversationModel import Conversation
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def chat(
    payload: ChatCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)  # 🔐 protect route
):
    # 🔥 1. fetch conversation
    conversation = db.query(Conversation).filter(
        Conversation.id == payload.conversation_id,
        Conversation.user_id == user_id   # 🔥 ownership check
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # 🔥 2. extract doc_id
    doc_id = conversation.doc_id

    # 🔥 3. generate answer
    answer = search(
        doc_id=doc_id,
        query=payload.query
    )

    # 🔥 4. save chat
    chat = save_chat(
        db=db,
        conversation_id=payload.conversation_id,
        query=payload.query,
        answer=answer
    )

    return {
        "message": "Chat saved",
        "success": True,
        "data": {
            "query": chat.query,
            "answer": chat.answer
        }
    }