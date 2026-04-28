class StageRunner:
    """Executes one stage at a time. Real implementation will call prompts, storage, and gating."""

    async def run(self, stage_name: str, book_id: str) -> dict[str, str]:
        return {
            "book_id": book_id,
            "stage_name": stage_name,
            "status": "not_implemented",
        }
