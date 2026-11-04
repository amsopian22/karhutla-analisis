# Handoff Report — Explorer 2 (Manuscript Draft & Bibliography Explorer)
**Tanggal**: 2026-11-03  
**Pengirim**: Explorer 2 (`explorer_survey_2`)  
**Penerima**: Orchestrator / Caller Agent (`a2eeb2c9-6928-4af1-8dab-de9837521b8d`)  
**Status**: Hard Handoff (Tugas Penyelidikan Selesai 100%)

---

## 1. Observation (Pengamatan Faktual Terverifikasi)

1. **Berkas Naskah Draf (`manuscript/manuscript_draft.md`)**:
   - Berkas berukuran 49.305 bytes, 366 baris, tersusun atas struktur dasar IMRaD:
     - Judul: *"Spatiotemporal Fire Intensity Modeling in Degraded Tropical Peatlands: Addressing Spatial Autocorrelation and Land Tenure Governance in Central Kalimantan"* (Baris 1).
     - Abstract: 310 kata (Baris 10–16).
     - Section 1 (Introduction): Baris 20–41, mencakup 4 paragraf dan 5 kontribusi terukur.
     - Section 2 (Materials and Methods): Baris 43–164. Di baris 55–69 terdapat gambar tata letak regional berupa diagram ASCII art:
       ```
              111°E             112°E             113°E             114°E             115°E
        0° +-----------------------------------------------------------------------------------+
           | [Northern Mineral Highlands: Murung Raya, Gunung Mas, Barito Utara]              |
       ```
     - Section 3 (Results): Baris 166–287, memuat Tabel 1 (SiPongi), Tabel 2 (Kabupaten), Tabel 3 (Model A vs B), dan Tabel 4 (SHAP).
       - Penomoran gambar di teks mengalami disorientasi parah: Baris 170 merujuk `(Table 1 and Figure 2)` untuk tren SiPongi (`01_tren_tahunan_el_nino.png`); Baris 195 merujuk `(Table 2 and Figure 3)` untuk kabupaten (`03_peringkat_kabupaten_terparah.png`); Baris 238 merujuk `(Table 3 and Figure 4)` untuk evaluasi model (`06_evaluasi_model_ml.png`); Baris 264 merujuk `(Table 4 and Figure 5)` untuk TreeSHAP (`07_shap_feature_importance.png`).
       - Gambar riil `02_heatmap_musiman_bulan.png` (distribusi harian), `04_analisis_gambut_dan_kanal.png` (gambut & kanal), dan `05_status_konsesi_esg.png` (status izin) dibahas narasinya di teks tetapi **TIDAK memiliki callout nomor gambar resmi**.
     - Section 4 (Discussion): Baris 289–312, memuat 4.1 (Peat-drainage nexus), 4.2 (Land tenure void), dan 4.3 (Methodological imperatives). **Tidak terdapat sub-bab mengenai keterbatasan studi (*Limitations and Threats to Validity*)**.
     - Section 5 (Conclusions and Policy Implications): Baris 315–330, memuat 4 kesimpulan dan 4 rekomendasi kebijakan.

2. **Bibliografi (`manuscript/references.bib`)**:
   - Berkas berukuran 12.660 bytes, 320 baris, memuat tepat 30 entri BibTeX.
   - Eksekusi audit python memverifikasi bahwa seluruh 30 kunci sitasi di `manuscript_draft.md` cocok 100% dengan entri di `references.bib` (0 hilang, 0 tak terpakai).
   - Analisis tahun terbitan menunjukkan:
     - 1970–1999: 2 entri (6,7%)
     - 2000–2009: 8 entri (26,7%)
     - 2010–2019: 17 entri (56,7%)
     - 2020: 3 entri (10,0%)
     - **2021–2026: 0 entri (0,0%)**. Sama sekali belum memuat literatur 5 tahun terakhir.

3. **Integritas Metrik Empiris (`output/reports/model_metrics.json`)**:
   - Nilai metrik pada naskah draf terkonfirmasi identik dengan data riil eksperimen:
     - Model A (Spatial Memorization): Test ROC-AUC = 0,7956, Test F1 = 0,4512; Spatial CV Mean ROC-AUC = 0,5399, Spatial CV Mean F1 = 0,0583 (Fold 2–5 F1 kolaps ke 0,0000).
     - Model B (Pure Biophysical): Test ROC-AUC = 0,7527, Test F1 = 0,3983; Precision reguler = 92,1%, Recall ekstrem = 65,8%; Spatial CV Mean ROC-AUC = 0,4950, Spatial CV Mean F1 = 0,1399 (2,4x lebih tinggi dari Model A).
     - TreeSHAP ranking teratas: Curah hujan 7h (0,0329), Jarak kanal (0,0322), Angin (0,0254), Dry spell (0,0224), Lanskap eks-PLG (0,0222), Kedalaman gambut (0,0209).

4. **Ketersediaan Perangkat Lunak LaTeX di Sistem**:
   - Perintah `which pdflatex latexmk xelatex bibtex` mengembalikan kode keluar 1 (*not found*). Verifikasi statis naskah LaTeX harus dilakukan melalui validator skrip Python mandiri (`verify_latex.py`) yang memeriksa keseimbangan lingkungan, resolusi referensi silang, penautan gambar, dan integritas BibTeX.

---

## 2. Logic Chain (Rantai Penalaran)

1. **Dari Observasi 1 (Penomoran Gambar Tidak Konsisten & ASCII Art) ke Tindakan Perbaikan**:
   - Diagram ASCII pada Figure 1 tidak dapat diterima dalam publikasi Scopus Q1.
   - Tiga figur utama (`02_`, `04_`, `05_`) telah dihasilkan dan dibahas datanya, namun tidak memiliki callout `\ref{}` atau *caption* resmi.
   - Dua figur lainnya (`06_` dan `07_`) mengalami pergeseran nomor menjadi Gambar 4 dan 5.
   - *Inferensi*: Seluruh 7 figur riil (`output/figures/01_` s.d. `07_`) harus dipetakan secara teratur menjadi Figure 1 hingga Figure 7 di naskah LaTeX dengan *caption* komprehensif yang menjelaskan konteks ilmiahnya.

2. **Dari Observasi 1 (Ketiadaan Sub-bab Keterbatasan) ke Rekomendasi Modifikasi Naskah**:
   - Dalam tinjauan sejawat (*peer review*) jurnal Q1 seperti *Remote Sensing* (MDPI) atau *IJWF*, penolakan paling sering dipicu oleh klaim yang berlebihan tanpa pengakuan atas batasan data sensor dan model.
   - Naskah saat ini hanya memuji keunggulan Model B atas Model A, tanpa mengakui bahwa nilai mutlak F1 pada Spatial CV (0,1399) masih rendah karena ketimpangan kelas yang tajam (15:85) dan keterbatasan resolusi reanalisis ERA5-Land (9 km).
   - *Inferensi*: Wajib disusun sub-bab *"4.4 Study Limitations, Uncertainties, and Threats to Validity"* di bagian Diskusi untuk membedah bias awan/asap satelit, resolusi cuaca, sifat temporal krisis Oktober 2026, dan batas kadaster APL.

3. **Dari Observasi 2 (0% Sitasi 2021–2026) ke Rekomendasi Pembaruan Bibliografi**:
   - Jurnal Q1 mewajibkan naskah berdialog dengan perkembangan ilmiah 3–5 tahun terakhir, khususnya dalam bidang dinamis seperti *spatial machine learning* dan penginderaan jauh gambut.
   - *Inferensi*: `references.bib` perlu diperkaya dengan 10 referensi mutakhir (2021–2025) bereputasi tinggi (*Nature Communications*, *Remote Sensing of Environment*, *Ecological Modelling*, *Land Use Policy*), memperluas bibliografi dari 30 menjadi 40 entri tanpa menghapus entri historis penting.

4. **Dari Observasi 4 (Kompiler LaTeX Lokal Tidak Terpasang) ke Desain Verifikasi Statis**:
   - Ketiadaan biner `pdflatex` di mesin lokal berarti verifikasi kelayakan naskah tidak boleh bergantung pada pembuatan biner PDF lokal.
   - *Inferensi*: Tim harus menerapkan verifikasi statis komprehensif menggunakan Python untuk memastikan sintaks LaTeX valid 100%, semua `\cite{}` terurai di `references.bib`, semua `\ref{}` terhubung ke `\label{}`, dan semua berkas gambar di `\includegraphics{}` benar-benar ada di *disk*.

---

## 3. Caveats (Batasan dan Asumsi)

1. **Asumsi Target Format Jurnal**: Diasumsikan format naskah ditargetkan untuk *Remote Sensing* (MDPI) / format modular standar akademik Q1 yang menggunakan kelas dokumen `article` dengan paket standar AMS, `booktabs`, `natbib`, dan `geometry` 2,5 cm. Ini menjamin portabilitas naskah ke template resmi MDPI atau jurnal penerbit lain (Elsevier, Springer, CSIRO).
2. **Lingkup Analisis Temporal**: Evaluasi empiris satelit berfokus pada episode krisis Oktober 2026 (43.937 titik api) yang diperkuat dengan tren multi-tahun SiPongi KLHK (2018–2026). Naskah tidak mengklaim sebagai panel harian 10 tahun penuh dari satelit, dan batasan ini diakui secara eksplisit pada sub-bab keterbatasan.
3. **Ketiadaan Kompiler LaTeX Lokal**: Verifikasi berkas `.tex` dilakukan secara statis (parsing AST/sintaksis regex Python), bukan eksekusi PDF engine lokal.

---

## 4. Conclusion (Kesimpulan Akhir & Rekomendasi)

1. Draf naskah ilmiah (`manuscript_draft.md`) telah memiliki substansi riset tingkat tinggi yang siap diangkat ke naskah publikasi Scopus Q1.
2. Penataan ulang struktural wajib dilakukan pada:
   - Pemetaan 7 figur riil (`01_` s.d. `07_`) ke dalam Figure 1 hingga Figure 7 dengan caption ilmiah berbobot tinggi.
   - Penambahan sub-bab *"4.4 Study Limitations, Uncertainties, and Threats to Validity"* pada Diskusi.
   - Penambahan 10 referensi mutakhir (2021–2025) ke dalam `references.bib`.
   - Adopsi arsitektur LaTeX modular (`manuscript/main.tex` dan `manuscript/sections/00_` s.d. `05_`).
3. Seluruh temuan, tabel perbandingan, formula matematika, dan matriks peletakan figur telah didokumentasikan secara komprehensif pada `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/explorer_survey_2/analysis.md`.

---

## 5. Verification Method (Metode Verifikasi Independen)

Untuk menguji ulang temuan analisis ini secara independen:

1. **Verifikasi Konsistensi Kunci Sitasi (Draft vs BibTeX)**:
   ```bash
   /opt/anaconda3/envs/karhutla_env/bin/python -c '
   import re
   with open("manuscript/manuscript_draft.md") as f:
       draft_cites = set(re.findall(r"@([A-Za-z0-9_\-]+)", f.read()))
   with open("manuscript/references.bib") as f:
       bib_keys = set(re.findall(r"@\w+\{([^,]+),", f.read()))
   print("Missing in bib:", draft_cites - bib_keys)
   print("Unused in draft:", bib_keys - draft_cites)
   '
   ```
   *Ekspektasi*: Mengembalikan `set()` kosong untuk keduanya (30 entri konsisten sempurna).

2. **Verifikasi Distribusi Tahun Terbitan**:
   ```bash
   /opt/anaconda3/envs/karhutla_env/bin/python -c '
   import re
   with open("manuscript/references.bib") as f:
       years = [int(y) for y in re.findall(r"year\s*=\s*\{?(\d{4})\}?", f.read())]
   print("Years >= 2021:", [y for y in years if y >= 2021])
   '
   ```
   *Ekspektasi*: Mengembalikan `[]` (membuktikan hipotesis bahwa belum ada literatur 2021–2026).

3. **Verifikasi Integritas Metrik Empiris**:
   Periksa kesesuaian nilai ROC-AUC dan F1-Score pada `manuscript_draft.md` baris 240–255 terhadap berkas `output/reports/model_metrics.json`.
