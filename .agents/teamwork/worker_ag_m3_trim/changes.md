# Laporan Perubahan Teknis (*Changes Report*) — Pemangkasan Kata Abstrak Manuskrip

**Agen**: `worker_ag_m3_trim`  
**Tanggal**: 2026-11-04  
**Target Jurnal**: *Applied Geography* (Elsevier, IF: 7.4, CiteScore: 8.3, Scopus Q1)  
**Lingkungan**: Conda `karhutla_env` (Python 3.10.22)  

---

## 1. Ringkasan Eksekutif Perubahan

Untuk menjamin kepatuhan mutlak (*unconditional immunity*) terhadap seluruh algoritma tokenisasi kata editorial Elsevier—khususnya parser batas kata regex naif `\b\w+\b` yang memecah angka desimal (`0.7956` $\rightarrow$ `0` + `7956`) dan kata majemuk bertanda hubung—telah dilakukan pemangkasan tepat **7 kata pengisi non-esensial** (*non-essential filler words*) dari teks abstrak. Pemangkasan ini dilakukan tanpa membuang atau mengubah satu pun angka empiris, metrik evaluasi model, maupun ambang batas TreeSHAP.

---

## 2. Rincian Modifikasi Berkas Sumber

### 2.1 `manuscript/sections/00_abstract.tex` (Line 3)
Modifikasi teks abstrak LaTeX dilakukan dengan presisi tinggi:
1. Menghapus `, Indonesia` setelah `Central Kalimantan`:
   - *Sebelum*: `...during the October 2026 crisis in Central Kalimantan, Indonesia, integrated with...`
   - *Sesudah*: `...during the October 2026 crisis in Central Kalimantan, integrated with...` (-1 kata)
2. Menghapus `depth` pada frasa peta gambut:
   - *Sebelum*: `...integrated with official peat depth maps, metric primary canal vectors...`
   - *Sesudah*: `...integrated with official peat maps, metric primary canal vectors...` (-1 kata)
3. Menghapus `ECMWF` sebelum `ERA5-Land`:
   - *Sebelum*: `...metric primary canal vectors (UTM Zone 49S), ECMWF ERA5-Land reanalysis,...`
   - *Sesudah*: `...metric primary canal vectors (UTM Zone 49S), ERA5-Land reanalysis,...` (-1 kata)
4. Menghapus `across unseen regions` setelah `generalizability`:
   - *Sebelum*: `...preserved spatial generalizability across unseen regions (holdout ROC-AUC:...`
   - *Sesudah*: `...preserved spatial generalizability (holdout ROC-AUC:...` (-3 kata)
5. Menghapus `attribution` setelah `TreeSHAP`:
   - *Sebelum*: `TreeSHAP attribution identified key non-linear thresholds:...`
   - *Sesudah*: `TreeSHAP identified key non-linear thresholds:...` (-1 kata)

**Total Kata Dipangkas**: Tepat **7 kata**.

### 2.2 `manuscript/manuscript_draft.md` (Line 17)
Penerapan modifikasi yang identik 100% secara leksikal pada draf Markdown untuk menjamin paritas multi-format.

---

## 3. Kompilasi Ulang Artefak Publikasi

1. **LaTeX ke PDF (`manuscript/main.pdf`)**:
   - Perintah: `cd manuscript && /opt/homebrew/bin/tectonic main.tex`
   - Hasil: Kompilasi sukses, exit code 0.
   - Ukuran berkas: 10.62 MiB.
   - Jumlah halaman: Tepat 28 halaman (sesuai spesifikasi).
2. **Markdown ke Word DOCX (`manuscript/submission_package/manuscript_main.docx`)**:
   - Perintah: `/opt/homebrew/bin/pandoc manuscript/manuscript_draft.md -o manuscript/submission_package/manuscript_main.docx --citeproc --bibliography=manuscript/references.bib`
   - Hasil: Kompilasi sukses, exit code 0.
   - Integritas struktur: 4 tabel Word native (`<w:tbl>`), persamaan matematika OMML (`<m:oMath>`), dan 7 gambar master 300 DPI tertanam secara sempurna.

---

## 4. Hasil Audit Tokenisasi Kata Lintas Format

| Format Berkas | Whitespace Split (`text.split()`) | Clean Words (`test_abstract_word_count.py`) | Regex Word Boundary (`\b\w+\b`) | Status Batas Elsevier ($\le 250$) |
| :--- | :---: | :---: | :---: | :---: |
| **LaTeX (`00_abstract.tex`)** | 234 kata | 237 kata | **247 kata** | **PASS (Margin: 3)** |
| **Markdown (`manuscript_draft.md`)** | 234 kata | 239 kata | **249 kata** | **PASS (Margin: 1)** |
| **Word DOCX (`manuscript_main.docx`)** | 221–223 kata | 230 kata | **240–247 kata** | **PASS (Margin: 3–10)** |
| **PDF (`main.pdf`)** | 228 kata | 237 kata | **245 kata** | **PASS (Margin: 5)** |

*Seluruh format terbukti lolos di bawah batas 250 kata pada semua metode tokenisasi.*

---

## 5. Audit Integritas Angka dan Metrik Empiris (100% Utuh)

Semua metrik dan nilai empiris terverifikasi tetap ada dan tidak berubah di keempat format:
- `43,937`: Titik api aktif satelit terverifikasi NASA FIRMS.
- `0.7956`: Holdout ROC-AUC Model A (Spatial Memorization).
- `0.5399`: Spatial Block CV ROC-AUC Model A yang runtuh.
- `0.0000`: F1-score Model A pada 4 dari 5 lipatan spasial.
- `0.7527`: Holdout ROC-AUC Model B (Pure Biophysical).
- `65.8%`: Extreme Fire Recall Model B.
- `0.1399`: Rata-rata Spatial Block CV F1-score Model B (retensi 2,4x lipat).
- `< 5.0 mm`: Ambang defisit curah hujan 7-harian TreeSHAP.
- `< 3.0 km`: Koridor kedekatan saluran drainase primer TreeSHAP.
- `> 14 days`: Ambang hari kering berturut-turut TreeSHAP.
- `75.4%`: Persentase kebakaran pada lahan terbuka non-konsesi (APL).
- `24.6%`: Persentase kebakaran pada konsesi korporasi (sawit & PBPH).

---

## 6. Status Verifikasi Pytest Otomatis

- Perintah: `/opt/anaconda3/envs/karhutla_env/bin/pytest -v tests/`
- Hasil: **37 PASSED (100%)** dalam 42.57 detik (exit code 0).
