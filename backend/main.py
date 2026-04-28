from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from db.base import Base
from db.seed import seed_demo_data
from db.session import SessionLocal, engine
from routes import books, chat, documents, files, pipeline

app = FastAPI(title="BookForge API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router, prefix="/v1/books", tags=["books"])
app.include_router(pipeline.router, prefix="/v1/pipeline", tags=["pipeline"])
app.include_router(chat.router, prefix="/v1/chat", tags=["chat"])
app.include_router(documents.router, prefix="/v1/documents", tags=["documents"])
app.include_router(files.router, prefix="/v1/files", tags=["files"])


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_demo_data(db)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.app_env}
