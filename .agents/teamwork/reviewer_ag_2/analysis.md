# Laporan Review Independen dan Analisis Kritis Adversarial (reviewer_ag_2)

**Target Jurnal**: *Applied Geography* (Elsevier, Impact Factor: 7.4, CiteScore: 8.3, Scopus Q1)  
**Entitas Peninjau**: `reviewer_ag_2` (Teamwork Reviewer & Adversarial Critic)  
**Tanggal**: 4 November 2026  
**Vonis Akhir**: **APPROVE**

---

## 1. Ringkasan Eksekutif Review (Review Summary)

Peninjauan independen dan pengujian adversarial yang mendalam telah dilakukan terhadap seluruh komponen paket submisi manuskrip ilmiah:
1. `manuscript/main.pdf` & `manuscript/main.tex` (serta seluruh berkas modular `manuscript/sections/*.tex`)
2. `manuscript/submission_package/manuscript_main.docx`
3. `manuscript/submission_package/highlights.docx` & `manuscript/highlights.md`
4. `manuscript/submission_package/cover_letter.docx` & `manuscript/cover_letter.md`
5. `manuscript/references.bib` & `manuscript/manuscript_draft.md`
6. Seluruh rangkaian pengujian terotomatisasi di direktori `tests/`

Berdasarkan investigasi forensik langsung terhadap berkas biner, parsing dokumen OpenXML (Word DOCX), inspeksi visual PDF, penelusuran referensi silang LaTeX, serta replikasi mandiri pengujian empiris pada lingkungan Conda `karhutla_env`, disimpulkan bahwa:
- **Tidak ditemukan indikasi pelanggaran integritas (*integrity violations*)**, tidak ada pemalsuan metrik, tidak ada implementasi dummy/fasad, dan seluruh skrip pengujian melakukan evaluasi langsung terhadap berkas artefak riil.
- Kompilasi dokumen bebas galat dengan ketajaman visual tingkat publikasi internasional (300 DPI).
- Seluruh batasan editorial jurnal *Applied Geography* dipatuhi secara ketat.

---

## 2. Hasil Audit Objektif Berdasarkan Dimensi Evaluasi

### A. Integritas Kompilasi Dokumen & Perenderan Visual (Document Compilation & Rendering Integrity)

| Parameter Evaluasi | Target / Standar Editorial | Hasil Observasi Riil | Status | Bukti Verifikasi |
|---|---|---|:---:|---|
| **Kompilasi LaTeX (`main.pdf`)** | Kompilasi bersih via Tectonic tanpa galat, tepat 28 halaman | Exit Code 0, ukuran 10.62 MB, **tepat 28 halaman** (A4) | **PASS** | `pdfinfo manuscript/main.pdf` -> `Pages: 28` |
| **Gaya Sitasi Bibliografi** | Elsevier Harvard Author-Year (`elsarticle-harv`) | Sitasi teks berbentuk `(Author, Year)` atau `Author (Year)`, daftar pustaka berurut abjad ber-DOI, 0 sitasi numerik `[n]` | **PASS** | Teks PDF bersih dari kurung siku sitasi numerik; natbib `authoryear,round` terverifikasi |
| **Resolusi Figur PDF** | Figur tajam 300 DPI | 7 figur beresolusi tinggi, kerapatan piksel efektif dalam PDF mencapai 550 s.d. 849 PPI | **PASS** | `pdfimages -list manuscript/main.pdf` menunjukkan x-ppi/y-ppi 550--849 PPI |
| **Tabel Asli Word DOCX** | 4 tabel native OpenXML (`<w:tbl>`), 0 raw markdown pipes | Ditemukan **tepat 4 elemen `<w:tbl>`**, masing-masing 10 s.d. 13 baris. Ditemukan 0 pola `\| --- \|` | **PASS** | Parsing XML `word/document.xml` via `ElementTree` |
| **Persamaan Matematika DOCX** | Elemen matematika native OMML (`<m:oMath>`) | Ditemukan **tepat 132 elemen `<m:oMath>`** dan 9 display equation paragraph (`<m:oMathPara>`). 0 sintaks LaTeX bocor di teks | **PASS** | Audit XML `word/document.xml` namespace Office Math |
| **Gambar Tersemat DOCX** | 7 gambar tersemat beresolusi publikasi 300 DPI | Ditemukan 7 berkas PNG di `word/media/`, DPI terverifikasi 300 (299.9994), hash SHA-256 identik 100% dengan master figures | **PASS** | Audit SHA-256 & Pillow `img.info['dpi']` |
| **Placeholder / Link Rusak** | Tidak ada teks placeholder atau `??` | 0 kemunculan `??`, `TODO`, `TBD`, `[INSERT FIG]`, atau `[INSERT TAB]` di PDF maupun DOCX | **PASS** | Regex search menyeluruh pada PDF text dan DOCX XML |

### B. Kepatuhan Pedoman Editorial Elsevier (*Applied Geography Guide for Authors*)

| Kriteria Pedoman | Batasan / Ketentuan Jurnal | Nilai Terverifikasi | Status |
|---|---|---|:---:|
| **Panjang Kata Abstrak (DOCX)** | Maksimum 250 kata | **237 kata** (clean alphanumeric) / 228 kata (whitespace) / 247 kata (hyphen-split) | **PASS** |
| **Panjang Kata Abstrak (LaTeX)** | Maksimum 250 kata | **244 kata** | **PASS** |
| **Panjang Kata Abstrak (Markdown)** | Maksimum 250 kata | **246 kata** | **PASS** |
| **Panjang Kata Abstrak (PDF)** | Maksimum 250 kata | **244 kata** | **PASS** |
| **Jumlah Butir Highlights** | 3 hingga 5 butir peluru | **Tepat 5 butir peluru** (di Markdown & DOCX) | **PASS** |
| **Panjang Karakter Highlights** | Maksimum 85 karakter per butir (termasuk spasi) | Butir 1: 72 karakter<br>Butir 2: 76 karakter<br>Butir 3: 75 karakter<br>Butir 4: 78 karakter<br>Butir 5: 79 karakter | **PASS** |
| **Jumlah Kata Kunci (*Keywords*)** | 1 hingga 7 kata kunci spesifik | **Tepat 7 kata kunci** identik di seluruh format (LaTeX, MD, DOCX) | **PASS** |
| **Kesesuaian Kata Kunci** | Relevan dengan geografi terapan & GIScience | 1. *Applied spatial geography*<br>2. *Tropical peatlands*<br>3. *Spatial autocorrelation*<br>4. *Spatial block cross-validation*<br>5. *Land tenure governance*<br>6. *Wildfire intensity modeling*<br>7. *Mega Rice Project* | **PASS** |
| **Authorship & Afiliasi** | Lengkap sesuai deklarasi | Ahmad Sopian (First & Corresponding Author), Rahmi Susanti (Co-Author) | **PASS** |
| **Pernyataan Wajib Editorial** | CRediT, Data Availability, Funding, Conflict of Interest | Seluruhnya hadir dan terformat profesional di teks naskah dan dokumen terpisah | **PASS** |

### C. Integritas Sitasi Literatur & Pemanggilan Visual/Tabular (*In-text Callout Integrity*)

1. **Resolusi Sitasi Literatur (BibTeX vs LaTeX)**:
   - Ditemukan **tepat 40 entri BibTeX** bereputasi internasional di `manuscript/references.bib`.
   - Ditemukan **tepat 40 kunci sitasi unik** pada teks naskah (`sections/*.tex` dan `main.tex`).
   - Tingkat resolusi mencapai **100.00%** (0 kunci yang menggantung (*dangling citations*), dan semua entri BibTeX disitir secara aktif).
2. **Pemanggilan Figur (Figures 1 s.d. 7)**:
   - Setiap figur memiliki label LaTeX yang terhubung dengan `\ref` di dalam teks narasi.
   - Pada Markdown dan Word DOCX, Figur 1 sampai 7 dipanggil secara eksplisit dan konsisten.
   - Tidak ada figur yatim (*orphaned figures*) atau referensi yang salah tempat (*mismatched callouts*):
     - Figure 1: Peta wilayah studi, zonasi eks-PLG, dan partisi Spatial Block CV.
     - Figure 2: Kepadatan spasial hotspot dan rezim FRP (6.648 ekstrem vs 37.289 reguler).
     - Figure 3: Citra satelit true-color Dadahup, koridor kanal buffer, dan kurva peluruhan jarak.
     - Figure 4: Peta tenurial APL (75,4%) vs konsesi sawit HGU (16,6%) & kehutanan PBPH (8,0%).
     - Figure 5: Dinamika decadal SiPongi (2018--2026) dan dinamika krisis harian Oktober 2026.
     - Figure 6: Evaluasi model ML (ROC-AUC 0.7527 dan matriks konfusi Model B).
     - Figure 7: Plot TreeSHAP beeswarm yang menunjukkan ambang batas kanal 3 km dan defisit hujan.
3. **Pemanggilan Tabel (Tables)**:
   - Pada Word DOCX dan Markdown, terdapat **4 tabel terformat native**:
     - Tabel 1: Distribusi hotspot per 14 kabupaten/kota.
     - Tabel 2: Rekam jejak luasan kebakaran SiPongi KLHK (2018--2026) dan siklus ENSO.
     - Tabel 3: Perbandingan komprehensif performa Model A vs Model B (Holdout vs Spatial Block CV).
     - Tabel 4: Peringkat kepentingan fitur dan tipping point biofisik berbasis TreeSHAP.
   - Pada berkas LaTeX/PDF, terdapat 5 tabel karena penambahan tabel inventaris fitur (`tab:feature_inventory`) di Bab Metodologi sebagai Tabel 1, diikuti 4 tabel hasil penelitian sebagai Tabel 2 s.d. 5. Semua pemanggilan menggunakan referensi dinamis LaTeX `Table~\ref{...}`, sehingga tidak terjadi pergeseran nomor (*numbering drift*) atau tautan rusak pada berkas terkompilasi.

---

## 3. Eksekusi Test Suite Terotomatisasi

Pengujian otomatis dijalankan secara mandiri pada lingkungan Conda `karhutla_env`:

```bash
/opt/anaconda3/envs/karhutla_env/bin/pytest -v tests/
```

### Ringkasan Hasil Pengujian Pytest:
- `tests/test_abstract_word_count.py`: 5 passed
- `tests/test_document_compilation_rendering.py`: 5 passed
- `tests/test_highlights_length.py`: 5 passed
- `tests/test_keywords_alignment.py`: 5 passed
- `tests/test_reference_figure_callout_consistency.py`: 5 passed
- **Total: 25 PASSED (100%) dalam 42.62 detik**.

### Ringkasan Hasil Pengujian Empiris Mandiri:
- `tests/test_empirical_metrics.py`: LULUS 100% (semua 43.937 baris data, metrik TP=1094, FP=2737, FN=568, TN=6586, ROC-AUC=0.7527, F1=0.3983 terbukti identik secara matematis).
- `tests/test_challenger_m2_re_2.py`: LULUS 100% (seluruh angka spasial dan temporal terbukti sinkron dengan dataset master).
- `tests/audit_review_report_numbers.py`: LULUS 100% (12 kategori angka laporan terverifikasi akurat).
- `tests/verify_latex.py`: LULUS 100% (0 error, 0 warning).

---

## 4. Evaluasi Adversarial & Uji Ketahanan (*Adversarial Stress-Testing*)

Sebagai penantang kritis (*critic*), aspek-aspek batas (*boundary conditions*) berikut telah diuji:

1. **Uji Ambang Batas Abstrak terhadap Variasi Tokenizer**:
   - Penghitungan kata berbasis pemisahan alfanumerik murni menghasilkan 237 kata.
   - Penghitungan kata berbasis pemisahan tanda hubung (*hyphen-split*) menghasilkan 247 kata.
   - Kesimpulan stres: Di bawah metode tokenisasi terketat sekalipun, jumlah kata abstrak tetap berada di bawah batas maksimum 250 kata (memiliki margin aman 3 kata).
2. **Uji Panjang Karakter Highlights**:
   - Karakter butir terpanjang adalah Butir 5 dengan 79 karakter (termasuk spasi).
   - Margin keselamatan terhadap batas 85 karakter adalah 6 karakter penuh.
3. **Uji Kebocoran Format / Artefak Konversi**:
   - Pemeriksaan parsing XML membuktikan bahwa tidak ada sintaks Markdown (`| --- |`, `**`, `###`) maupun perintah LaTeX (`\begin{equation}`) yang bocor menjadi teks polos (*plain text*) di dokumen Word DOCX.
   - Semua persamaan matematika diubah secara elegan menjadi bahasa XML Office Math (OMML), sehingga pengguna Microsoft Word dapat mengeditnya secara alami sebagai persamaan Word asli.
4. **Pemeriksaan Integritas Ilmiah (*Integrity Audit*)**:
   - Tidak ditemukan kode pengujian palsu (*tautological tests*). Setiap tes membaca dan membedah file target secara fisik.
   - Model Machine Learning yang tersimpan di `output/models/karhutla_rf_model.joblib` adalah model Random Forest riil yang dilatih pada 43.937 data observasi satelit.

---

## 5. Kesimpulan Review (Conclusion)

Paket submisi naskah untuk jurnal *Applied Geography* telah memenuhi standar tertinggi penerbitan ilmiah internasional Elsevier, baik dari segi kedalaman metodologi spasial, integritas perenderan tipografi/visual, ketepatan sitasi pustaka, hingga kepatuhan mutlak terhadap batasan redaksional.

**Vonis Resmi**: **APPROVE** (Disetujui untuk submisi).
