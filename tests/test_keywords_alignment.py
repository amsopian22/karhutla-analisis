"""
test_keywords_alignment.py
==========================
Programmatic verification of author keywords across all manuscript formats:
1. LaTeX: manuscript/sections/00_abstract.tex
2. Markdown: manuscript/manuscript_draft.md
3. Word DOCX: manuscript/submission_package/manuscript_main.docx

Elsevier Applied Geography Guide for Authors Requirement:
- Authors must provide between 1 and 7 keywords.
- Keywords should be specific and relevant to applied spatial geography and GIScience.
"""

import os
import re
import zipfile
import xml.etree.ElementTree as ET
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LATEX_ABSTRACT_PATH = os.path.join(REPO_ROOT, "manuscript", "sections", "00_abstract.tex")
MARKDOWN_DRAFT_PATH = os.path.join(REPO_ROOT, "manuscript", "manuscript_draft.md")
DOCX_MANUSCRIPT_PATH = os.path.join(REPO_ROOT, "manuscript", "submission_package", "manuscript_main.docx")

MIN_KEYWORDS = 1
MAX_KEYWORDS = 7

# Core applied spatial geography and GIScience domain concept anchors
APPLIED_GEOGRAPHY_ANCHORS = {
    "spatial",
    "geography",
    "autocorrelation",
    "cross-validation",
    "tenure",
    "peatlands",
    "governance",
    "wildfire",
    "modeling",
}


def clean_keyword_list(raw_string: str) -> list[str]:
    """Split and clean semicolon-separated keyword string."""
    tokens = [k.strip().rstrip(".").strip() for k in raw_string.split(";") if k.strip()]
    return [t for t in tokens if t]


def get_latex_keywords() -> list[str]:
    """Extract keywords list from LaTeX abstract section."""
    assert os.path.exists(LATEX_ABSTRACT_PATH), f"LaTeX file missing: {LATEX_ABSTRACT_PATH}"
    with open(LATEX_ABSTRACT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"\\textbf\{Keywords:\}.*?\\textit\{(.*?)\}", content, re.DOTALL)
    assert match, "Failed to match \\textbf{Keywords:} in LaTeX abstract"
    return clean_keyword_list(match.group(1))


def get_markdown_keywords() -> list[str]:
    """Extract keywords list from Markdown manuscript draft."""
    assert os.path.exists(MARKDOWN_DRAFT_PATH), f"Markdown file missing: {MARKDOWN_DRAFT_PATH}"
    with open(MARKDOWN_DRAFT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"\*\*Keywords:\*\*\s*(.*?)(?:\n\n|\n---|\Z)", content, re.DOTALL)
    assert match, "Failed to match **Keywords:** in Markdown draft"
    return clean_keyword_list(match.group(1))


def get_docx_keywords() -> list[str]:
    """Extract keywords list from Word DOCX package."""
    assert os.path.exists(DOCX_MANUSCRIPT_PATH), f"DOCX file missing: {DOCX_MANUSCRIPT_PATH}"
    with zipfile.ZipFile(DOCX_MANUSCRIPT_PATH) as z:
        doc_xml = z.read("word/document.xml")

    root = ET.fromstring(doc_xml)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    kw_string = ""
    for p in root.findall(".//w:p", ns):
        text = "".join([t.text for t in p.findall(".//w:t", ns) if t.text]).strip()
        if "keywords:" in text.lower():
            idx = text.lower().find("keywords:")
            kw_string = text[idx + len("keywords:"):].strip()
            break

    assert kw_string, "Failed to locate 'Keywords:' in Word document XML"
    return clean_keyword_list(kw_string)


def test_latex_keywords_count():
    """Verify LaTeX keywords count is strictly between 1 and 7."""
    keywords = get_latex_keywords()
    count = len(keywords)
    print(f"\n[LaTeX Keywords] Count: {count} -> {keywords}")
    assert MIN_KEYWORDS <= count <= MAX_KEYWORDS, (
        f"LaTeX keywords count ({count}) out of bounds [{MIN_KEYWORDS}, {MAX_KEYWORDS}]!"
    )


def test_markdown_keywords_count():
    """Verify Markdown keywords count is strictly between 1 and 7."""
    keywords = get_markdown_keywords()
    count = len(keywords)
    print(f"\n[Markdown Keywords] Count: {count} -> {keywords}")
    assert MIN_KEYWORDS <= count <= MAX_KEYWORDS, (
        f"Markdown keywords count ({count}) out of bounds [{MIN_KEYWORDS}, {MAX_KEYWORDS}]!"
    )


def test_docx_keywords_count():
    """Verify Word DOCX keywords count is strictly between 1 and 7."""
    keywords = get_docx_keywords()
    count = len(keywords)
    print(f"\n[DOCX Keywords] Count: {count} -> {keywords}")
    assert MIN_KEYWORDS <= count <= MAX_KEYWORDS, (
        f"DOCX keywords count ({count}) out of bounds [{MIN_KEYWORDS}, {MAX_KEYWORDS}]!"
    )


def test_keywords_exact_alignment_with_applied_geography():
    """Verify keywords embody core applied spatial geography and GIScience concepts."""
    keywords_latex = get_latex_keywords()
    keywords_md = get_markdown_keywords()
    keywords_docx = get_docx_keywords()

    # Consolidate all words in lower-case
    combined_words = set(
        re.findall(r"\b[a-z-]+\b", " ".join(keywords_latex + keywords_md + keywords_docx).lower())
    )

    print("\n[Thematic Domain Alignment Check]")
    matched_anchors = APPLIED_GEOGRAPHY_ANCHORS.intersection(combined_words)
    print(f"  Matched domain anchors: {matched_anchors}")

    # Must match essential spatial geography pillars
    assert "spatial" in combined_words, "Missing core 'spatial' concept in keywords"
    assert "geography" in combined_words, "Missing core 'geography' concept in keywords"
    assert "autocorrelation" in combined_words, "Missing 'autocorrelation' methodological concept in keywords"
    assert "cross-validation" in combined_words or "validation" in combined_words, (
        "Missing validation concept in keywords"
    )
    assert "tenure" in combined_words or "governance" in combined_words, (
        "Missing tenure/governance concept in keywords"
    )


def test_keywords_cross_format_parity():
    """Verify keywords are identical across LaTeX, Markdown, and Word DOCX."""
    kw_latex = [k.lower() for k in get_latex_keywords()]
    kw_md = [k.lower() for k in get_markdown_keywords()]
    kw_docx = [k.lower() for k in get_docx_keywords()]

    print("\n[Cross-Format Keywords Equality Check]")
    print(f"  LaTeX:    {kw_latex}")
    print(f"  Markdown: {kw_md}")
    print(f"  DOCX:     {kw_docx}")

    assert kw_latex == kw_md, f"Keywords mismatch between LaTeX and Markdown!\n{kw_latex}\n!=\n{kw_md}"
    assert kw_md == kw_docx, f"Keywords mismatch between Markdown and DOCX!\n{kw_md}\n!=\n{kw_docx}"
    assert len(kw_latex) == 7, f"Expected exactly 7 keywords for Applied Geography, got {len(kw_latex)}"


if __name__ == "__main__":
    print("=" * 65)
    print("RUNNING KEYWORDS ALIGNMENT VERIFICATION SUITE")
    print("=" * 65)
    test_latex_keywords_count()
    test_markdown_keywords_count()
    test_docx_keywords_count()
    test_keywords_exact_alignment_with_applied_geography()
    test_keywords_cross_format_parity()
    print("\n>>> ALL KEYWORDS ALIGNMENT TESTS PASSED (100% COMPLIANT) <<<")
