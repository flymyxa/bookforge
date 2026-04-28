from pydantic import BaseModel, Field


class ActivityCreate(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
