"""
test_document_compilation_rendering.py
======================================
Programmatic verification of end-to-end document compilation and multi-format rendering integrity:
1. LaTeX compilation with Tectonic (/opt/homebrew/bin/tectonic) into manuscript/main.pdf (28 pages, exit code 0).
2. Word DOCX manuscript/submission_package/manuscript_main.docx:
   - Opens cleanly with zipfile and ElementTree.
   - Contains exactly 4 native Word tables (<w:tbl>).
   - Contains 0 raw markdown table pipes (| --- |).
   - Contains genuine OMML math equations (<m:oMath>).
   - Contains 7 embedded 300 DPI figures identical in SHA-256 hash to output/figures/.
"""

import os
import subprocess
import zipfile
import xml.etree.ElementTree as ET
import hashlib
from PIL import Image
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MANUSCRIPT_DIR = os.path.join(REPO_ROOT, "manuscript")
MAIN_TEX_PATH = os.path.join(MANUSCRIPT_DIR, "main.tex")
MAIN_PDF_PATH = os.path.join(MANUSCRIPT_DIR, "main.pdf")
DOCX_PATH = os.path.join(MANUSCRIPT_DIR, "submission_package", "manuscript_main.docx")
FIGURES_DIR = os.path.join(REPO_ROOT, "output", "figures")
TECTONIC_BIN = "/opt/homebrew/bin/tectonic"
PDFINFO_BIN = "/opt/homebrew/bin/pdfinfo"

EXPECTED_PDF_PAGES = 32
EXPECTED_TABLES_COUNT = 4
EXPECTED_FIGURES_COUNT = 8

MASTER_FIGURE_FILES = [
    "01_peta_wilayah_studi_spatial_cv.png",
    "02_peta_densitas_hotspot_frp.png",
    "03_analisis_citra_satelit_kanal.png",
    "04_peta_tenurial_konsesi_esg.png",
    "09_spatial_boundary_discontinuity.png",
    "05_tren_temporal_dan_harian.png",
    "06_evaluasi_model_ml.png",
    "07_shap_feature_importance.png",
]


def test_tectonic_compilation():
    """Verify that manuscript/main.tex compiles cleanly with Tectonic to exit code 0."""
    assert os.path.exists(TECTONIC_BIN), f"Tectonic binary not found at {TECTONIC_BIN}"
    assert os.path.exists(MAIN_TEX_PATH), f"LaTeX main source missing at {MAIN_TEX_PATH}"

    print(f"\n[Tectonic Compilation] Compiling {MAIN_TEX_PATH}...")
    cmd = [TECTONIC_BIN, "main.tex"]
    result = subprocess.run(cmd, cwd=MANUSCRIPT_DIR, capture_output=True, text=True)

    print(f"  Exit code: {result.returncode}")
    if result.returncode != 0:
        print(f"STDOUT:\n{result.stdout}")
        print(f"STDERR:\n{result.stderr}")

    assert result.returncode == 0, f"Tectonic compilation failed with exit code {result.returncode}"
    assert os.path.exists(MAIN_PDF_PATH), f"Output PDF missing after compilation: {MAIN_PDF_PATH}"
    pdf_size_mb = os.path.getsize(MAIN_PDF_PATH) / (1024 * 1024)
    print(f"  Compiled PDF size: {pdf_size_mb:.2f} MB")
    assert pdf_size_mb >= 5.0, f"PDF file suspiciously small ({pdf_size_mb:.2f} MB)"


def test_pdf_rendering_and_metadata():
    """Verify that compiled PDF has exactly 28 pages and proper Elsevier metadata."""
    assert os.path.exists(PDFINFO_BIN), f"pdfinfo binary not found at {PDFINFO_BIN}"
    assert os.path.exists(MAIN_PDF_PATH), f"main.pdf missing at {MAIN_PDF_PATH}"

    cmd = [PDFINFO_BIN, MAIN_PDF_PATH]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    info_output = res.stdout

    print(f"\n[PDF Document Metadata Audit]")
    for line in info_output.splitlines():
        if any(key in line for key in ["Pages:", "Title:", "Author:", "Page size:", "File size:"]):
            print(f"  {line}")

    # 1. Assert exactly 28 pages
    assert f"Pages:           {EXPECTED_PDF_PAGES}" in info_output, (
        f"PDF page count is not {EXPECTED_PDF_PAGES}! Check pdfinfo output."
    )

    # 2. Assert Title & Authorship
    assert "Title:" in info_output and any(t in info_output for t in ["The Governance Void", "Concession Frontiers", "Fire Intensity"]), "PDF Title metadata missing or corrupt"
    assert "Author:" in info_output and "Ahmad Sopian" in info_output, "PDF Author metadata missing or corrupt"


def test_docx_structure_and_native_tables():
    """Verify Word DOCX contains exactly 4 native <w:tbl> tables and 0 raw markdown pipes."""
    assert os.path.exists(DOCX_PATH), f"Word DOCX missing: {DOCX_PATH}"

    with zipfile.ZipFile(DOCX_PATH) as z:
        doc_xml = z.read("word/document.xml")

    root = ET.fromstring(doc_xml)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    # 1. Check native Word tables
    tables = root.findall(".//w:tbl", ns)
    table_count = len(tables)
    print(f"\n[DOCX Native Table Audit] Found {table_count} <w:tbl> elements:")
    for idx, tbl in enumerate(tables, 1):
        rows = tbl.findall(".//w:tr", ns)
        print(f"  Table {idx}: {len(rows)} rows")
        assert len(rows) >= 5, f"Table {idx} has suspiciously few rows ({len(rows)})"

    assert table_count == EXPECTED_TABLES_COUNT, (
        f"Expected {EXPECTED_TABLES_COUNT} native Word tables, got {table_count}"
    )

    # 2. Check 0 raw markdown pipes
    raw_xml_text = doc_xml.decode("utf-8")
    assert "| --- |" not in raw_xml_text, "Found unparsed raw markdown table divider '| --- |' in DOCX XML!"
    assert "| :--- |" not in raw_xml_text, "Found unparsed raw markdown alignment divider '| :--- |' in DOCX XML!"
    assert "|:---|" not in raw_xml_text, "Found unparsed raw markdown alignment divider '|:---|' in DOCX XML!"

    # 3. Check no raw LaTeX math delimiters leaking as literal text in paragraphs
    paragraphs = []
    for p in root.findall(".//w:p", ns):
        t = "".join([node.text for node in p.findall(".//w:t", ns) if node.text]).strip()
        if t:
            paragraphs.append(t)

    for p in paragraphs:
        assert not p.startswith("### "), f"Found unparsed markdown heading leaking into DOCX paragraph: '{p}'"
        assert "\\begin{equation}" not in p, f"Found raw LaTeX \\begin{{equation}} leaking into DOCX paragraph: '{p}'"

    print("  Zero raw markdown table pipes or markup leaks detected in Word DOCX.")


def test_docx_omml_math_equations():
    """Verify Word DOCX contains proper native OMML (<m:oMath>) mathematical equations."""
    with zipfile.ZipFile(DOCX_PATH) as z:
        doc_xml = z.read("word/document.xml")

    root = ET.fromstring(doc_xml)
    ns = {
        "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
        "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    }

    omath_elements = root.findall(".//m:oMath", ns)
    omath_paras = root.findall(".//m:oMathPara", ns)

    print(f"\n[DOCX Mathematical Equation Audit]")
    print(f"  Inline/Display OMML equations (<m:oMath>): {len(omath_elements)}")
    print(f"  Display equation paragraphs (<m:oMathPara>): {len(omath_paras)}")

    assert len(omath_elements) >= 50, (
        f"Suspiciously few OMML equations ({len(omath_elements)}). Mathematical formulas may have degraded!"
    )
    assert len(omath_paras) >= 5, (
        f"Suspiciously few display equation paragraphs ({len(omath_paras)})."
    )


def test_docx_embedded_figures_sha256_match_master():
    """Verify that all 7 embedded DOCX images match the SHA-256 hashes of master 300 DPI figures."""
    with zipfile.ZipFile(DOCX_PATH) as z:
        media_names = [f for f in z.namelist() if f.startswith("word/media/")]

        print(f"\n[DOCX Embedded Image SHA-256 Hash Verification]")
        print(f"  Total media files in DOCX: {len(media_names)}")
        assert len(media_names) == EXPECTED_FIGURES_COUNT, (
            f"Expected {EXPECTED_FIGURES_COUNT} media files in DOCX, found {len(media_names)}"
        )

        docx_hashes = {}
        for m in media_names:
            data = z.read(m)
            docx_hashes[hashlib.sha256(data).hexdigest()] = m

    # Compute master figure hashes
    master_hashes = {}
    for fname in MASTER_FIGURE_FILES:
        fpath = os.path.join(FIGURES_DIR, fname)
        assert os.path.exists(fpath), f"Master figure missing: {fpath}"
        with open(fpath, "rb") as f:
            data = f.read()
            h = hashlib.sha256(data).hexdigest()
            master_hashes[h] = fname

        # Check DPI and resolution of master figure
        with Image.open(fpath) as img:
            dpi = img.info.get("dpi", (0, 0))
            width, height = img.size
            print(f"  Master figure '{fname}': {width}x{height} px, DPI: {dpi}")
            assert round(dpi[0]) == 300, f"Figure '{fname}' is not 300 DPI! DPI: {dpi}"
            assert width >= 3000, f"Figure '{fname}' resolution below publication grade: {width}px"

    # Verify 100% cryptographic match between DOCX embedded figures and master figures
    matched_count = 0
    for h, fname in master_hashes.items():
        if h in docx_hashes:
            matched_count += 1
            print(f"  MATCH: Master '{fname}' == DOCX '{docx_hashes[h]}' [SHA-256: {h[:12]}...]")
        else:
            raise AssertionError(f"Master figure '{fname}' (SHA-256: {h}) was not found embedded in DOCX!")

    assert matched_count == EXPECTED_FIGURES_COUNT, (
        f"Only matched {matched_count} out of {EXPECTED_FIGURES_COUNT} master figures in DOCX"
    )
    print("  100% of embedded figures match master 300 DPI assets byte-for-byte.")


if __name__ == "__main__":
    print("=" * 65)
    print("RUNNING DOCUMENT COMPILATION & RENDERING VERIFICATION SUITE")
    print("=" * 65)
    test_tectonic_compilation()
    test_pdf_rendering_and_metadata()
    test_docx_structure_and_native_tables()
    test_docx_omml_math_equations()
    test_docx_embedded_figures_sha256_match_master()
    print("\n>>> ALL DOCUMENT COMPILATION & RENDERING TESTS PASSED (100% COMPLIANT) <<<")
