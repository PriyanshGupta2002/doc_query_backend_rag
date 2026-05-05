from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.db.session import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)

    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)

    query = Column(String(1000), nullable=False)
    answer = Column(String(5000), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)