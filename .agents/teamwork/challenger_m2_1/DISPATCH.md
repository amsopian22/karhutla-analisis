## 2026-11-03T03:48:36Z
Anda adalah Challenger 1 untuk Milestone 2 (Naskah Publikasi LaTeX Scopus Q1).
Identitas & Lokasi Kerja:
- Working directory Anda: /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/challenger_m2_1
- Baca dokumen wajib: /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/ORIGINAL_REQUEST.md
- Baca arsitektur proyek: /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/PROJECT.md
- Berkas yang diuji: manuscript/main.tex, manuscript/sections/, manuscript/references.bib, dan tests/verify_latex.py

Tugas Pengujian:
1. Jalankan pengujian statis mandiri menggunakan Python di conda karhutla_env:
   /opt/anaconda3/envs/karhutla_env/bin/python tests/verify_latex.py
2. Lakukan audit pengujian independen tambahan:
   - Apakah ada unclosed LaTeX environments (\begin{...} tanpa \end{...})?
   - Apakah seluruh label gambar (fig:...), tabel (tab:...), dan persamaan (eq:...) ada dan terujuk (\ref{...}) tanpa broken references?
   - Apakah semua berkas gambar yang dirujuk ada di disk (output/figures/01_ s.d. 07_)?
   - Apakah ada sitasi \cite{...} yang undefined di manuscript/references.bib?
   - Apakah ada syntax error pada berkas BibTeX?
3. Tentukan vonis akhir (APPROVE atau REQUEST_CHANGES).
4. Tulis handoff.md di working directory Anda dan kirimkan send_message ke pemanggil.
