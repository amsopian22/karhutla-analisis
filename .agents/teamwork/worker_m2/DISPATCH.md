## 2026-11-03T03:39:23Z
Anda adalah Worker M2: Publication-Ready LaTeX Manuscript Writer.
Identitas & Lokasi Kerja:
- Working directory Anda: /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/worker_m2
- Baca dokumen wajib: /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/ORIGINAL_REQUEST.md
- Baca arsitektur proyek: /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/PROJECT.md
- Baca cetak biru & laporan peer review: /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/reports/review_report.md
- Baca naskah draf awal: /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/manuscript/manuscript_draft.md
- Baca bibliografi: /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/manuscript/references.bib
- Periksa 7 figur ilmiah di: /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/figures/ (01_ s.d. 07_)

Berkas yang Anda miliki secara eksklusif (Write Ownership):
- /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/manuscript/references.bib
- /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/manuscript/main.tex
- /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/manuscript/sections/ (00_abstract.tex, 01_introduction.tex, 02_materials_methods.tex, 03_results.tex, 04_discussion.tex, 05_conclusions.tex)
- /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/tests/verify_latex.py

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Tugas Utama (R2):
1. Perbarui `manuscript/references.bib`: tambahkan 10 referensi mutakhir (2021–2025) bereputasi tinggi (sebagaimana direkomendasikan pada `review_report.md` Seksi 3.4 & Seksi 6) sehingga totalnya menjadi 40 entri BibTeX valid tanpa merusak 30 entri yang sudah ada.
2. Susun naskah ilmiah lengkap siap publikasi dalam bahasa Inggris akademik format LaTeX standar Scopus Q1 (struktur modular: `main.tex` memanggil `sections/00_abstract.tex` s.d. `05_conclusions.tex`):
   - Gunakan kelas dokumen `article` dengan paket-paket standar: `amsmath, amssymb, graphicx, booktabs, hyperref, natbib, microtype, geometry, caption, subcaption`.
   - Title, Authors, Abstract, Keywords.
   - Section 1: Introduction (termasuk sitasi literatur klasik dan mutakhir 2021-2025).
   - Section 2: Materials and Methods (penjelasan geospasial presisi, dataset satelit FIRMS, kanal eks-PLG dengan koordinat proyeksi UTM 49S EPSG:32749, formula jarak Euclidean Persamaan 1, FWI Persamaan 2, biner target FRP Persamaan 3, Spatial Block CV GroupKFold Persamaan 4, TreeSHAP Persamaan 5, tabel ringkasan dataset).
   - Section 3: Results (integrasi Tabel 1 s.d. Tabel 4 dalam format booktabs, integrasi Figures 1 s.d. 7 secara berurutan dengan caption komprehensif, narasi analitis presisi).
   - Section 4: Discussion (4.1 Peat-drainage nexus, 4.2 Land tenure governance void, 4.3 Spatial ML imperatives, dan SUB-BAB BARU 4.4 "Study Limitations, Uncertainties, and Threats to Validity" yang membedah spatial memorization, class imbalance trade-off, resolusi ERA5, limitasi deteksi peat smoldering tanpa flaming, cakupan temporal krisis, dan Area of Applicability).
   - Section 5: Conclusions and Policy Implications.
3. Integrasikan ke-7 figur ilmiah dari `output/figures/` dengan jalur relatif yang valid (`../output/figures/` atau deklarasi `\graphicspath{{../output/figures/}}`):
   - Figure 1: 01_tren_tahunan_el_nino.png
   - Figure 2: 02_heatmap_musiman_bulan.png
   - Figure 3: 03_peringkat_kabupaten_terparah.png
   - Figure 4: 04_analisis_gambut_dan_kanal.png
   - Figure 5: 05_status_konsesi_esg.png
   - Figure 6: 06_evaluasi_model_ml.png
   - Figure 7: 07_shap_feature_importance.png
   Setiap gambar wajib memiliki callout di teks (`Figure~\ref{fig:...}`).
4. Pastikan 100% kunci sitasi `\cite{...}` cocok dengan kunci di `references.bib` (0 undefined citation keys, 0 missing keys).
5. Buat dan jalankan skrip validator statis `tests/verify_latex.py` (eksekusi via `/opt/anaconda3/envs/karhutla_env/bin/python tests/verify_latex.py`) untuk memverifikasi keseimbangan lingkungan LaTeX (`\begin` vs `\end`), kelengkapan dan keberadaan berkas figur, resolusi seluruh `\label` dan `\ref`, serta validitas seluruh `\cite` ke `references.bib`. Pastikan validator menghasilkan 0 error!
6. Setelah selesai dan pengujian lulus, buat `handoff.md` di direktori kerja Anda dan kirimkan `send_message` ke pemanggil.
