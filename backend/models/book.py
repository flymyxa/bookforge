from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    genre: str = Field(min_length=1, max_length=120)
    series: str | None = Field(default=None, max_length=200)


class BookSummary(BaseModel):
    id: str
    title: str
    genre: str
    status: str
