class StorageService:
    """Supabase storage wrapper placeholder."""

    async def put_text(self, path: str, content: str) -> dict[str, str]:
        return {"path": path, "status": "stubbed", "content_preview": content[:80]}
