from pydantic import BaseModel


class PipelineStage(BaseModel):
    id: str
    book_id: str
    stage: str
    status: str
    progress: int


class PipelineStageUpdate(BaseModel):
    status: str | None = None
    progress: int | None = None


class PipelineAdvanceResponse(BaseModel):
    book_id: str
    current_stage: str | None
    next_stage: str | None
    progress: int
    status: str


class FoundationBuildResponse(BaseModel):
    book_id: str
    status: str
    generated_documents: list[str]


class ChapterWriteResponse(BaseModel):
    book_id: str
    chapter_id: str
    chapter_number: int
    status: str
