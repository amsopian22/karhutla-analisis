"""
test_abstract_word_count.py
===========================
Programmatic verification of abstract word count across ALL manuscript formats:
1. LaTeX: manuscript/sections/00_abstract.tex
2. Markdown: manuscript/manuscript_draft.md
3. Word DOCX: manuscript/submission_package/manuscript_main.docx
4. PDF: manuscript/main.pdf

Elsevier Applied Geography Guide for Authors Requirement:
- Abstract word count must not exceed 250 words (strictly <= 250 words).
"""

import os
import re
import subprocess
import zipfile
import xml.etree.ElementTree as ET
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LATEX_ABSTRACT_PATH = os.path.join(REPO_ROOT, "manuscript", "sections", "00_abstract.tex")
MARKDOWN_DRAFT_PATH = os.path.join(REPO_ROOT, "manuscript", "manuscript_draft.md")
DOCX_MANUSCRIPT_PATH = os.path.join(REPO_ROOT, "manuscript", "submission_package", "manuscript_main.docx")
PDF_MANUSCRIPT_PATH = os.path.join(REPO_ROOT, "manuscript", "main.pdf")

MAX_ABSTRACT_WORDS = 250
MIN_ABSTRACT_WORDS = 150  # Sanity lower bound to ensure non-empty extraction


def clean_words(text: str) -> list[str]:
    """Tokenize clean words, stripping punctuation and whitespace."""
    # Replace non-word tokens (excluding hyphens inside words)
    cleaned = re.sub(r"[^\w\s-]", " ", text)
    return [w for w in cleaned.split() if w]


def get_latex_abstract_text() -> str:
    """Extract clean abstract body from LaTeX source."""
    assert os.path.exists(LATEX_ABSTRACT_PATH), f"LaTeX abstract not found: {LATEX_ABSTRACT_PATH}"
    with open(LATEX_ABSTRACT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(
        r"\\begin\{abstract\}(.*?)(?:\\vspace|\\noindent\\textbf\{Keywords:\}|\\end\{abstract\})",
        content,
        re.DOTALL,
    )
    assert match, "Failed to match abstract block in LaTeX source"
    raw_abstract = match.group(1)

    # Strip LaTeX commands like \noindent, \texttt{...}, \textit{...}, math $...$, etc.
    text = re.sub(r"\\[a-zA-Z]+(\[[^\]]*\])?(\{([^}]*)\})?", r" \3 ", raw_abstract)
    text = re.sub(r"[{}\$~%\\`'\"]", " ", text)
    return text.strip()


def get_markdown_abstract_text() -> str:
    """Extract clean abstract body from Markdown draft."""
    assert os.path.exists(MARKDOWN_DRAFT_PATH), f"Markdown draft not found: {MARKDOWN_DRAFT_PATH}"
    with open(MARKDOWN_DRAFT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(
        r"## Abstract\s+(.*?)\s+\*\*Keywords:\*\*",
        content,
        re.DOTALL,
    )
    assert match, "Failed to match abstract block in Markdown draft"
    raw_abstract = match.group(1)

    # Strip markdown emphasis, math delimiters, inline code
    text = re.sub(r"[`*_$~]", " ", raw_abstract)
    return text.strip()


def get_docx_abstract_text() -> str:
    """Extract clean abstract body from Word DOCX package."""
    assert os.path.exists(DOCX_MANUSCRIPT_PATH), f"DOCX manuscript not found: {DOCX_MANUSCRIPT_PATH}"
    with zipfile.ZipFile(DOCX_MANUSCRIPT_PATH) as z:
        doc_xml = z.read("word/document.xml")

    root = ET.fromstring(doc_xml)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    paragraphs = []
    for p in root.findall(".//w:p", ns):
        t = "".join([node.text for node in p.findall(".//w:t", ns) if node.text]).strip()
        if t:
            paragraphs.append(t)

    # The abstract paragraph directly follows the paragraph containing 'Abstract'
    abstract_text = ""
    for i, p in enumerate(paragraphs):
        if p.strip().lower() == "abstract":
            abstract_text = paragraphs[i + 1]
            break

    assert abstract_text, "Failed to locate abstract paragraph in Word document.xml"
    return abstract_text


def get_pdf_abstract_text() -> str:
    """Extract clean abstract body from compiled PDF document."""
    assert os.path.exists(PDF_MANUSCRIPT_PATH), f"PDF manuscript not found: {PDF_MANUSCRIPT_PATH}"
    # Use pdftotext for reliable page 1 text extraction
    pdftotext_bin = "/opt/homebrew/bin/pdftotext"
    if not os.path.exists(pdftotext_bin):
        pdftotext_bin = "pdftotext"

    cmd = [pdftotext_bin, "-f", "1", "-l", "1", PDF_MANUSCRIPT_PATH, "-"]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    pdf_page1 = res.stdout

    match = re.search(r"Abstract\s+(.*?)\s+Keywords:", pdf_page1, re.DOTALL)
    assert match, "Failed to extract abstract from PDF page 1 text"
    return match.group(1).strip()


def test_latex_abstract_word_count():
    """Verify LaTeX abstract word count is strictly <= 250 words."""
    abstract_text = get_latex_abstract_text()
    words = clean_words(abstract_text)
    word_count = len(words)
    print(f"\n[LaTeX Abstract] Word count: {word_count} words")
    assert word_count >= MIN_ABSTRACT_WORDS, f"LaTeX abstract too short ({word_count} words)"
    assert word_count <= MAX_ABSTRACT_WORDS, (
        f"LaTeX abstract exceeds {MAX_ABSTRACT_WORDS} words! Found: {word_count} words "
        f"(+{word_count - MAX_ABSTRACT_WORDS} words over limit)"
    )


def test_markdown_abstract_word_count():
    """Verify Markdown abstract word count is strictly <= 250 words."""
    abstract_text = get_markdown_abstract_text()
    words = clean_words(abstract_text)
    word_count = len(words)
    print(f"\n[Markdown Abstract] Word count: {word_count} words")
    assert word_count >= MIN_ABSTRACT_WORDS, f"Markdown abstract too short ({word_count} words)"
    assert word_count <= MAX_ABSTRACT_WORDS, (
        f"Markdown abstract exceeds {MAX_ABSTRACT_WORDS} words! Found: {word_count} words "
        f"(+{word_count - MAX_ABSTRACT_WORDS} words over limit)"
    )


def test_docx_abstract_word_count():
    """Verify Word DOCX abstract word count is strictly <= 250 words."""
    abstract_text = get_docx_abstract_text()
    words = clean_words(abstract_text)
    word_count = len(words)
    print(f"\n[DOCX Abstract] Word count: {word_count} words")
    assert word_count >= MIN_ABSTRACT_WORDS, f"DOCX abstract too short ({word_count} words)"
    assert word_count <= MAX_ABSTRACT_WORDS, (
        f"DOCX abstract exceeds {MAX_ABSTRACT_WORDS} words! Found: {word_count} words "
        f"(+{word_count - MAX_ABSTRACT_WORDS} words over limit)"
    )


def test_pdf_abstract_word_count():
    """Verify compiled PDF abstract word count is strictly <= 250 words."""
    abstract_text = get_pdf_abstract_text()
    words = clean_words(abstract_text)
    word_count = len(words)
    print(f"\n[PDF Abstract] Word count: {word_count} words")
    assert word_count >= MIN_ABSTRACT_WORDS, f"PDF abstract too short ({word_count} words)"
    assert word_count <= MAX_ABSTRACT_WORDS, (
        f"PDF abstract exceeds {MAX_ABSTRACT_WORDS} words! Found: {word_count} words "
        f"(+{word_count - MAX_ABSTRACT_WORDS} words over limit)"
    )


def test_abstract_cross_format_consistency():
    """Verify cross-format abstract word counts are mutually consistent and <= 250 words."""
    counts = {
        "LaTeX": len(clean_words(get_latex_abstract_text())),
        "Markdown": len(clean_words(get_markdown_abstract_text())),
        "DOCX": len(clean_words(get_docx_abstract_text())),
        "PDF": len(clean_words(get_pdf_abstract_text())),
    }

    print("\n[Cross-Format Abstract Summary]")
    for fmt, cnt in counts.items():
        print(f"  - {fmt:8s}: {cnt:3d} words (<= {MAX_ABSTRACT_WORDS})")
        assert cnt <= MAX_ABSTRACT_WORDS, f"{fmt} abstract exceeds {MAX_ABSTRACT_WORDS} words ({cnt})"

    # Maximum difference across formats should be small (< 15 words) due only to minor typesetting markup
    max_diff = max(counts.values()) - min(counts.values())
    assert max_diff <= 15, f"Excessive word count divergence across formats: {max_diff} words ({counts})"


if __name__ == "__main__":
    print("=" * 65)
    print("RUNNING ABSTRACT WORD COUNT VERIFICATION SUITE")
    print("=" * 65)
    test_latex_abstract_word_count()
    test_markdown_abstract_word_count()
    test_docx_abstract_word_count()
    test_pdf_abstract_word_count()
    test_abstract_cross_format_consistency()
    print("\n>>> ALL ABSTRACT WORD COUNT TESTS PASSED (100% COMPLIANT) <<<")
