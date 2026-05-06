import fitz  # PyMuPDF
import re
from pathlib import Path
from typing import Any


def clean_text(text: str) -> str:
    """Remove control characters that can break JSON/LLMs."""
    # Removes ASCII control characters except \n, \r, \t
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)


def extract_pages(pdf_path: Path) -> list[dict[str, Any]]:
    """
    Extract text page-by-page from a PDF.
    Returns a list of dicts: {page_number: int, text: str}.
    Blank pages are skipped.
    """
    doc = fitz.open(str(pdf_path))
    pages: list[dict[str, Any]] = []

    for page_index in range(len(doc)):
        page = doc[page_index]
        text = page.get_text()
        text = clean_text(text)
        if text.strip():
            pages.append({"page_number": page_index + 1, "text": text.strip()})

    doc.close()
    return pages
