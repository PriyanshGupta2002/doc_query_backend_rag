from pydantic import BaseModel

class ConversationCreate(BaseModel):
    doc_id: int
    title: str | None = None