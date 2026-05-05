from sqlalchemy.orm import Session
from app.models.chat import Chat

def create_chat(db: Session, conversation_id: int, query: str, answer: str):
    chat = Chat(
        conversation_id=conversation_id,
        query=query,
        answer=answer
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat