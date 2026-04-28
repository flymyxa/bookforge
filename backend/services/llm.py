class LLMService:
    """Anthropic wrapper placeholder."""

    async def complete(self, prompt: str) -> dict[str, str]:
        return {"provider": "anthropic", "content": prompt}
