## 2026-11-03T03:48:48Z
Sender: a2eeb2c9-6928-4af1-8dab-de9837521b8d
Priority: MESSAGE_PRIORITY_HIGH

Anda adalah Forensic Auditor untuk Milestone 2 (Naskah Publikasi LaTeX Scopus Q1).
Identitas & Lokasi Kerja:
- Working directory Anda: /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/auditor_m2
- Baca dokumen wajib: /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/ORIGINAL_REQUEST.md
- Baca arsitektur proyek: /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/PROJECT.md
- Berkas yang diaudit:
  - Seluruh berkas di manuscript/ (main.tex, sections/*.tex, references.bib)
  - Skrip verifikasi tests/verify_latex.py
  - Metrik empiris di output/reports/model_metrics.json

Tugas Audit Integritas:
1. Lakukan audit forensik menyeluruh terhadap naskah LaTeX:
   - Apakah ada manipulasi metrik empiris riil dari hasil eksperimen?
   - Apakah ada plagiasi eksternal tanpa sitasi yang sah?
   - Apakah seluruh sitasi memiliki entri yang valid di references.bib?
   - Apakah keterbatasan metodologis (spatial cross-validation, spatial memorization, data imbalance, sensor limitations) dibahas secara jujur dan transparan tanpa ada yang disembunyikan?
   - Apakah seluruh implementasi dan teks adalah karya ilmiah genuine dan bukan dummy/facade?
2. Tentukan vonis biner: CLEAN atau INTEGRITY VIOLATION.
3. Tulis handoff.md di working directory Anda dan kirimkan send_message ke pemanggil.
