from sqlalchemy.orm import Session
from app.models.chat import Chat


def save_chat(
    db: Session,
    conversation_id: int,
    query: str,
    answer: str
):
    chat = Chat(
        conversation_id=conversation_id,
        query=query,
        answer=answer
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat


def fetch_chat(
    db: Session,
    conversation_id: int,
    page: int = 1,
    limit: int = 20
):
    skip = (page - 1) * limit

    chats = (
        db.query(Chat)
        .filter(Chat.conversation_id == conversation_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    total_chats = (
        db.query(Chat)
        .filter(Chat.conversation_id == conversation_id)
        .count()
    )

    return {
        "success": True,
        "data": {
            "chats": chats,
            "count": total_chats
        }
    }