# LAPORAN ANALISIS PENGUJIAN STRES DAN INTEGRITAS BINER MANUSKRIP (CHALLENGER 1)
**Target Jurnal**: *Applied Geography* (Elsevier, Impact Factor: 7.4, CiteScore: 8.3, Scopus Q1)  
**Metodologi**: *Empirical Adversarial Stress Testing* (Inspeksi Biner, Parsing XML, Audit Tectonic, dan Validasi Pytest)  
**Tanggal Pengujian**: 2026-11-04  
**Evaluator**: `challenger_ag_1` (Senior Data Scientist & Empirical Challenger)

---

## 1. Ringkasan Eksekutif & Vonis Evaluasi

Berdasarkan pengujian empiris adversarial independen yang dilakukan terhadap paket submisi manuskrip (*submission package*) untuk jurnal *Applied Geography*, seluruh 4 dimensi kritis—kompilasi dokumen, integritas biner/struktur XML DOCX, konsistensi rujukan silang & *callouts*, serta kepatuhan panduan Elsevier—telah diuji secara ketat.

| Dimensi Pengujian | Status Pengujian | Skor / Hasil Empiris | Status Gate |
|---|---|---|---|
| **1. Kompilasi LaTeX / Tectonic** | PASSED | Exit code 0, 28 halaman, 10.62 MB, 0 *broken ref/cite* | **VALID** |
| **2. Integritas Biner & XML DOCX** | PASSED | 0 markdown pipes, 4 tabel native lengkap, 132 OMML math, 7 media 300 DPI | **VALID** |
| **3. Konsistensi Callout & Sitasi** | PASSED | Gambar 1–7 & Tabel 1–4 sekuensial, 100% kunci BibTeX teresolusi (0 *dangling*) | **VALID** |
| **4. Kepatuhan Panduan Penulis** | PASSED | Abstrak 237–246 kata (≤250), Highlights 5 butir (72–79 kar ≤85), 7 kata kunci | **VALID** |
| **5. Eksekusi Test Suite Pytest** | PASSED | 37 dari 37 pengujian lolos (100% *pass rate* dalam 106.54 detik) | **VALID** |

**Vonis Eksplisit**: **APPROVE** (Seluruh kriteria integritas terpenuhi secara empiris tanpa cacat).

---

## 2. Pengujian Stres Kompilasi Dokumen (LaTeX & Tectonic Engine)

### 2.1. Protokol dan Eksekusi Kompilasi
Pengujian kompilasi dijalankan langsung pada berkas sumber `manuscript/main.tex` menggunakan engine Tectonic v0.15.0 (`/opt/homebrew/bin/tectonic main.tex`).

- **Return Code**: `0` (Kompilasi sukses tanpa kesalahan fatal).
- **Ukuran Berkas Output PDF**: `11.14 MB` (`10.62 MiB`), membuktikan seluruh 7 gambar beresolusi tinggi (300 DPI) telah terkompresi dan disematkan sempurna melalui xdvipdfmx.
- **Jumlah Halaman**: Tepat **28 halaman**, sesuai dengan standar artikel riset komprehensif.
- **Audit Metadata PDF**:
  - `Title`: *Spatiotemporal Fire Intensity Modeling in Degraded Tropical Peatlands: Addressing Spatial Autocorrelation and Land Tenure Governance in Central Kalimantan*
  - `Author`: *Ahmad Sopian and Rahmi Susanti*
  - `Subject`: *Applied Spatial Geography, Tropical Peatlands, and Wildfire Governance*

### 2.2. Audit Peringatan Engine TeX (*TeX Warnings & Boxes*)
- **Peringatan Referensi**: `0` rujukan undefined (`There were undefined references` = 0).
- **Peringatan Sitasi**: `0` sitasi undefined (`Citation ... undefined` = 0).
- **Peringatan Karakter Fon**: `0` missing glyphs (`Missing character: There is no ... in font` = 0).
- **Audit Overfull Boxes**: Tidak ditemukan *severe overfull box* (> 15 pt). Semua pemutusan baris terkelola rapi dengan paket `microtype` dan `setstretch{1.14}`. Peringatan minor `Underfull \hbox (badness 1533)` di `02_materials_methods.tex:156` merupakan perataan alami paragraf matematika yang tidak mendistorsi tata letak visual.

---

## 3. Pengujian Stres Integritas Biner dan Struktur XML Word DOCX

Pemeriksaan mendalam dilakukan terhadap berkas `manuscript/submission_package/manuscript_main.docx` melalui parsing pustaka `zipfile` dan `xml.etree.ElementTree`.

### 3.1. Uji Kontaminasi Karakter & Sintaks Markdown
- **Markdown Pipes**: Dilakukan pemindaian teks pada seluruh simpul XML (`word/document.xml`). Hasil: **0 kemunculan** pola `| --- |`, `|---|`, atau `|:---|`.
- **ASCII Box Drawing**: Karakter kotak terminal (`┌`, `┬`, `┐`, `├`, `┼`, `┤`, `└`, `┴`, `┘`, `│`, `─`, `+---+`) **tidak ditemukan sama sekali (0%)**.
- **Kebocoran Perintah LaTeX**: Tidak ditemukan string perintah LaTeX mentah seperti `\begin{table}`, `\end{tabular}`, `\ref{...}`, atau `\cite{...}` dalam teks narasi DOCX.

### 3.2. Struktur dan Kelengkapan Tabel Native Word (`<w:tbl>`)
Ditemukan tepat **4 tabel native Word** yang dibangun menggunakan elemen `<w:tbl>`, `<w:tr>`, dan `<w:tc>`:
1. **Table 1** (11 baris, 4 kolom per baris): Distribusi titik api per kabupaten/kota, persentase, dan karakteristik geomorfologi/gambut. Seluruh baris terisi penuh.
2. **Table 2** (10 baris, 4 kolom per baris): Trajektori dekadal luasan terbakar SiPongi KLHK (2018–2026) dan rezim ENSO/iklim.
3. **Table 3** (13 baris, 4 kolom per baris): Perbandingan komparatif Model A (dengan koordinat) vs Model B (biofisik murni) pada *Random Holdout* dan 5-fold *Spatial Block Cross-Validation*.
4. **Table 4** (13 baris, 4 kolom per baris): Peringkat atribusi fitur TreeSHAP dari peringkat 1 hingga 12 dengan nilai *mean absolute SHAP* dan mekanisme biofisik.

### 3.3. Struktur Persamaan Matematika Native OMML (`<m:oMath>`)
- Ditemukan **9 blok persamaan matematika terpisah** (`<m:oMathPara>`) dan total **132 elemen formula OMML** (`<m:oMath>`).
- Persamaan kunci seperti jarak kanal Euclidean ($d_{\text{canal},i}$), formulasi Fire Weather Index ($\text{FWI}$), fungsi pembobot kelas ($w_c$), partisi spasial disjoint ($\mathcal{D} = \bigcup_{k=1}^K \mathcal{D}_k$), serta nilai TreeSHAP ($\phi_j(f, x)$) dirender secara native menggunakan struktur fraksi, akar pangkat, superskrip/subskrip, dan operator union OpenXML asli, bukan teks biasa.
- Simbol matematika di dalam sel tabel (misalnya $P_{\text{7d}}$, $d_{\text{canal}}$, $< 5.0$, $< 3.0$) disematkan sebagai objek formula OMML di dalam sel `<w:tc>`.

### 3.4. Integritas Media dan Verifikasi Hash Kriptografis Gambar
Terdapat tepat **7 berkas gambar** di dalam direktori `word/media/` pada arsip ZIP DOCX. Masing-masing diuji kecocokan hash kriptografis SHA-256 dan kerapatan resolusi visual (DPI) terhadap berkas master di `output/figures/`:

| No | Berkas Master (`output/figures/`) | Berkas Media DOCX | SHA-256 Hash Match | Resolusi (Pixel) | Kerapatan (DPI) | Status |
|:--:|---|---|:---:|:---:|:---:|:---:|
| 1 | `01_peta_wilayah_studi_spatial_cv.png` | `word/media/rId11.png` | `28a34683be64...` (100%) | 4685 x 2594 | 300 DPI | MATCH |
| 2 | `02_peta_densitas_hotspot_frp.png` | `word/media/rId27.png` | `969f6b67ede6...` (100%) | 4593 x 3081 | 300 DPI | MATCH |
| 3 | `03_analisis_citra_satelit_kanal.png` | `word/media/rId31.png` | `668950b2fc25...` (100%) | 4771 x 2957 | 300 DPI | MATCH |
| 4 | `04_peta_tenurial_konsesi_esg.png` | `word/media/rId35.png` | `8d780ca086c8...` (100%) | 4086 x 3081 | 300 DPI | MATCH |
| 5 | `05_tren_temporal_dan_harian.png` | `word/media/rId39.png` | `182ed0d1f00e...` (100%) | 4794 x 1831 | 300 DPI | MATCH |
| 6 | `06_evaluasi_model_ml.png` | `word/media/rId43.png` | `5daadde62868...` (100%) | 4200 x 1650 | 300 DPI | MATCH |
| 7 | `07_shap_feature_importance.png` | `word/media/rId47.png` | `fd8304642e60...` (100%) | 3170 x 1861 | 300 DPI | MATCH |

*Catatan Teknis*: Nilai pembacaan DPI PIL sebesar `(299.9994, 299.9994)` merupakan hasil konversi floating-point standar dari satuan metrik PNG (11.811 dots/meter / 39.3700787 in/meter = 299.9994 DPI), yang secara definitif merepresentasikan standar industri 300 DPI.

---

## 4. Pengujian Konsistensi Rujukan Silang (*Cross-References & Callouts*)

### 4.1. Pemanggilan Sekuensial Gambar dan Tabel di LaTeX
Pengujian alur teks linear pada `manuscript/main.tex` membuktikan bahwa pemanggilan pertama (*first in-text callout*) untuk seluruh gambar dan tabel berjalan secara sekuensial tanpa anomali:
- **Urutan Gambar**:  
  $\text{Figure 1 (offset 10033)} < \text{Figure 2 (30585)} < \text{Figure 3 (37210)} < \text{Figure 4 (38015)} < \text{Figure 5 (40886)} < \text{Figure 6 (45110)} < \text{Figure 7 (49891)}$ $\rightarrow$ **VALID SEKUANSIAL**.
- **Urutan Tabel**:  
  $\text{Table 1 (offset 30544)} < \text{Table 2 (40853)} < \text{Table 3 (45073)} < \text{Table 4 (49858)}$ $\rightarrow$ **VALID SEKUANSIAL**.
- **Integritas Label-Ref**: Seluruh 7 label gambar utama (`fig:study_area`, `fig:fire_density_frp`, `fig:satellite_canal_forensic`, `fig:tenurial_concession`, `fig:temporal_dynamics`, `fig:model_evaluation`, `fig:shap_importance`) dan 4 label tabel (`tab:regency_distribution`, `tab:decadal_sipongi`, `tab:model_comparison`, `tab:shap_ranking`) dirujuk secara eksplisit dalam teks naratif. Tidak ada rujukan menggantung (*dangling reference* = 0).

### 4.2. Pemanggilan Sekuensial Gambar dan Tabel di Word DOCX
Pemeriksaan teks pada `manuscript_main.docx` memastikan urutan pemanggilan naratif yang paralel:
- **Urutan Gambar DOCX**:  
  $\text{Figure 1 (karakter 11436)} < \text{Figure 2 (22478)} < \text{Figure 3 (26516)} < \text{Figure 4 (28428)} < \text{Figure 5 (31951)} < \text{Figure 6 (34190)} < \text{Figure 7 (37794)}$ $\rightarrow$ **VALID SEKUANSIAL**.
- **Urutan Tabel DOCX**:  
  $\text{Table 1 (karakter 22466)} < \text{Table 2 (30830)} < \text{Table 3 (34178)} < \text{Table 4 (37782)}$ $\rightarrow$ **VALID SEKUANSIAL**.
- **Deteksi Broken Reference**: Pola error seperti `[?]`, `Error! Reference source not found`, atau tag LaTeX yang tidak terproses bernilai **0**.

### 4.3. Resolusi Sitasi BibTeX
- Berkas `manuscript/references.bib` berisi **50 entri sitasi lengkap** tanpa adanya kunci duplikat.
- Terdapat **47 kunci sitasi unik** yang dirujuk dalam teks LaTeX (`\cite`, `\citep`, `\citet`).
- Seluruh 47 kunci sitasi teresolusi 100% terhadap entri di `references.bib` tanpa satupun sitasi menggantung (*0 dangling citations*).

---

## 5. Kepatuhan Panduan Penulis *Applied Geography* (Elsevier)

### 5.1. Batasan Jumlah Kata Abstrak (Maksimal 250 Kata)
Penghitungan kata abstrak pada seluruh format dokumen:
- **LaTeX** (`sections/00_abstract.tex`): **244 kata** (≤ 250 kata) $\rightarrow$ **MEMENUHI SYARAT**.
- **Markdown** (`manuscript_draft.md`): **246 kata** (≤ 250 kata) $\rightarrow$ **MEMENUHI SYARAT**.
- **Word DOCX** (`manuscript_main.docx`): **237 kata** (≤ 250 kata) $\rightarrow$ **MEMENUHI SYARAT**.
- **Compiled PDF** (`main.pdf`): **244 kata** (≤ 250 kata) $\rightarrow$ **MEMENUHI SYARAT**.

### 5.2. Format Research Highlights
Ketentuan Elsevier: 3–5 butir, masing-masing maksimal 85 karakter termasuk spasi:
1. `43,937 active fire detections analyzed across degraded Borneo peatlands.` — **72 karakter** (≤ 85)
2. `Coordinate-based ML collapses under Spatial Block CV via Tobler's First Law.` — **76 karakter** (≤ 85)
3. `Pure biophysical Random Forest retains 2.4-fold higher spatial CV F1-score.` — **75 karakter** (≤ 85)
4. `75.4% of fires occur on unallocated public lands (APL), revealing tenure void.` — **78 karakter** (≤ 85)
5. `Explainable AI reveals critical 3 km canal corridor and 14-day drought trigger.` — **79 karakter** (≤ 85)

Format pada `manuscript/highlights.md` dan `manuscript/submission_package/highlights.docx` memiliki keselarasan paritas 100%.

### 5.3. Kata Kunci (*Keywords*)
Manuskrip memuat **7 kata kunci** (batas 1–7) yang selaras dengan ruang lingkup *Applied Geography*:
1. *Applied spatial geography*
2. *Tropical peatlands*
3. *Spatial autocorrelation*
4. *Spatial block cross-validation*
5. *Land tenure governance*
6. *Wildfire intensity modeling*
7. *Mega Rice Project*

---

## 6. Verifikasi Test Suite Pytest

Eksekusi penuh terhadap seluruh berkas pengujian di direktori `tests/` menggunakan lingkungan conda `karhutla_env`:

```bash
/opt/anaconda3/envs/karhutla_env/bin/pytest -v tests/
```

**Hasil Eksekusi**:
- **Total Test Cases**: 37 pengujian
- **Status**: **37 PASSED** (0 failed, 0 errors, 0 skipped)
- **Durasi Eksekusi**: 106.54 detik
- **Rincian Modul**:
  - `tests/test_abstract_word_count.py`: 5 passed
  - `tests/test_challenger_adversarial_suite.py`: 12 passed
  - `tests/test_document_compilation_rendering.py`: 5 passed
  - `tests/test_highlights_length.py`: 5 passed
  - `tests/test_keywords_alignment.py`: 5 passed
  - `tests/test_reference_figure_callout_consistency.py`: 5 passed

---

## 7. Kesimpulan dan Rekomendasi

Paket submisi manuskrip (*submission package*) `manuscript/` telah melewati seluruh pengujian integritas struktural, kompilasi biner, konsistensi spasial, dan kepatuhan panduan publikasi internasional dengan hasil sempurna. Tidak ditemukan cacat rendering, inkonsistensi data, maupun pelanggaran pedoman Elsevier. Dokumen siap untuk tahap penyerahan resmi (*formal submission*).
