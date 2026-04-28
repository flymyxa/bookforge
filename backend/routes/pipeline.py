from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import AgentActivityRecord, BookRecord, ChapterRecord, DocumentRecord, PipelineStageRecord
from db.session import get_db
from models.activity import ActivityListResponse
from models.activity_write import ActivityCreate
from models.pipeline import (
    FoundationBuildResponse,
    ChapterWriteResponse,
    PipelineAdvanceResponse,
    PipelineStage,
    PipelineStageUpdate,
)

router = APIRouter()

STAGE_ORDER = {
    "discovery": 10,
    "foundation": 20,
    "summaries": 30,
    "writing": 40,
    "editing": 50,
    "assembly": 60,
}


def sort_stages(stages: list[PipelineStageRecord]) -> list[PipelineStageRecord]:
    return sorted(
        stages,
        key=lambda stage: (STAGE_ORDER.get(stage.stage, 999), stage.updated_at),
    )


def extract_discovery_notes(creative_vision: str) -> list[str]:
    marker = "## Discovery Notes"
    if marker not in creative_vision:
        return []

    _, notes_block = creative_vision.split(marker, 1)
    lines = [line.strip()[2:] for line in notes_block.splitlines() if line.strip().startswith("- ")]
    return [line for line in lines if line]


def build_world_bible(book: BookRecord, notes: list[str]) -> str:
    bullets = "\n".join(f"- {note}" for note in notes) or "- Awaiting discovery detail."
    return (
        f"# WORLD_BIBLE\n\n"
        f"## Premise Anchor\n"
        f"{book.title} is a {book.genre} project shaped by these discovery notes:\n"
        f"{bullets}\n\n"
        f"## World Direction\n"
        f"- Define the governing rules of power, place, and consequence.\n"
        f"- Keep the setting emotionally aligned with the project promise.\n"
        f"- Preserve recurring motifs from the discovery phase.\n"
    )


def build_character_bible(book: BookRecord, notes: list[str]) -> str:
    bullets = "\n".join(f"- {note}" for note in notes) or "- Awaiting character discovery detail."
    return (
        f"# CHARACTER_BIBLE\n\n"
        f"## Project Anchor\n"
        f"- Title: {book.title}\n"
        f"- Genre: {book.genre}\n\n"
        f"## Character Inputs\n"
        f"{bullets}\n\n"
        f"## Character Design Targets\n"
        f"- Clarify protagonist fear, desire, and contradiction.\n"
        f"- Map emotional pressure points for allies and rivals.\n"
        f"- Keep motivations legible inside the commercial genre lane.\n"
    )


def build_chapter_one(
    book: BookRecord,
    creative_vision: str,
    world_bible: str,
    character_bible: str,
) -> tuple[str, str]:
    title = "Chapter 1: The First Blueprint"
    content = (
        f"# {title}\n\n"
        f"{book.title} opens with a protagonist trying to impose order on a hostile world.\n\n"
        f"## Story Intent\n"
        f"- Establish the emotional promise from discovery.\n"
        f"- Introduce the world's governing pressure.\n"
        f"- Show the protagonist reaching for control as an act of care.\n\n"
        f"## Creative Vision Extract\n"
        f"{creative_vision[:500].strip()}\n\n"
        f"## World Bible Extract\n"
        f"{world_bible[:500].strip()}\n\n"
        f"## Character Bible Extract\n"
        f"{character_bible[:500].strip()}\n\n"
        f"The chapter draft is intentionally compact in this MVP, but it is now a persisted manuscript artifact that downstream editing and assembly can consume.\n"
    )
    return title, content


@router.get("/{book_id}", response_model=list[PipelineStage])
async def get_pipeline(book_id: str, db: Session = Depends(get_db)) -> list[PipelineStage]:
    stages = sort_stages(db.scalars(
        select(PipelineStageRecord)
        .where(PipelineStageRecord.book_id == book_id)
    ).all())
    return [
        PipelineStage(
            id=stage.id,
            book_id=stage.book_id,
            stage=stage.stage,
            status=stage.status,
            progress=stage.progress,
        )
        for stage in stages
    ]


@router.get("/{book_id}/activity", response_model=ActivityListResponse)
async def get_pipeline_activity(book_id: str, db: Session = Depends(get_db)) -> ActivityListResponse:
    activities = db.scalars(
        select(AgentActivityRecord)
        .where(AgentActivityRecord.book_id == book_id)
        .order_by(AgentActivityRecord.created_at.asc())
    ).all()
    return ActivityListResponse(book_id=book_id, activity=[activity.message for activity in activities])


@router.patch("/{book_id}/stages/{stage_id}", response_model=PipelineStage)
async def update_pipeline_stage(
    book_id: str,
    stage_id: str,
    payload: PipelineStageUpdate,
    db: Session = Depends(get_db),
) -> PipelineStage:
    stage = db.get(PipelineStageRecord, stage_id)
    if not stage or stage.book_id != book_id:
        raise HTTPException(status_code=404, detail="Pipeline stage not found")

    if payload.status is not None:
        stage.status = payload.status
    if payload.progress is not None:
        stage.progress = max(0, min(100, payload.progress))
    stage.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(stage)

    return PipelineStage(
        id=stage.id,
        book_id=stage.book_id,
        stage=stage.stage,
        status=stage.status,
        progress=stage.progress,
    )


@router.post("/{book_id}/activity", response_model=ActivityListResponse)
async def create_pipeline_activity(
    book_id: str,
    payload: ActivityCreate,
    db: Session = Depends(get_db),
) -> ActivityListResponse:
    book = db.get(BookRecord, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.add(AgentActivityRecord(book_id=book_id, message=payload.message))
    db.commit()

    activities = db.scalars(
        select(AgentActivityRecord)
        .where(AgentActivityRecord.book_id == book_id)
        .order_by(AgentActivityRecord.created_at.asc())
    ).all()
    return ActivityListResponse(book_id=book_id, activity=[activity.message for activity in activities])


@router.post("/{book_id}/advance", response_model=PipelineAdvanceResponse)
async def advance_pipeline(book_id: str, db: Session = Depends(get_db)) -> PipelineAdvanceResponse:
    book = db.get(BookRecord, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    stages = sort_stages(db.scalars(
        select(PipelineStageRecord)
        .where(PipelineStageRecord.book_id == book_id)
    ).all())
    if not stages:
        raise HTTPException(status_code=404, detail="Pipeline stages not found")

    current_stage = next(
        (stage for stage in stages if stage.status in {"running", "blocked"}),
        None,
    )
    if current_stage is None:
        current_stage = next((stage for stage in stages if stage.status != "complete"), stages[-1])

    next_stage_name: str | None = None

    if current_stage.progress < 100:
        current_stage.progress = min(100, current_stage.progress + 25)
        current_stage.status = "complete" if current_stage.progress == 100 else "running"
        current_stage.updated_at = datetime.utcnow()
        db.add(
            AgentActivityRecord(
                book_id=book_id,
                message=f"{current_stage.stage.capitalize()} advanced to {current_stage.progress}%",
            )
        )

    if current_stage.progress == 100:
        current_index = stages.index(current_stage)
        if current_index + 1 < len(stages):
            next_stage = stages[current_index + 1]
            next_stage_name = next_stage.stage
            if next_stage.status == "idle":
                next_stage.status = "running"
                next_stage.progress = max(next_stage.progress, 5)
                next_stage.updated_at = datetime.utcnow()
            book.status = next_stage.stage
            db.add(
                AgentActivityRecord(
                    book_id=book_id,
                    message=f"{current_stage.stage.capitalize()} completed. {next_stage.stage.capitalize()} is now active.",
                )
            )
        else:
            book.status = "complete"
            next_stage_name = None
            db.add(
                AgentActivityRecord(
                    book_id=book_id,
                    message="Pipeline completed.",
                )
            )
    else:
        book.status = current_stage.stage

    db.commit()
    db.refresh(current_stage)
    db.refresh(book)

    return PipelineAdvanceResponse(
        book_id=book_id,
        current_stage=current_stage.stage,
        next_stage=next_stage_name,
        progress=current_stage.progress,
        status=book.status,
    )


@router.post("/{book_id}/foundation/build", response_model=FoundationBuildResponse)
async def build_foundation(book_id: str, db: Session = Depends(get_db)) -> FoundationBuildResponse:
    book = db.get(BookRecord, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    creative_vision = db.scalars(
        select(DocumentRecord).where(
            DocumentRecord.book_id == book_id,
            DocumentRecord.name == "Creative Vision",
        )
    ).first()
    world_bible = db.scalars(
        select(DocumentRecord).where(
            DocumentRecord.book_id == book_id,
            DocumentRecord.name == "World Bible",
        )
    ).first()
    character_bible = db.scalars(
        select(DocumentRecord).where(
            DocumentRecord.book_id == book_id,
            DocumentRecord.name == "Character Bible",
        )
    ).first()
    foundation_stage = db.scalars(
        select(PipelineStageRecord).where(
            PipelineStageRecord.book_id == book_id,
            PipelineStageRecord.stage == "foundation",
        )
    ).first()
    discovery_stage = db.scalars(
        select(PipelineStageRecord).where(
            PipelineStageRecord.book_id == book_id,
            PipelineStageRecord.stage == "discovery",
        )
    ).first()
    writing_stage = db.scalars(
        select(PipelineStageRecord).where(
            PipelineStageRecord.book_id == book_id,
            PipelineStageRecord.stage == "writing",
        )
    ).first()

    if not creative_vision or not creative_vision.content:
        raise HTTPException(status_code=400, detail="Creative Vision must exist before foundation build")

    notes = extract_discovery_notes(creative_vision.content)

    generated_documents: list[str] = []

    if world_bible:
        world_bible.content = build_world_bible(book, notes)
        world_bible.status = "ready"
        generated_documents.append(world_bible.name)

    if character_bible:
        character_bible.content = build_character_bible(book, notes)
        character_bible.status = "ready"
        generated_documents.append(character_bible.name)

    if foundation_stage:
        foundation_stage.status = "complete"
        foundation_stage.progress = 100
        foundation_stage.updated_at = datetime.utcnow()

    if discovery_stage:
        discovery_stage.status = "complete"
        discovery_stage.progress = 100
        discovery_stage.updated_at = datetime.utcnow()

    if writing_stage and writing_stage.status == "idle":
        writing_stage.status = "running"
        writing_stage.progress = max(writing_stage.progress, 5)
        writing_stage.updated_at = datetime.utcnow()

    book.status = "writing" if writing_stage else "foundation"

    db.add_all(
        [
            AgentActivityRecord(book_id=book_id, message="Foundation builder generated World Bible"),
            AgentActivityRecord(book_id=book_id, message="Foundation builder generated Character Bible"),
        ]
    )
    if writing_stage:
        db.add(
            AgentActivityRecord(
                book_id=book_id,
                message="Foundation completed. Writing is now active.",
            )
        )

    db.commit()

    return FoundationBuildResponse(
        book_id=book_id,
        status=book.status,
        generated_documents=generated_documents,
    )


@router.post("/{book_id}/writing/chapter-1", response_model=ChapterWriteResponse)
async def write_chapter_one(book_id: str, db: Session = Depends(get_db)) -> ChapterWriteResponse:
    book = db.get(BookRecord, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    creative_vision = db.scalars(
        select(DocumentRecord).where(
            DocumentRecord.book_id == book_id,
            DocumentRecord.name == "Creative Vision",
        )
    ).first()
    world_bible = db.scalars(
        select(DocumentRecord).where(
            DocumentRecord.book_id == book_id,
            DocumentRecord.name == "World Bible",
        )
    ).first()
    character_bible = db.scalars(
        select(DocumentRecord).where(
            DocumentRecord.book_id == book_id,
            DocumentRecord.name == "Character Bible",
        )
    ).first()
    writing_stage = db.scalars(
        select(PipelineStageRecord).where(
            PipelineStageRecord.book_id == book_id,
            PipelineStageRecord.stage == "writing",
        )
    ).first()
    existing_chapter = db.scalars(
        select(ChapterRecord).where(
            ChapterRecord.book_id == book_id,
            ChapterRecord.number == 1,
        )
    ).first()

    if not creative_vision or not creative_vision.content or not world_bible or not world_bible.content or not character_bible or not character_bible.content:
        raise HTTPException(status_code=400, detail="Foundation documents must be ready before writing Chapter 1")

    title, content = build_chapter_one(
        book,
        creative_vision.content,
        world_bible.content,
        character_bible.content,
    )

    if existing_chapter:
        existing_chapter.title = title
        existing_chapter.content = content
        existing_chapter.status = "ready"
        chapter = existing_chapter
    else:
        chapter = ChapterRecord(
            book_id=book_id,
            number=1,
            title=title,
            status="ready",
            content=content,
        )
        db.add(chapter)

    if writing_stage:
        writing_stage.status = "complete"
        writing_stage.progress = 100
        writing_stage.updated_at = datetime.utcnow()

    book.status = "draft_ready"

    db.add(
        AgentActivityRecord(
            book_id=book_id,
            message="Chapter 1 drafted from Creative Vision, World Bible, and Character Bible.",
        )
    )

    db.commit()
    db.refresh(chapter)

    return ChapterWriteResponse(
        book_id=book_id,
        chapter_id=chapter.id,
        chapter_number=chapter.number,
        status=chapter.status,
    )
