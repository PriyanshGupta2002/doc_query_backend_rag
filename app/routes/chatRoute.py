from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.chatSchema import ChatCreate,ChatApiResponse
from app.services.chatService import save_chat,fetch_chat
from app.services.search import search
from app.db.session import SessionLocal
from app.models.conversationModel import Conversation
from app.core.dependencies import get_current_user
from app.schemas.responseSchema import responseModel

router = APIRouter(prefix="/chat", tags=["Chat"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=responseModel)
def chat(
    payload: ChatCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user),  # 🔐 protect route
):
    # 🔥 1. fetch conversation
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == payload.conversation_id,
            Conversation.user_id == user_id,  # 🔥 ownership check
        )
        .first()
    )

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # 🔥 2. extract doc_id
    doc_id = conversation.doc_id

    # 🔥 3. generate answer
    answer = search(doc_id=doc_id, query=payload.query)

    # 🔥 4. save chat
    chat = save_chat(
        db=db,
        conversation_id=payload.conversation_id,
        query=payload.query,
        answer=answer,
    )

    return responseModel(
        data={
            "query": chat.query,
            "answer": chat.answer,
            "id": chat.id,
            "created_at": chat.created_at,
        },
        message="Chat created successfully",
        success=True,
    )

@router.get(
    "/{conversation_id}",
    response_model=ChatApiResponse
)
def get_chats(
    conversation_id: int,
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return fetch_chat(
        db=db,
        conversation_id=conversation_id,
        page=page,
        limit=limit
    )