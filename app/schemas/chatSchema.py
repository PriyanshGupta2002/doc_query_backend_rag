from pydantic import BaseModel
from typing import List


class ChatCreate(BaseModel):
    conversation_id: int
    query: str


class ChatResponse(BaseModel):
    id: int
    conversation_id: int
    query: str
    answer: str

    class Config:
        from_attributes = True


class ChatDataResponse(BaseModel):
    chats: List[ChatResponse]
    count: int


class ChatApiResponse(BaseModel):
    success: bool
    data: ChatDataResponse