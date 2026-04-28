from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import AgentActivityRecord, BookRecord, ChatMessageRecord, DocumentRecord, PipelineStageRecord


def seed_demo_data(db: Session) -> None:
    existing = db.scalar(select(BookRecord.id).limit(1))
    if existing:
        return

    db.add_all(
        [
            BookRecord(id="demo", title="Dungeon Seed Protocol", genre="LitRPG", status="discovery"),
            BookRecord(id="ghost-market", title="The Ghost Market Index", genre="Non-fiction", status="foundation"),
        ]
    )
    db.flush()

    db.add_all(
        [
            DocumentRecord(book_id="demo", name="Creative Vision", status="ready"),
            DocumentRecord(book_id="demo", name="World Bible", status="queued"),
            DocumentRecord(book_id="demo", name="Character Bible", status="queued"),
            DocumentRecord(book_id="ghost-market", name="Creative Vision", status="ready"),
        ]
    )
    db.add_all(
        [
            PipelineStageRecord(book_id="demo", stage="discovery", status="complete", progress=100),
            PipelineStageRecord(book_id="demo", stage="foundation", status="running", progress=40),
            PipelineStageRecord(book_id="demo", stage="writing", status="idle", progress=0),
            PipelineStageRecord(book_id="ghost-market", stage="discovery", status="complete", progress=100),
            PipelineStageRecord(book_id="ghost-market", stage="foundation", status="running", progress=65),
        ]
    )
    db.add_all(
        [
            AgentActivityRecord(book_id="demo", message="Kate generated Creative Vision"),
            AgentActivityRecord(book_id="demo", message="Ruth seeded canon ledger"),
            AgentActivityRecord(book_id="demo", message="Foundation builder is drafting the world bible"),
            AgentActivityRecord(book_id="ghost-market", message="Discovery answers were synthesized into Creative Vision"),
        ]
    )
    db.add_all(
        [
            ChatMessageRecord(book_id="demo", role="assistant", content="Tell me about the emotional core of the series."),
            ChatMessageRecord(book_id="demo", role="user", content="A stranded dungeon architect builds a city inside a dead god."),
            ChatMessageRecord(book_id="ghost-market", role="assistant", content="What reader problem does this book solve?"),
        ]
    )
    db.commit()
