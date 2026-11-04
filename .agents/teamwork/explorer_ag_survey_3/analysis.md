# Laporan Analisis Komprehensif: Integritas Kompilasi Dokumen, Rendering Multi-Format, dan Infrastruktur Verifikasi Programatik

**Penyusun**: Agent `explorer_ag_survey_3` (teamwork_explorer)  
**Tanggal**: 4 November 2026  
**Repositori**: `karhutla-analisis`  
**Target Jurnal**: *Applied Geography* (Elsevier, IF: 7.4, CiteScore: 8.3, Scopus Q1)  
**Lingkungan Eksekusi**: Conda `karhutla_env` (Python 3.10) & Toolchain macOS  

---

## 1. Ringkasan Eksekutif (Executive Summary)

Investigasi mendalam terhadap seluruh pipeline kompilasi naskah (*LaTeX/PDF*, *Markdown*, dan *Word DOCX*), aset visual-tabular, serta infrastruktur pengujian programmatic telah diselesaikan dengan temuan inti sebagai berikut:
1. **Toolchain Kompilasi LaTeX/PDF Berfungsi Sempurna melalui Tectonic**: Kompiler Rust-based `/opt/homebrew/bin/tectonic` (v0.16.9) terpasang di sistem dan mampu mengompilasi `manuscript/main.tex` menjadi `manuscript/main.pdf` (26 halaman, 11,1 MB) secara mandiri (termasuk resolusi BibTeX otomatis) dalam satu pass dengan 0 error. Sebaliknya, distribusi TeX Live di lingkungan conda `diskominfo` mengalami kegagalan *format file* (`mktexfmt: pdflatex.fmt not found`).
2. **Kompilasi Word (DOCX) Berbasis Pandoc**: Dokumen `manuscript_main.docx` (11,9 MB) dihasilkan dari `manuscript/manuscript_draft.md` menggunakan `/opt/homebrew/bin/pandoc` (v3.8.3) dengan filter `--citeproc` dan `--bibliography=references.bib`. Dokumen ini menyematkan 7 gambar beresolusi tinggi (300 DPI) dan 4 tabel terformat XML secara rapi tanpa artefak ASCII.
3. **Disparitas Kritis Antara Naskah Markdown/DOCX vs LaTeX/PDF**:
   - **Ketidaksesuaian Urutan & Penomoran Gambar**: Pada `manuscript_draft.md` dan `manuscript_main.docx`, gambar temporal (`05_tren_temporal_dan_harian.png`) ditarik ke Sub-bab 3.1 sebagai Figure 2, sehingga mengacaukan seluruh penomoran figur berikutnya.
   - **Panggilan Teks Rusak (*Broken In-Text Callouts*)**: Pada `manuscript_draft.md`, teks menyebutkan *"Table 3 and Figure 4"* untuk evaluasi model (seharusnya Figure 6), *"Table 4 and Figure 5"* untuk SHAP (seharusnya Figure 7), dan *"Figure 5"* untuk beeswarm TreeSHAP. Selain itu, Figure 4 (peta tenurial) dan Figure 5 (forensik kanal) sama sekali tidak memiliki kalimat pemanggil aktif di dalam narasi teks. Sebaliknya, naskah LaTeX `03_results.tex` memiliki keterhubungan 100% konsisten antara `\ref` dan `\label` untuk Figures 1–7.
   - **Target Jurnal Usang pada Draft**: `manuscript_draft.md` baris 10 masih mencantumkan *Remote Sensing of Environment / International Journal of Wildland Fire / MDPI Remote Sensing*, belum diperbarui ke *Applied Geography*.
4. **Pelanggaran Pedoman Penulis Elsevier (*Applied Geography Guide for Authors*)**:
   - **Panjang Abstrak Melebihi Batas**: Abstrak saat ini memiliki panjang **350 kata** pada semua format (`00_abstract.tex`, `manuscript_draft.md`, `manuscript_main.docx`), padahal batas ketat *Applied Geography* adalah **$\le$ 250 kata** (kelebihan 100 kata / 40%).
   - **Jumlah Kata Kunci (*Keywords*) Berlebih**: Terdapat **10 kata kunci** di LaTeX dan **9 kata kunci** di Markdown/DOCX, melebihi batas ketentuan Elsevier yaitu **1 hingga 7 kata kunci**.
   - **Gaya Sitasi Bibliografi**: LaTeX menggunakan `unsrtnat` (bernomor), padahal *Applied Geography* mewajibkan format sitasi nama-tahun (*Author-Year / Harvard style*).
5. **Kepatuhan Highlights**: Berkas `highlights.md` dan `highlights.docx` telah memenuhi syarat 100%: 5 butir peluru (*bullets*), masing-masing berkarakter antara 75 hingga 80 karakter (batas maks: 85 karakter dengan spasi).

---

## 2. Investigasi Kompilasi LaTeX & Rendering PDF

### 2.1. Arsitektur Berkas LaTeX
Naskah LaTeX berpusat pada `manuscript/main.tex` yang dirancang secara modular dan memanggil bagian-bagian terpisah di `manuscript/sections/`:
- `sections/00_abstract.tex` (2.904 bytes): Abstrak dan kata kunci.
- `sections/01_introduction.tex` (5.762 bytes): Latar belakang, Hukum Pertama Tobler, paradoks tenurial.
- `sections/02_materials_methods.tex` (20.503 bytes): Wilayah studi, pipeline data, formulasi model Machine Learning, Spatial Block CV (GroupKFold), dan TreeSHAP.
- `sections/03_results.tex` (23.538 bytes): 6 sub-bab hasil, 4 tabel `booktabs`, dan penyisipan 6 figur ilmiah.
- `sections/04_discussion.tex` (12.455 bytes): Sintesis geografi terapan, jebakan memorisasi spasial, implikasi tenurial APL, dan Sub-bab 4.4 limitasi studi.
- `sections/05_conclusions.tex` (3.829 bytes): Rekomendasi mitigasi kebijakan, ambang batas intervensi (14 hari kemarau, 3 km kanal).
- `references.bib` (16.979 bytes): 40 entri sitasi bereputasi tinggi Q1/Nature/PNAS.

### 2.2. Paket dan Tipografi yang Digunakan
- **Kelas Dokumen**: `\documentclass[11pt,a4paper]{article}` dengan geometri margin 1 inci (`geometry`).
- **Font & Tipografi**: `mathpazo` (Palatino typeface), `amsmath`, `amssymb`, `microtype` (optical margin kerning), `setspace` (`\setstretch{1.14}`).
- **Pengaturan Judul & Tata Letak**: `titlesec` (hierarki seksi navyblue `#102C57` dan slate `#1E293B`), `fancyhdr` (running headers penulis dan topik), `enumitem`.
- **Tabel & Gambar**: `graphicx` (`\graphicspath{{../output/figures/}{output/figures/}}`), `booktabs`, `array`, `tabularx`, `caption`, `subcaption`.
- **Bibliografi & Hyperlink**: `natbib` (`[square,numbers,sort&compress]`), `url`, `xurl`, `hyperref` (skema warna `citeblue` `#0F4C81`).

### 2.3. Evaluasi Toolchain Kompiler pada Sistem
Pengujian eksekusi kompiler menghasilkan temuan penting:
1. **`/opt/homebrew/bin/tectonic` (Tectonic 0.16.9)**:
   - **Status**: Sangat direkomendasikan & berfungsi sempurna.
   - **Hasil Uji**: Mengeksekusi `main.tex` menghasilkan PDF sebesar 10.609.130 bytes (~10,6 MB) dalam 12 detik tanpa peringatan eror. Tectonic secara otomatis mengelola siklus TeX $\rightarrow$ BibTeX $\rightarrow$ TeX $\rightarrow$ xdvipdfmx secara terisolasi tanpa mencemari direktori dengan berkas tambahan (.aux, .bbl, .log).
2. **`/opt/anaconda3/envs/diskominfo/bin/pdflatex` (TeX Live 2026)**:
   - **Status**: Tidak dapat dijalankan langsung karena hilangnya *fmt engine*.
   - **Pesan Eror**: `mktexfmt: No such file or directory; I can't find the format file 'pdflatex.fmt'!`.
3. **Pemeriksaan Berkas PDF Eksisting (`manuscript/main.pdf`)**:
   - Ukuran: 11.124.481 bytes (~11,1 MB).
   - Jumlah Halaman: 26 halaman A4.
   - Metadata Creator: `LaTeX with hyperref, mathpazo, and tectonic`.
   - Produser: `xdvipdfmx (0.1)`.
   - Rendering: Seluruh persamaan (Eq. 1–5), tabel (Tab. 1–4), dan grafik (Fig. 1–7) ter-render tajam dan terindeks rapi.

---

## 3. Investigasi Dokumen Word (DOCX) & Alur Pandoc

### 3.1. Mekanisme Pembangkitan Dokumen
Pemeriksaan jejak git dan eksperimen reverse-engineering membuktikan bahwa seluruh berkas `.docx` di `manuscript/submission_package/` dikompilasi secara otomatis menggunakan **Pandoc 3.8.3** dari berkas sumber Markdown:
```bash
# Manuscript Utama
/opt/homebrew/bin/pandoc manuscript/manuscript_draft.md \
    -o manuscript/submission_package/manuscript_main.docx \
    --citeproc --bibliography=manuscript/references.bib

# Dokumen Pelengkap
/opt/homebrew/bin/pandoc manuscript/highlights.md \
    -o manuscript/submission_package/highlights.docx
/opt/homebrew/bin/pandoc manuscript/cover_letter.md \
    -o manuscript/submission_package/cover_letter.docx
/opt/homebrew/bin/pandoc manuscript/credit_statement.md \
    -o manuscript/submission_package/credit_statement.docx
/opt/homebrew/bin/pandoc manuscript/declaration_of_interest.md \
    -o manuscript/submission_package/declaration_of_interest.docx
```
Ukuran biner berkas yang dihasilkan melalui perintah pandoc di atas identik 100% hingga tingkat byte dengan berkas yang ada di repositori (`11.941.224 bytes` untuk `manuscript_main.docx`, `13.974 bytes` untuk `cover_letter.docx`, `10.930 bytes` untuk `highlights.docx`).

### 3.2. Integritas Struktur Internal DOCX (`manuscript_main.docx`)
Audit menggunakan inspeksi XML internal ZIP (`word/document.xml` dan `word/media/`):
- **Aset Gambar Tersemat**: Terdapat 7 berkas gambar biner PNG di dalam kontainer DOCX:
  1. `word/media/rId11.png` (1.435.188 bytes) $\rightarrow$ `01_peta_wilayah_studi_spatial_cv.png`
  2. `word/media/rId27.png` (400.955 bytes) $\rightarrow$ `05_tren_temporal_dan_harian.png`
  3. `word/media/rId31.png` (2.014.379 bytes) $\rightarrow$ `02_peta_densitas_hotspot_frp.png`
  4. `word/media/rId34.png` (2.830.381 bytes) $\rightarrow$ `04_peta_tenurial_konsesi_esg.png`
  5. `word/media/rId38.png` (4.654.798 bytes) $\rightarrow$ `03_analisis_citra_satelit_kanal.png`
  6. `word/media/rId42.png` (337.108 bytes) $\rightarrow$ `06_evaluasi_model_ml.png`
  7. `word/media/rId46.png` (527.272 bytes) $\rightarrow$ `07_shap_feature_importance.png`
  Semua gambar mempertahankan resolusi asli **300 DPI** tanpa kompresi destruktif.
- **Tabel Tersemat**: Terdeteksi 4 entitas `<w:tbl>` yang ter-render sebagai tabel Word asli yang rapi dengan garis sel, sel tebal untuk kepala tabel, dan perataan angka kanan:
  1. Tabel 1: Rekam jejak kebakaran dekadal SiPongi (2018–2026).
  2. Tabel 2: Distribusi spasial hotspot per kabupaten/kota.
  3. Tabel 3: Perbandingan metrik Model A vs Model B (Holdout & Spatial CV).
  4. Tabel 4: Peringkat fitur TreeSHAP.
- **Kebersihan Markup**: Tidak ditemukan artefak markdown mentah yang tidak ter-parse (`**`, `###`, pipe table mentah `|---|`, atau kotak ASCII art). Sitasi bibliografi terurai dengan baik menjadi format teks naratif (misalnya: *"Page et al. (2002); Dommain et al. (2011)"*).

---

## 4. Audit Aset Visual dan Tabular (Cross-Format Consistency)

### 4.1. Resolusi dan Dimensi Gambar (Pillow Inspection)
Pemeriksaan metadata biner seluruh gambar di `manuscript/submission_package/figures/` dan `output/figures/` mengonfirmasi pemenuhan standar 300 DPI untuk publikasi:

| Nama Berkas Aset | Dimensi Piksel | Resolusi (DPI) | Ukuran Berkas | Kesesuaian Jurnal |
| :--- | :---: | :---: | :---: | :---: |
| `01_peta_wilayah_studi_spatial_cv.png` | 4685 $\times$ 2594 | 300.0 DPI | 1,44 MB | Lulus (Sangat Tajam) |
| `02_peta_densitas_hotspot_frp.png` | 4593 $\times$ 3081 | 300.0 DPI | 2,01 MB | Lulus (Sangat Tajam) |
| `03_analisis_citra_satelit_kanal.png` | 4771 $\times$ 2957 | 300.0 DPI | 4,65 MB | Lulus (Ultra-Detail) |
| `04_peta_tenurial_konsesi_esg.png` | 4086 $\times$ 3081 | 300.0 DPI | 2,83 MB | Lulus (Sangat Tajam) |
| `05_tren_temporal_dan_harian.png` | 4794 $\times$ 1831 | 300.0 DPI | 401 KB | Lulus (Sangat Tajam) |
| `06_evaluasi_model_ml.png` | 4200 $\times$ 1650 | 300.0 DPI | 337 KB | Lulus (Sangat Tajam) |
| `07_shap_feature_importance.png` | 3170 $\times$ 1861 | 300.0 DPI | 527 KB | Lulus (Sangat Tajam) |
| `08_transboundary_haze_dispersion.png` | 3900 $\times$ 2400 | 300.0 DPI | 729 KB | Lulus (Sangat Tajam) |

### 4.2. Matriks Kesetaraan SHA-256 (Hash Matching)
Uji hash kriptografis membuktikan bahwa gambar di `manuscript/submission_package/figures/Figure_0X.png` identik 1:1 dengan gambar ilmiah di `output/figures/`:
- `Figure_01.png` $\equiv$ `01_peta_wilayah_studi_spatial_cv.png` (`28a34683be64...`)
- `Figure_02.png` $\equiv$ `02_peta_densitas_hotspot_frp.png` (`969f6b67ede6...`)
- `Figure_03.png` $\equiv$ `03_analisis_citra_satelit_kanal.png` (`668950b2fc25...`)
- `Figure_04.png` $\equiv$ `04_peta_tenurial_konsesi_esg.png` (`8d780ca086c8...`)
- `Figure_05.png` $\equiv$ `05_tren_temporal_dan_harian.png` (`182ed0d1f00e...`)
- `Figure_06.png` $\equiv$ `06_evaluasi_model_ml.png` (`5daadde62868...`)
- `Figure_07.png` $\equiv$ `07_shap_feature_importance.png` (`fd8304642e60...`)
- `Figure_08.png` $\equiv$ `08_transboundary_haze_dispersion.png` (`752a6f9e2ef7...`)

### 4.3. Anomali Ketidakselarasan Penomoran Figur & Tabel
Ditemukan inkonsistensi struktural antara alur LaTeX (`03_results.tex`) dan alur Markdown (`manuscript_draft.md`):

```
+---------------+-------------------------------------+-------------------------------------+
| Entitas       | Urutan pada LaTeX (03_results.tex)  | Urutan pada Markdown (draft.md)     |
+---------------+-------------------------------------+-------------------------------------+
| Figure 1      | 01_peta_wilayah_studi_spatial_cv    | 01_peta_wilayah_studi_spatial_cv    |
| Figure 2      | 02_peta_densitas_hotspot_frp        | 05_tren_temporal_dan_harian [MIS]   |
| Figure 3      | 03_analisis_citra_satelit_kanal     | 02_peta_densitas_hotspot_frp [MIS]  |
| Figure 4      | 04_peta_tenurial_konsesi_esg        | 04_peta_tenurial_konsesi_esg        |
| Figure 5      | 05_tren_temporal_dan_harian         | 03_analisis_citra_satelit_kanal [MIS|
| Figure 6      | 06_evaluasi_model_ml                | 06_evaluasi_model_ml                |
| Figure 7      | 07_shap_feature_importance          | 07_shap_feature_importance          |
| In-Text Call  | 100% Sesuai label fig:*             | RUSAK:                              |
|               |                                     | - Model eval dipanggil "Figure 4"   |
|               |                                     | - SHAP ranking dipanggil "Figure 5" |
|               |                                     | - TreeSHAP dipanggil "Figure 5"     |
|               |                                     | - Fig 4 & Fig 5 asli tanpa callout  |
+---------------+-------------------------------------+-------------------------------------+
```
**Rekomendasi Penyelarasan**: Urutan naskah Markdown `manuscript_draft.md` harus diselaraskan secara penuh mengikuti urutan modular LaTeX (`03_results.tex`) dan penamaan berkas `Figure_01` hingga `Figure_07` di paket submisi.

---

## 5. Audit Kepatuhan Pedoman Penulis *Applied Geography* (Elsevier)

| Parameter Pedoman | Ketentuan Jurnal | Status Saat Ini (LaTeX / Word) | Evaluasi Kepatuhan | Tindakan Remediasi |
| :--- | :--- | :--- | :--- | :--- |
| **Panjang Abstrak** | Maksimal 250 kata | **350 kata** (`00_abstract.tex`)<br>**350 kata** (`draft.md` / `.docx`) | ❌ **GAGAL** (Kelebihan 100 kata) | Ringkas abstrak menjadi $\le 245$ kata tanpa menghilangkan metrik kunci (43.937 hotspot, ROC-AUC 0.7527 vs 0.5399, APL 75,4%). |
| **Jumlah Highlights** | 3 s.d. 5 butir peluru | **5 butir peluru** (`highlights.md`) | ✅ **LULUS** | Pertahankan 5 butir peluru. |
| **Panjang Highlights** | Maksimal 85 karakter per butir (termasuk spasi) | Butir 1: 76 karakter<br>Butir 2: 80 karakter<br>Butir 3: 75 karakter<br>Butir 4: 76 karakter<br>Butir 5: 77 karakter | ✅ **LULUS SEMPURNA** | Semua $\le 85$ karakter. Tidak perlu perubahan. |
| **Jumlah Kata Kunci** | 1 s.d. 7 kata kunci | **10 kata kunci** (LaTeX)<br>**9 kata kunci** (Markdown) | ❌ **GAGAL** (Kelebihan 3 kata kunci) | Pilih 6–7 kata kunci paling representatif untuk *Applied Geography*. |
| **Format Sitasi Teks** | Format Nama-Tahun (*Author-Year*) | LaTeX: `[1]`, `[2]` (`unsrtnat`)<br>Word: `Page et al. (2002)` | ⚠️ **PARSIAL** (LaTeX bernomor, Word sudah benar) | Ubah `main.tex` dari `\bibliographystyle{unsrtnat}` ke `authoryear` (`elsarticle-harv` atau `natbib authoryear`). |
| **Pernyataan Penulis** | CRediT authorship statement wajib | Ada di `credit_statement.md`, `main.tex`, dan DOCX | ✅ **LULUS** | Sesuai taksonomi CRediT standar Elsevier. |
| **Aksesibilitas Data** | Data Availability Statement wajib | Ada di `main.tex`, `draft.md`, dan DOCX | ✅ **LULUS** | Menautkan ke repo publik GitHub dan portal NASA FIRMS / CDS. |

---

## 6. Spesifikasi Teknis Skrip Pengujian Programatik Baru

Untuk memenuhi mandat `ORIGINAL_REQUEST.md` (bagian Verification Resources) secara objektif dan dapat diaudit secara berkelanjutan (*Continuous Integration*), dirancang 5 skrip verifikasi Python baru di direktori `tests/`:

### 6.1. Skrip 1: `tests/test_abstract_word_count.py`
- **Tujuan**: Memverifikasi secara independen bahwa panjang abstrak pada berkas LaTeX (`sections/00_abstract.tex`), Markdown (`manuscript_draft.md`), dan Word DOCX (`manuscript_main.docx`) tidak melebihi 250 kata.
- **Logika Algoritma**:
  1. *Parser LaTeX*: Mengekstrak teks di antara `\begin{abstract}` dan `\end{abstract}` (atau sebelum `\textbf{Keywords:}`), menghapus tag LaTeX (`\noindent`, `\textit{...}`, `\textbf{...}`, rumus math `$F_1$`, dll.), lalu menghitung token berbasis spasi (`split()`).
  2. *Parser Markdown*: Mengekstrak paragraf di bawah `## Abstract` hingga `**Keywords:**`, menghapus tautan dan markup penekanan, lalu menghitung token kata.
  3. *Parser Word DOCX*: Membaca kontainer `word/document.xml` menggunakan modul bawaan `zipfile` dan `xml.etree.ElementTree`, mengidentifikasi paragraf abstrak setelah heading "Abstract", lalu menghitung kata.
- **Kriteria Keberhasilan (*Exit Code*)**:
  - `exit 0`: Jika `word_count <= 250` pada ketiga berkas.
  - `exit 1`: Jika salah satu berkas memiliki `word_count > 250`, dengan menampilkan selisih kelebihan kata.

### 6.2. Skrip 2: `tests/test_highlights_length.py`
- **Tujuan**: Memverifikasi jumlah butir peluru (3–5 butir) dan panjang karakter maksimum per butir ($\le 85$ karakter dengan spasi) pada `manuscript/highlights.md` dan `manuscript/submission_package/highlights.docx`.
- **Logika Algoritma**:
  1. Mengekstrak baris yang diawali bullet point `*` atau `-` pada Markdown.
  2. Mengekstrak elemen paragraf berformat list/bullet pada berkas DOCX.
  3. Memvalidasi batasan: `3 <= len(bullets) <= 5`.
  4. Melakukan iterasi tiap butir peluru dan memeriksa `len(bullet_text) <= 85`.
- **Kriteria Keberhasilan**:
  - `exit 0`: 100% butir berada di rentang 3–5 dan tiap butir $\le 85$ karakter.
  - `exit 1`: Jumlah butir di luar rentang atau terdapat butir yang melebihi 85 karakter.

### 6.3. Skrip 3: `tests/test_keywords_alignment.py`
- **Tujuan**: Memverifikasi bahwa jumlah kata kunci berada dalam batas editorial (1–7 kata kunci) serta mengevaluasi keselarasan taksonomi dengan ruang lingkup *Applied Geography*.
- **Logika Algoritma**:
  1. Mem-parsing kata kunci yang dipisahkan oleh tanda titik koma (`;`) pada `00_abstract.tex`, `manuscript_draft.md`, dan `manuscript_main.docx`.
  2. Menghitung jumlah kata kunci unik: `assert 1 <= num_keywords <= 7`.
  3. Memeriksa keberadaan kata kunci tematik wajib Applied Geography (misalnya: *Spatial autocorrelation*, *Spatial block cross-validation*, *Land tenure governance*, *Tropical peatlands*, *Wildfire modeling*, *Mega Rice Project*).
- **Kriteria Keberhasilan**:
  - `exit 0`: Jumlah kata kunci 1–7 dan memuat terminologi spasial-geografis wajib.
  - `exit 1`: Jumlah kata kunci $> 7$ atau tidak memuat terminologi geografi terapan.

### 6.4. Skrip 4: `tests/test_reference_figure_callout_consistency.py`
- **Tujuan**: Menjamin tidak ada gambar atau tabel yang tidak terpanggil dalam teks (*uncalled assets*), tidak ada referensi silang yang rusak (*dangling references*), dan penomoran figur sinkron antara teks dan berkas fisik.
- **Logika Algoritma**:
  1. *Pemeriksaan LaTeX*:
     - Mengekstrak semua `\label{fig:...}` dan `\label{tab:...}`.
     - Mengekstrak semua `\ref{fig:...}` dan `\ref{tab:...}`.
     - Memverifikasi bahwa setiap label memiliki setidaknya 1 callout aktif di teks narasi.
     - Memverifikasi bahwa setiap `\includegraphics` merujuk ke berkas gambar fisik yang ada di disk.
  2. *Pemeriksaan Markdown & Word DOCX*:
     - Mengekstrak pola pemanggilan teks: `Figure X`, `Fig. X`, `Table Y`, `Tab. Y`.
     - Mengekstrak caption gambar `![**Figure X...**](...)` dan tabel markdown `**Table Y...**`.
     - Memverifikasi keselarasan indeks numerik (misal: jika ada caption Figure 4, harus ada pemanggilan "Figure 4" atau "Fig. 4" di paragraf terkait).
     - Memverifikasi bahwa tidak ada penyebutan figur yang salah (misal menyebut Figure 4 untuk Model Evaluation yang bernomor Figure 6).
- **Kriteria Keberhasilan**:
  - `exit 0`: 100% figur dan tabel terhubung dua arah tanpa referensi rusak atau tertukar.
  - `exit 1`: Ditemukan figur tanpa panggilan, nomor figur tertukar, atau referensi silang tak terselesaikan.

### 6.5. Skrip 5: `tests/test_document_compilation_rendering.py`
- **Tujuan**: Memvalidasi alur kompilasi ujung-ke-ujung (*end-to-end compilation*) dokumen LaTeX ke PDF dan Markdown ke DOCX secara otomatis, serta memeriksa integritas rendering visual.
- **Logika Algoritma**:
  1. Menjalankan kompilasi LaTeX:
     - Mengeksekusi `/opt/homebrew/bin/tectonic -o <temp_build> manuscript/main.tex`.
     - Memverifikasi `exit_code == 0`, berkas PDF tercipta, ukuran $> 5$ MB, dan halaman $> 20$.
  2. Menjalankan kompilasi Pandoc DOCX:
     - Mengeksekusi pandoc untuk `manuscript_draft.md` $\rightarrow$ `manuscript_main.docx` dengan flag `--citeproc`.
     - Memverifikasi `exit_code == 0` dan ukuran DOCX $> 10$ MB.
  3. Memeriksa Integritas Biner DOCX (ZIP XML):
     - Memastikan 7 berkas gambar di `word/media/` berukuran $\ge 300$ KB (menjamin resolusi 300 DPI, bukan thumbnail).
     - Memastikan keberadaan 4 tag `<w:tbl>` yang valid.
     - Memindai `document.xml` terhadap sisa-sisa markup unparsed seperti kotak ASCII `+---+`, tag mentah `$$`, atau `<!--`.
- **Kriteria Keberhasilan**:
  - `exit 0`: Kompilasi PDF dan DOCX lulus 100% dan lolos audit inspeksi visual XML.
  - `exit 1`: Terjadi kegagalan kompilasi atau terdeteksi artefak markup yang belum ter-render.

---

## 7. Rangkuman Tindakan Lanjutan untuk Tim (*Actionable Next Steps*)

1. **Untuk Agen Penulis / Editor Naskah**:
   - Pangkas abstrak di `sections/00_abstract.tex` dan `manuscript_draft.md` dari 350 kata menjadi $\le 250$ kata.
   - Kurangi kata kunci dari 10/9 menjadi 6 kata kunci berfokus geografi terapan.
   - Sinkronkan urutan sub-bab dan nomor figur pada `manuscript_draft.md` agar identik dengan `03_results.tex` (Figure 1: Wilayah Studi; Figure 2: Kepadatan Hotspot & FRP; Figure 3: Forensik Kanal; Figure 4: Tenurial Konsesi; Figure 5: Dinamika Temporal; Figure 6: Evaluasi Model ML; Figure 7: TreeSHAP).
   - Perbaiki kalimat pemanggil teks (*in-text callouts*) di `manuscript_draft.md` yang sebelumnya menyebut nomor figur yang keliru.
   - Ubah `\bibliographystyle` di `main.tex` ke gaya nama-tahun (*Author-Year*).
2. **Untuk Agen Kompilator**:
   - Jalankan kompilasi ulang PDF menggunakan `/opt/homebrew/bin/tectonic manuscript/main.tex`.
   - Jalankan kompilasi ulang seluruh DOCX menggunakan `/opt/homebrew/bin/pandoc --citeproc`.
3. **Untuk Agen Verifikator Programatik**:
   - Implementasikan 5 skrip verifikasi baru di `tests/` sesuai spesifikasi di atas.
   - Jalankan seluruh rangkaian tes pengujian (`pytest tests/` atau runner skrip mandiri) sebelum finalisasi paket submisi.
