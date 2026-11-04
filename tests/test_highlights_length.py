"""
test_highlights_length.py
=========================
Programmatic verification of research highlights across Markdown and Word DOCX formats:
1. Markdown: manuscript/highlights.md
2. Word DOCX: manuscript/submission_package/highlights.docx

Elsevier Applied Geography Guide for Authors Requirement:
- Highlights are mandatory for this journal.
- They must consist of 3 to 5 bullet points.
- Each bullet point must not exceed 85 characters including spaces.
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MD_HIGHLIGHTS_PATH = os.path.join(REPO_ROOT, "manuscript", "highlights.md")
DOCX_HIGHLIGHTS_PATH = os.path.join(REPO_ROOT, "manuscript", "submission_package", "highlights.docx")

MIN_BULLETS = 3
MAX_BULLETS = 5
MAX_CHARACTERS = 85
MIN_CHARACTERS = 20  # Sanity check to prevent empty or truncated bullets


def get_markdown_highlights() -> list[str]:
    """Parse bullet points from Markdown highlights file."""
    assert os.path.exists(MD_HIGHLIGHTS_PATH), f"Highlights file not found: {MD_HIGHLIGHTS_PATH}"
    with open(MD_HIGHLIGHTS_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    bullets = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("*", "-")):
            # Remove leading marker and excess whitespace
            bullet = stripped.lstrip("*-").strip()
            if bullet:
                bullets.append(bullet)

    return bullets


def get_docx_highlights() -> list[str]:
    """Parse bullet points from Word DOCX highlights file."""
    assert os.path.exists(DOCX_HIGHLIGHTS_PATH), f"Highlights DOCX not found: {DOCX_HIGHLIGHTS_PATH}"
    with zipfile.ZipFile(DOCX_HIGHLIGHTS_PATH) as z:
        doc_xml = z.read("word/document.xml")

    root = ET.fromstring(doc_xml)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    bullets = []
    for p in root.findall(".//w:p", ns):
        text = "".join([t.text for t in p.findall(".//w:t", ns) if t.text]).strip()
        # Exclude headers like 'Research Highlights'
        if text and not text.lower().startswith("research highlights"):
            bullets.append(text)

    return bullets


def test_markdown_highlights_count():
    """Verify that Markdown highlights contain between 3 and 5 bullet points."""
    bullets = get_markdown_highlights()
    count = len(bullets)
    print(f"\n[Markdown Highlights] Bullet count: {count}")
    assert MIN_BULLETS <= count <= MAX_BULLETS, (
        f"Markdown highlights count ({count}) must be between {MIN_BULLETS} and {MAX_BULLETS}!"
    )


def test_markdown_highlights_character_length():
    """Verify that every Markdown bullet point is strictly <= 85 characters including spaces."""
    bullets = get_markdown_highlights()
    print(f"\n[Markdown Highlights] Character lengths:")
    for idx, bullet in enumerate(bullets, 1):
        char_len = len(bullet)
        print(f"  Bullet {idx} ({char_len:2d} chars): {bullet}")
        assert char_len >= MIN_CHARACTERS, (
            f"Markdown Bullet {idx} is suspiciously short ({char_len} chars): '{bullet}'"
        )
        assert char_len <= MAX_CHARACTERS, (
            f"Markdown Bullet {idx} exceeds {MAX_CHARACTERS} characters ({char_len} chars): '{bullet}'"
        )


def test_docx_highlights_count():
    """Verify that Word DOCX highlights contain between 3 and 5 bullet points."""
    bullets = get_docx_highlights()
    count = len(bullets)
    print(f"\n[DOCX Highlights] Bullet count: {count}")
    assert MIN_BULLETS <= count <= MAX_BULLETS, (
        f"DOCX highlights count ({count}) must be between {MIN_BULLETS} and {MAX_BULLETS}!"
    )


def test_docx_highlights_character_length():
    """Verify that every Word DOCX bullet point is strictly <= 85 characters including spaces."""
    bullets = get_docx_highlights()
    print(f"\n[DOCX Highlights] Character lengths:")
    for idx, bullet in enumerate(bullets, 1):
        char_len = len(bullet)
        print(f"  Bullet {idx} ({char_len:2d} chars): {bullet}")
        assert char_len >= MIN_CHARACTERS, (
            f"DOCX Bullet {idx} is suspiciously short ({char_len} chars): '{bullet}'"
        )
        assert char_len <= MAX_CHARACTERS, (
            f"DOCX Bullet {idx} exceeds {MAX_CHARACTERS} characters ({char_len} chars): '{bullet}'"
        )


def test_highlights_cross_format_parity():
    """Verify that Markdown and DOCX highlights match in count and length."""
    md_bullets = get_markdown_highlights()
    docx_bullets = get_docx_highlights()

    assert len(md_bullets) == len(docx_bullets), (
        f"Bullet count mismatch: Markdown ({len(md_bullets)}) vs DOCX ({len(docx_bullets)})"
    )

    print("\n[Cross-Format Parity Check]")
    for i, (mb, db) in enumerate(zip(md_bullets, docx_bullets), 1):
        # Normalize typographic quotes or dashes for direct comparison
        norm_mb = mb.replace("'", "'").replace("'", "'")
        norm_db = db.replace("’", "'").replace("‘", "'")
        print(f"  Bullet {i}: MD {len(mb)} chars, DOCX {len(db)} chars")
        assert len(mb) <= MAX_CHARACTERS and len(db) <= MAX_CHARACTERS
        assert norm_mb.lower() == norm_db.lower(), (
            f"Bullet {i} text mismatch between formats:\n  MD:   {mb}\n  DOCX: {db}"
        )


if __name__ == "__main__":
    print("=" * 65)
    print("RUNNING HIGHLIGHTS LENGTH VERIFICATION SUITE")
    print("=" * 65)
    test_markdown_highlights_count()
    test_markdown_highlights_character_length()
    test_docx_highlights_count()
    test_docx_highlights_character_length()
    test_highlights_cross_format_parity()
    print("\n>>> ALL HIGHLIGHTS LENGTH TESTS PASSED (100% COMPLIANT) <<<")
