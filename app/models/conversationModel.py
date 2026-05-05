from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from datetime import datetime
from app.db.session import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doc_id = Column(Integer, ForeignKey("documents.id"), nullable=False)

    title = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.now)