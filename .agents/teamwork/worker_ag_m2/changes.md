# Ringkasan Perubahan: Milestone 2 (M2) Submission Package Compilation & Visual/Tabular Integrity

**Penyusun**: `worker_ag_m2` (teamwork_worker)  
**Tanggal**: 4 November 2026  
**Repositori**: `karhutla-analisis`  
**Target Jurnal**: *Applied Geography* (Elsevier, IF: 7.4, CiteScore: 8.3, Scopus Q1)  

---

## 1. Berkas yang Dikompilasi & Diperbarui

Berdasarkan *Exclusive File Write Ownership*, berkas berikut telah diregenerasi dan diverifikasi penuh:

1. `manuscript/submission_package/manuscript_main.docx` (11,95 MB / 11.950.782 bytes):
   - Dikompilasi ulang dari `manuscript/manuscript_draft.md` menggunakan `/opt/homebrew/bin/pandoc` dengan argumen `--citeproc --bibliography=manuscript/references.bib`.
   - Mengintegrasikan seluruh teks hasil pembaruan M1 (abstrak terkalibrasi $\le 250$ kata, penomoran urut Gambar 1–7 selaras dengan LaTeX, dan 4 tabel terformat rapi).
   - Seluruh sitasi ter-render secara naratif dan terurai ke dalam daftar pustaka tanpa artefak tanda kurung ganda atau kurung siku mentah.

2. `manuscript/submission_package/highlights.docx` (10,93 KB / 10.930 bytes):
   - Dikompilasi ulang dari `manuscript/highlights.md` menggunakan Pandoc.
   - Memuat tepat 5 butir peluru dengan panjang karakter per butir berkisar antara 72 hingga 79 karakter (batas maksimum pedoman: $\le 85$ karakter).

3. `manuscript/submission_package/cover_letter.docx` (13,97 KB / 13.974 bytes):
   - Dikompilasi ulang dari `manuscript/cover_letter.md` menggunakan Pandoc.
   - Memuat surat pengantar resmi ke Editor-in-Chief *Applied Geography* dengan penegasan kontribusi geografi spasial terapan, justifikasi mitigasi autokorelasi spasial, data tenurial APL, dan deklarasi etika.

4. `manuscript/main.pdf` (11,14 MB / 11.138.804 bytes):
   - Dikompilasi dari `manuscript/main.tex` menggunakan kompiler Rust-based `/opt/homebrew/bin/tectonic` dalam 0 error.
   - Menghasilkan dokumen cetak 28 halaman A4 dengan tipografi Palatino (`mathpazo`), gaya sitasi nama-tahun (*Author-Year*, Harvard format via `elsarticle-harv`), running headers ganda, dan 7 figur visual resolusi tinggi (300 DPI).

---

## 2. Audit Integritas Tabular, Visual, dan Matematis

### 2.1. Audit Tabel Word (`<w:tbl>`)
- Terdeteksi tepat **4 entitas tabel XML asli** (`<w:tbl>`):
  - **Tabel 1**: Distribusi spasial hotspot per kabupaten/kota (11 baris).
  - **Tabel 2**: Rekam jejak kebakaran dekadal SiPongi KLHK 2018–2026 (10 baris).
  - **Tabel 3**: Perbandingan performa komprehensif Model A vs Model B pada Holdout & Spatial Block CV (13 baris).
  - **Tabel 4**: Peringkat TreeSHAP dan ambang batas biofisik (13 baris).
- **Kebersihan Format**: 0 baris sisa raw markdown pipes (`| --- |`) dan 0 tabel ASCII art (`+---+`).

### 2.2. Audit Persamaan Matematika (OMML)
- Terdeteksi **132 elemen matematika OMML** (`<m:oMath>`) untuk notasi simbol variabel ($P_{\text{7d}}$, $F_1$, $\text{FRP}$, dll.).
- Terdeteksi **9 blok paragraf persamaan matematika penuh** (`<m:oMathPara>`) yang merepresentasikan Persamaan 1 hingga Persamaan 9 (jarak kanal Euclidean UTM 49S, indikator eks-PLG, FWI empiris, binerisasi FRP, pembobotan kelas, subset fitur $X_A$ & $X_B$, partisi spatial block, dan formulasi nilai Shapley).

### 2.3. Audit Aset Visual dan Dimensi Gambar (300 DPI)
- Kontainer `word/media/` memuat **7 berkas gambar PNG biner beresolusi penuh** tanpa kompresi destruktif.
- Hash kriptografis SHA-256 membuktikan kesetaraan identik 100% antara gambar di dalam DOCX dan gambar master di `output/figures/`:
  - `Figure 1`: `01_peta_wilayah_studi_spatial_cv.png` (4685 $\times$ 2594 px, 300.0 DPI, SHA-256 match)
  - `Figure 2`: `02_peta_densitas_hotspot_frp.png` (4593 $\times$ 3081 px, 300.0 DPI, SHA-256 match)
  - `Figure 3`: `03_analisis_citra_satelit_kanal.png` (4771 $\times$ 2957 px, 300.0 DPI, SHA-256 match)
  - `Figure 4`: `04_peta_tenurial_konsesi_esg.png` (4086 $\times$ 3081 px, 300.0 DPI, SHA-256 match)
  - `Figure 5`: `05_tren_temporal_dan_harian.png` (4794 $\times$ 1831 px, 300.0 DPI, SHA-256 match)
  - `Figure 6`: `06_evaluasi_model_ml.png` (4200 $\times$ 1650 px, 300.0 DPI, SHA-256 match)
  - `Figure 7`: `07_shap_feature_importance.png` (3170 $\times$ 1861 px, 300.0 DPI, SHA-256 match)
- Penomoran dan caption teks pada paragraf terurut sempurna dari `Figure 1.` hingga `Figure 7.` tanpa ada figur yang hilang atau tertukar.

### 2.4. Audit Batasan Kata Abstrak Programatik
- Panjang abstrak pada `manuscript_main.docx`: **228 kata** (memenuhi batas $\le 250$ kata).
- Panjang abstrak pada `main.pdf`: **235 kata** (memenuhi batas $\le 250$ kata).
