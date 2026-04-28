from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    id: str
    role: str
    content: str


class ChatMessageCreate(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    book_id: str
    messages: list[ChatMessage]
