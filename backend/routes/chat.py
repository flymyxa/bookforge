from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import AgentActivityRecord, BookRecord, ChatMessageRecord, DocumentRecord, PipelineStageRecord
from db.session import get_db
from models.chat import ChatMessage, ChatMessageCreate, ChatResponse

router = APIRouter()


def serialize_messages(messages: list[ChatMessageRecord]) -> list[ChatMessage]:
    return [
        ChatMessage(id=message.id, role=message.role, content=message.content)
        for message in messages
    ]


def build_creative_vision(book: BookRecord, user_messages: list[ChatMessageRecord]) -> str:
    discovery_points = "\n".join(
        f"- {message.content.strip()}" for message in user_messages if message.content.strip()
    )
    return (
        f"# CREATIVE_VISION\n\n"
        f"## Project\n"
        f"- Title: {book.title}\n"
        f"- Genre: {book.genre}\n"
        f"- Series: {book.series or 'Standalone / not set'}\n\n"
        f"## Discovery Notes\n"
        f"{discovery_points or '- Awaiting discovery input.'}\n"
    )


@router.get("/{book_id}", response_model=ChatResponse)
async def get_chat_messages(book_id: str, db: Session = Depends(get_db)) -> ChatResponse:
    book = db.get(BookRecord, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    messages = db.scalars(
        select(ChatMessageRecord)
        .where(ChatMessageRecord.book_id == book_id)
        .order_by(ChatMessageRecord.created_at.asc())
    ).all()
    return ChatResponse(book_id=book_id, messages=serialize_messages(messages))


@router.post("/{book_id}", response_model=ChatResponse)
async def chat(book_id: str, payload: ChatMessageCreate, db: Session = Depends(get_db)) -> ChatResponse:
    book = db.get(BookRecord, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    cleaned_message = payload.message.strip()
    user_message = ChatMessageRecord(book_id=book_id, role="user", content=cleaned_message)
    assistant_reply = ChatMessageRecord(
        book_id=book_id,
        role="assistant",
        content=f"Discovery note captured: {cleaned_message}",
    )
    db.add_all([user_message, assistant_reply])

    discovery_stage = db.scalars(
        select(PipelineStageRecord)
        .where(
            PipelineStageRecord.book_id == book_id,
            PipelineStageRecord.stage == "discovery",
        )
    ).first()
    foundation_stage = db.scalars(
        select(PipelineStageRecord)
        .where(
            PipelineStageRecord.book_id == book_id,
            PipelineStageRecord.stage == "foundation",
        )
    ).first()
    creative_vision = db.scalars(
        select(DocumentRecord)
        .where(
            DocumentRecord.book_id == book_id,
            DocumentRecord.name == "Creative Vision",
        )
    ).first()

    db.flush()

    all_user_messages = db.scalars(
        select(ChatMessageRecord)
        .where(
            ChatMessageRecord.book_id == book_id,
            ChatMessageRecord.role == "user",
        )
        .order_by(ChatMessageRecord.created_at.asc())
    ).all()

    if creative_vision:
        creative_vision.status = "ready"
        creative_vision.content = build_creative_vision(book, all_user_messages)

    if discovery_stage:
        was_complete = discovery_stage.status == "complete" or discovery_stage.progress == 100
        discovery_stage.progress = min(100, max(discovery_stage.progress, 20) + 20)
        discovery_stage.status = "complete" if discovery_stage.progress == 100 else "running"
        discovery_stage.updated_at = datetime.utcnow()
    else:
        was_complete = False

    book.status = "discovery"

    db.add(
        AgentActivityRecord(
            book_id=book_id,
            message="Discovery note appended to Creative Vision",
        )
    )

    if discovery_stage and discovery_stage.progress == 100 and foundation_stage and not was_complete:
        foundation_stage.status = "running" if foundation_stage.status == "idle" else foundation_stage.status
        foundation_stage.progress = max(foundation_stage.progress, 5)
        foundation_stage.updated_at = datetime.utcnow()
        book.status = "foundation"
        db.add(
            AgentActivityRecord(
                book_id=book_id,
                message="Discovery is complete. Foundation is now active.",
            )
        )

    db.commit()

    messages = db.scalars(
        select(ChatMessageRecord)
        .where(ChatMessageRecord.book_id == book_id)
        .order_by(ChatMessageRecord.created_at.asc())
    ).all()
    return ChatResponse(book_id=book_id, messages=serialize_messages(messages))
