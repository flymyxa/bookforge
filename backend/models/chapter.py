from pydantic import BaseModel


class ChapterSummary(BaseModel):
    id: str
    book_id: str
    number: int
    title: str
    status: str


class ChapterDetail(BaseModel):
    id: str
    book_id: str
    number: int
    title: str
    status: str
    content: str
