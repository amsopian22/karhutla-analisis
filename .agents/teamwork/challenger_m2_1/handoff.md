# LAPORAN PENGUJIAN EMPIRIS (HANDOFF REPORT) — CHALLENGER 1
**Milestone**: Milestone 2 — Naskah Publikasi LaTeX Scopus Q1  
**Agen**: Challenger 1 (Archetype: Empirical Challenger | Roles: Critic, Specialist)  
**Tanggal**: 2026-11-03  
**Status Vonis**: **REQUEST_CHANGES**

---

## 1. Observation (Hasil Pengamatan Langsung)

### 1.1 Hasil Eksekusi Pengujian Otomatis Bawaan (`tests/verify_latex.py`)
Perintah yang dijalankan:
```bash
/opt/anaconda3/envs/karhutla_env/bin/python tests/verify_latex.py
```
Hasil:
- Skrip selesai dengan kode keluar `0` (Exit Code 0).
- Memverifikasi keberadaan `main.tex`, `references.bib`, 6 berkas modular di `sections/`, dan 7 gambar PNG di `output/figures/`.
- Memverifikasi 40 entri BibTeX dan 40 sitasi naskah (0 undefined).
- Memverifikasi 51 label dan 12 referensi silang (0 unresolved).
- Mengonfirmasi keberadaan Sub-bab 4.4 (*Study Limitations, Uncertainties, and Threats to Validity*) serta 5 topik limitasi metodologis.

### 1.2 Hasil Audit Uji Mandiri Independen (`audit_manuscript_independent.py`)
Perintah yang dijalankan:
```bash
/opt/anaconda3/envs/karhutla_env/bin/python .agents/teamwork/challenger_m2_1/audit_manuscript_independent.py
```
Hasil:
- **Keseimbangan Kurung & Lingkungan**:
  - Kurung kurawal `{` dan `}` seimbang sempurna (0 mismatch).
  - Lingkungan `\begin{...}` dan `\end{...}` 100% berpasangan dan bersarang dengan valid (0 unclosed environments).
- **Integritas Gambar di Disk**:
  - Seluruh 7 berkas gambar (`01_` s.d. `07_`) terverifikasi valid secara biner via PIL (resolusi tinggi antara 3300x1560 hingga 4200x1650 px, format PNG, ukuran 202--509 KB).
- **Integritas Bibliografi BibTeX**:
  - 40 entri BibTeX di `references.bib` valid, memiliki field wajib (`author`, `title`, `year`), 0 duplikasi, 0 karakter khusus tak-ter-escape (`%`, `_`, `&`, `#`), dan 100% disitir aktif di naskah.
- **Konsistensi Metrik Empiris**:
  - Seluruh angka empiris pada naskah (43.937 titik api, 75,4% APL, 16,6% Sawit, 8,0% PBPH; Model A: Holdout AUC 0.7956, Spatial CV AUC 0.5399, Spatial CV F1 0.0583; Model B: Holdout AUC 0.7527, Spatial CV AUC 0.4950, Spatial CV F1 0.1399, Extreme Recall 65,82%, Regular Precision 92,1%) terbukti 100% konsisten dengan berkas sumber `model_metrics.json` dan `eda_summary.json`.

### 1.3 Temuan Anomali & Defek Teknis

#### Temuan 1 [CRITICAL COMPILATION RISK]: Hilangnya Paket `xcolor` pada `manuscript/main.tex`
- **Lokasi**: `manuscript/main.tex`, baris 13:
  ```latex
  \usepackage[colorlinks=true,linkcolor=blue!70!black,citecolor=blue!70!black,urlcolor=blue!70!black]{hyperref}
  ```
- **Fakta**: Sintaks pencampuran warna `blue!70!black` merupakan fitur spesifik dari paket `xcolor`. Namun, paket `\usepackage{xcolor}` **tidak diimpor** di mana pun dalam `main.tex`.
- **Dampak**: Jika naskah dikompilasi pada distribusi TeX standar (TeX Live, MacTeX, MiKTeX, atau Overleaf), kompiler `pdflatex`/`lualatex` akan langsung mengalami galat fatal:
  `! Package hyperref Error: Color `blue!70!black' not defined.`

#### Temuan 2 [FORMATTING DEFECT]: Keberadaan Artefak Sintaks Markdown Bold dalam Teks LaTeX
- **Lokasi & Kutipan Baris**:
  1. `manuscript/sections/03_results.tex`, baris 89:
     ```latex
     ... accounted for **51.92\%** (22,813 hotspots) of all active fires detected across the province.
     ```
  2. `manuscript/sections/03_results.tex`, baris 178:
     ```latex
     ... yielding a mean $F_1$-score of 0.1399---representing a **2.40-fold improvement** over Model~A.
     ```
  3. `manuscript/sections/04_discussion.tex`, baris 29:
     ```latex
     ... achieving a mean spatial $F_1$-score of 0.1399---representing a **2.40-fold improvement** over Model~A.
     ```
- **Fakta**: Karakter ganda bintang `**...**` adalah sintaks Markdown, bukan LaTeX.
- **Dampak**: Pada PDF yang dicetak, teks tersebut akan menampilkan tanda bintang ganda secara harafiah (`**51.92%**` dan `**2.40-fold improvement**`). Hal ini merusak estetika profesional publikasi jurnal internasional Scopus Q1. Sintaks yang benar adalah `\textbf{51.92\%}` dan `\textbf{2.40-fold improvement}`.

#### Temuan 3 [STRUCTURAL / EDITORIAL CALLOUT OMISSIONS]: 9 Persamaan Bernomor Tanpa In-Text Callout
- **Lokasi**: `manuscript/sections/02_materials_methods.tex`:
  - `eq:canal_dist` (Persamaan 1, baris 55)
  - `eq:ex_plg` (Persamaan 2, baris 65)
  - `eq:fwi` (Persamaan 3, baris 86)
  - `eq:target` (Persamaan 4, baris 152)
  - `eq:class_weight` (Persamaan 5, baris 159)
  - `eq:features_a` (Persamaan 6, baris 171)
  - `eq:features_b` (Persamaan 7, baris 176)
  - `eq:spatial_cv` (Persamaan 8, baris 191)
  - `eq:shap` (Persamaan 9, baris 211)
- **Fakta**: Seluruh 9 persamaan diberi label `\label{eq:...}`, namun tidak ada satu pun yang dipanggil atau dirujuk dalam teks menggunakan `\eqref{eq:...}` atau `\ref{eq:...}`.
- **Dampak**: Standar jurnal ilmiah Q1 (seperti *Remote Sensing of Environment*, *Ecological Modelling*) mewajibkan setiap persamaan matematis yang bernomor memiliki referensi aktif dalam narasi (misalnya: *“as formulated in Equation~\eqref{eq:canal_dist}”*).

---

## 2. Logic Chain (Rantai Logika Pengujian)

1. **Premis 1 (Standar Eksekusi & Validitas Kompilasi)**:
   Sebuah naskah LaTeX yang berstatus *Publication-Ready* untuk jurnal Scopus Q1 harus dapat dikompilasi tanpa galat dependensi paket pada sistem TeX manapun.
2. **Premis 2 (Ketergantungan Paket xcolor)**:
   Opsi `blue!70!black` pada paket `hyperref` (baris 13 `main.tex`) secara teknis memerlukan deklarasi `\usepackage{xcolor}` sebelum pemanggilan `hyperref`. Karena deklarasi tersebut absen, dokumen rentan gagal dikompilasi pada lingkungan penerbit.
3. **Premis 3 (Kebersihan Sintaksis Typesetting)**:
   Keberadaan artefak Markdown `**...**` pada 3 lokasi (`03_results.tex:89, 178` dan `04_discussion.tex:29`) merupakan cacat format yang akan tertera secara visual di PDF akhir.
4. **Premis 4 (Kohesi Referensi Silang Akademik)**:
   Pemberian label persamaan tanpa adanya callout `\eqref{...}` dalam narasi mengindikasikan struktur referensi silang yang belum tuntas untuk 9 formula metodologi inti.
5. **Kesimpulan Deduktif**:
   Meskipun struktur ilmiah, narasi, dan konsistensi datanya sangat solid (memenuhi seluruh kriteria R1 dan data R2), adanya risiko kompilasi fatal (Temuan 1) dan cacat format teks (Temuan 2) menuntut perbaikan sebelum dapat dinyatakan disetujui (APPROVE). Oleh karena itu, vonis yang tepat secara profesional adalah **REQUEST_CHANGES**.

---

## 3. Caveats (Batasan Pengujian)

1. **Ketiadaan Biner LaTeX pada Mesin Host**:
   Biner `pdflatex` atau `xelatex` tidak terinstal pada sistem operasi mesin (`which pdflatex` mengembalikan non-zero). Verifikasi dilakukan menggunakan skrip simulasi parsing parser token independen, validasi regex, dan audit dependensi paket.
2. **Lingkup Gambar Tambahan (Figure 08)**:
   File `output/figures/08_transboundary_haze_dispersion.png` tersedia di disk dan dibahas secara konseptual di bagian masa depan (Section 5.3), namun tidak dijadikan figur naskah utama karena naskah difokuskan pada 7 figur utama sesuai spesifikasi R2.

---

## 4. Conclusion (Kesimpulan & Vonis Akhir)

**Vonis**: **REQUEST_CHANGES**

Naskah publikasi memiliki mutu ilmiah yang sangat tinggi, struktur IMRaD yang kokoh, pembahasan limitasi (Section 4.4) yang komprehensif dan jujur, serta keselarasan data empiris 100%. Namun, naskah memerlukan perbaikan teknis minor yang terarah sebelum siap dikirim ke penerbit:
1. **Tambahkan** `\usepackage{xcolor}` tepat sebelum `\usepackage[...]{hyperref}` pada `manuscript/main.tex`.
2. **Gantikan** seluruh sintaks Markdown bold `**...**` dengan `\textbf{...}` pada `manuscript/sections/03_results.tex` (baris 89 dan 178) serta `manuscript/sections/04_discussion.tex` (baris 29).
3. **Tambahkan** callout eksplisit `Equation~\eqref{eq:...}` pada narasi di `manuscript/sections/02_materials_methods.tex` untuk menghubungkan formula 1 s.d. 9 ke dalam teks penjelas.

---

## 5. Verification Method (Metode Verifikasi Ulang Independen)

Untuk memverifikasi secara independen bahwa perbaikan telah selesai dan berhasil:

1. **Jalankan Verifikasi Bawaan Proyek**:
   ```bash
   /opt/anaconda3/envs/karhutla_env/bin/python tests/verify_latex.py
   ```
2. **Jalankan Skrip Audit Independen Challenger 1**:
   ```bash
   /opt/anaconda3/envs/karhutla_env/bin/python .agents/teamwork/challenger_m2_1/audit_manuscript_independent.py
   ```
   *Kondisi Kelulusan*: Menghasilkan 0 Errors, 0 Warnings terkait `xcolor` dan `**`, serta semua callout terhubung.
3. **Pemeriksaan Berkas Manual (Spot Check)**:
   - Periksa `manuscript/main.tex` baris 12-14: pastikan `\usepackage{xcolor}` ada sebelum `hyperref`.
   - Periksa `manuscript/sections/03_results.tex` dan `04_discussion.tex`: pastikan tidak ada karakter `**`.
