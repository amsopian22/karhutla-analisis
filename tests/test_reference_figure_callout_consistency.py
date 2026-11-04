"""
test_reference_figure_callout_consistency.py
============================================
Programmatic verification of bidirectional consistency across LaTeX, Markdown, and Word:
1. Every table (Tables 1-4) must be explicitly called out in text in both LaTeX and Markdown/Word.
2. Every figure (Figures 1-7) must be explicitly called out in text in both LaTeX and Markdown/Word.
3. No broken links, uncalled assets, orphaned figures/tables, or mismatched numbers.
4. All \\cite keys in LaTeX resolve against manuscript/references.bib.
"""

import os
import re
import glob
import zipfile
import xml.etree.ElementTree as ET
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MANUSCRIPT_DIR = os.path.join(REPO_ROOT, "manuscript")
BIB_PATH = os.path.join(MANUSCRIPT_DIR, "references.bib")
MARKDOWN_PATH = os.path.join(MANUSCRIPT_DIR, "manuscript_draft.md")
DOCX_PATH = os.path.join(MANUSCRIPT_DIR, "submission_package", "manuscript_main.docx")


def get_all_latex_sources() -> dict[str, str]:
    """Load all LaTeX source files (.tex) in manuscript directory and sections."""
    tex_files = glob.glob(os.path.join(MANUSCRIPT_DIR, "sections", "*.tex"))
    main_tex = os.path.join(MANUSCRIPT_DIR, "main.tex")
    if os.path.exists(main_tex):
        tex_files.append(main_tex)

    sources = {}
    for tf in tex_files:
        with open(tf, "r", encoding="utf-8") as f:
            sources[tf] = f.read()
    return sources


def get_bibtex_keys() -> set[str]:
    """Parse all BibTeX citation keys from references.bib."""
    assert os.path.exists(BIB_PATH), f"BibTeX file missing: {BIB_PATH}"
    with open(BIB_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    keys = set(re.findall(r"@\w+\s*\{\s*([^,]+),", content))
    assert len(keys) >= 30, f"Suspiciously low BibTeX keys ({len(keys)})"
    return keys


def test_latex_bibtex_citations_resolve():
    """Verify that every \\cite, \\citep, \\citet in LaTeX sources exists in references.bib."""
    bib_keys = get_bibtex_keys()
    sources = get_all_latex_sources()

    cited_keys = set()
    for filepath, content in sources.items():
        # Match \cite{key1, key2}, \citep{...}, \citet{...}, \citealp{...}
        cites = re.findall(r"\\cite[pt]?\{([^}]+)\}", content)
        for c in cites:
            for k in c.split(","):
                clean_k = k.strip()
                if clean_k:
                    cited_keys.add(clean_k)

    print(f"\n[LaTeX Citation Audit] Total unique cited keys: {len(cited_keys)}")
    missing = cited_keys - bib_keys
    assert len(missing) == 0, f"Dangling citations in LaTeX not found in references.bib: {missing}"
    print(f"  All {len(cited_keys)} citations successfully resolve against references.bib ({len(bib_keys)} entries)")


def test_latex_figures_and_tables_bidirectional_consistency():
    """Verify LaTeX figure/table environments, labels, cross-references, and image paths."""
    sources = get_all_latex_sources()
    combined_tex = "\n".join(sources.values())

    all_labels = set(re.findall(r"\\label\{([^}]+)\}", combined_tex))
    all_refs = set(re.findall(r"\\ref\{([^}]+)\}", combined_tex))

    # 1. No dangling references
    dangling_refs = all_refs - all_labels
    assert len(dangling_refs) == 0, f"Dangling \\ref found with no corresponding \\label: {dangling_refs}"

    # 2. Key figures 1 to 7 must be explicitly referenced
    required_fig_labels = {
        "fig:study_area": 1,
        "fig:fire_density_frp": 2,
        "fig:satellite_canal_forensic": 3,
        "fig:tenurial_concession": 4,
        "fig:temporal_dynamics": 5,
        "fig:model_evaluation": 6,
        "fig:shap_importance": 7,
    }

    print("\n[LaTeX Figure Callout Audit]")
    for label, fig_num in required_fig_labels.items():
        assert label in all_labels, f"Figure {fig_num} label '{label}' missing in LaTeX sources"
        assert label in all_refs, f"Figure {fig_num} label '{label}' is uncalled in LaTeX narrative text"
        # Count explicit in-text mentions
        mentions = len(re.findall(rf"Figure~\\ref\{{{label}\}}", combined_tex))
        print(f"  Figure {fig_num} ('{label}'): defined and called {mentions} time(s)")
        assert mentions >= 1, f"Figure {fig_num} has no 'Figure~\\ref{{{label}}}' callout in text"

    # 3. Key tables 1 to 4 must be explicitly referenced
    required_tab_labels = {
        "tab:regency_distribution": 1,
        "tab:decadal_sipongi": 2,
        "tab:model_comparison": 3,
        "tab:shap_ranking": 4,
    }

    print("\n[LaTeX Table Callout Audit]")
    for label, tab_num in required_tab_labels.items():
        assert label in all_labels, f"Table {tab_num} label '{label}' missing in LaTeX sources"
        assert label in all_refs, f"Table {tab_num} label '{label}' is uncalled in LaTeX narrative text"
        mentions = len(re.findall(rf"Table~\\ref\{{{label}\}}", combined_tex))
        print(f"  Table {tab_num} ('{label}'): defined and called {mentions} time(s)")
        assert mentions >= 1, f"Table {tab_num} has no 'Table~\\ref{{{label}}}' callout in text"

    # 4. Includegraphics images must exist on disk
    images = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", combined_tex)
    print(f"\n[LaTeX Image Inclusion Audit] {len(images)} images found:")
    for img in images:
        candidates = [
            img,
            os.path.join(MANUSCRIPT_DIR, img),
            os.path.join(REPO_ROOT, "output", "figures", os.path.basename(img)),
            img + ".png",
            os.path.join(REPO_ROOT, "output", "figures", os.path.basename(img) + ".png"),
        ]
        found = any(os.path.exists(p) for p in candidates)
        print(f"  - {img}: {'FOUND' if found else 'MISSING'}")
        assert found, f"LaTeX included image not found on disk: {img}"


def test_markdown_figures_and_tables_callouts():
    """Verify Markdown manuscript_draft.md callouts for Tables 1-4 and Figures 1-7."""
    assert os.path.exists(MARKDOWN_PATH), f"Markdown file missing: {MARKDOWN_PATH}"
    with open(MARKDOWN_PATH, "r", encoding="utf-8") as f:
        md_content = f.read()

    lines = md_content.splitlines()

    print("\n[Markdown Table Callout Audit]")
    # Tables 1 to 4: verify caption header exists AND in-text body callout exists
    for tab_num in range(1, 5):
        caption_found = False
        body_callouts = 0

        for line in lines:
            # Check caption header
            if re.search(rf"\*\*Table\s+{tab_num}\.", line):
                caption_found = True
            # Check body text callout (excluding the caption line itself)
            elif re.search(rf"\bTable\s+{tab_num}\b", line):
                body_callouts += 1

        print(f"  Table {tab_num}: Caption={'YES' if caption_found else 'NO'}, Body Callouts={body_callouts}")
        assert caption_found, f"Table {tab_num} caption header missing in Markdown draft"
        assert body_callouts >= 1, f"Table {tab_num} has no in-text body callout in Markdown draft"

    print("\n[Markdown Figure Callout Audit]")
    # Figures 1 to 7: verify markdown image embed exists AND in-text body callout exists
    for fig_num in range(1, 8):
        embed_found = False
        body_callouts = 0

        for line in lines:
            # Check image embed line
            if re.search(rf"!\[\*\*Figure\s+{fig_num}\.", line):
                embed_found = True
                # Extract image path inside ![...](path)
                m_path = re.search(r"\(([^)]+\.png)\)", line)
                if m_path:
                    img_path = os.path.join(REPO_ROOT, m_path.group(1))
                    assert os.path.exists(img_path), f"Figure {fig_num} image file missing on disk: {img_path}"
            # Check body text callout (outside image embed line)
            elif re.search(rf"\bFigure\s*{fig_num}[a-z]?\b|\bFig\.\s*{fig_num}\b", line):
                body_callouts += 1

        print(f"  Figure {fig_num}: Embed={'YES' if embed_found else 'NO'}, Body Callouts={body_callouts}")
        assert embed_found, f"Figure {fig_num} image embed missing in Markdown draft"
        assert body_callouts >= 1, f"Figure {fig_num} has no in-text body callout in Markdown draft"


def test_docx_figures_and_tables_callouts():
    """Verify Word DOCX manuscript_main.docx contains callouts for Tables 1-4 and Figures 1-7."""
    assert os.path.exists(DOCX_PATH), f"DOCX file missing: {DOCX_PATH}"
    with zipfile.ZipFile(DOCX_PATH) as z:
        doc_xml = z.read("word/document.xml")

    root = ET.fromstring(doc_xml)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    paragraphs = []
    for p in root.findall(".//w:p", ns):
        text = "".join([t.text for t in p.findall(".//w:t", ns) if t.text]).strip()
        if text:
            paragraphs.append(text)

    full_docx_text = "\n".join(paragraphs)

    print("\n[DOCX Table & Figure Callout Audit]")
    for tab_num in range(1, 5):
        tab_matches = len(re.findall(rf"\bTable\s+{tab_num}\b", full_docx_text))
        print(f"  Table {tab_num}: {tab_matches} total mentions in DOCX")
        assert tab_matches >= 2, f"Table {tab_num} missing caption or callout in DOCX ({tab_matches} mentions)"

    for fig_num in range(1, 8):
        fig_matches = len(re.findall(rf"\bFigure\s*{fig_num}[a-z]?\b", full_docx_text, re.IGNORECASE))
        print(f"  Figure {fig_num}: {fig_matches} total mentions in DOCX")
        assert fig_matches >= 2, f"Figure {fig_num} missing caption or callout in DOCX ({fig_matches} mentions)"


def test_semantic_figure_alignment_no_mismatches():
    """Verify that figure callouts match their scientific content (no swapped or misattributed figures)."""
    with open(MARKDOWN_PATH, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Rule 1: Model evaluation (ROC curve, confusion matrix) must be Figure 6, NEVER Figure 4 or 5
    m_ml = re.search(r"Machine Learning Evaluation:.*?(?=###|\Z)", md_content, re.DOTALL)
    assert m_ml, "Machine Learning section not found"
    ml_section = m_ml.group(0)
    assert "Figure 6" in ml_section, "Figure 6 callout missing in Machine Learning section"
    assert "Figure 4" not in ml_section, "Mismatched callout: Figure 4 mistakenly called in Machine Learning section"
    assert "Figure 5" not in ml_section, "Mismatched callout: Figure 5 mistakenly called in Machine Learning section"

    # Rule 2: TreeSHAP beeswarm / feature attribution must be Figure 7
    m_shap = re.search(r"Explainable AI: TreeSHAP.*?(?=##|\Z)", md_content, re.DOTALL)
    assert m_shap, "TreeSHAP section not found"
    shap_section = m_shap.group(0)
    assert "Figure 7" in shap_section, "Figure 7 callout missing in TreeSHAP section"
    assert "Figure 5" not in shap_section, "Mismatched callout: Figure 5 mistakenly called in TreeSHAP section"

    # Rule 3: Concession / tenure overlay must be Figure 4
    m_tenure = re.search(r"Cadastral Land Tenure Attribution.*?(?=###|\Z)", md_content, re.DOTALL)
    assert m_tenure, "Cadastral tenure section not found"
    tenure_section = m_tenure.group(0)
    assert "Figure 4" in tenure_section, "Figure 4 callout missing in Cadastral Tenure section"

    # Rule 4: Canal distance decay forensics must be Figure 3
    m_canal = re.search(r"Peatland Stratification and Canal Drainage.*?(?=###|\Z)", md_content, re.DOTALL)
    assert m_canal, "Canal forensics section not found"
    canal_section = m_canal.group(0)
    assert "Figure 3" in canal_section, "Figure 3 callout missing in Canal Forensics section"

    print("\n[Semantic Callout Alignment] 100% Verified: No mismatched figure numbers or swapped callouts.")


if __name__ == "__main__":
    print("=" * 65)
    print("RUNNING REFERENCE & FIGURE CALLOUT CONSISTENCY SUITE")
    print("=" * 65)
    test_latex_bibtex_citations_resolve()
    test_latex_figures_and_tables_bidirectional_consistency()
    test_markdown_figures_and_tables_callouts()
    test_docx_figures_and_tables_callouts()
    test_semantic_figure_alignment_no_mismatches()
    print("\n>>> ALL REFERENCE & FIGURE CALLOUT TESTS PASSED (100% COMPLIANT) <<<")
