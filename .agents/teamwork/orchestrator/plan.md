# Orchestrator Plan: Evaluasi Ilmiah & Manuskrip LaTeX Karhutla Kalteng

## Tujuan Proyek
1. R1: Evaluasi ilmiah menyeluruh & Peer Review mendalam atas luaran riset karhutla Kalteng (manuscript_draft.md, model_metrics.json, figures 01-07, scripts src/), menghasilkan `output/reports/review_report.md` dalam Bahasa Indonesia berbobot Senior Journal Reviewer.
2. R2: Penyusunan naskah ilmiah lengkap siap publikasi dalam bahasa Inggris akademik format LaTeX standar Scopus Q1 (IMRaD, analisis keterbatasan metodologis tanpa mengubah data empiris, integrasi 7 figur dengan caption komprehensif, sitasi valid ke references.bib, dan verifikasi statis bebas galat).

## Rencana Tahapan (Step-by-Step Verifiable Plan)

### Fase 0: Survey & Scoping (Eksplorasi Paralel)
- [ ] Dispatch 3 Explorer secara paralel:
  - **Explorer 1**: Memeriksa metrik empiris (`output/reports/model_metrics.json`, `eda_summary.json`), kode analisis (`src/train_model.py`, `src/process_real_data.py`, dll.), dan figur ilmiah (`01_` s.d. `07_`).
  - **Explorer 2**: Memeriksa manuskrip draf (`manuscript/manuscript_draft.md`), bibliografi (`manuscript/references.bib`), standar jurnal Scopus Q1 (Remote Sensing / IMRaD), dan pemenuhan struktur LaTeX.
  - **Explorer 3**: Memeriksa metodologi pemodelan spasial (Spatial Block CV, autokorelasi spasial / spatial memorization, ketimpangan kelas / class imbalance) untuk perumusan draf peer review.
- [ ] Sintesis hasil survei ke dalam `PROJECT.md` (Arsitektur, Inventaris Fitur, Milestone, Layout).

### Fase 1: Milestone 1 — Comprehensive Peer Review Report (R1)
- [ ] Worker menyusun `output/reports/review_report.md` dalam Bahasa Indonesia terstruktur:
  - Ringkasan eksekutif & kekuatan riset.
  - Kelemahan metodologis (spatial cross-validation vs random CV, spatial memorization, class imbalance 1:99).
  - Ancaman terhadap validitas internal, eksternal, dan konstruk.
  - Rekomendasi konkret untuk revisi naskah publikasi.
- [ ] Reviewer memeriksa kelengkapan, ketajaman telaah, dan keterpenuhan kriteria Scopus Q1.
- [ ] Challenger menguji konsistensi metrik empiris terhadap laporan review.
- [ ] Forensic Auditor memverifikasi integritas dokumen dan keaslian analisis.
- [ ] Gate evaluation Milestone 1.

### Fase 2: Milestone 2 — Publication-Ready LaTeX Manuscript (R2)
- [ ] Worker menyusun naskah LaTeX (`manuscript/main.tex` atau dokumen modular sesuai standar jurnal Q1):
  - Format LaTeX profesional IMRaD lengkap (Title, Abstract, Introduction, Materials and Methods, Results, Discussion, Conclusion).
  - Pembahasan mendalam keterbatasan metodologis (Spatial CV, autokorelasi spasial, class imbalance) di bagian Discussion tanpa mengubah data empiris riil.
  - Integrasi 7 figur ilmiah (`01_` s.d. `07_`) dengan caption komprehensif.
  - Penautan sitasi yang 100% valid ke `manuscript/references.bib` tanpa broken citation.
- [ ] Reviewer meninjau kualitas akademik bahasa Inggris, kesesuaian struktur IMRaD, dan ketepatan penyajian ilmiah.
- [ ] Challenger menguji kompilasi statis LaTeX, pengecekan broken references, missing figures, dan undefined citation keys.
- [ ] Forensic Auditor memverifikasi bahwa metrik empiris tidak dimanipulasi dan tidak ada plagiasi tanpa atribusi.
- [ ] Gate evaluation Milestone 2.

### Fase 3: Milestone 3 — Final Verification & Audit
- [ ] Verifikasi statis menyeluruh terhadap seluruh artefak.
- [ ] Final gate review dan laporan serah terima ke Sentinel / Parent.
