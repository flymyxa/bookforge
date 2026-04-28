from pathlib import Path


class AssemblyService:
    """Skeleton for manuscript assembly using python-docx."""

    async def assemble(self, output_path: str) -> Path:
        return Path(output_path)
