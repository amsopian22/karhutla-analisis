# Comprehensive Specification Mining & Manuscript Audit Report
**Journal Target:** *Applied Geography* (Elsevier — Impact Factor: 7.4, CiteScore: 8.3, Scopus Q1)  
**Lead Investigator:** explorer_ag_survey_1 (`teamwork_spec_miner`)  
**Audit Date:** 2026-11-04  
**Working Environment:** `/opt/anaconda3/envs/karhutla_env/bin/python` (Python 3.10)

---

## Executive Summary

Audit komprehensif ini memeriksa keselarasan seluruh berkas naskah (*manuscript submission package*) terhadap pedoman resmi penulisan jurnal Elsevier *Applied Geography* (*Guide for Authors*) dan kriteria penerimaan pada `ORIGINAL_REQUEST.md`. Penyelidikan dilakukan secara objektif dan terukur menggunakan skrip Python (`zipfile`, `xml.etree.ElementTree`, `re`, `natbib/bibtex parser`) pada lingkungan conda `karhutla_env`.

### Status Kepatuhan Inti:
1. **Research Highlights:** **LULUS (100% COMPLIANT)**. Tepat 5 butir (*bullet points*), dengan panjang karakter antara 75 hingga 80 karakter (batas maksimum Elsevier: 85 karakter termasuk spasi). Format konsisten di `highlights.md` dan `highlights.docx`.
2. **Abstract Word Count:** **TIDAK LULUS (VIOLATION)**.
   - `00_abstract.tex`: **363 kata** (+113 kata / 45.2% melebihi batas 250 kata).
   - `manuscript_draft.md`: **369 kata** (+119 kata / 47.6% melebihi batas 250 kata).
   - `manuscript_main.docx`: **368 kata** (+118 kata / 47.2% melebihi batas 250 kata).
   *Tindakan*: Disediakan draf abstrak terkalibrasi 242 kata yang mempertahankan seluruh temuan kuantitatif esensial.
3. **Keywords:** **TIDAK LULUS (VIOLATION)**.
   - `00_abstract.tex`: **10 kata kunci** (batas Elsevier: 1–7 kata kunci).
   - `manuscript_draft.md`: **9 kata kunci** (batas Elsevier: 1–7 kata kunci).
   - `manuscript_main.docx`: **9 kata kunci** (batas Elsevier: 1–7 kata kunci).
   - `main.tex` hyperref: 7 kata kunci, namun belum memuat istilah sentral *Applied Geography* (seperti *Spatial autocorrelation*, *Land tenure governance*, dan *GIScience*).
4. **Reference & In-text Citation Style:** **DISCREPANCY DETECTED**.
   - Pedoman *Applied Geography*: Standar **APA 7th edition / author-year** (misal: Smith et al., 2020) dengan daftar pustaka alfabetis.
   - `main.tex` saat ini: Menggunakan `\usepackage[square,numbers,sort&compress]{natbib}` dan `\bibliographystyle{unsrtnat}` (gaya numerik urutan sitasi `[1]`). Meskipun diizinkan pada tahap awal lewat *Your Paper Your Way*, penyelarasan ke author-year sangat dianjurkan.
5. **Front Matter & Deklarasi Etika:** **LULUS (100% COMPLIANT)**.
   - CRediT Authorship Statement lengkap untuk Ahmad Sopian & Rahmi Susanti.
   - Declaration of Competing Interest lengkap dan bertanggal.
   - Data Availability Statement memuat repositori publik GitHub (`https://github.com/amsopian22/karhutla-analisis`).
   - Cover Letter tertuju tepat ke Editor-in-Chief *Applied Geography*.
6. **Metadata Judul Jurnal:** **DISCREPANCY DETECTED**.
   - `manuscript_draft.md` baris 10 masih mencantumkan target jurnal lama (*Remote Sensing of Environment* / *IJWF* / *MDPI Remote Sensing*). Perlu diselaraskan menjadi *Applied Geography*.

---

## Features Discovered

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| 1 | Editorial Guidelines | Highlights Bullet Count | Elsevier mensyaratkan 3 hingga 5 butir ringkasan penelitian (*bullet points*) | File `highlights.md` & `highlights.docx` | Tepat 5 butir (*bullets*) | Gagal jika < 3 atau > 5 butir | Elsevier Guide for Authors; audit skrip Python |
| 2 | Editorial Guidelines | Highlights Character Length | Setiap butir highlight maksimal 85 karakter termasuk spasi | Butir 1 s.d. 5 teks highlight | B1: 76, B2: 80, B3: 75, B4: 76, B5: 77 karakter | Pelanggaran jika panjang karakter > 85 | Audit programatik via Python `len(b)` |
| 3 | Editorial Guidelines | Abstract Word Count | Abstrak maksimal 250 kata, merangkum latar belakang, metode, hasil utama, dan simpulan | File `00_abstract.tex`, `manuscript_draft.md`, `manuscript_main.docx` | .tex: 363 kata, .md: 369 kata, .docx: 368 kata | Pelanggaran berat (>110 kata di atas batas) | Ekstraksi token kata Python `re.split` |
| 4 | Editorial Guidelines | Keywords Count & Scope | Elsevier mensyaratkan antara 1 hingga 7 kata kunci yang merefleksikan disiplin spasial | Teks keywords di .tex, .md, dan .docx | .tex: 10 keywords, .md: 9 keywords, .docx: 9 keywords | Pelanggaran batas maksimum (harus <= 7) | Parsing semikolon dan koma di berkas sumber |
| 5 | Citation & References | In-text Citation Style | Gaya sitasi teks harus konsisten dengan format APA (author-year) | Teks pengutipan di LaTeX, Markdown, dan DOCX | LaTeX: numerik `[1]`, Markdown: `(@Page2002Nature)`, DOCX: `(Page et al. (2002))` | Inkonsistensi format antara LaTeX numerik vs Word/MD author-year | Inspeksi `main.tex`, `01_introduction.tex`, `document.xml` |
| 6 | Citation & References | Reference Bibliography Style | Daftar pustaka terurut alfabetis berformat APA 7th | `manuscript/references.bib` (425 baris) | 26 entri referensi lengkap dengan DOI | Ketidaksesuaian jika menggunakan `unsrtnat` di LaTeX | Inspeksi `references.bib` dan `main.tex` |
| 7 | Ethical Governance | CRediT Author Statement | Pembagian kontribusi penulis berstandar taksonomi CRediT Elsevier (14 peran) | `credit_statement.md`, `credit_statement.docx`, `main.tex` | Ahmad Sopian (8 peran), Rahmi Susanti (5 peran + domain kesehatan lingkungan) | Tidak valid jika peran tidak sesuai taksonomi CRediT | Panduan CRediT Elsevier & inspeksi berkas |
| 8 | Ethical Governance | Declaration of Interest | Pernyataan transparansi konflik kepentingan finansial / personal | `declaration_of_interest.md` & `.docx` | Deklarasi standar tanpa konflik kepentingan, tertanggal 4 November 2026 | Ditolak redaksi jika tidak disertakan | Elsevier Ethics Guidelines |
| 9 | Ethical Governance | Data Availability Statement | Pernyataan keterbukaan data dan transparansi kode analisis | `main.tex`, `manuscript_draft.md`, `manuscript_main.docx` | Tautan langsung ke repositori GitHub: `https://github.com/amsopian22/karhutla-analisis` | Red flag jika data mentah/proses tidak dapat diakses | Kebijakan Open Data Elsevier |
| 10 | Editorial Submission | Cover Letter Journal Fit | Surat pengantar yang menjelaskan relevansi naskah terhadap Aims & Scope *Applied Geography* | `cover_letter.md`, `cover_letter.docx` | Menekankan geografi terapan, Hukum Pertama Tobler, mitigasi autokorelasi spasial, dan tata kelola tenurial APL | Desk rejection jika dinilai di luar ruang lingkup (*out of scope*) | Elsevier Editorial System Requirements |
| 11 | Thematic Alignment | Aims & Scope Fit | Penyelarasan narasi naskah dengan tagline "Putting problems in a geographical perspective" | Naskah keseluruhan | Menyoroti fenomena biofisik dan sosial-spasial (APL vs konsesi) di lahan gambut terdegradasi | Penolakan redaksi jika hanya berfokus pada algoritma ML murni | Elsevier Applied Geography Aims & Scope |
| 12 | Visual Integrity | LaTeX Compilation & Cross-references | Kompilasi LaTeX bebas error dengan resolusi gambar tinggi dan tautan label utuh | `manuscript/main.tex`, `manuscript/sections/*.tex` | Tectonic exit code 0; 7 gambar ditemukan; 57 label & 21 referensi silang terhubung | PDF rusak atau terdapat tanda tanya `??` jika label hilang | Uji kompilasi Tectonic 0.16.9 |
| 13 | Visual Integrity | Word Document Embedding | Berkas Word submission memuat tabel terformat dan gambar resolusi tinggi | `manuscript/submission_package/manuscript_main.docx` | 7 gambar resolusi tinggi dalam folder `word/media/`, 4 tabel Word | Gambar pecah atau tabel berantakan | Pemeriksaan arsip zip XML DOCX |

---

## Edge Cases

| # | Feature | Input | Observed Behavior |
|---|---------|-------|-------------------|
| 1 | Highlights Length | Butir 2: "Coordinate models collapse under Spatial Block CV, proving spatial memorization." | Panjang tepat 80 karakter. Jika ditambahkan 6 karakter lagi akan melanggar batas 85 karakter. |
| 2 | Highlights Formatting in Word | `highlights.docx` | Butir tersimpan menggunakan penomoran format list Word (`<w:numPr>`), bukan karakter bullet manual (UTF-8 bullet). Ini adalah praktik terbaik agar layout rapi di MS Word. |
| 3 | Abstract LaTeX Markup Tokens | `00_abstract.tex` | Skrip penghitung kata awal menghitung token LaTeX seperti `\noindent`, `\vspace{0.4em}`, `\textbf{...}`, dan satuan `\,km` sebagai kata. Setelah dibersihkan dari sintaks LaTeX, jumlah kata murni adalah 362 kata (tetap melanggar batas 250 kata). |
| 4 | Abstract Multi-paragraph in Word | `manuscript_main.docx` | Abstrak dalam Word terbagi menjadi dua paragraf (P4: 158 kata, P5: 210 kata) dengan total 368 kata. Dalam beberapa sistem submission online Elsevier, abstrak diharapkan berupa satu paragraf tunggal bersambung. |
| 5 | Pandoc LaTeX Math in DOCX | Sintaks matematika `$H_1$`, `$F_1$`, `$\ge$` dalam `manuscript_draft.md` dan `cover_letter.md` | Pandoc mengonversi ekspresi matematika menjadi objek Word Equation XML (`<m:oMath>`). Teks standar `<w:t>` tidak membaca objek ini sehingga tampak kosong pada ekstraksi teks sederhana, namun dirender dengan benar sebagai simbol Unicode matematis ($\ge$, $H_1$, $F_1$) di antarmuka Word. |
| 6 | Double Parentheses Citation in DOCX | Pengutipan Markdown `(@Page2002Nature)` | Menghasilkan tanda kurung ganda dalam Word: `(Page et al. (2002))` alih-alih `(Page et al., 2002)`. Hal ini terjadi jika Pandoc dijalankan tanpa filter `--citeproc` dan berkas CSL APA 7th edition. |
| 7 | Citation Divergence (Numeric vs Author-Year) | `main.tex` vs `manuscript_draft.md` | `main.tex` menggunakan `\usepackage[square,numbers]{natbib}` (numerik), sedangkan draf naskah dan pedoman resmi *Applied Geography* menggunakan format author-year (APA 7th). Pengubahan ke `\usepackage[authoryear,round]{natbib}` dan `\bibliographystyle{elsarticle-harv}` atau `\bibliographystyle{apalike}` menyelesaikan divergensi ini. |
| 8 | Old Target Journal Header in Draft | `manuscript/manuscript_draft.md` baris 10 | Masih tertulis `Target Journal: *Remote Sensing of Environment* / *International Journal of Wildland Fire* / *MDPI Remote Sensing*`. Hal ini berpotensi membingungkan tim editorial jika tidak diperbarui. |

---

## Detailed Audit by Requirement

### 1. Research Highlights
- **Pedoman Elsevier Applied Geography:** Wajib 3 hingga 5 butir ringkasan (*bullet points*). Setiap butir **maksimal 85 karakter termasuk spasi**.
- **Hasil Pengukuran Berkas Saat Ini:**
  - Butir 1: `43,937 NASA FIRMS active fires analyzed across Central Kalimantan peatlands.`
    - Panjang: **76 karakter** (STATUS: LULUS)
  - Butir 2: `Coordinate models collapse under Spatial Block CV, proving spatial memorization.`
    - Panjang: **80 karakter** (STATUS: LULUS)
  - Butir 3: `Pure biophysical Random Forest retains 2.4-fold higher spatial CV F1-score.`
    - Panjang: **75 karakter** (STATUS: LULUS)
  - Butir 4: `75.4% of fires occurred on unallocated APL land, exposing a governance void.`
    - Panjang: **76 karakter** (STATUS: LULUS)
  - Butir 5: `TreeSHAP identifies key thresholds: 14-day dry spell and 3 km canal corridor.`
    - Panjang: **77 karakter** (STATUS: LULUS)
- **Simpulan:** Highlights memenuhi syarat 100%. Tidak ada pelanggaran batas karakter.

---

### 2. Abstract Word Count
- **Pedoman Elsevier Applied Geography:** Maksimal **250 kata**.
- **Hasil Pengukuran Berkas Saat Ini:**
  - `manuscript/sections/00_abstract.tex`: **363 kata** (Pelanggaran: +113 kata).
  - `manuscript/manuscript_draft.md`: **369 kata** (Pelanggaran: +119 kata).
  - `manuscript/submission_package/manuscript_main.docx`: **368 kata** (Pelanggaran: +118 kata).
- **Rekomendasi Solusi Teks Abstrak Ringkas (242 Kata):**
  ```markdown
  Tropical peatlands in Southeast Asia represent vital carbon repositories destabilized by drainage canals and recurrent wildfires. Operational fire hazard prediction remains hindered by spatial autocorrelation in machine learning models—causing spatial memorization and failure across unseen regions—and unresolved land tenure attribution. Here, we present a spatiotemporal study integrating 43,937 NASA FIRMS active fire hotspots (October 2026) across Central Kalimantan with official peat depth maps, projected canal networks (UTM Zone 49S), ECMWF ERA5-Land weather reanalysis, and cadastral overlays covering 627 palm oil (HGU) and 185 forestry (PBPH) concessions. Under 5-fold Spatial Block Cross-Validation (GroupKFold by regency), a coordinate-dependent Random Forest baseline (Model A) collapsed from a holdout ROC-AUC of 0.7956 to a spatial CV ROC-AUC of 0.5399, with F1-scores dropping to zero in four folds. In contrast, a Pure Biophysical Model trained without coordinates (Model B) retained generalizable performance (holdout ROC-AUC: 0.7527; severe fire recall: 65.8%; regular fire precision: 92.1%; spatial CV mean F1: 0.1399, 2.4-fold higher than Model A). TreeSHAP attribution identified critical thresholds governing severe fire radiative power: 7-day precipitation deficit (<5.0 mm), canal proximity (<3.0 km), consecutive dry spells (>14 days), and peat depth (>200 cm). Cadastral spatial overlays revealed that 75.4% of fires (33,138 hotspots) occurred on unallocated Non-Concession land (Area Penggunaan Lain / APL), while palm oil and forestry concessions accounted for 16.6% and 8.0%, respectively. These findings demonstrate that peatland fire governance must address unmanaged APL lands and provide operational thresholds for spatial early warning and canal-blocking interventions.
  ```
  *Verifikasi*: Teks di atas tepat **242 kata** (memenuhi batas <= 250 kata, mempertahankan seluruh angka kuantitatif, metrik ROC-AUC, F1, SHAP, dan persentase tenurial APL 75.4%).

---

### 3. Keywords Audit
- **Pedoman Elsevier Applied Geography:** Antara **1 hingga 7 kata kunci**.
- **Hasil Pengukuran Berkas Saat Ini:**
  - `00_abstract.tex`: 10 kata kunci (Melanggar batas: > 7).
  - `manuscript_draft.md`: 9 kata kunci (Melanggar batas: > 7).
  - `manuscript_main.docx`: 9 kata kunci (Melanggar batas: > 7).
  - `main.tex` hyperref: 7 kata kunci (tetapi belum memuat istilah sentral *Applied Geography*).
- **Rekomendasi 7 Kata Kunci Optimal untuk *Applied Geography*:**
  1. *Tropical peatlands*
  2. *Peatland wildfires*
  3. *Spatial autocorrelation*
  4. *Spatial block cross-validation*
  5. *Land tenure governance*
  6. *GIScience*
  7. *Central Kalimantan*

---

### 4. Reference & In-text Citation Style
- **Pedoman Elsevier Applied Geography:** Standar **APA 7th edition / author-year** format.
- **Hasil Pengukuran:**
  - `main.tex`: Menggunakan gaya sitasi numerik `unsrtnat` (`[1]`). Untuk kepatuhan menyeluruh terhadap APA author-year, paket natbib pada `main.tex` dapat diselaraskan menjadi:
    ```latex
    \usepackage[authoryear,round]{natbib}
    ...
    \bibliographystyle{elsarticle-harv} % atau apalike
    ```
    Karena seluruh kutipan di `manuscript/sections/*.tex` sudah menggunakan makro `\citep{...}`, penggantian opsi natbib ini akan langsung merender format `(Page et al., 2002)`.
  - `references.bib`: Memiliki 425 baris data referensi yang lengkap, valid, dan memuat DOI resmi untuk semua entri utama.
  - `manuscript_main.docx`: Menghasilkan tanda kurung ganda `(Page et al. (2002))` akibat parsing sitasi markdown dasar. Perlu diproses menggunakan `--citeproc` dan CSL APA.

---

### 5. Statements & Front Matter
- **CRediT Authorship Statement:**
  - Penulis 1: **Ahmad Sopian** (First & Corresponding Author, Independent Researcher, Samarinda, ahmadsopian22@gmail.com).
    - Peran: Conceptualization, Methodology, Software, Formal Analysis, Data Curation, Visualization, Writing - Original Draft, Project Administration.
  - Penulis 2: **Rahmi Susanti** (Co-Author, Faculty of Public Health, Universitas Mulawarman, Samarinda, rahmi.susanti@fkm.unmul.ac.id).
    - Peran: Conceptualization, Methodology, Validation, Investigation, Environmental Health and Haze Exposure Analysis, Writing - Review & Editing.
  - Berkas terpisah: `credit_statement.md` dan `credit_statement.docx` telah tersedia dan konsisten.
- **Declaration of Competing Interest:**
  - Kalimat standar Elsevier: *"The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper."*
  - Berkas terpisah: `declaration_of_interest.md` dan `declaration_of_interest.docx` tersedia, bertanggal 4 November 2026.
- **Data Availability Statement:**
  - Mencantumkan repositori terbuka GitHub: `https://github.com/amsopian22/karhutla-analisis`.
  - Mencantumkan sumber satelit NASA FIRMS, reanalisis ECMWF Copernicus, dan peta BBLSDLP/KLHK.
- **Cover Letter:**
  - Ditujukan resmi ke *Editor-in-Chief Applied Geography, Elsevier Science*.
  - Narasi menekankan mitigasi autokorelasi spasial (Hukum Pertama Tobler), validasi blok spasial, dan tata kelola lahan non-konsesi (APL 75,4%).

---

### 6. Verification Rules Mapping Matrix

| Acceptance Criteria ID | Parameter | Threshold / Specification | Current State | Actionable Verification Command | Status |
|---|---|---|---|---|---|
| AC-1 | Abstract Length | $\le 250$ words | 363 words (.tex) / 369 words (.md) | Python whitespace tokenization | **FAIL** (Action needed) |
| AC-2 | Highlights Count | $3 \le n \le 5$ bullets | 5 bullets | Python line / bullet count | **PASS** |
| AC-3 | Highlights Length | $\le 85$ characters/bullet | Max: 80 chars (B2) | Python string length check | **PASS** |
| AC-4 | Keywords Count | $1 \le n \le 7$ keywords | 10 (.tex) / 9 (.md) | Semicolon count | **FAIL** (Action needed) |
| AC-5 | CRediT Statement | Standard CRediT roles | Present for both authors | Text inspection | **PASS** |
| AC-6 | Data Availability | Direct URL to GitHub repo | `https://github.com/amsopian22/karhutla-analisis` | URL check in text | **PASS** |
| AC-7 | Competing Interest | Explicit declaration | Standard statement present | Text inspection | **PASS** |
| AC-8 | LaTeX Compilation | Exit code 0, no missing labels | Exit code 0, 0 missing labels | `tectonic main.tex` | **PASS** |
| AC-9 | Word Media Embedding | 7 figures in media folder | 7 figures present in docx media | Zip inspection of docx | **PASS** |
| AC-10 | Aims & Scope Text | Target journal listed | Listed old journals in draft baris 10 | Text inspection | **FAIL** (Action needed) |

---

## Action Plan for Refinement Phase

Berdasarkan temuan di atas, berikut adalah langkah konkret yang direkomendasikan untuk agen tahap perbaikan (*refiner*):
1. **Pembaruan Abstrak**: Ganti teks abstrak di `00_abstract.tex`, `manuscript_draft.md`, dan dokumen Word dengan draf terkalibrasi 242 kata.
2. **Pangkas Kata Kunci**: Tetapkan 7 kata kunci tematik geografi terapan di `00_abstract.tex`, `manuscript_draft.md`, `main.tex` hyperref, dan dokumen Word.
3. **Penyelarasan Target Jurnal**: Perbarui baris 10 `manuscript_draft.md` agar secara eksplisit menyebutkan *Applied Geography*.
4. **Opsi Gaya Sitasi LaTeX**: Sesuaikan natbib di `main.tex` ke format `[authoryear,round]` dengan style `elsarticle-harv` atau `apalike` jika tim menghendaki keselarasan penuh gaya APA di versi cetak LaTeX.
5. **Kompilasi Ulang Paket Submission**: Jalankan `tectonic main.tex` untuk menghasilkan `main.pdf` terbarui, serta konversi ulang Pandoc dengan CSL APA 7th untuk menghasilkan `manuscript_main.docx`, `highlights.docx`, dan `cover_letter.docx` yang rapi.
