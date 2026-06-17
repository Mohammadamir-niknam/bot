"""Security validation helpers."""
from __future__ import annotations
from pathlib import Path
from html import escape

def sanitize_text(value: str, limit: int = 4096) -> str:
    return escape(value.strip()[:limit])

def is_allowed_image(filename: str | None, allowed: tuple[str, ...]) -> bool:
    if not filename:
        return False
    return Path(filename).suffix.lower().lstrip(".") in allowed
