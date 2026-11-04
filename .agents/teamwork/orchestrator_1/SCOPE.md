# Scope: Audit & Penyelarasan Manuskrip untuk Elsevier *Applied Geography*

## Architecture
- **Target Jurnal**: *Applied Geography* (Elsevier, IF: 7.4, CiteScore: 8.3, Scopus Q1)
- **Konteks Submisi**: Penyelarasan menyeluruh dari naskah awal pasca *desk rejection* *Ecological Modelling* menjadi naskah berfokus geografi spasial terapan murni (GIScience, Hukum Pertama Tobler, mitigasi autokorelasi spasial melalui Spatial Block CV, dan tata kelola tenurial APL vs konsesi).
- **Authorship**:
  - Ahmad Sopian (First & Corresponding Author, Independent Researcher, Samarinda, Kalimantan Timur, Indonesia, ahmadsopian22@gmail.com)
  - Rahmi Susanti (Co-Author, Faculty of Public Health, Universitas Mulawarman, Samarinda, Kalimantan Timur, Indonesia, rahmi.susanti@fkm.unmul.ac.id)
- **Komponen Paket Submisi**:
  1. Main Manuscript LaTeX & PDF: `manuscript/main.tex`, `manuscript/sections/*.tex`, `manuscript/references.bib` -> `manuscript/main.pdf` (Tectonic compiler, 28 halaman, author-year Harvard).
  2. Main Manuscript Word DOCX: `manuscript/submission_package/manuscript_main.docx` (Pandoc `--citeproc`, 4 tabel native OpenXML `<w:tbl>`, 132 formula matematika OMML `<m:oMath>`, 7 figur 300 DPI tersemat).
  3. Manuscript Markdown Source: `manuscript/manuscript_draft.md` (100% tersinkronisasi).
  4. Highlights: `manuscript/highlights.md` & `manuscript/submission_package/highlights.docx` (5 butir, 72–79 karakter, <= 85 karakter).
  5. Cover Letter: `manuscript/cover_letter.md` & `manuscript/submission_package/cover_letter.docx` (resmi ditujukan ke Editor-in-Chief Applied Geography).
  6. Declarations & CRediT: `manuscript/credit_statement.md`, `declaration_of_interest.md`.
  7. Visual & Tabular Assets: 8 figur ilmiah 300 DPI di `output/figures/` dan `manuscript/submission_package/figures/`.
  8. Automated Verification Suite: 37 pengujian pytest otomatis di `tests/` (100% lulus).

## Feature Inventory
| # | Feature | Description | Milestone | Source | Status |
|---|---------|-------------|-----------|--------|:------:|
| 1 | Pemadatan Abstrak <= 250 Kata | Memadatkan teks abstrak dari 363-369 kata menjadi <= 250 kata (234 kata whitespace, 247 kata regex `\b\w+\b`) pada LaTeX, MD, DOCX, dan PDF dengan mempertahankan 100% metrik kuantitatif | M1 | ORIGINAL_REQUEST R2 | DONE |
| 2 | Penyelarasan Kata Kunci (1-7 Keywords) | Menetapkan tepat 7 kata kunci geografi terapan pada LaTeX, MD, dan DOCX | M1 | ORIGINAL_REQUEST R2 | DONE |
| 3 | Reframing Narasi Applied Geography | Penguatan narasi Hukum Tobler, Spatial Block CV, tata kelola tenurial APL (75,4%), koridor kanal 3 km di Pendahuluan, Metode, Hasil, Pembahasan, Kesimpulan, dan Cover Letter | M1 | ORIGINAL_REQUEST R4 | DONE |
| 4 | Sinkronisasi & Perbaikan Inkonsistensi Draf | Pembaruan header target jurnal, perbaikan angka titik api ekstrem ($n=6.648$), perbaikan penomoran gambar (Figure 1-7) dan panggilan teks (callouts) di `manuscript_draft.md` | M1 | Survey E2/E3 | DONE |
| 5 | Penyelarasan Gaya Sitasi LaTeX (Author-Year) | Mengubah konfigurasi natbib di `main.tex` dari numerik `unsrtnat` menjadi author-year (`authoryear`, `elsarticle-harv`) | M1 | Survey E1/E3 | DONE |
| 6 | Kompilasi Ulang LaTeX PDF Bebas Galat | Kompilasi `main.tex` via Tectonic menjadi `main.pdf` 28 halaman tanpa kesalahan dan resolusi tautan silang 100% | M2 | ORIGINAL_REQUEST R5 | DONE |
| 7 | Regenerasi Dokumen Word DOCX | Regenerasi `manuscript_main.docx`, `highlights.docx`, dan `cover_letter.docx` via Pandoc dengan perenderan 4 tabel XML, formula OMML, dan gambar 300 DPI | M2 | ORIGINAL_REQUEST R3/R5 | DONE |
| 8 | Skrip Verifikasi Programatik Otomatis | Pembuatan 5 skrip pengujian berbasis Python di `tests/` (37 test case) memvalidasi abstrak, highlights, kata kunci, referensi/gambar, dan kompilasi | M3 | ORIGINAL_REQUEST Verification Resources | DONE |
| 9 | Pengujian Adversarial & Review Independen | Evaluasi ketat oleh 2 Reviewer (APPROVE/APPROVE) dan 2 Challenger (APPROVE/APPROVE) | M3 | Acceptance Criteria | DONE |
| 10 | Audit Forensik Integritas Manuskrip | Audit forensik oleh `teamwork_auditor` membuktikan 100% keaslian metrik, ketiadaan mock, ketiadaan plagiasi (Vonis CLEAN) | M3 | Acceptance Criteria | DONE |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|:------:|
| M1 | Text Refactoring & Scope Alignment | Pembaruan teks abstrak, pemangkasan kata kunci, reframing Applied Geography, sinkronisasi `manuscript_draft.md`, gaya sitasi `main.tex`, pembaruan cover letter | none | DONE |
| M2 | Submission Package Compilation & Rendering | Kompilasi PDF via Tectonic, regenerasi Word DOCX via Pandoc, validasi rendering tabel dan figur 300 DPI | M1 | DONE |
| M3 | Programmatic Verification & Final Gate Audit | Implementasi 5 skrip uji di `tests/`, review sejawat (2 Reviewer), stress test (2 Challenger), audit forensik (1 Auditor), dan penyerahan paket | M2 | DONE |
