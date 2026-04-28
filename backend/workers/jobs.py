async def run_pipeline_job(ctx: dict, book_id: str) -> dict[str, str]:
    return {
        "book_id": book_id,
        "status": "queued_worker_not_connected",
    }
