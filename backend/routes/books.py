from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import AgentActivityRecord, BookRecord, DocumentRecord, PipelineStageRecord
from db.session import get_db
from models.book import BookCreate, BookSummary

router = APIRouter()


@router.get("", response_model=list[BookSummary])
async def list_books(db: Session = Depends(get_db)) -> list[BookSummary]:
    books = db.scalars(select(BookRecord).order_by(BookRecord.created_at.desc())).all()
    return [BookSummary(id=book.id, title=book.title, genre=book.genre, status=book.status) for book in books]


@router.get("/{book_id}", response_model=BookSummary)
async def get_book(book_id: str, db: Session = Depends(get_db)) -> BookSummary:
    book = db.get(BookRecord, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookSummary(id=book.id, title=book.title, genre=book.genre, status=book.status)


@router.post("", response_model=BookSummary)
async def create_book(payload: BookCreate, db: Session = Depends(get_db)) -> BookSummary:
    book = BookRecord(
        title=payload.title,
        genre=payload.genre,
        series=payload.series,
        status="created",
    )
    db.add(book)
    db.flush()

    db.add_all(
        [
            DocumentRecord(book_id=book.id, name="Creative Vision", status="queued"),
            DocumentRecord(book_id=book.id, name="World Bible", status="queued"),
            DocumentRecord(book_id=book.id, name="Character Bible", status="queued"),
            PipelineStageRecord(book_id=book.id, stage="discovery", status="running", progress=5),
            PipelineStageRecord(book_id=book.id, stage="foundation", status="idle", progress=0),
            PipelineStageRecord(book_id=book.id, stage="writing", status="idle", progress=0),
            AgentActivityRecord(book_id=book.id, message="Book record created"),
        ]
    )
    db.commit()
    db.refresh(book)

    return BookSummary(id=book.id, title=book.title, genre=book.genre, status=book.status)
