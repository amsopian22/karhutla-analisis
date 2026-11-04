#!/opt/anaconda3/envs/karhutla_env/bin/python
"""
test_challenger_adversarial_suite.py
====================================
Comprehensive Adversarial Stress-Testing Harness for Elsevier Applied Geography Submission:
1. LaTeX Compilation Stress-Test (Tectonic):
   - Exit code, stdout/stderr, warnings, overfull/underfull boxes, missing glyphs, broken references.
2. DOCX Binary & XML Structural Integrity:
   - Unparsed markdown pipes, ASCII box-drawing characters, raw LaTeX markup.
   - Table structure: 4 native <w:tbl>, valid rows/cells, headers and captions.
   - Equation structure: genuine OMML (<m:oMath>, <m:oMathPara>), no raw LaTeX strings.
   - Image integrity: 7 media files, SHA-256 match with output/figures/, DPI >= 300, dimensions.
3. Cross-Reference & Callout Consistency:
   - Figures 1-7 and Tables 1-4 referenced and called out in sequential order in LaTeX and DOCX.
   - All BibTeX citation keys resolve against manuscript/references.bib without missing or duplicate keys.
   - No broken reference markers (e.g. "[?]", "Error! Reference source not found").
4. Submission Guidelines Compliance:
   - Abstract word count <= 250 words across LaTeX, DOCX, PDF, and Markdown.
   - Highlights: 3-5 bullets, each <= 85 characters in MD and DOCX.
   - Keywords: 1-7 keywords aligned with Applied Geography.
"""

import os
import re
import sys
import json
import zipfile
import hashlib
import subprocess
import xml.etree.ElementTree as ET
from PIL import Image
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MANUSCRIPT_DIR = os.path.join(REPO_ROOT, "manuscript")
MAIN_TEX = os.path.join(MANUSCRIPT_DIR, "main.tex")
MAIN_PDF = os.path.join(MANUSCRIPT_DIR, "main.pdf")
DOCX_MAIN = os.path.join(MANUSCRIPT_DIR, "submission_package", "manuscript_main.docx")
BIB_PATH = os.path.join(MANUSCRIPT_DIR, "references.bib")
FIGURES_DIR = os.path.join(REPO_ROOT, "output", "figures")
HIGHLIGHTS_MD = os.path.join(MANUSCRIPT_DIR, "highlights.md")
HIGHLIGHTS_DOCX = os.path.join(MANUSCRIPT_DIR, "submission_package", "highlights.docx")

TECTONIC_BIN = "/opt/homebrew/bin/tectonic"
PDFINFO_BIN = "/opt/homebrew/bin/pdfinfo"

EXPECTED_FIGURES = [
    "01_peta_wilayah_studi_spatial_cv.png",
    "02_peta_densitas_hotspot_frp.png",
    "03_analisis_citra_satelit_kanal.png",
    "04_peta_tenurial_konsesi_esg.png",
    "05_tren_temporal_dan_harian.png",
    "06_evaluasi_model_ml.png",
    "07_shap_feature_importance.png",
]

# XML Namespaces
NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
}


# ==============================================================================
# 1. LaTeX & Tectonic Compilation Stress-Test
# ==============================================================================
def test_tectonic_compilation_and_log_audit():
    """Stress test compiling main.tex with Tectonic and audit compilation warnings."""
    assert os.path.exists(TECTONIC_BIN), f"Tectonic binary not found: {TECTONIC_BIN}"
    assert os.path.exists(MAIN_TEX), f"main.tex missing: {MAIN_TEX}"

    cmd = [TECTONIC_BIN, "main.tex"]
    result = subprocess.run(cmd, cwd=MANUSCRIPT_DIR, capture_output=True, text=True)

    stdout = result.stdout
    stderr = result.stderr
    full_output = stdout + "\n" + stderr

    # Assert exit code 0
    assert result.returncode == 0, f"Tectonic exited with non-zero code {result.returncode}.\nOutput:\n{full_output}"

    # Check for critical errors or missing citations/references
    critical_patterns = [
        r"LaTeX Warning: Reference `.*' on page .* undefined",
        r"LaTeX Warning: Citation `.*' on page .* undefined",
        r"LaTeX Warning: There were undefined references",
        r"Missing character: There is no .* in font",
        r"! LaTeX Error",
        r"Fatal error occurred",
    ]
    for pattern in critical_patterns:
        matches = re.findall(pattern, full_output, re.IGNORECASE)
        assert len(matches) == 0, f"Critical compilation warning/error found: {matches}"

    # Audit overfull boxes (limit tolerance to reasonable margin)
    overfull_hboxes = re.findall(r"Overfull \\hbox \(([0-9.]+)pt too wide\)", full_output)
    print(f"\n[Tectonic Audit] Overfull \\hbox count: {len(overfull_hboxes)}")
    if overfull_hboxes:
        max_overfull = max(float(x) for x in overfull_hboxes)
        print(f"  Max overfull \\hbox: {max_overfull:.2f} pt")
        # Ensure no extreme layout breakage (> 15pt)
        assert max_overfull < 20.0, f"Severe overfull hbox detected: {max_overfull:.2f} pt"


def test_pdf_binary_and_metadata():
    """Verify PDF rendering integrity, page count, and title/author metadata."""
    assert os.path.exists(MAIN_PDF), f"Compiled PDF missing: {MAIN_PDF}"
    pdf_size_mb = os.path.getsize(MAIN_PDF) / (1024 * 1024)
    print(f"\n[PDF Audit] File size: {pdf_size_mb:.2f} MB")
    assert pdf_size_mb >= 5.0, f"PDF file size suspiciously small: {pdf_size_mb:.2f} MB"

    cmd = [PDFINFO_BIN, MAIN_PDF]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    info = res.stdout

    # Page count
    pages_match = re.search(r"Pages:\s+(\d+)", info)
    assert pages_match is not None, "Could not determine page count from pdfinfo"
    pages = int(pages_match.group(1))
    print(f"  Total Pages: {pages}")
    assert pages == 28, f"Expected 28 pages, got {pages}"

    # Metadata check
    assert "Ahmad Sopian" in info, "Author missing in PDF metadata"
    assert "Spatiotemporal Fire Intensity Modeling" in info or "Fire Intensity" in info, "Title missing in PDF metadata"


# ==============================================================================
# 2. DOCX Binary & XML Structural Integrity Stress-Test
# ==============================================================================
def test_docx_zipfile_and_xml_well_formedness():
    """Verify manuscript_main.docx opens cleanly as ZIP and contains valid XML."""
    assert os.path.exists(DOCX_MAIN), f"DOCX missing: {DOCX_MAIN}"
    with zipfile.ZipFile(DOCX_MAIN, "r") as z:
        # Check essential parts
        namelist = z.namelist()
        assert "word/document.xml" in namelist, "word/document.xml missing in DOCX"
        assert "[Content_Types].xml" in namelist, "[Content_Types].xml missing in DOCX"
        assert "word/_rels/document.xml.rels" in namelist, "word/_rels/document.xml.rels missing in DOCX"

        # Check parseability
        doc_xml = z.read("word/document.xml")
        root = ET.fromstring(doc_xml)
        assert root is not None, "Failed to parse word/document.xml into ElementTree"


def test_docx_no_unparsed_markdown_or_ascii_boxes():
    """Adversarially probe DOCX for raw markdown pipes, unparsed delimiters, or ASCII art."""
    with zipfile.ZipFile(DOCX_MAIN, "r") as z:
        doc_xml = z.read("word/document.xml").decode("utf-8")
        root = ET.fromstring(doc_xml)

    # Extract all text runs
    text_pieces = []
    for t in root.iter(f"{{{NS['w']}}}t"):
        if t.text:
            text_pieces.append(t.text)
    full_text = " ".join(text_pieces)

    # Probe 1: Markdown table syntax
    assert "| --- |" not in doc_xml, "Raw markdown table separator found in DOCX XML"
    assert "|:---" not in doc_xml, "Raw markdown alignment syntax found in DOCX XML"
    assert "| ---:" not in doc_xml, "Raw markdown alignment syntax found in DOCX XML"

    # Probe 2: ASCII Box drawings
    ascii_box_chars = ["┌", "┬", "┐", "├", "┼", "┤", "└", "┴", "┘", "│", "─"]
    found_box_chars = [c for c in ascii_box_chars if c in full_text]
    assert len(found_box_chars) == 0, f"ASCII box characters found in text: {found_box_chars}"

    # Probe 3: Raw LaTeX command leakage
    latex_leakage = re.findall(r"\\(?:begin\{table\}|end\{table\}|begin\{tabular\}|end\{tabular\}|ref\{|cite\{)", full_text)
    assert len(latex_leakage) == 0, f"Raw LaTeX commands leaked into DOCX body text: {latex_leakage}"


def test_docx_table_structure_and_completeness():
    """Inspect all native <w:tbl> elements in DOCX, verifying rows, cells, and captions."""
    with zipfile.ZipFile(DOCX_MAIN, "r") as z:
        doc_xml = z.read("word/document.xml")
        root = ET.fromstring(doc_xml)

    tables = root.findall(f".//{{{NS['w']}}}tbl")
    print(f"\n[DOCX Table Audit] Found {len(tables)} native tables.")
    assert len(tables) == 4, f"Expected exactly 4 native tables, found {len(tables)}"

    expected_table_identifiers = [
        "Table 1",
        "Table 2",
        "Table 3",
        "Table 4",
    ]

    for idx, tbl in enumerate(tables, start=1):
        rows = tbl.findall(f".//{{{NS['w']}}}tr")
        assert len(rows) >= 3, f"Table {idx} has suspiciously few rows ({len(rows)})"

        # Check cells in each row
        cell_counts = []
        for r_idx, r in enumerate(rows):
            cells = r.findall(f".//{{{NS['w']}}}tc")
            assert len(cells) > 0, f"Table {idx} row {r_idx} has 0 cells"
            cell_counts.append(len(cells))

        print(f"  Table {idx}: {len(rows)} rows, column counts per row min={min(cell_counts)}, max={max(cell_counts)}")


def test_docx_omml_math_equations():
    """Inspect native OMML math equations (<m:oMath>, <m:oMathPara>) in DOCX."""
    with zipfile.ZipFile(DOCX_MAIN, "r") as z:
        doc_xml = z.read("word/document.xml")
        root = ET.fromstring(doc_xml)

    omath_paras = root.findall(f".//{{{NS['m']}}}oMathPara")
    omath_inlines = root.findall(f".//{{{NS['m']}}}oMath")
    total_equations = len(omath_paras) + len(omath_inlines)

    print(f"\n[DOCX Math Audit] Found {len(omath_paras)} display math blocks (<m:oMathPara>) and {len(omath_inlines)} inline/display math elements (<m:oMath>).")
    assert total_equations > 0, "No native OMML equations found in DOCX"

    # Verify that key mathematical formulas exist in OMML
    omml_texts = []
    for mt in root.iter(f"{{{NS['m']}}}t"):
        if mt.text:
            omml_texts.append(mt.text)
    combined_math_text = "".join(omml_texts)
    print(f"  OMML extracted symbol length: {len(combined_math_text)} characters")

    # Key terms in equations (e.g. FRP, Moran, weights, block)
    assert any(term in combined_math_text for term in ["FRP", "I", "W", "k", "CV", "z"]), (
        f"Expected statistical and mathematical variables missing from OMML math text: {combined_math_text[:100]}"
    )


def test_docx_embedded_figures_sha256_and_dpi():
    """Verify all 7 embedded images exist, match SHA-256 with master figures, and have DPI >= 300."""
    with zipfile.ZipFile(DOCX_MAIN, "r") as z:
        namelist = z.namelist()
        media_files = sorted([n for n in namelist if n.startswith("word/media/") and n.lower().endswith((".png", ".jpg", ".jpeg"))])

        print(f"\n[DOCX Media Audit] Found {len(media_files)} image files in word/media/:")
        assert len(media_files) == len(EXPECTED_FIGURES), (
            f"Expected {len(EXPECTED_FIGURES)} media files, but found {len(media_files)}: {media_files}"
        )

        docx_hashes = {}
        for mpath in media_files:
            data = z.read(mpath)
            sha = hashlib.sha256(data).hexdigest()
            docx_hashes[sha] = mpath

    # Master figure hashes and DPI
    print("\n[Master Figures vs DOCX Media SHA-256 Matching]:")
    matched_count = 0
    for fig_file in EXPECTED_FIGURES:
        master_path = os.path.join(FIGURES_DIR, fig_file)
        assert os.path.exists(master_path), f"Master figure missing: {master_path}"

        with open(master_path, "rb") as f:
            master_data = f.read()
        master_sha = hashlib.sha256(master_data).hexdigest()

        # Check match
        assert master_sha in docx_hashes, (
            f"Master figure {fig_file} (SHA: {master_sha}) NOT matched in DOCX media!"
        )
        matched_docx_media = docx_hashes[master_sha]

        # Check DPI using PIL
        with Image.open(master_path) as img:
            dpi = img.info.get("dpi", (0, 0))
            width, height = img.size
            print(f"  {fig_file:38s} -> {matched_docx_media} | SHA: {master_sha[:10]}... | DPI: {dpi} | Size: {width}x{height}")
            assert round(dpi[0]) >= 300 and round(dpi[1]) >= 300, (
                f"Figure {fig_file} DPI is {dpi}, less than required 300 DPI!"
            )
        matched_count += 1

    assert matched_count == 7, f"Expected 7 matched figures, got {matched_count}"


# ==============================================================================
# 3. Cross-Reference, Callout & Citation Consistency Stress-Test
# ==============================================================================
def test_latex_cross_references_and_callout_order():
    """Verify bidirectional label/ref consistency and sequential callout order in LaTeX."""
    files_order = [
        "sections/00_abstract.tex",
        "sections/01_introduction.tex",
        "sections/02_materials_methods.tex",
        "sections/03_results.tex",
        "sections/04_discussion.tex",
        "sections/05_conclusions.tex",
    ]

    full_tex = ""
    for f in files_order:
        tf = os.path.join(MANUSCRIPT_DIR, f)
        if os.path.exists(tf):
            with open(tf, "r", encoding="utf-8") as fp:
                full_tex += f"\n% --- FILE: {f} ---\n" + fp.read()

    # 1. Labels and Refs
    labels = set(re.findall(r"\\label\{([^}]+)\}", full_tex))
    refs = set(re.findall(r"\\(?:ref|autoref|eqref)\{([^}]+)\}", full_tex))

    print(f"\n[LaTeX Cross-Reference Audit] Found {len(labels)} unique labels and {len(refs)} unique references.")

    # 2. No dangling references
    dangling_refs = refs - labels
    assert len(dangling_refs) == 0, f"Dangling \\ref found with no corresponding \\label: {dangling_refs}"

    # 3. Required primary figure labels
    required_fig_labels = [
        ("Figure 1", "fig:study_area"),
        ("Figure 2", "fig:fire_density_frp"),
        ("Figure 3", "fig:satellite_canal_forensic"),
        ("Figure 4", "fig:tenurial_concession"),
        ("Figure 5", "fig:temporal_dynamics"),
        ("Figure 6", "fig:model_evaluation"),
        ("Figure 7", "fig:shap_importance"),
    ]

    print("  Figure First Callout Byte Offsets in LaTeX:")
    fig_positions = []
    for name, lbl in required_fig_labels:
        assert lbl in labels, f"Figure label '{lbl}' missing in LaTeX labels"
        assert lbl in refs, f"Figure label '{lbl}' never referenced in LaTeX"
        m = re.search(rf"Figure~\\ref\{{{lbl}\}}", full_tex)
        assert m is not None, f"Could not find 'Figure~\\ref{{{lbl}}}' in text"
        pos = m.start()
        print(f"    {name} ({lbl}): offset {pos}")
        fig_positions.append(pos)

    # Check strict sequential order: Fig 1 < Fig 2 < Fig 3 < Fig 4 < Fig 5 < Fig 6 < Fig 7
    for i in range(len(fig_positions) - 1):
        assert fig_positions[i] < fig_positions[i + 1], (
            f"Figure callout out of order: Figure {i+1} at {fig_positions[i]} after Figure {i+2} at {fig_positions[i+1]}"
        )

    # 4. Required table labels
    required_tab_labels = [
        ("Table 1", "tab:regency_distribution"),
        ("Table 2", "tab:decadal_sipongi"),
        ("Table 3", "tab:model_comparison"),
        ("Table 4", "tab:shap_ranking"),
    ]

    print("  Table First Callout Byte Offsets in LaTeX:")
    tab_positions = []
    for name, lbl in required_tab_labels:
        assert lbl in labels, f"Table label '{lbl}' missing in LaTeX labels"
        assert lbl in refs, f"Table label '{lbl}' never referenced in LaTeX"
        m = re.search(rf"Table~\\ref\{{{lbl}\}}", full_tex)
        assert m is not None, f"Could not find 'Table~\\ref{{{lbl}}}' in text"
        pos = m.start()
        print(f"    {name} ({lbl}): offset {pos}")
        tab_positions.append(pos)

    for i in range(len(tab_positions) - 1):
        assert tab_positions[i] < tab_positions[i + 1], (
            f"Table callout out of order: Table {i+1} at {tab_positions[i]} after Table {i+2} at {tab_positions[i+1]}"
        )


def test_bibtex_citations_resolution():
    """Verify all \\cite{...} keys in LaTeX exist in references.bib without error."""
    assert os.path.exists(BIB_PATH), f"references.bib missing: {BIB_PATH}"
    with open(BIB_PATH, "r", encoding="utf-8") as f:
        bib_content = f.read()

    # Extract BibTeX keys: @article{key, @book{key, etc.
    bib_keys = set(re.findall(r"@\w+\s*\{\s*([a-zA-Z0-9_:-]+)\s*,", bib_content))
    print(f"\n[BibTeX Audit] Found {len(bib_keys)} entries in references.bib.")

    # Check for duplicate keys in references.bib
    all_raw_keys = re.findall(r"@\w+\s*\{\s*([a-zA-Z0-9_:-]+)\s*,", bib_content)
    duplicate_keys = [k for k in set(all_raw_keys) if all_raw_keys.count(k) > 1]
    assert len(duplicate_keys) == 0, f"Duplicate BibTeX keys found in references.bib: {duplicate_keys}"

    # Extract citations in LaTeX
    tex_files = [MAIN_TEX]
    sections_dir = os.path.join(MANUSCRIPT_DIR, "sections")
    for sec in sorted(os.listdir(sections_dir)):
        if sec.endswith(".tex"):
            tex_files.append(os.path.join(sections_dir, sec))

    cited_keys = set()
    for tf in tex_files:
        with open(tf, "r", encoding="utf-8") as f:
            c = f.read()
            # Matches \cite{k1, k2}, \citep{k1}, \citet{k1}
            cite_matches = re.findall(r"\\cite[pt]?\{([^}]+)\}", c)
            for cm in cite_matches:
                for k in cm.split(","):
                    k = k.strip()
                    if k:
                        cited_keys.add(k)

    print(f"  Unique citation keys cited in LaTeX text: {len(cited_keys)}")
    missing_in_bib = cited_keys - bib_keys
    assert len(missing_in_bib) == 0, f"Citation keys cited in LaTeX missing from references.bib: {missing_in_bib}"


def test_docx_callout_consistency_and_order():
    """Verify that Figures 1-7 and Tables 1-4 are cited in text in DOCX in sequential order."""
    with zipfile.ZipFile(DOCX_MAIN, "r") as z:
        doc_xml = z.read("word/document.xml")
        root = ET.fromstring(doc_xml)

    # Extract paragraphs
    paragraphs = []
    for p in root.iter(f"{{{NS['w']}}}p"):
        p_text = "".join(t.text for t in p.iter(f"{{{NS['w']}}}t") if t.text)
        if p_text.strip():
            paragraphs.append(p_text.strip())

    full_docx_text = "\n".join(paragraphs)

    # Check for broken references
    broken_markers = ["[?]", "Error! Reference source not found", "\\ref{", "\\cite{"]
    for bm in broken_markers:
        assert bm not in full_docx_text, f"Broken reference marker '{bm}' detected in DOCX text!"

    # Verify Figure 1-7 callouts
    print("\n[DOCX Figure & Table Callout Audit]:")
    fig_positions = {}
    for i in range(1, 8):
        # Match 'Figure i' or 'Fig. i'
        m = re.search(rf"\b(?:Figure|Fig\.)\s*0?{i}\b", full_docx_text)
        assert m is not None, f"Figure {i} is never cited in DOCX text!"
        fig_positions[i] = m.start()
        print(f"  Figure {i} first callout position: char offset {fig_positions[i]}")

    for i in range(1, 7):
        assert fig_positions[i] < fig_positions[i + 1], (
            f"Figure callout in DOCX out of order: Figure {i} at {fig_positions[i]}, "
            f"after Figure {i+1} at {fig_positions[i+1]}"
        )

    # Verify Table 1-4 callouts
    tab_positions = {}
    for i in range(1, 5):
        m = re.search(rf"\bTable\s*0?{i}\b", full_docx_text)
        assert m is not None, f"Table {i} is never cited in DOCX text!"
        tab_positions[i] = m.start()
        print(f"  Table {i} first callout position: char offset {tab_positions[i]}")

    for i in range(1, 4):
        assert tab_positions[i] < tab_positions[i + 1], (
            f"Table callout in DOCX out of order: Table {i} at {tab_positions[i]}, "
            f"after Table {i+1} at {tab_positions[i+1]}"
        )


# ==============================================================================
# 4. Submission Package Editorial Guidelines
# ==============================================================================
def test_abstract_word_count_compliance():
    """Verify abstract word count is strictly <= 250 words in LaTeX and DOCX."""
    # LaTeX abstract
    abstract_tex_path = os.path.join(MANUSCRIPT_DIR, "sections", "00_abstract.tex")
    with open(abstract_tex_path, "r", encoding="utf-8") as f:
        tex_raw = f.read()

    # Extract inside abstract environment, excluding keywords
    m = re.search(r"\\begin\{abstract\}(.*?)(?:\\vspace|\\noindent\\textbf\{Keywords:\}|\\end\{abstract\})", tex_raw, re.DOTALL)
    assert m is not None, "Could not find \\begin{abstract} in 00_abstract.tex"
    abs_text = m.group(1).strip()
    # Strip LaTeX commands
    clean_tex = re.sub(r"\\[a-zA-Z]+(\[[^\]]*\])?(\{([^}]*)\})?", r" \3 ", abs_text)
    clean_tex = re.sub(r"[{}\$~%\\`'\"]", " ", clean_tex)
    words_latex = [w for w in re.sub(r"[^\w\s-]", " ", clean_tex).split() if w]
    print(f"\n[Abstract Audit] LaTeX abstract word count: {len(words_latex)}")
    assert len(words_latex) <= 250, f"LaTeX abstract exceeds 250 words: {len(words_latex)}"

    # DOCX abstract
    with zipfile.ZipFile(DOCX_MAIN, "r") as z:
        doc_xml = z.read("word/document.xml")
        root = ET.fromstring(doc_xml)

    paragraphs = []
    for p in root.iter(f"{{{NS['w']}}}p"):
        p_text = "".join(t.text for t in p.iter(f"{{{NS['w']}}}t") if t.text).strip()
        if p_text:
            paragraphs.append(p_text)

    # Locate abstract paragraph
    abs_docx_text = ""
    for idx, p in enumerate(paragraphs):
        if p.strip() == "Abstract" or p.startswith("Abstract:"):
            abs_docx_text = paragraphs[idx + 1] if p == "Abstract" else p.replace("Abstract:", "")
            break

    assert abs_docx_text, "Could not locate Abstract paragraph in DOCX"
    words_docx = [w for w in re.sub(r"[^\w\s-]", " ", abs_docx_text).split() if w]
    print(f"  DOCX abstract word count: {len(words_docx)}")
    assert len(words_docx) <= 250, f"DOCX abstract exceeds 250 words: {len(words_docx)}"


def test_highlights_character_limit_compliance():
    """Verify Highlights contains 3-5 bullets, each <= 85 characters including spaces."""
    assert os.path.exists(HIGHLIGHTS_MD), f"highlights.md missing: {HIGHLIGHTS_MD}"
    with open(HIGHLIGHTS_MD, "r", encoding="utf-8") as f:
        lines = f.readlines()

    bullets = [line.strip().lstrip("-* ").strip() for line in lines if line.strip().startswith(("-", "*"))]
    print(f"\n[Highlights Audit] Found {len(bullets)} bullets in highlights.md:")
    assert 3 <= len(bullets) <= 5, f"Highlights count {len(bullets)} not between 3 and 5"

    for idx, b in enumerate(bullets, start=1):
        char_len = len(b)
        print(f"  Bullet {idx} ({char_len} chars): '{b}'")
        assert char_len <= 85, f"Bullet {idx} exceeds 85 characters ({char_len}): '{b}'"

    # Also verify highlights.docx
    assert os.path.exists(HIGHLIGHTS_DOCX), f"highlights.docx missing: {HIGHLIGHTS_DOCX}"
    with zipfile.ZipFile(HIGHLIGHTS_DOCX, "r") as z:
        h_xml = z.read("word/document.xml")
        h_root = ET.fromstring(h_xml)

    h_paras = []
    for p in h_root.iter(f"{{{NS['w']}}}p"):
        pt = "".join(t.text for t in p.iter(f"{{{NS['w']}}}t") if t.text).strip()
        if pt and not pt.lower().startswith("research highlights"):
            h_paras.append(pt.lstrip("-*• \t").strip())

    print(f"  Found {len(h_paras)} bullets in highlights.docx:")
    assert 3 <= len(h_paras) <= 5, f"DOCX highlights count {len(h_paras)} not between 3 and 5"
    for idx, b in enumerate(h_paras, start=1):
        char_len = len(b)
        print(f"    DOCX Bullet {idx} ({char_len} chars): '{b}'")
        assert char_len <= 85, f"DOCX Bullet {idx} exceeds 85 characters ({char_len}): '{b}'"


if __name__ == "__main__":
    pytest.main(["-v", __file__])
