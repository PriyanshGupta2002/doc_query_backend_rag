from pydantic import BaseModel

class ChatCreate(BaseModel):
    conversation_id: int
    query: str

class ChatResponse(BaseModel):
    id: int
    query: str

    class Config:
        orm_mode = True