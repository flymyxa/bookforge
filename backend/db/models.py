from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


def make_id() -> str:
    return uuid4().hex


class BookRecord(Base):
    __tablename__ = "books"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=make_id)
    title: Mapped[str] = mapped_column(String(200))
    genre: Mapped[str] = mapped_column(String(120))
    series: Mapped[str | None] = mapped_column(String(200), nullable=True)
    status: Mapped[str] = mapped_column(String(64), default="discovery")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    documents: Mapped[list["DocumentRecord"]] = relationship(back_populates="book", cascade="all, delete-orphan")
    pipeline_stages: Mapped[list["PipelineStageRecord"]] = relationship(back_populates="book", cascade="all, delete-orphan")
    activities: Mapped[list["AgentActivityRecord"]] = relationship(back_populates="book", cascade="all, delete-orphan")
    chat_messages: Mapped[list["ChatMessageRecord"]] = relationship(back_populates="book", cascade="all, delete-orphan")
    chapters: Mapped[list["ChapterRecord"]] = relationship(back_populates="book", cascade="all, delete-orphan")


class DocumentRecord(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=make_id)
    book_id: Mapped[str] = mapped_column(ForeignKey("books.id"))
    name: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(64), default="queued")
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    book: Mapped[BookRecord] = relationship(back_populates="documents")


class PipelineStageRecord(Base):
    __tablename__ = "pipeline_stages"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=make_id)
    book_id: Mapped[str] = mapped_column(ForeignKey("books.id"))
    stage: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(64), default="idle")
    progress: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    book: Mapped[BookRecord] = relationship(back_populates="pipeline_stages")


class AgentActivityRecord(Base):
    __tablename__ = "agent_activities"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=make_id)
    book_id: Mapped[str] = mapped_column(ForeignKey("books.id"))
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    book: Mapped[BookRecord] = relationship(back_populates="activities")


class ChatMessageRecord(Base):
    __tablename__ = "chat_messages"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=make_id)
    book_id: Mapped[str] = mapped_column(ForeignKey("books.id"))
    role: Mapped[str] = mapped_column(String(32))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    book: Mapped[BookRecord] = relationship(back_populates="chat_messages")


class ChapterRecord(Base):
    __tablename__ = "chapters"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=make_id)
    book_id: Mapped[str] = mapped_column(ForeignKey("books.id"))
    number: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(64), default="draft")
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    book: Mapped[BookRecord] = relationship(back_populates="chapters")
