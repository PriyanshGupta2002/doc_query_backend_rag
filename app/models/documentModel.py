from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.db.session import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    doc_url = Column(String(500), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    status = Column(String(50), default="processing")

    created_at = Column(DateTime, default=datetime.now)
    
    progress = Column(Integer, default=0)

    name = Column(String(16))