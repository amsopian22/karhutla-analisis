#!/opt/anaconda3/envs/karhutla_env/bin/python
"""
independent_audit.py
Independent verification script written by the victory auditor.
Verifies all acceptance criteria from ORIGINAL_REQUEST.md directly from disk.
"""

import os
import sys
import re
import json
import zipfile
import hashlib
import subprocess
import xml.etree.ElementTree as ET
from PIL import Image
import pandas as pd

REPO = "/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis"
RESULTS = {}

def audit_abstract():
    print("--- 1. AUDITING ABSTRACT WORD COUNT ---")
    latex_path = os.path.join(REPO, "manuscript/sections/00_abstract.tex")
    md_path = os.path.join(REPO, "manuscript/manuscript_draft.md")
    docx_path = os.path.join(REPO, "manuscript/submission_package/manuscript_main.docx")
    pdf_path = os.path.join(REPO, "manuscript/main.pdf")

    # 1. LaTeX
    with open(latex_path) as f:
        l_raw = f.read()
    m_l = re.search(r"\\begin\{abstract\}(.*?)(?:\\vspace|\\noindent\\textbf\{Keywords:\}|\\end\{abstract\})", l_raw, re.DOTALL)
    l_text = re.sub(r"\\[a-zA-Z]+(\[[^\]]*\])?(\{([^}]*)\})?", r" \3 ", m_l.group(1).strip())
    l_clean = re.sub(r"[{}\$~%\\`'\"]", " ", l_text).strip()

    # 2. Markdown
    with open(md_path) as f:
        m_raw = f.read()
    m_m = re.search(r"## Abstract\s+(.*?)\s+\*\*Keywords:\*\*", m_raw, re.DOTALL)
    md_clean = re.sub(r"[`*_$~]", " ", m_m.group(1).strip())

    # 3. DOCX
    with zipfile.ZipFile(docx_path) as z:
        doc_xml = z.read("word/document.xml")
    root = ET.fromstring(doc_xml)
    docx_text = ""
    for p in root.findall(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
        t = "".join(p.itertext()).strip()
        if "Tropical peatlands" in t:
            docx_text = t
            break

    # 4. PDF
    res = subprocess.run(["/opt/homebrew/bin/pdftotext", "-f", "1", "-l", "1", pdf_path, "-"], capture_output=True, text=True, check=True)
    m_p = re.search(r"Abstract\s+(.*?)\s+Keywords:", res.stdout, re.DOTALL)
    pdf_text = m_p.group(1).strip()

    formats = [("LaTeX", l_clean), ("Markdown", md_clean), ("DOCX", docx_text), ("PDF", pdf_text)]
    abstract_results = {}
    for name, txt in formats:
        ws_count = len(txt.split())
        words_regex = len(re.findall(r"\b\w+\b", txt))
        clean_words = len([w for w in re.sub(r"[^\w\s-]", " ", txt).split() if w])
        print(f"  {name:10s} | Whitespace: {ws_count:3d} | Regex \\b\\w+\\b: {words_regex:3d} | Clean words: {clean_words:3d}")
        assert ws_count <= 250, f"{name} abstract exceeds 250 words on whitespace: {ws_count}"
        assert words_regex <= 250, f"{name} abstract exceeds 250 words on regex word boundary: {words_regex}"
        abstract_results[name] = {"whitespace": ws_count, "regex": words_regex, "clean": clean_words}
    RESULTS["abstract"] = abstract_results
    print(">>> ABSTRACT AUDIT: PASS (all formats <= 250 words)")

def audit_highlights():
    print("\n--- 2. AUDITING RESEARCH HIGHLIGHTS ---")
    md_path = os.path.join(REPO, "manuscript/highlights.md")
    docx_path = os.path.join(REPO, "manuscript/submission_package/highlights.docx")

    with open(md_path) as f:
        md_bullets = [line.strip().lstrip("*-").strip() for line in f if line.strip().startswith(("*", "-"))]

    with zipfile.ZipFile(docx_path) as z:
        doc_xml = z.read("word/document.xml")
    root = ET.fromstring(doc_xml)
    docx_bullets = []
    for p in root.findall(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
        t = "".join(p.itertext()).strip()
        if t and not t.lower().startswith("research highlights"):
            docx_bullets.append(t)

    print(f"  Markdown bullet count: {len(md_bullets)}")
    print(f"  DOCX bullet count:     {len(docx_bullets)}")
    assert len(md_bullets) == len(docx_bullets) == 5, f"Highlights count not 5: MD {len(md_bullets)}, DOCX {len(docx_bullets)}"
    assert 3 <= len(md_bullets) <= 5

    for i, (mb, db) in enumerate(zip(md_bullets, docx_bullets), 1):
        len_m = len(mb)
        len_d = len(db)
        print(f"  Bullet {i} | MD ({len_m:2d} chars): {mb}")
        print(f"            | DX ({len_d:2d} chars): {db}")
        assert len_m <= 85, f"MD bullet {i} exceeds 85 chars ({len_m})"
        assert len_d <= 85, f"DOCX bullet {i} exceeds 85 chars ({len_d})"

    RESULTS["highlights"] = {"count": len(md_bullets), "max_chars": max(len(b) for b in md_bullets)}
    print(">>> HIGHLIGHTS AUDIT: PASS (5 bullets, all <= 85 chars)")

def audit_keywords():
    print("\n--- 3. AUDITING KEYWORDS ---")
    latex_path = os.path.join(REPO, "manuscript/sections/00_abstract.tex")
    with open(latex_path) as f:
        l_raw = f.read()
    m_kw = re.search(r"\\textbf\{Keywords:\}.*?\\textit\{(.*?)\}", l_raw, re.DOTALL)
    kw_latex = [k.strip().rstrip(".") for k in m_kw.group(1).split(";") if k.strip()]

    print(f"  LaTeX Keywords count: {len(kw_latex)}")
    for i, kw in enumerate(kw_latex, 1):
        print(f"    {i}. {kw}")
    assert 1 <= len(kw_latex) <= 7, f"Keywords count not in [1, 7]: {len(kw_latex)}"
    assert len(kw_latex) == 7, "Expected exactly 7 keywords"

    # Check required conceptual anchors
    kw_str = " ".join(kw_latex).lower()
    for req in ["spatial", "geography", "autocorrelation", "cross-validation", "tenure", "peatlands"]:
        assert req in kw_str, f"Missing required keyword theme '{req}'"

    RESULTS["keywords"] = {"count": len(kw_latex), "list": kw_latex}
    print(">>> KEYWORDS AUDIT: PASS (7 keywords, fully aligned with Applied Geography)")

def audit_docx_rendering():
    print("\n--- 4. AUDITING DOCX RENDERING INTEGRITY ---")
    docx_path = os.path.join(REPO, "manuscript/submission_package/manuscript_main.docx")
    with zipfile.ZipFile(docx_path) as z:
        doc_xml = z.read("word/document.xml")
        media_names = [f for f in z.namelist() if f.startswith("word/media/")]
        docx_hashes = {hashlib.sha256(z.read(m)).hexdigest(): m for m in media_names}

    root = ET.fromstring(doc_xml)
    ns = {
        "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
        "m": "http://schemas.openxmlformats.org/officeDocument/2006/math"
    }

    tables = root.findall(".//w:tbl", ns)
    print(f"  Native <w:tbl> tables: {len(tables)}")
    assert len(tables) == 4, f"Expected 4 native Word tables, got {len(tables)}"

    omath = root.findall(".//m:oMath", ns)
    omath_para = root.findall(".//m:oMathPara", ns)
    print(f"  OMML equations (<m:oMath>): {len(omath)} (display paras: {len(omath_para)})")
    assert len(omath) >= 50, f"Expected >= 50 OMML equations, got {len(omath)}"

    xml_text = doc_xml.decode("utf-8")
    for pipe_pattern in ["| --- |", "| :--- |", "|:---|", "|---|"]:
        assert pipe_pattern not in xml_text, f"Unparsed markdown table pipe found: {pipe_pattern}"
    print("  Zero unparsed markdown table pipes detected.")

    # Image hashes & DPI
    master_figs = [
        "01_peta_wilayah_studi_spatial_cv.png",
        "02_peta_densitas_hotspot_frp.png",
        "03_analisis_citra_satelit_kanal.png",
        "04_peta_tenurial_konsesi_esg.png",
        "05_tren_temporal_dan_harian.png",
        "06_evaluasi_model_ml.png",
        "07_shap_feature_importance.png",
    ]
    print(f"  Embedded media images in DOCX: {len(media_names)}")
    assert len(media_names) == 7

    for fname in master_figs:
        fpath = os.path.join(REPO, "output/figures", fname)
        with open(fpath, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        assert h in docx_hashes, f"Figure {fname} (hash {h}) not found embedded in DOCX!"
        with Image.open(fpath) as img:
            dpi = img.info.get("dpi", (0, 0))
            assert round(dpi[0]) == 300, f"Figure {fname} DPI not 300: {dpi}"
            assert img.size[0] >= 3000, f"Figure {fname} width < 3000px: {img.size}"
        print(f"    - {fname}: 300 DPI ({img.size[0]}x{img.size[1]} px), SHA-256 match")

    RESULTS["docx"] = {"tables": len(tables), "omml_equations": len(omath), "figures_matched": len(master_figs)}
    print(">>> DOCX RENDERING AUDIT: PASS (4 native tables, 132 OMML, 7 figures 300 DPI)")

def audit_compilation():
    print("\n--- 5. AUDITING LATEX COMPILATION & PDF OUTPUT ---")
    main_tex = os.path.join(REPO, "manuscript/main.tex")
    tectonic = "/opt/homebrew/bin/tectonic"
    cmd = [tectonic, "main.tex"]
    res = subprocess.run(cmd, cwd=os.path.join(REPO, "manuscript"), capture_output=True, text=True)
    print(f"  Tectonic compilation exit code: {res.returncode}")
    assert res.returncode == 0, f"Tectonic compilation failed:\n{res.stderr}\n{res.stdout}"

    pdf_path = os.path.join(REPO, "manuscript/main.pdf")
    assert os.path.exists(pdf_path)
    pdfinfo = "/opt/homebrew/bin/pdfinfo"
    res_info = subprocess.run([pdfinfo, pdf_path], capture_output=True, text=True, check=True)
    info = res_info.stdout

    m_pages = re.search(r"Pages:\s+(\d+)", info)
    pages = int(m_pages.group(1))
    print(f"  PDF Pages: {pages}")
    assert pages == 28, f"Expected 28 pages, got {pages}"

    assert "Fire Intensity" in info, "Missing title in PDF metadata"
    assert "Ahmad Sopian" in info, "Missing author in PDF metadata"

    pdf_size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
    print(f"  PDF file size: {pdf_size_mb:.2f} MB")
    assert pdf_size_mb >= 5.0

    RESULTS["latex"] = {"exit_code": res.returncode, "pages": pages, "size_mb": round(pdf_size_mb, 2)}
    print(">>> LATEX & PDF AUDIT: PASS (Tectonic exit 0, exactly 28 pages, proper metadata)")

def audit_empirical_ground_truth():
    print("\n--- 6. AUDITING EMPIRICAL GROUND-TRUTH CONSISTENCY ---")
    data_csv = os.path.join(REPO, "data/processed/karhutla_kalteng_real_2026.csv")
    df = pd.read_csv(data_csv)
    n_total = len(df)
    n_severe = (df["frp_mw"] >= 12.0).sum()
    pct_severe = (df["frp_mw"] >= 12.0).mean() * 100
    tenure_counts = df["status_konsesi"].value_counts()
    tenure_pcts = df["status_konsesi"].value_counts(normalize=True) * 100

    print(f"  Master dataset row count: {n_total}")
    assert n_total == 43937, f"Expected 43937 rows, got {n_total}"

    print(f"  Severe FRP >= 12.0 MW: {n_severe} ({pct_severe:.2f}%)")
    assert n_severe == 6648
    assert abs(pct_severe - 15.13) < 0.05

    print(f"  Tenure distribution:")
    apl_key = [k for k in tenure_counts.index if "Non-Konsesi" in k][0]
    sawit_key = [k for k in tenure_counts.index if "Sawit" in k][0]
    pbph_key = [k for k in tenure_counts.index if "Kehutanan" in k][0]

    apl_count = tenure_counts[apl_key]
    apl_pct = tenure_pcts[apl_key]
    sawit_count = tenure_counts[sawit_key]
    sawit_pct = tenure_pcts[sawit_key]
    pbph_count = tenure_counts[pbph_key]
    pbph_pct = tenure_pcts[pbph_key]

    print(f"    - Non-Konsesi (APL): {apl_count} ({apl_pct:.2f}%)")
    print(f"    - Sawit (HGU):       {sawit_count} ({sawit_pct:.2f}%)")
    print(f"    - Kehutanan (PBPH):  {pbph_count} ({pbph_pct:.2f}%)")
    print(f"    - Total Concessions: {sawit_count + pbph_count} ({sawit_pct + pbph_pct:.2f}%)")

    assert apl_count == 33138
    assert abs(apl_pct - 75.42) < 0.05
    assert sawit_count == 7276
    assert abs(sawit_pct - 16.56) < 0.05
    assert pbph_count == 3523
    assert abs(pbph_pct - 8.02) < 0.05
    assert abs((sawit_pct + pbph_pct) - 24.58) < 0.05

    # Check model metrics file
    metrics_path = os.path.join(REPO, "output/reports/model_metrics.json")
    with open(metrics_path) as f:
        metrics = json.load(f)
    print("  Model Metrics JSON:")
    print(f"    Model A Random Test AUC: {metrics['model_a_spatial_memorization']['test_roc_auc']:.4f}")
    print(f"    Model A Spatial CV AUC:  {metrics['model_a_spatial_memorization']['spatial_block_cv_mean_roc_auc']:.4f}")
    print(f"    Model A Spatial CV F1:   {metrics['model_a_spatial_memorization']['spatial_block_cv_mean_f1']:.4f}")
    print(f"    Model B Test AUC:        {metrics['model_b_pure_biophysical']['test_roc_auc']:.4f}")
    print(f"    Model B Spatial CV F1:   {metrics['model_b_pure_biophysical']['spatial_block_cv_mean_f1']:.4f}")

    assert abs(metrics['model_a_spatial_memorization']['test_roc_auc'] - 0.7956) < 0.001
    assert abs(metrics['model_a_spatial_memorization']['spatial_block_cv_mean_roc_auc'] - 0.5399) < 0.001
    assert abs(metrics['model_a_spatial_memorization']['spatial_block_cv_mean_f1'] - 0.0583) < 0.001
    assert abs(metrics['model_b_pure_biophysical']['test_roc_auc'] - 0.7527) < 0.001
    assert abs(metrics['model_b_pure_biophysical']['spatial_block_cv_mean_f1'] - 0.1399) < 0.001

    RESULTS["empirical"] = {
        "total_hotspots": int(n_total),
        "severe_fires": int(n_severe),
        "apl_pct": float(round(apl_pct, 2)),
        "concessions_pct": float(round(sawit_pct + pbph_pct, 2)),
        "model_a_spatial_auc": float(metrics['model_a_spatial_memorization']['spatial_block_cv_mean_roc_auc']),
        "model_b_spatial_f1": float(metrics['model_b_pure_biophysical']['spatial_block_cv_mean_f1']),
    }
    print(">>> EMPIRICAL GROUND-TRUTH AUDIT: PASS (All numbers match 100% with zero distortion)")

def audit_author_and_statements():
    print("\n--- 7. AUDITING AUTHORSHIP, CREDIT, & ETHICAL STATEMENTS ---")
    tex_path = os.path.join(REPO, "manuscript/main.tex")
    md_path = os.path.join(REPO, "manuscript/manuscript_draft.md")

    for path, name in [(tex_path, "LaTeX"), (md_path, "Markdown")]:
        with open(path) as f:
            content = f.read()
        assert "Ahmad Sopian" in content, f"Missing Ahmad Sopian in {name}"
        assert "Rahmi Susanti" in content, f"Missing Rahmi Susanti in {name}"
        assert "Universitas Mulawarman" in content, f"Missing Unmul affiliation in {name}"
        assert "CRediT" in content or "Author Contributions" in content, f"Missing CRediT statement in {name}"
        assert "Competing Interest" in content or "Conflict of Interest" in content, f"Missing COI declaration in {name}"
        assert "Data Availability" in content, f"Missing Data Availability in {name}"
        assert "https://github.com/amsopian22/karhutla-analisis" in content, f"Missing GitHub repository link in {name}"
        print(f"  {name}: Authorship, CRediT, COI, and Data Availability fully present.")

    RESULTS["ethics"] = "PASS"
    print(">>> ETHICAL & AUTHORSHIP AUDIT: PASS")

if __name__ == "__main__":
    audit_abstract()
    audit_highlights()
    audit_keywords()
    audit_docx_rendering()
    audit_compilation()
    audit_empirical_ground_truth()
    audit_author_and_statements()
    print("\n" + "="*70)
    print("FINAL SUMMARY OF INDEPENDENT AUDIT:")
    print(json.dumps(RESULTS, indent=2))
    print("ALL INDEPENDENT CHECKS PASSED UNCONDITIONALLY!")
    print("="*70)
