import re
from typing import Iterable

MULTISPACE = re.compile(r"\s+")


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\u00a0", " ")
    text = MULTISPACE.sub(" ", text)
    text = text.strip()
    return text


def split_sentences(text: str) -> list[str]:
    # Lightweight sentence splitter to avoid heavy model downloads
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", text)
    return [p.strip() for p in parts if p.strip()]


def iter_nonempty(lines: Iterable[str]) -> Iterable[str]:
    for line in lines:
        s = line.strip()
        if s:
            yield s