from pydantic import BaseModel


class ActivityListResponse(BaseModel):
    book_id: str
    activity: list[str]
