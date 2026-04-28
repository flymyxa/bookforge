from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import DocumentRecord
from db.session import get_db
from models.document import DocumentDetail, DocumentListResponse, DocumentSummary

router = APIRouter()


@router.get("/{book_id}", response_model=DocumentListResponse)
async def list_documents(book_id: str, db: Session = Depends(get_db)) -> DocumentListResponse:
    documents = db.scalars(
        select(DocumentRecord)
        .where(DocumentRecord.book_id == book_id)
        .order_by(DocumentRecord.created_at.asc())
    ).all()
    return DocumentListResponse(
        book_id=book_id,
        documents=[
            DocumentSummary(id=document.id, name=document.name, status=document.status)
            for document in documents
        ],
    )


@router.get("/{book_id}/{document_id}", response_model=DocumentDetail)
async def get_document(book_id: str, document_id: str, db: Session = Depends(get_db)) -> DocumentDetail:
    document = db.get(DocumentRecord, document_id)
    if not document or document.book_id != book_id:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Document not found")

    return DocumentDetail(
        id=document.id,
        book_id=document.book_id,
        name=document.name,
        status=document.status,
        content=document.content,
    )
