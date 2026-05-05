from sqlalchemy.orm import Session
from app.models.conversationModel import Conversation

def create_conversation(db: Session, user_id: int, doc_id: int, title: str = None):
    convo = Conversation(
        user_id=user_id,
        doc_id=doc_id,
        title=title
    )

    db.add(convo)
    db.commit()
    db.refresh(convo)

    return convo