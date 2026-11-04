# Laporan Handoff Challenger 1: Re-evaluasi Gate Milestone 2 (Naskah Publikasi LaTeX Scopus Q1)

## 1. Observation (Pengamatan Empiris)

Pengujian dan audit independen dilakukan secara langsung di lingkungan conda `karhutla_env` pada repositori `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis` terhadap seluruh artefak Milestone 2 (`manuscript/main.tex`, `manuscript/sections/*.tex`, `manuscript/references.bib`, `tests/verify_latex.py`, dan `tests/check_latex_metrics.py`).

Berikut adalah fakta empiris dan kutipan verbatim dari pengujian:

1. **Eksekusi Pengujian Statis Resmi (`tests/verify_latex.py`)**:
   - Perintah: `/opt/anaconda3/envs/karhutla_env/bin/python tests/verify_latex.py`
   - Hasil keluaran:
     ```text
     ==================================================================
           VERIFIKASI STATIS NASKAH ILMIAH LATEX (tests/verify_latex.py)
     ==================================================================
     [PASS]  main.tex ditemukan (3042 bytes)
     [PASS]  references.bib ditemukan (16979 bytes)
     [PASS]  Bagian modular 00_abstract.tex s.d. 05_conclusions.tex ditemukan (6 bagian)
     [PASS]  Gambar 01_ s.d. 07_ ditemukan (7 gambar ilmiah)
     [PASS]  Dokumen lengkap berhasil disusun (628 baris, 74030 karakter)
     [PASS]  Seluruh lingkungan LaTeX seimbang secara sempurna (0 mismatch).
     [PASS]  Ditemukan 40 entri BibTeX valid di references.bib (Target 40 terpenuhi)
     [PASS]  Ditemukan 40 kunci sitasi unik pada teks naskah (100% terdefinisi, 0 undefined keys, 0 uncited).
     [PASS]  Ditemukan 51 label unik tanpa duplikasi.
     [PASS]  Ditemukan 21 referensi silang unik pada teks (100% terselesaikan sempurna).
     [PASS]  Figur fig:decadal_trend s.d. fig:shap_importance terdefinisi dan memiliki callout aktif.
     [PASS]  7 file gambar terkonfirmasi disisipkan via \includegraphics.
     [PASS]  Persamaan eq:canal_dist, eq:fwi, eq:target, eq:spatial_cv, eq:shap ditemukan.
     [PASS]  Tabel tab:decadal_sipongi, tab:regency_distribution, tab:model_comparison, tab:shap_ranking ditemukan.
     [PASS]  Sub-bab 4.4 'Study Limitations, Uncertainties, and Threats to Validity' terkonfirmasi ada.
     HASIL VERIFIKASI: 0 Error, 0 Warning. Status: LULUS SEMPURNA.
     ```
   - Exit code: `0`.

2. **Audit Independen Keseimbangan Lingkungan LaTeX (`\begin{...}` vs `\end{...}`)**:
   - Pengujian parsing hierarki AST dilakukan per berkas modular dan dokumen gabungan.
   - Seluruh berkas modular (`00_abstract.tex` hingga `05_conclusions.tex` dan `main.tex`) memiliki pasangan `\begin` dan `\end` seimbang secara lokal (0 unclosed environments).
   - Penghitungan kurung kurawal `{` vs `}`: Open = 788, Close = 788, Selisih = 0.
   - Penghitungan pembatas matematika inline `$`: 340 (genap, 100% berpasangan).

3. **Audit Independen Label dan Referensi Silang (`\label`, `\ref`, `\eqref`)**:
   - Total label unik terdefinisi: 51 label (0 duplikat).
   - Total callout referensi silang aktif: 21 referensi (12 `\ref`, 9 `\eqref`).
   - 100% referensi silang berhasil dipetakan ke label tujuan (0 broken references).
   - 30 label yang tidak memiliki callout teks adalah label struktural bab/subbab (`sec:...`, `subsec:...`, `subsubsec:...`), yang merupakan konvensi baku LaTeX. Seluruh 7 figur ilmiah (`fig:...`), 4 tabel (`tab:...`), dan 10 persamaan (`eq:...`) memiliki referensi aktif di dalam teks.

4. **Audit Independen Bibliografi (`references.bib`) dan Sitasi (`\cite`, `\citep`, `\citet`)**:
   - Berkas `references.bib` memuat tepat 40 entri BibTeX bereputasi tinggi (Nature, PNAS, Nature Geoscience, Remote Sensing of Environment, Science Reports, Ecological Modelling, dll.).
   - Setiap entri BibTeX memiliki kurung kurawal seimbang dan metadata wajib lengkap (`author`, `title`, `year`, `journal`/`booktitle`).
   - Tepat 40 kunci sitasi unik disitir di dalam naskah LaTeX.
   - Korespondensi 100% dua arah: 0 undefined citation keys dan 0 uncited entries di `references.bib`.

5. **Audit Deteksi Residu Sintaks Markdown (`**`, `#`, dll.)**:
   - Pemindaian regex baris demi baris pada seluruh 7 berkas `.tex` menghasilkan:
     - Residu Markdown bold `**`: 0 ditemukan.
     - Residu Markdown heading `#`: 0 ditemukan.
     - Residu Markdown link `[text](url)`: 0 ditemukan.
     - Residu Markdown code block ```` ``` ````: 0 ditemukan.
     - Residu Markdown list bullet `- `: 0 ditemukan.
   - Tidak ada kebocoran sintaks Markdown pada naskah LaTeX.

6. **Audit Konsistensi Angka Empiris (`tests/check_latex_metrics.py`)**:
   - Perintah: `/opt/anaconda3/envs/karhutla_env/bin/python tests/check_latex_metrics.py`
   - Exit code: `0`.
   - 100% angka empiris di dalam teks naskah cocok dengan data kebenaran dasar (`model_metrics.json` dan `eda_summary.json`):
     - Model B Holdout ROC-AUC: 0.7527 | $F_1$-score: 0.3983 | Precision Reguler: 92.1% | Recall Ekstrem: 65.82%.
     - Model B Spatial Block CV: Mean ROC-AUC 0.4950 ($\pm$0.0490) | Mean $F_1$-score 0.1399 (2.4x lebih tinggi dari Model A, positif di 5 fold).
     - Model A Spatial Block CV: Mean ROC-AUC 0.5399 | Mean $F_1$-score 0.0583 (runtuh ke 0.0000 di 4 dari 5 fold).
     - Matriks Konfusi Model B: TP = 1.094, FP = 2.737, FN = 568, TN = 6.586.
     - 12 nilai TreeSHAP feature importance (P_7d 0.0329, d_canal 0.0322, dst.) identik hingga 4 desimal.

7. **Kompilasi Nyata Naskah PDF (`tectonic manuscript/main.tex`)**:
   - Kompilasi dieksekusi menggunakan `/opt/homebrew/bin/tectonic manuscript/main.tex`.
   - Exit code: `0`.
   - Menghasilkan berkas `manuscript/main.pdf` berukuran 2.24 MB (2.135.991 bytes) dengan total panjang 26 halaman terformat rapi sesuai standar publikasi Scopus Q1.

---

## 2. Logic Chain (Rantai Logika Pembuktian)

1. **Berdasarkan Pengamatan 1**: Skrip verifikasi statis resmi proyek `tests/verify_latex.py` lulus 100% tanpa error maupun warning, membuktikan terpenuhinya seluruh kriteria penerimaan otomatis.
2. **Berdasarkan Pengamatan 2**: Tidak ada unclosed environments atau unclosed delimiters (selisih open-close brace = 0, dollar math pairs genap), membuktikan naskah LaTeX memiliki struktur sintaksis yang *well-formed*.
3. **Berdasarkan Pengamatan 3**: Seluruh referensi gambar, tabel, dan persamaan terhubung ke label yang sah tanpa *broken references*, membuktikan integritas cross-referencing naskah.
4. **Berdasarkan Pengamatan 4**: Ke-40 sitasi naskah berkorespondensi 100% secara dwiarah ke 40 entri `references.bib`, membuktikan integritas bibliografi naskah bebas dari *undefined citation keys*.
5. **Berdasarkan Pengamatan 5**: Pemindaian teks membuktikan tidak ada satupun artefak Markdown (`**`, `#`, dll.), memastikan teks telah dikonversi secara bersih dan tuntas ke format LaTeX.
6. **Berdasarkan Pengamatan 6**: Naskah mempertahankan akurasi ilmiah 100% terhadap metrik empiris eksperimen tanpa distorsi atau manipulasi data.
7. **Berdasarkan Pengamatan 7**: Eksekusi kompilasi PDF berhasil menghasilkan dokumen 26 halaman bebas fatal error, membuktikan bahwa naskah siap digunakan secara praktis (*publication-ready*).

---

## 3. Caveats (Batasan & Asumsi)

1. Kompilasi PDF menggunakan compiler Tectonic menghasilkan beberapa peringatan minor bertipe *Overfull/Underfull \hbox* yang merupakan hal lumrah pada tata letak tabel lebar dan teks justified di LaTeX, dan tidak mempengaruhi keterbacaan maupun integritas ilmiah dokumen.
2. Naskah ditargetkan untuk standar artikel Scopus Q1 umum (format artikel modular IMRaD dengan `natbib`). Format spesifik jurnal tertentu (misalnya template khusus MDPI `.cls` atau Elsevier `elsarticle.cls`) dapat diterapkan dengan mudah pada tahap submission akhir tanpa mengubah konten maupun struktur referensi.

---

## 4. Conclusion (Kesimpulan & Vonis Akhir)

**Vonis Akhir: APPROVE**

Naskah publikasi ilmiah LaTeX pada direktori `manuscript/` memenuhi seluruh kriteria kelayakan ilmiah dan integritas teknis untuk Gate Milestone 2:
- Struktur IMRaD modular lengkap dan mendalam (628 baris, 74.030 karakter).
- Sub-bab 4.4 menyajikan evaluasi kritis keterbatasan riset (*spatial memorization*, *class imbalance*, *scale mismatch ERA5*, *sensor smoldering limits*, dan *APL heterogeneity*).
- Seluruh 7 figur ilmiah (300 DPI) terintegrasi dengan caption komprehensif.
- 100% sintaks valid, 0 unclosed environments, 0 broken references, 0 markdown remnants, dan 40 sitasi terverifikasi sempurna.
- Kompilasi PDF 26 halaman (`manuscript/main.pdf`) sukses tanpa galat.

Milestone 2 dinyatakan **LULUS** dan siap dilanjutkan ke Milestone 3.

---

## 5. Verification Method (Metode Verifikasi Ulang)

Untuk mereproduksi dan memvalidasi temuan ini secara mandiri:

1. Jalankan pengujian statis resmi proyek:
   ```bash
   /opt/anaconda3/envs/karhutla_env/bin/python tests/verify_latex.py
   ```
   *Ekspektasi*: Keluar dengan exit code 0 dan pesan `HASIL VERIFIKASI: 0 Error, 0 Warning`.

2. Jalankan pengujian konsistensi metrik empiris:
   ```bash
   /opt/anaconda3/envs/karhutla_env/bin/python tests/check_latex_metrics.py
   ```
   *Ekspektasi*: Keluar dengan exit code 0 dan seluruh metrik status `[PASS]`.

3. Kompilasi naskah menjadi PDF:
   ```bash
   /opt/homebrew/bin/tectonic manuscript/main.tex
   ```
   *Ekspektasi*: Menghasilkan `manuscript/main.pdf` 26 halaman.
