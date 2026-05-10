from pydantic import BaseModel
from typing import List


class DocumentResponse(BaseModel):
    id: int
    doc_url: str
    user_id: int
    status: str
    progress:int
    name:str

    class Config:
        from_attributes = True


class DocsDataResponse(BaseModel):
    docs: List[DocumentResponse]
    count: int


class ApiResponse(BaseModel):
    success: bool
    message:str
    data: DocsDataResponse