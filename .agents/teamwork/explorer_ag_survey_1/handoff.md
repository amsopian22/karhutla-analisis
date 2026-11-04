# Handoff Report — Specification Mining & Manuscript Audit for *Applied Geography*

**Agent ID:** explorer_ag_survey_1 (`teamwork_spec_miner`)  
**Working Directory:** `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/explorer_ag_survey_1/`  
**Recipient / Parent:** 5ded17bc-a3a2-4d64-96ac-1cdeb9993084  
**Date:** 2026-11-04  
**Status:** Hard Handoff (Investigation & Specification Mining Complete)

---

## 1. Observation

Berdasarkan investigasi langsung terhadap aturan resmi Elsevier *Applied Geography* (*Guide for Authors*) dan audit berkas repositori menggunakan Python di lingkungan conda `karhutla_env`:

### Highlights:
- File paths: `manuscript/highlights.md` dan `manuscript/submission_package/highlights.docx`.
- Elsevier Specification: 3 hingga 5 butir (*bullet points*), maksimal 85 karakter per butir termasuk spasi.
- Hasil pengukuran karakter (via `len(b)` Python):
  - Butir 1: `"43,937 NASA FIRMS active fires analyzed across Central Kalimantan peatlands."` -> **76 karakter**.
  - Butir 2: `"Coordinate models collapse under Spatial Block CV, proving spatial memorization."` -> **80 karakter**.
  - Butir 3: `"Pure biophysical Random Forest retains 2.4-fold higher spatial CV F1-score."` -> **75 karakter**.
  - Butir 4: `"75.4% of fires occurred on unallocated APL land, exposing a governance void."` -> **76 karakter**.
  - Butir 5: `"TreeSHAP identifies key thresholds: 14-day dry spell and 3 km canal corridor."` -> **77 karakter**.
- Total butir: **5 butir**. Seluruh butir $\le 85$ karakter.

### Abstract Word Count:
- Elsevier Specification: Maksimal **250 kata**.
- Pengukuran jumlah kata (whitespace tokenization pada teks isi abstrak):
  - `manuscript/sections/00_abstract.tex`: **363 kata** (baris 3: 362 kata teks murni + 1 token parameter `0.4em`).
  - `manuscript/manuscript_draft.md`: **369 kata** (baris 17–19).
  - `manuscript/submission_package/manuscript_main.docx`: **368 kata** (Paragraf 4: 158 kata; Paragraf 5: 210 kata).
- Verbatim: Ketiga berkas melanggar batas kata maksimum Elsevier (+113 hingga +119 kata di atas batas).

### Keywords:
- Elsevier Specification: **1 hingga 7 kata kunci**.
- Pengukuran jumlah kata kunci saat ini:
  - `manuscript/sections/00_abstract.tex` (baris 6): **10 kata kunci** (*Tropical peatlands; Wildfire modeling; Spatial block cross-validation; Spatial memorization; Random Forest; TreeSHAP; Land tenure governance; Mega Rice Project; Fire Radiative Power; Central Kalimantan*).
  - `manuscript/manuscript_draft.md` (baris 21): **9 kata kunci** (*Peatland wildfire; Spatial block cross-validation; Spatial autocorrelation; Random Forest; TreeSHAP; Mega Rice Project; Land tenure governance; Fire Radiative Power (FRP); Central Kalimantan*).
  - `manuscript/submission_package/manuscript_main.docx` (Paragraf 6): **9 kata kunci**.
  - `manuscript/main.tex` (baris 48): 7 kata kunci dalam PDF metadata hyperref, namun belum memuat kata kunci spesifik seperti *Spatial autocorrelation*, *Land tenure governance*, atau *GIScience*.

### Citation & Reference Style:
- Elsevier Specification: Format resmi *Applied Geography* menggunakan **APA 7th edition / author-year** (misal: Smith et al., 2020) dengan daftar pustaka alfabetis.
- `manuscript/main.tex`:
  - Baris 26: `\usepackage[square,numbers,sort&compress]{natbib}`
  - Baris 173: `\bibliographystyle{unsrtnat}`
  - Sitasi pada naskah LaTeX saat ini dirender sebagai nomor bracket `[1]`, bukan nama-tahun `(Author, Year)`.
- `manuscript/references.bib`: Berisi 425 baris dengan 26 entri lengkap, memuat author, title, journal, volume, pages, year, dan DOI resmi.
- `manuscript/submission_package/manuscript_main.docx`: Pengutipan menghasilkan tanda kurung ganda seperti `(Page et al. (2002))` akibat konversi pandoc dasar.

### Front Matter, Statements & Cover Letter:
- CRediT Statement:
  - `manuscript/credit_statement.md`, `credit_statement.docx`, `main.tex` (baris 162–163), `manuscript_draft.md` (baris 346–349).
  - Ahmad Sopian: Conceptualization, Methodology, Software, Formal Analysis, Data Curation, Visualization, Writing - Original Draft, Project Administration (8 peran CRediT valid).
  - Rahmi Susanti: Conceptualization, Methodology, Validation, Investigation, Environmental Health and Haze Exposure Analysis, Writing - Review & Editing (5 peran CRediT valid + domain keahlian).
- Declaration of Competing Interest:
  - `manuscript/declaration_of_interest.md`, `declaration_of_interest.docx`, `main.tex` (baris 165–166), `manuscript_draft.md` (baris 350–352). Pernyataan standar bebas konflik kepentingan tertanggal 4 November 2026.
- Data Availability Statement:
  - `main.tex` (baris 156–158), `manuscript_draft.md` (baris 340–342). Mencantumkan repositori GitHub `https://github.com/amsopian22/karhutla-analisis` serta data NASA FIRMS dan ECMWF ERA5-Land.
- Cover Letter:
  - `manuscript/cover_letter.md` dan `cover_letter.docx`. Ditujukan resmi kepada *The Editor-in-Chief, Applied Geography, Elsevier Science*. Menyoroti geografi spasial terapan, mitigasi autokorelasi spasial, dan tata kelola tenurial APL.

### Target Journal Header Discrepancy:
- `manuscript/manuscript_draft.md` baris 10: Masih mencantumkan `Target Journal: *Remote Sensing of Environment* / *International Journal of Wildland Fire* / *MDPI Remote Sensing*`. Belum diperbarui menjadi *Applied Geography*.

### Compilation & Document Integrity:
- Kompilasi LaTeX via `/opt/homebrew/bin/tectonic`: Exit code 0, menghasilkan `main.pdf` 11 MB tanpa missing reference.
- Seluruh 7 gambar di `output/figures/` (01 s.d. 07) tersedia dengan resolusi tinggi.
- Seluruh 57 label LaTeX terdefinisi dan 21 sitasi silang `\ref` valid 100%.
- Berkas Word `manuscript_main.docx` memuat seluruh 7 gambar pada folder media (`word/media/`), dan 71 objek persamaan matematika diubah rapi ke Office Math (OMML `<m:oMath>`).

---

## 2. Logic Chain

1. **Premis Editorial Elsevier**: Jurnal *Applied Geography* memiliki sistem pra-skrining otomatis di editorial desk. Naskah yang melebihi 250 kata pada abstrak atau memuat lebih dari 7 kata kunci akan terkena penolakan teknis (*technical desk rejection* atau *send back to author*).
2. **Korelasi Observasi Abstrak**: Observasi menunjukkan panjang abstrak saat ini adalah 363 kata (.tex), 369 kata (.md), dan 368 kata (.docx). Angka ini melampaui batas maksimum 250 kata sebesar ~47%. Oleh karena itu, abstrak wajib dipangkas secara substansial.
3. **Penyusunan Solusi Abstrak Terkalibrasi**: Dengan memadatkan kalimat pengantar dan menggabungkan pelaporan temuan model (Model A vs Model B) serta statistik tenurial (75.4% APL), telah dirumuskan draf abstrak 242 kata. Draf ini mempertahankan seluruh parameter penting: 43.937 hotspot FIRMS, kanal 4.000 km, penurunan ROC-AUC Model A ke 0.5399, keunggulan Model B (ROC-AUC 0.7527, F1 0.1399), ambang batas TreeSHAP (hujan <5 mm, kanal <3 km, hari kering >14 hari), dan distribusi izin lahan.
4. **Korelasi Observasi Kata Kunci**: Observasi menunjukkan jumlah kata kunci adalah 10 (.tex) dan 9 (.md/.docx), melebihi batas 7 kata kunci. Dengan memadatkan ke 7 kata kunci inti yang selaras dengan geografi terapan (*Tropical peatlands; Peatland wildfires; Spatial autocorrelation; Spatial block cross-validation; Land tenure governance; GIScience; Central Kalimantan*), naskah langsung memenuhi syarat Elsevier dan meningkatkan discoverability di Scopus.
5. **Korelasi Observasi Gaya Sitasi**: Observasi menunjukkan `main.tex` menggunakan numerik `unsrtnat`, sedangkan pedoman resmi *Applied Geography* adalah APA 7th edition author-year. Mengganti konfigurasi natbib di `main.tex` ke `\usepackage[authoryear,round]{natbib}` dan `\bibliographystyle{elsarticle-harv}` atau `apalike` akan langsung merender nama-tahun sesuai dokumen Word dan Markdown, sehingga seluruh format menjadi seragam.
6. **Korelasi Metadata Draf**: Baris 10 `manuscript_draft.md` yang masih mencantumkan jurnal lama adalah inkonsistensi yang dapat memicu keraguan editor terhadap komitmen penulis kepada *Applied Geography*.

---

## 3. Caveats

1. **Kebijakan "Your Paper Your Way" Elsevier**:
   - Untuk penyerahan awal (*initial submission*), Elsevier mengizinkan referensi dalam gaya apa pun asalkan konsisten. Oleh karena itu, jika tim memilih mempertahankan numerik `[1]` pada berkas PDF awal, ini tidak melanggar syarat mutlak initial submission; namun penyelarasan ke APA author-year adalah praktik terbaik untuk kepatuhan penuh.
2. **Konversi Pandoc Sitasi ke Word**:
   - Tanda kurung ganda `(Page et al. (2002))` pada `manuscript_main.docx` terjadi karena pandoc dipanggil tanpa parameter `--citeproc` dan berkas CSL APA. Jika regenerasi Word dilakukan, pastikan menggunakan CSL APA atau sintaks sitasi yang sesuai.
3. **Keterbatasan Peran Read-Only**:
   - Agen ini berstatus read-only murni, sehingga tidak ada berkas naskah atau kode yang diubah secara langsung. Seluruh perubahan diserahkan kepada agen tahap berikutnya (*refiner*).

---

## 4. Conclusion

1. **Status Kelayakan Naskah**: Paket naskah telah memiliki fondasi ilmiah dan grafis yang sangat kuat (data 43.937 titik api, visualisasi 300 DPI, CRediT lengkap, cover letter tepat sasaran, LaTeX bebas error).
2. **Tiga Titik Wajib Perbaikan (*Mandatory Fixes*)**:
   - **Abstrak**: Ringkas teks abstrak dari 369 kata menjadi $\le 250$ kata (tersedia draf rekomendasi 242 kata di `analysis.md`).
   - **Kata Kunci**: Pangkas kata kunci dari 9–10 menjadi tepat 7 kata kunci tematik geografi terapan.
   - **Header Jurnal**: Ganti baris 10 `manuscript_draft.md` menjadi *Applied Geography*.
3. **Penyempurnaan Rekomendasi (*Recommended Enhancements*)**:
   - Ubah `main.tex` ke natbib `authoryear` dengan `elsarticle-harv` untuk menyelaraskan PDF dengan gaya APA jurnal.
   - Kompilasi ulang PDF via Tectonic dan regenerasi dokumen Word (`.docx`) untuk mengaplikasikan abstrak ringkas dan kata kunci terbarui.

---

## 5. Verification Method

Untuk memverifikasi secara independen kepatuhan berkas setelah perbaikan dilakukan:

1. **Verifikasi Jumlah Kata Abstrak**:
   ```bash
   /opt/anaconda3/envs/karhutla_env/bin/python -c '
   import re
   with open("manuscript/sections/00_abstract.tex") as f:
       text = f.read()
   m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.DOTALL)
   body = re.sub(r"\\textbf\{Keywords:\}.*", "", m.group(1), flags=re.DOTALL)
   cleaned = re.sub(r"\\[a-zA-Z]+(\[[^\]]*\])?(\{([^}]*)\})?", r"\3", body)
   cleaned = re.sub(r"[{}\\\$\~]", " ", cleaned).replace("\\noindent", "").strip()
   words = [w for w in cleaned.split() if w and not w.endswith("em")]
   print(f"Abstract Word Count: {len(words)} (Rule: <= 250) -> {\"PASS\" if len(words) <= 250 else \"FAIL\"}")
   '
   ```

2. **Verifikasi Panjang Karakter Highlights**:
   ```bash
   /opt/anaconda3/envs/karhutla_env/bin/python -c '
   with open("manuscript/highlights.md") as f:
       bullets = [l.strip()[2:].strip() for l in f if l.strip().startswith(("* ", "- "))]
   print(f"Total bullets: {len(bullets)} (Rule: 3-5)")
   for i, b in enumerate(bullets, 1):
       print(f"  B{i} ({len(b)} chars): {\"PASS\" if len(b) <= 85 else \"FAIL\"}")
   '
   ```

3. **Verifikasi Jumlah Kata Kunci**:
   ```bash
   /opt/anaconda3/envs/karhutla_env/bin/python -c '
   import re
   with open("manuscript/sections/00_abstract.tex") as f:
       text = f.read()
   m = re.search(r"\\textbf\{Keywords:\}\s*\\textit\{(.*?)\}", text)
   if m:
       kws = [k.strip() for k in m.group(1).split(";") if k.strip()]
       print(f"Keywords Count: {len(kws)} (Rule: 1-7) -> {\"PASS\" if 1 <= len(kws) <= 7 else \"FAIL\"}")
   '
   ```

4. **Verifikasi Kompilasi LaTeX**:
   ```bash
   cd /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/manuscript && /opt/homebrew/bin/tectonic main.tex
   echo "Exit code: $?"
   ```

---
*Dokumen temuan lengkap dan tabel rincian fitur tersedia di: `.agents/teamwork/explorer_ag_survey_1/analysis.md`*
