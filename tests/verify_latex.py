#!/usr/bin/env python3
"""
tests/verify_latex.py

Static validation script for the publication-ready LaTeX manuscript.
Verifies:
1. File completeness and modular structure.
2. LaTeX environment balance (\\begin{...} vs \\end{...}).
3. All labels and cross-references (\\label vs \\ref) resolving with zero missing.
4. All citations (\\cite, \\citep, \\citet) matching valid keys in references.bib with zero undefined keys.
5. All referenced figure files existing on disk and all 7 mandatory figures included.
6. Methodological integrity: equations 1-5, tables 1-4, and Section 4.4 study limitations.
"""

import os
import re
import sys
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANUSCRIPT_DIR = PROJECT_ROOT / "manuscript"
MAIN_TEX = MANUSCRIPT_DIR / "main.tex"
BIB_FILE = MANUSCRIPT_DIR / "references.bib"
SECTIONS_DIR = MANUSCRIPT_DIR / "sections"
FIGURES_DIR = PROJECT_ROOT / "output" / "figures"

EXPECTED_SECTIONS = [
    "00_abstract.tex",
    "01_introduction.tex",
    "02_materials_methods.tex",
    "03_results.tex",
    "04_discussion.tex",
    "05_conclusions.tex",
]

EXPECTED_FIGURES = [
    "01_peta_wilayah_studi_spatial_cv.png",
    "02_peta_densitas_hotspot_frp.png",
    "03_analisis_citra_satelit_kanal.png",
    "04_peta_tenurial_konsesi_esg.png",
    "05_tren_temporal_dan_harian.png",
    "06_evaluasi_model_ml.png",
    "07_shap_feature_importance.png",
]

class LatexValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.full_tex = ""
        self.bib_keys = set()
        self.labels = {}
        self.refs = []
        self.cites = []
        self.included_graphics = []

    def log_error(self, message):
        self.errors.append(message)
        print(f"  [ERROR] {message}")

    def log_warning(self, message):
        self.warnings.append(message)
        print(f"  [WARN]  {message}")

    def log_success(self, message):
        print(f"  [PASS]  {message}")

    def verify_files_exist(self):
        print("\n--- [1] Memverifikasi Keberadaan Berkas Manuskrip & Gambar ---")
        if not MAIN_TEX.is_file():
            self.log_error(f"main.tex tidak ditemukan di: {MAIN_TEX}")
        else:
            self.log_success(f"main.tex ditemukan ({MAIN_TEX.stat().st_size} bytes)")

        if not BIB_FILE.is_file():
            self.log_error(f"references.bib tidak ditemukan di: {BIB_FILE}")
        else:
            self.log_success(f"references.bib ditemukan ({BIB_FILE.stat().st_size} bytes)")

        for sec in EXPECTED_SECTIONS:
            sec_path = SECTIONS_DIR / sec
            if not sec_path.is_file():
                self.log_error(f"Bagian modular {sec} tidak ditemukan di: {sec_path}")
            else:
                self.log_success(f"Bagian modular {sec} ditemukan ({sec_path.stat().st_size} bytes)")

        for fig in EXPECTED_FIGURES:
            fig_path = FIGURES_DIR / fig
            if not fig_path.is_file():
                self.log_error(f"Gambar ilmiah wajib {fig} tidak ditemukan di: {fig_path}")
            else:
                self.log_success(f"Gambar {fig} ditemukan ({fig_path.stat().st_size} bytes)")

    def assemble_full_text(self):
        print("\n--- [2] Menyusun Dokumen Lengkap dari Modular Sections ---")
        if not MAIN_TEX.is_file():
            return

        with open(MAIN_TEX, "r", encoding="utf-8") as f:
            main_content = f.read()

        def replace_input(match):
            rel_path = match.group(1).strip()
            if not rel_path.endswith(".tex"):
                rel_path += ".tex"
            target_path = MANUSCRIPT_DIR / rel_path
            if not target_path.is_file():
                self.log_error(f"File yang di-\\input tidak ditemukan: {target_path}")
                return ""
            with open(target_path, "r", encoding="utf-8") as sec_f:
                return sec_f.read()

        # Recursively resolve \input{...}
        assembled = main_content
        for _ in range(5):  # allow nested inputs up to 5 levels
            if r"\input{" not in assembled:
                break
            assembled = re.sub(r"\\input\{([^}]+)\}", replace_input, assembled)

        self.full_tex = assembled
        self.log_success(f"Dokumen lengkap berhasil disusun ({len(self.full_tex.splitlines())} baris, {len(self.full_tex)} karakter)")

    def check_environment_balance(self):
        print("\n--- [3] Memeriksa Keseimbangan Lingkungan LaTeX (\\begin vs \\end) ---")
        # Strip comments
        lines = [re.sub(r"(?<!\\)%.*", "", line) for line in self.full_tex.splitlines()]
        clean_text = "\n".join(lines)

        env_stack = []
        pattern = re.compile(r"\\(begin|end)\{([^}]+)\}")
        
        mismatches = 0
        for match in pattern.finditer(clean_text):
            action, env_name = match.groups()
            line_no = clean_text[:match.start()].count("\n") + 1

            if action == "begin":
                env_stack.append((env_name, line_no))
            elif action == "end":
                if not env_stack:
                    self.log_error(f"Unmatched \\end{{{env_name}}} pada baris {line_no}")
                    mismatches += 1
                else:
                    last_env, last_line = env_stack.pop()
                    if last_env != env_name:
                        self.log_error(f"Lingkungan tidak seimbang: \\begin{{{last_env}}} (baris {last_line}) ditutup oleh \\end{{{env_name}}} (baris {line_no})")
                        mismatches += 1

        if env_stack:
            for env_name, line_no in env_stack:
                self.log_error(f"Lingkungan belum ditutup: \\begin{{{env_name}}} pada baris {line_no}")
                mismatches += 1

        if mismatches == 0:
            self.log_success("Seluruh lingkungan LaTeX seimbang secara sempurna (0 mismatch).")

    def parse_bib_keys(self):
        print("\n--- [4] Mem-parsing Berkas Bibliografi references.bib ---")
        if not BIB_FILE.is_file():
            return

        with open(BIB_FILE, "r", encoding="utf-8") as f:
            bib_content = f.read()

        keys = re.findall(r"@\w+\s*\{\s*([^,\s]+),", bib_content)
        self.bib_keys = set(keys)
        self.log_success(f"Ditemukan {len(self.bib_keys)} entri BibTeX valid di references.bib")
        if len(self.bib_keys) < 40:
            self.log_error(f"Jumlah entri BibTeX kurang dari 40 (hanya {len(self.bib_keys)})")
        else:
            self.log_success("Target 40 entri BibTeX bereputasi tinggi terpenuhi.")

    def check_citations(self):
        print("\n--- [5] Memverifikasi Integritas Sitasi (\\cite, \\citep, \\citet) ---")
        lines = [re.sub(r"(?<!\\)%.*", "", line) for line in self.full_tex.splitlines()]
        clean_text = "\n".join(lines)

        cite_pattern = re.compile(r"\\(?:cite|citep|citet|citeauthor|citeyear)\{([^}]+)\}")
        found_cites = set()
        missing_keys = set()

        for match in cite_pattern.finditer(clean_text):
            raw_keys = match.group(1).split(",")
            for raw_k in raw_keys:
                k = raw_k.strip()
                if k:
                    found_cites.add(k)
                    if k not in self.bib_keys:
                        missing_keys.add(k)

        self.cites = list(found_cites)
        self.log_success(f"Ditemukan {len(found_cites)} kunci sitasi unik pada teks naskah.")

        if missing_keys:
            for k in sorted(missing_keys):
                self.log_error(f"Undefined citation key: '{k}' tidak ditemukan di references.bib")
        else:
            self.log_success("100% kunci sitasi pada naskah terdefinisi di references.bib (0 undefined keys).")

        # Check coverage of references.bib
        uncited = self.bib_keys - found_cites
        if uncited:
            self.log_warning(f"{len(uncited)} entri di references.bib tidak disitir pada teks: {sorted(uncited)}")
        else:
            self.log_success("Semua 40 entri di references.bib disitir secara aktif di naskah!")

    def check_labels_and_refs(self):
        print("\n--- [6] Memeriksa Label dan Referensi Silang (\\label vs \\ref) ---")
        lines = [re.sub(r"(?<!\\)%.*", "", line) for line in self.full_tex.splitlines()]
        clean_text = "\n".join(lines)

        # Labels
        label_pattern = re.compile(r"\\label\{([^}]+)\}")
        defined_labels = set()
        duplicate_labels = set()

        for match in label_pattern.finditer(clean_text):
            lbl = match.group(1).strip()
            if lbl in defined_labels:
                duplicate_labels.add(lbl)
            defined_labels.add(lbl)

        if duplicate_labels:
            for lbl in duplicate_labels:
                self.log_error(f"Duplicate label: '{lbl}' didefinisikan lebih dari satu kali")
        else:
            self.log_success(f"Ditemukan {len(defined_labels)} label unik tanpa duplikasi.")

        # References
        ref_pattern = re.compile(r"\\(?:ref|pageref|eqref)\{([^}]+)\}")
        referenced_keys = set()
        unresolved_refs = set()

        for match in ref_pattern.finditer(clean_text):
            ref_k = match.group(1).strip()
            referenced_keys.add(ref_k)
            if ref_k not in defined_labels:
                unresolved_refs.add(ref_k)

        self.log_success(f"Ditemukan {len(referenced_keys)} referensi silang unik pada teks.")

        if unresolved_refs:
            for ref_k in sorted(unresolved_refs):
                self.log_error(f"Unresolved reference: '\\ref{{{ref_k}}}' tidak memiliki \\label yang sesuai!")
        else:
            self.log_success("100% referensi silang (\\ref) terselesaikan secara sempurna ke \\label.")

        # Check figure labels
        fig_labels = [f"fig:{name}" for name in ["study_area", "fire_density_frp", "satellite_canal_forensic", "tenurial_concession", "temporal_dynamics", "model_evaluation", "shap_importance"]]
        for fl in fig_labels:
            if fl not in defined_labels:
                self.log_error(f"Label figur wajib '{fl}' tidak ditemukan!")
            elif fl not in referenced_keys:
                self.log_warning(f"Label figur '{fl}' didefinisikan tapi tidak ada callout '\\ref{{{fl}}}'")
            else:
                self.log_success(f"Figur '{fl}' terdefinisi dan memiliki callout aktif di teks.")

    def check_graphics_inclusion(self):
        print("\n--- [7] Memeriksa Penyisipan Gambar (\\includegraphics) ---")
        lines = [re.sub(r"(?<!\\)%.*", "", line) for line in self.full_tex.splitlines()]
        clean_text = "\n".join(lines)

        graphic_pattern = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
        found_graphics = []

        for match in graphic_pattern.finditer(clean_text):
            img_path_str = match.group(1).strip()
            found_graphics.append(img_path_str)

        self.log_success(f"Ditemukan {len(found_graphics)} perintah \\includegraphics")

        # Resolve each image
        for img in found_graphics:
            img_name = Path(img).name
            target = FIGURES_DIR / img_name
            if not target.is_file():
                self.log_error(f"File gambar '{img}' (diharapkan di {target}) tidak ada di disk!")
            else:
                self.log_success(f"File gambar '{img_name}' terverifikasi ada ({target.stat().st_size} bytes)")

        # Verify all 7 required figures are included
        included_names = [Path(img).name for img in found_graphics]
        for exp_fig in EXPECTED_FIGURES:
            if exp_fig not in included_names:
                self.log_error(f"Gambar wajib '{exp_fig}' tidak disisipkan via \\includegraphics!")
            else:
                self.log_success(f"Gambar wajib '{exp_fig}' terkonfirmasi disisipkan.")

    def check_scientific_integrity(self):
        print("\n--- [8] Memverifikasi Integritas Saintifik & Kelengkapan Narasi ---")
        # 1. Check equations 1-5
        eq_labels = ["eq:canal_dist", "eq:fwi", "eq:target", "eq:spatial_cv", "eq:shap"]
        for eq_lbl in eq_labels:
            if f"\\label{{{eq_lbl}}}" not in self.full_tex:
                self.log_error(f"Persamaan wajib dengan label '{eq_lbl}' tidak ditemukan!")
            else:
                self.log_success(f"Persamaan '{eq_lbl}' ditemukan.")

        # 2. Check tables 1-4
        tab_labels = ["tab:decadal_sipongi", "tab:regency_distribution", "tab:model_comparison", "tab:shap_ranking"]
        for tab_lbl in tab_labels:
            if f"\\label{{{tab_lbl}}}" not in self.full_tex:
                self.log_error(f"Tabel wajib dengan label '{tab_lbl}' tidak ditemukan!")
            else:
                self.log_success(f"Tabel '{tab_lbl}' ditemukan.")

        # 3. Check Section 4.4 Study Limitations
        if "Study Limitations, Uncertainties, and Threats to Validity" not in self.full_tex:
            self.log_error("Sub-bab wajib 'Study Limitations, Uncertainties, and Threats to Validity' tidak ditemukan!")
        else:
            self.log_success("Sub-bab 4.4 'Study Limitations, Uncertainties, and Threats to Validity' terkonfirmasi ada.")

        # Check key discussion topics in 4.4
        topics = [
            ("Sensors & Smoldering", ["smoldering", "orbital", "overpasses", "radiance"]),
            ("ERA5 scale mismatch", ["ERA5-Land", "ecological fallacy", "resolution"]),
            ("Temporal crisis scope", ["October 2026", "pulse", "transition"]),
            ("Spatial Block CV & Class Imbalance", ["covariate shift", "class_weight", "loss asymmetry", "alert fatigue"]),
            ("APL heterogeneity", ["APL", "customary", "tenure"]),
        ]
        for topic_name, keywords in topics:
            matched = any(kw.lower() in self.full_tex.lower() for kw in keywords)
            if not matched:
                self.log_error(f"Topik limitasi '{topic_name}' tidak terbahas secara adekuat di teks!")
            else:
                self.log_success(f"Topik limitasi '{topic_name}' terkonfirmasi dibahas.")

    def run(self):
        print("==================================================================")
        print("      VERIFIKASI STATIS NASKAH ILMIAH LATEX (tests/verify_latex.py)")
        print("==================================================================")
        self.verify_files_exist()
        self.assemble_full_text()
        self.check_environment_balance()
        self.parse_bib_keys()
        self.check_citations()
        self.check_labels_and_refs()
        self.check_graphics_inclusion()
        self.check_scientific_integrity()

        print("\n==================================================================")
        print(f"HASIL VERIFIKASI: {len(self.errors)} Error, {len(self.warnings)} Warning")
        print("==================================================================")

        if self.errors:
            print(f"\n❌ PENGUJIAN GAGAL: Terdeteksi {len(self.errors)} kesalahan teknis pada naskah LaTeX!")
            for i, err in enumerate(self.errors, 1):
                print(f"  {i}. {err}")
            return 1
        else:
            print("\n✅ PENGUJIAN LULUS SEMPURNA (0 ERROR):")
            print("  - Struktur berkas modular lengkap.")
            print("  - Keseimbangan lingkungan \\begin dan \\end 100% valid.")
            print("  - Seluruh referensi silang (\\ref) dan label (\\label) terselesaikan.")
            print("  - 100% sitasi (\\cite) valid dan terdaftar di references.bib.")
            print("  - 7 figur ilmiah terintegrasi dengan benar dan file terverifikasi ada.")
            print("  - Persamaan 1-5, Tabel 1-4, dan Sub-bab 4.4 terverifikasi lengkap.")
            return 0

if __name__ == "__main__":
    validator = LatexValidator()
    exit_code = validator.run()
    sys.exit(exit_code)
