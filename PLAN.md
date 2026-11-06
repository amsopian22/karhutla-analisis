# RENCANA EKSEKUSI PENGEMBANGAN DAN SUBMISSION (PLAN.md)
# Jurnal Target: Remote Sensing Applications: Society and Environment (RSASE, Elsevier)

Dokumen ini adalah rencana operasional terstruktur untuk mengeksekusi penyesuaian seluruh komponen naskah, kode analisis, paket pengajuan (*submission package*), dan unit tes pengujian ke jurnal **Remote Sensing Applications: Society and Environment (RSASE)** melalui portal resmi [Editorial Manager RSASE](https://www.editorialmanager.com/rsase/default.aspx).

---

## 1. Profil Bibliometrik & Parameter Jurnal Target

| Parameter | Spesifikasi Resmi | Catatan & Implikasi Proyek |
|:---|:---|:---|
| **Nama Jurnal** | *Remote Sensing Applications: Society and Environment* (RSASE) | Diterbitkan oleh Elsevier B.V. (ISSN: 2352-9385) |
| **Portal Pengajuan** | `https://www.editorialmanager.com/rsase/default.aspx` | Menggunakan sistem Elsevier Editorial Manager (`rsase`) |
| **Indeksasi Scopus** | **Scopus Q1** | Bidang: *Geography, Planning and Development* & *Earth Sciences* |
| **Scopus CiteScore** | **7.9** | Menunjukkan reputasi sitasi tinggi dan pengaruh keilmuan kuat |
| **Clarivate Impact Factor** | **4.5 – 4.9** (5-Year IF: ~5.2) | Terindeks di Web of Science Core Collection (ESCI/JCR) |
| **Model Publikasi** | **Hybrid Journal ($0 USD APC via Subscription)** | Penulis memilih rute **Subscription (Bebas Biaya Publikasi)** |
| **Format Review** | Single-Blind (default) & Double-Blind didukung | Naskah disediakan dalam **dua format**: Anonim & Lengkap |
| **Batas Panjang Abstrak** | 150 – 250 kata | Abstrak terkalibrasi saat ini: **246 kata** (Patuh) |
| **Aturan Highlights** | 3–5 butir, maksimal 85 karakter per butir (termasuk spasi) | 5 butir terkalibrasi (seluruhnya $\le 77$ karakter) |
| **Jumlah Kata Kunci** | 4 – 7 kata kunci spesifik | Disesuaikan ke 7 kata kunci penginderaan jauh terapan |

---

## 2. Rincian Langkah Eksekusi (Step-by-Step Execution Plan)

### Tahap 1: Pemutakhiran Cover Letter dan Title Page
- [ ] **1.1. Pemutakhiran `manuscript/cover_letter.md`**:
  - Tujukan ke: *The Editor-in-Chief, Remote Sensing Applications: Society and Environment (RSASE), Elsevier*.
  - Perkuat penekanan pada sintesis **Penginderaan Jauh (Remote Sensing)** $\times$ **Lingkungan Gambut (Environment)** $\times$ **Tata Kelola / Kebijakan (Society)**.
  - Tegaskan 5 temuan kunci: (1) Void tata kelola APL 75,4%; (2) Spatial BDD lonjakan kerapatan +56,5%; (3) Evaluasi memorisasi spasial koordinat vs retensi model biofisik murni; (4) Ambang batas TreeSHAP kanal 3 km dan dry spell 14 hari; (5) Kebijakan penyangga perbatasan 3 km dan restorasi hidrologis.
  - Konfirmasi deklarasi etik, orisinalitas, rute publikasi Subscription ($0 APC), dan repositori data publik.
- [ ] **1.2. Pemutakhiran `manuscript/title_page.md`**:
  - Perbarui metadata `Target Journal: Remote Sensing Applications: Society and Environment (Elsevier)`.
  - Pastikan rincian afiliasi lengkap: Ahmad Sopian (Independent Researcher) & Rahmi Susanti (Universitas Mulawarman).

### Tahap 2: Optimalisasi Kata Kunci dan Metadata LaTeX
- [ ] **2.1. Penyesuaian Kata Kunci pada `manuscript/sections/00_abstract.tex`**:
  - Harmonisasi 7 kata kunci spesifik RSASE:  
    `Remote sensing applications; Satellite active fires; Tropical peatlands; Spatial boundary discontinuity; Spatial block cross-validation; Land tenure governance; Fire Radiative Power.`
- [ ] **2.2. Pemutakhiran Metadata Dokumen di `manuscript/main.tex`**:
  - Perbarui tag `pdfsubject` dan `pdfkeywords` pada paket `hyperref` agar selaras dengan RSASE.

### Tahap 3: Sinkronisasi Naskah Markdown
- [ ] **3.1. Pemutakhiran `manuscript/manuscript_draft.md`**:
  - Ganti header target jurnal ke RSASE dan sinkronkan kata kunci baru.
- [ ] **3.2. Pemutakhiran `manuscript/manuscript_without_author_details.md`**:
  - Pastikan teks naskah anonim untuk double-blind review 100% identik dengan naskah utama tanpa detail identitas.

### Tahap 4: Rekompilasi Dokumen Paket Pengajuan (*Submission Package*)
- [ ] **4.1. Kompilasi Ulang Dokumen Word (.docx) via Pandoc**:
  - `manuscript_main.docx` (Naskah lengkap dengan sitasi CSL/BibTeX dan gambar 300 DPI).
  - `manuscript_without_author_details.docx` (Naskah anonim).
  - `title_page.docx` (Halaman judul dan detail penulis).
  - `cover_letter.docx` & `cover_letter.pdf` (Surat pengantar naskah).
  - `highlights.docx` (Research highlights).
  - `credit_statement.docx` & `declaration_of_interest.docx`.
- [ ] **4.2. Kompilasi Ulang Naskah PDF via Tectonic**:
  - Kompilasi `manuscript/main.tex` $\rightarrow$ `manuscript/main.pdf` (32 halaman, tipografi Palatino, bebas error badness kritis).

### Tahap 5: Penyesuaian Unit Tes Harness (*Test Suite*)
- [ ] **5.1. Pemutakhiran `tests/test_keywords_alignment.py`**:
  - Sesuaikan daftar kata kunci ekspektasi dengan 7 kata kunci baru RSASE.
- [ ] **5.2. Pemutakhiran `tests/test_challenger_adversarial_suite.py`**:
  - Perbarui string target jurnal yang diaudit.
- [ ] **5.3. Eksekusi Pengujian Penuh**:
  - Jalankan `/opt/anaconda3/envs/karhutla_env/bin/pytest tests/ -v` dan pastikan seluruh 41 pengujian berstatus **PASSED (100%)**.

### Tahap 6: Version Control & Handover
- [ ] **6.1. Git Commit & Push**:
  - Commit seluruh berkas yang dimutakhirkan dengan pesan terstruktur.
  - Push ke cabang `main` di GitHub ([amsopian22/karhutla-analisis](https://github.com/amsopian22/karhutla-analisis)).
- [ ] **6.2. Verifikasi Kesiapan Portal Editorial Manager**:
  - Berikan panduan navigasi langkah demi langkah untuk pengunggahan berkas di [Editorial Manager RSASE](https://www.editorialmanager.com/rsase/default.aspx).

---

## 3. Matriks Integritas Data & Angka Terverifikasi (Verifikasi Wajib)

Setiap modifikasi naskah dan dokumen wajib menjaga konsistensi angka absolut berikut:

| Parameter Metrik | Nilai Eksak Terverifikasi | Sumber Data & Skrip |
|:---|:---|:---|
| **Total Observasi Titik Api** | **43.937 titik** (NASA FIRMS 5–12 Okt 2026) | `data/processed/karhutla_kalteng_2019_2026.csv` |
| **Titik Api Non-Konsesi (APL)** | **33.138 titik (75,42%)** | `src/spatial_join_concessions.py` |
| **Titik Api Konsesi Sawit (HGU)** | **7.276 titik (16,56%)** | `src/spatial_join_concessions.py` |
| **Titik Api Kehutanan (PBPH)** | **3.523 titik (8,02%)** | `src/spatial_join_concessions.py` |
| **Target Kebakaran Ekstrem (FRP $\ge$ 12 MW)** | **6.648 titik (15,13%)** | `src/process_real_data.py` |
| **Titik di Ekosistem Lahan Gambut** | **32.643 titik (74,30%)** | Peta BBLSDLP 2019 / `src/process_real_data.py` |
| **Kerapatan Interior Konsesi ($-3$ s.d. $0\text{ km}$)** | **0,1830 titik/km²** (8.961 titik / 48.959,58 km²) | `output/reports/spatial_bdd_summary.json` |
| **Kerapatan Exterior Frontier APL ($0$ s.d. $+3\text{ km}$)** | **0,2864 titik/km²** (9.224 titik / 32.203,09 km²) | `output/reports/spatial_bdd_summary.json` |
| **Diskontinuitas Step Jump ($\tau_{\text{BDD}}$)** | **+0,1034 titik/km² (+56,5% lonjakan, rasio 1,565)** | `src/spatial_boundary_discontinuity.py` |
| **Paritas Energi Termal (FRP Parity)** | **$p = 0,278$** (Mann-Whitney U, tidak berbeda signifikan) | `src/spatial_boundary_discontinuity.py` |
| **Placebo Boundary Test ($-1\text{ km}$)** | **Rasio 1,084** (tidak ada lonjakan semu di interior) | `output/reports/spatial_bdd_summary.json` |
| **Spatial CV ROC-AUC Model A** | **0,5399** ($F_1 = 0,0583$; 4 dari 5 blok bernilai 0,0000) | `output/reports/model_metrics.json` |
| **Spatial CV ROC-AUC Model B** | **0,4950** ($F_1 = 0,1399$; retensi 2,40x lipat di semua blok) | `output/reports/model_metrics.json` |
| **Holdout Test Model B** | ROC-AUC **0,7527**; Recall Ekstrem **65,82%**; Presisi Reguler **92,1%** | `output/reports/model_metrics.json` |
