from pydantic import BaseModel
from typing import Optional

class ChatMessage(BaseModel):
    content: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    message: str
    session_id: str

class UploadResponse(BaseModel):
    status: str
    message: str
    file_name: Optional[str] = None
