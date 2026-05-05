from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.conversationSchema import ConversationCreate
from app.services.createCoversationService import create_conversation
from app.core.dependencies import get_current_user
from app.db.session import SessionLocal

router = APIRouter(prefix="/conversations", tags=["Conversation"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_conv(
    payload: ConversationCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    convo = create_conversation(
        db=db,
        user_id=user_id,
        doc_id=payload.doc_id,
        title=payload.title
    )

    return {
        "message": "Conversation created",
        "data": {"conversation_id": convo.id}
    }