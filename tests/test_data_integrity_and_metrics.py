"""
Test Suite: Data Integrity, Spatial BDD Metrics, and Scientific Consistency
Ensures all reported numerical figures, spatial BDD metrics, hypothesis numbering,
and feature definitions match between raw/processed datasets, summary JSONs, and manuscript sources.
"""

import os
import json
import re
import pytest
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROCESSED = os.path.join(BASE_DIR, "data", "processed", "karhutla_kalteng_2019_2026.csv")
BDD_SUMMARY_PATH = os.path.join(BASE_DIR, "output", "reports", "spatial_bdd_summary.json")
MANUSCRIPT_TEX_DIR = os.path.join(BASE_DIR, "manuscript", "sections")
MANUSCRIPT_MD = os.path.join(BASE_DIR, "manuscript", "manuscript_without_author_details.md")


def test_master_dataset_integrity():
    """Verify master processed dataset contains exact 43,937 observations and consistent tenure splits."""
    assert os.path.exists(DATA_PROCESSED), f"Dataset not found: {DATA_PROCESSED}"
    df = pd.read_csv(DATA_PROCESSED)

    # 1. Total observations
    assert len(df) == 43937, f"Expected 43,937 rows, got {len(df)}"

    # 2. Tenure classification counts (status_konsesi)
    tenure_counts = df["status_konsesi"].value_counts().to_dict()
    assert tenure_counts.get("Non-Konsesi (Area Penggunaan Lain / Komunitas)") == 33138, f"APL count mismatch: {tenure_counts}"
    assert tenure_counts.get("Konsesi Perkebunan Sawit (HGU)") == 7276, f"HGU count mismatch: {tenure_counts}"
    assert tenure_counts.get("Konsesi Kehutanan (IUPHHK-HTI/HA)") == 3523, f"PBPH count mismatch: {tenure_counts}"

    # 3. Severe fire counts (FRP >= 12.0 MW)
    severe_fires = (df["frp_mw"] >= 12.0).sum()
    assert severe_fires == 6648, f"Expected 6,648 severe fires, got {severe_fires}"

    # 4. Peatland soil counts
    peat_mask = df["tipe_lahan"].astype(str).str.lower().str.contains("peat|gambut")
    peat_count = peat_mask.sum()
    assert peat_count == 32643, f"Expected 32,643 peat fires, got {peat_count}"


def test_spatial_bdd_metrics():
    """Verify Spatial Boundary Discontinuity summary metrics and robustness checks."""
    assert os.path.exists(BDD_SUMMARY_PATH), f"Spatial BDD summary not found: {BDD_SUMMARY_PATH}"
    with open(BDD_SUMMARY_PATH, "r") as f:
        bdd = json.load(f)

    # 1. Interior vs Exterior baseline density
    summary_3km = bdd["discontinuity_3km_summary"]
    interior_density = summary_3km["interior_minus_3km_to_0"]["density_per_km2"]
    exterior_density = summary_3km["exterior_0_to_plus_3km"]["density_per_km2"]
    assert pytest.approx(interior_density, abs=0.001) == 0.1830
    assert pytest.approx(exterior_density, abs=0.001) == 0.2864

    # 2. Step jump tau_BDD and percentage
    metrics = summary_3km["discontinuity_metrics"]
    tau_bdd = metrics["density_difference_per_km2"]
    pct_jump = metrics["density_percentage_increase"]
    assert pytest.approx(tau_bdd, abs=0.001) == 0.1034
    assert pytest.approx(pct_jump, abs=0.1) == 56.5

    # 3. Combustion intensity parity (Mann-Whitney p-value)
    mw_p = metrics["mann_whitney_p_value"]
    assert pytest.approx(mw_p, abs=0.01) == 0.278

    # 4. Robustness checks present
    assert "robustness_checks" in bdd, "Robustness checks missing from spatial BDD summary"
    rob = bdd["robustness_checks"]

    # Bandwidth sensitivity
    bw = rob["bandwidth_sensitivity"]
    assert bw["bandwidth_1km"]["percentage_increase"] == 12.0
    assert bw["bandwidth_2km"]["percentage_increase"] == 31.9
    assert bw["bandwidth_3km"]["percentage_increase"] == 56.5

    # Placebo test
    placebo = rob["placebo_boundary_test_minus_1km"]
    assert pytest.approx(placebo["placebo_density_ratio"], abs=0.01) == 1.084

    # Decomposition
    decomp = rob["concession_type_breakdown"]
    assert pytest.approx(decomp["oil_palm_hgu"]["interior_density_per_km2"], abs=0.001) == 0.2268
    assert pytest.approx(decomp["forestry_pbph"]["interior_density_per_km2"], abs=0.001) == 0.0766


def test_hypothesis_numbering_consistency():
    """Verify hypothesis numbering is strictly harmonized across all manuscript files."""
    tex_files = [os.path.join(MANUSCRIPT_TEX_DIR, f) for f in os.listdir(MANUSCRIPT_TEX_DIR) if f.endswith(".tex")]
    assert len(tex_files) > 0

    all_content = ""
    for tf in tex_files:
        with open(tf, "r") as f:
            all_content += f.read() + "\n"

    # H1 must be Spatial Boundary Discontinuity / corporate liability
    assert "Spatial Boundary Discontinuity" in all_content or "corporate strict liability" in all_content

    # H2 must have sub-hypotheses H2a and H2b
    assert "H_{2a}" in all_content or "H2a" in all_content
    assert "H_{2b}" in all_content or "H2b" in all_content

    # Check for forbidden legacy phrasing: "Hypothesis H_1 (Spatial Memorization Collapse)"
    assert "Hypothesis $\\mathbf{H_1}$ (Spatial Memorization Collapse)" not in all_content
    assert "Hypothesis $\\mathbf{H_2}$ (Biophysical Generalizability)" not in all_content


def test_abstract_word_count():
    """Verify Abstract adheres strictly to journal word count constraints (<= 250 words)."""
    abstract_tex = os.path.join(MANUSCRIPT_TEX_DIR, "00_abstract.tex")
    with open(abstract_tex, "r") as f:
        text = f.read()

    # Extract body between \begin{abstract} and \end{abstract}
    m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.DOTALL)
    assert m is not None, "Abstract block not found"
    body = m.group(1)

    # Remove LaTeX commands, math, and keywords
    body = re.sub(r"\\textbf\{Keywords:.*?$", "", body, flags=re.DOTALL)
    body = re.sub(r"\\[a-zA-Z]+(\[[^\]]*\])?(\{[^\}]*\})?", " ", body)
    body = re.sub(r"\$[^$]*\$", " ", body)
    body = re.sub(r"[^a-zA-Z0-9\s]", " ", body)
    words = [w for w in body.split() if len(w) > 0]
    word_count = len(words)

    assert word_count <= 250, f"Abstract exceeds 250 words: {word_count} words"
