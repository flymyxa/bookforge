from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import ChapterRecord
from db.session import get_db
router = APIRouter()


@router.get("/{book_id}/manuscript")
async def get_manuscript_download(book_id: str) -> dict[str, str]:
    return {
        "book_id": book_id,
        "message": "File download endpoint placeholder. Connect this to storage and assembly output.",
    }


@router.get("/{book_id}/chapters/{chapter_number}")
async def get_chapter_file(book_id: str, chapter_number: int, db: Session = Depends(get_db)) -> dict[str, str]:
    chapter = db.scalars(
        select(ChapterRecord).where(
            ChapterRecord.book_id == book_id,
            ChapterRecord.number == chapter_number,
        )
    ).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    return {
        "book_id": book_id,
        "chapter_id": chapter.id,
        "title": chapter.title,
        "content": chapter.content,
    }
