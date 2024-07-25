# app/models.py
from typing import List
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    messages: List[Message]
    temperature: float
    max_tokens: int = 2048
    stream: bool = False

class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    choices: List[dict]