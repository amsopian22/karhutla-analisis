# Handoff Report — reviewer_ag_1

**Milestone**: Manuscript Peer Review & Verification for Elsevier *Applied Geography*  
**Date**: 2026-11-04  
**Verdict**: **APPROVE**  

---

## 1. Observation

Berdasarkan investigasi langsung dan eksekusi alat mandiri, berikut adalah observasi faktual yang tercatat:

1. **Pedoman Editorial & Batasan Formal (Word & Character Counts)**:
   - File `manuscript/sections/00_abstract.tex`: Teks abstrak di antara `\begin{abstract}` dan `\textbf{Keywords:}` diekstrak dan dihitung kata menggunakan skrip `tests/test_abstract_word_count.py` dan uji manual Python: tepat **241 kata** ($\le 250$ kata).
   - File `manuscript/manuscript_draft.md`: Bagian abstrak diekstrak: tepat **241 kata** ($\le 250$ kata).
   - File `manuscript/submission_package/manuscript_main.docx` dan `manuscript/main.pdf`: Paragraf abstrak diekstrak via OpenXML parser dan `pdftotext`: tepat **241 kata**.
   - File `manuscript/highlights.md`: Terdiri dari tepat 5 butir dengan panjang karakter:
     - Butir 1: 74 karakter
     - Butir 2: 76 karakter
     - Butir 3: 75 karakter
     - Butir 4: 78 karakter
     - Butir 5: 79 karakter  
     Semua butir berada dalam rentang 3–5 butir dan masing-masing $\le 85$ karakter termasuk spasi.
   - Kata Kunci (`manuscript/sections/00_abstract.tex` baris 6): Tepat 7 kata kunci spesifik: *"Applied spatial geography; Tropical peatlands; Spatial autocorrelation; Spatial block cross-validation; Land tenure governance; Wildfire intensity modeling; Mega Rice Project."*

2. **Eksekusi Test Suite Proyek**:
   - Perintah: `/opt/anaconda3/envs/karhutla_env/bin/pytest -v tests/`
   - Hasil: `25 passed in 46.90s` (100% kelulusan mencakup validasi kata abstrak, panjang karakter highlights, keselarasan kata kunci, konsistensi pemanggilan gambar/tabel, kompilasi Tectonic PDF 28 halaman, struktur tabel Word DOCX, persamaan OMML, dan verifikasi SHA-256 gambar tersemat).

3. **Verifikasi Empiris & Ketiadaan Pelanggaran Integritas**:
   - Perintah: `/opt/anaconda3/envs/karhutla_env/bin/python tests/test_empirical_metrics.py` dan `tests/test_challenger_m2_re_2.py`
   - Hasil: Berjalan sukses dengan kode keluar 0.
   - Dataset master `data/processed/karhutla_kalteng_2019_2026.csv` berisi tepat 43.937 baris setelah kliping 8.892 titik luar batas (16,83%) dari 52.829 data mentah NASA FIRMS.
   - Metrik evaluasi Model B: Holdout ROC-AUC = 0.7527, F1-Score = 0.3983, Precision Reguler = 92.06%, Recall Ekstrem = 65.82%, TN = 6.586, FP = 2.737, FN = 568, TP = 1.094.
   - Evaluasi Spatial Block CV: Model B menghasilkan rata-rata F1-score = 0.1399 vs Model A = 0.0583 (keunggulan retensi 2,4 kali lipat di mana Model A ambruk ke F1 = 0,0000 di 4 dari 5 fold spasial).
   - Data status tenurial: 75,42% (33.138 titik) berada di Non-Konsesi (APL), 16,56% di HGU Sawit, dan 8,02% di PBPH Kehutanan.

4. **Kompilasi dan Perenderan Aset Submisi**:
   - `manuscript/main.pdf`: Dokumen 28 halaman berhasil dikompilasi oleh Tectonic tanpa galat, ukuran 11,1 MB, dengan seluruh metadata Title, Author, dan Subject tercatat sempurna.
   - `manuscript/submission_package/manuscript_main.docx`: Berukuran 11,9 MB, berisi 4 tabel asli (`<w:tbl>`), tanpa sisa pipa markdown (`| --- |`), berisi rumus matematika OMML (`<m:oMath>`), dan 7 gambar 300 DPI dengan hash SHA-256 identik dengan master gambar di `output/figures/`.

5. **Cover Letter & Penyelarasan Skop**:
   - `manuscript/cover_letter.md`: Menyatakan keterbukaan editorial atas *desk rejection* sebelumnya dari *Ecological Modelling*, menegaskan fokus riset pada Geografi Spasial Terapan dan GIScience (Hukum Pertama Tobler, mitigasi autokorelasi spasial, mitigasi kebocoran data spasial, analisis kadaster APL vs konsesi, dan simulasi dispersi Monsun regional), serta memuat deklarasi etika dan orisinalitas lengkap.

---

## 2. Logic Chain

1. **Premis 1 (Kepatuhan Formal Elsevier)**: Elsevier *Applied Geography* mensyaratkan abstrak $\le 250$ kata, highlights 3–5 butir ($\le 85$ karakter/butir), kata kunci 1–7 butir, serta pernyataan CRediT, ketersediaan data, dan deklarasi benturan kepentingan.
   - *Bukti (Observasi 1)*: Abstrak 241 kata, highlights 5 butir (74–79 karakter), kata kunci 7 butir, dan seluruh bagian deklarasi lengkap dan tersinkronisasi lintas LaTeX, Markdown, PDF, dan DOCX.
2. **Premis 2 (Kesesuaian Aims & Scope)**: Naskah sebelumnya ditolak *Ecological Modelling* karena tidak memodelkan dinamika biologis metabolik. Jurnal target baru (*Applied Geography*) berfokus pada penerapan spasial geografis, pemodelan spasial, analisis bahaya wilayah, dan tata kelola sumber daya.
   - *Bukti (Observasi 5 & Naskah)*: Seluruh bab (Pendahuluan hingga Pembahasan) secara eksplisit berakar pada Hukum Pertama Tobler, membandingkan Model A (hafalan koordinat) vs Model B (biofisik tergeneralisasi) melalui *Spatial Block Cross-Validation*, membedah jarak metrik UTM 49S terhadap jaringan kanal eks-PLG, serta mengurai keterkaitan spasial tenurial APL 75,4% vs konsesi.
3. **Premis 3 (Integritas Ilmiah & Komputasional)**: Sesuai mandat auditor dan peninjau adversarial, tidak boleh ada angka tiruan, hasil hardcoded, atau fa\c{c}ade implementation.
   - *Bukti (Observasi 2 & 3)*: Seluruh 25 pengujian pytest lulus, dan pengujian empiris mereproduksi persis seluruh metrik dari model Random Forest terlatih dan dataset master 43.937 titik api. Tidak ada pelanggaran integritas.
4. **Kesimpulan Deduktif**: Karena seluruh persyaratan formal, substantif, etis, dan teknis terpenuhi secara objektif dan terverifikasi 100%, naskah dinilai layak untuk disetujui (*APPROVE*).

---

## 3. Caveats

- **Ruang Lingkup Validitas Sensor**: Pengamatan FIRMS merepresentasikan radiasi termal permukaan (*surface flaming*) pada jam lintasan satelit polar tertentu; pembakaran membara (*smoldering*) di kedalaman gambut tropis yang terisolasi kanopi memiliki radiasi termal tereduksi, sebagaimana diakui secara transparan dalam Bab 4.4.1.
- **Skala Grid Reanalisis Meteorologis**: Data cuaca ERA5-Land ($0.1^\circ \approx 9$ km) diagregasi harian pada tingkat centroid kabupaten, sehingga badai konvektif lokal skala mikro tidak terresolusi secara eksplisit (dibahas di Bab 4.4.2).
- **Asumsi Non-Konsesi (APL)**: Klasifikasi APL 75,4% merupakan kategori hukum formal kadaster agregat yang di lapangannya mencakup mosaik tanah adat, transmigrasi, petani swadaya, dan gambut terdegradasi tanpa pengelola (dibahas di Bab 4.4.5).
- Di luar poin-poin ilmiah di atas yang telah diuraikan dalam naskah, tidak ada celah kepatuhan administratif atau editorial yang belum diinvestigasi.

---

## 4. Conclusion

Paket submisi manuskrip untuk Elsevier *Applied Geography* memenuhi seluruh kriteria kelayakan ilmiah, keselarasan skop, standar kepatuhan pedoman pengarang, dan integritas data secara sempurna.

**Keputusan Akhir: APPROVE**

---

## 5. Verification Method

Untuk mereproduksi dan memverifikasi laporan ini secara independen:

1. **Jalankan Test Suite Utama**:
   ```bash
   conda activate karhutla_env
   pytest -v tests/
   ```
   *Ekspektasi*: 25 pengujian lulus (100% passed).

2. **Jalankan Uji Empiris & Integritas Metrik**:
   ```bash
   /opt/anaconda3/envs/karhutla_env/bin/python tests/test_empirical_metrics.py
   /opt/anaconda3/envs/karhutla_env/bin/python tests/test_challenger_m2_re_2.py
   /opt/anaconda3/envs/karhutla_env/bin/python tests/audit_review_report_numbers.py
   ```
   *Ekspektasi*: Kode keluar 0, seluruh metrik dan pembagian spasial cocok 100% dengan ground truth.

3. **Periksa Berkas Submisi**:
   - Inspeksi visual `manuscript/main.pdf` (28 halaman)
   - Inspeksi struktur `manuscript/submission_package/manuscript_main.docx`
   - Verifikasi karakter `manuscript/highlights.md` dan kata `manuscript/sections/00_abstract.tex`.
