from pydantic import BaseModel


class DocumentSummary(BaseModel):
    id: str
    name: str
    status: str


class DocumentListResponse(BaseModel):
    book_id: str
    documents: list[DocumentSummary]


class DocumentDetail(BaseModel):
    id: str
    book_id: str
    name: str
    status: str
    content: str | None
