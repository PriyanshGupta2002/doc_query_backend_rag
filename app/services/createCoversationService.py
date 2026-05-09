from sqlalchemy.orm import Session
from app.models.conversationModel import Conversation


def create_conversation(db: Session, user_id: int, doc_id: int, title: str = None):
    # check if conversation already exists
    existing_conversation = db.query(Conversation).filter(
        Conversation.doc_id == doc_id, Conversation.user_id == user_id
    ).first()
    if existing_conversation:
        return existing_conversation
    convo = Conversation(user_id=user_id, doc_id=doc_id, title=title)
    db.add(convo)
    db.commit()
    db.refresh(convo)

    return convo
