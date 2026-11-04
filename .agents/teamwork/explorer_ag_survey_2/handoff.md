# HANDOFF REPORT: AUDIT TEKSTUAL, BAHASA INGGRIS AKADEMIK, & KESELARASAN TEMATIK *APPLIED GEOGRAPHY*

**Agent:** `explorer_ag_survey_2`  
**Working Directory:** `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/explorer_ag_survey_2/`  
**Recipient / Parent Agent:** `5ded17bc-a3a2-4d64-96ac-1cdeb9993084`  
**Date:** 2026-11-04  
**Type:** Hard Handoff (Investigation & Thematic Audit Complete)  

---

## 1. Observation

Berdasarkan audit langsung berbasis perkakas (*tool-assisted direct inspection*) terhadap seluruh berkas naskah dan data proyek:

1. **Panjang Abstrak Melebihi Batas Ketentuan (Editorial Limit Violation)**:
   - File `manuscript/sections/00_abstract.tex`: Memiliki panjang **384 kata** (setelah ekstraksi sintaks LaTeX), atau **353 kata** pada versi terkompilasi.
   - File `manuscript/manuscript_draft.md`: Memiliki panjang **369 kata**.
   - Ketentuan Elsevier *Applied Geography*: *"Abstract word count must not exceed 250 words"*. Naskah melanggar batas maksimum sebesar +103 hingga +134 kata.
   - Verifikasi perintah Python:
     ```bash
     /opt/anaconda3/envs/karhutla_env/bin/python -c '...'
     # Output: Abstract (tex) word count: 353; Draft (md) word count: 369
     ```

2. **Jumlah Kata Kunci (Keywords) Melebihi Kuota**:
   - File `manuscript/sections/00_abstract.tex` (baris 6): Memuat **10 kata kunci** (*Tropical peatlands; Wildfire modeling; Spatial block cross-validation; Spatial memorization; Random Forest; TreeSHAP; Land tenure governance; Mega Rice Project; Fire Radiative Power; Central Kalimantan*).
   - File `manuscript/manuscript_draft.md` (baris 21): Memuat **9 kata kunci**.
   - Ketentuan *Applied Geography*: Membatasi kata kunci antara **1 hingga 7 kata kunci** (*Provide between 1 and 7 keywords*).

3. **Inkonsistensi Header Target Jurnal pada Draf Markdown**:
   - File `manuscript/manuscript_draft.md` (baris 10): Masih tertulis:  
     `**Target Journal:** *Remote Sensing of Environment* / *International Journal of Wildland Fire* / *MDPI Remote Sensing*`.  
     Belum diperbarui ke *Applied Geography*.

4. **Inkonsistensi Jumlah Titik Api Ekstrem ($n$)**:
   - File `manuscript/manuscript_draft.md` (baris 128): Tertulis `severe fires represented 15.1% of all detections ($n = 6,634$)`.
   - File `manuscript/sections/02_materials_methods.tex` (baris 163): Tertulis `6,648 detections (15.13%)`.
   - Data riil pada `data/processed/karhutla_kalteng_real_2026.csv`: `(df["frp_mw"] >= 12.0).sum() == 6648`. Angka pada markdown draft merupakan data lama sebelum sinkronisasi.

5. **Penomoran Gambar Ganda pada Draf Markdown**:
   - File `manuscript/manuscript_draft.md`: Baris 217 memberi judul `Figure 4` untuk peta tenurial, tetapi baris 240 merujuk `Figure 4` untuk evaluasi model ML. Baris 233 memberi judul `Figure 5` untuk citra kanal, tetapi baris 269 merujuk `Figure 5` untuk TreeSHAP.

6. **Highlights Memenuhi Syarat Panjang Karakter**:
   - File `manuscript/highlights.md`: 5 butir dengan panjang karakter: 76, 80, 75, 76, dan 77 karakter (seluruhnya $\le 85$ karakter termasuk spasi).

7. **Kompilasi LaTeX Tersedia melalui Tectonic**:
   - Kompiler LaTeX `tectonic` terinstal pada `/opt/homebrew/bin/tectonic`. Berkas `manuscript/main.pdf` berukuran 11,1 MB berhasil dikompilasi sebelumnya.

---

## 2. Logic Chain

1. **Dari Observasi 1 (Abstrak 384/369 kata vs batas 250 kata)**:  
   Jika artikel disubmit dengan abstrak melebihi 250 kata, sistem editorial Elsevier akan otomatis mengembalikan manuskrip (*unsubmit/desk rejection*) pada tahap *technical screening*. Oleh karena itu, abstrak wajib dipadatkan menjadi $\le 250$ kata (telah disusun usulan versi 246 kata) yang tetap mempertahankan seluruh metrik kuantitatif utama (43.937 titik api, 75,4% APL, Model A vs B Spatial CV, ambang batas TreeSHAP).

2. **Dari Observasi 2 (10 kata kunci vs batas 1--7)**:  
   Pedoman *Applied Geography* menetapkan batas 1--7 kata kunci. Mengurangi jumlah kata kunci menjadi tepat 7 istilah geografi spasial yang kuat (*Applied spatial geography; Tropical peatlands; Spatial autocorrelation; Spatial block cross-validation; Land tenure governance; Wildfire intensity modeling; Mega Rice Project*) menjamin kepatuhan editorial dan meningkatkan visibilitas pengindeksan (*indexing discoverability*).

3. **Dari Penolakan Awal di *Ecological Modelling***:  
   *Ecological Modelling* menolak manuskrip karena fokus jurnal tersebut adalah simulasi biologi/ekologi matematis mekanistik. Manuskrip ini adalah studi geografi spasial terapan, sains informasi geografis (GIScience), dan tata kelola tenurial lahan. Maka, seluruh bagian pendahuluan, metode, pembahasan, dan kesimpulan harus menggeser penekanan dari "uji coba algoritma machine learning biasa" menjadi "solusi geografi spasial terhadap Hukum Pertama Tobler dan mitigasi kebakaran pada tata ruang APL".

4. **Dari Observasi 3, 4, dan 5 (Inkonsistensi internal antar-berkas)**:  
   Perbedaan angka antara markdown ($n=6.634$) dan LaTeX ($n=6.648$), target jurnal lama pada header markdown, dan tabrakan penomoran gambar menandakan bahwa berkas markdown belum tersinkronisasi penuh dengan naskah LaTeX. Implementer berikutnya harus menyinkronkan seluruh draf markdown agar paket submisi konsisten secara sempurna.

---

## 3. Caveats

1. **Keterbatasan Peran Read-Only**: Sesuai mandat peran explorer, agen ini tidak melakukan modifikasi langsung pada berkas kode maupun manuskrip utama. Seluruh teks usulan perbaikan disajikan secara lengkap dan siap pakai di dalam `analysis.md`.
2. **Kompilasi DOCX**: Agen ini mengidentifikasi bahwa berkas Word di `manuscript/submission_package/` dikonversi melalui pandoc/docx generator. Implementer wajib mengompilasi ulang berkas `.docx` setelah draf markdown dan LaTeX diperbarui.
3. **Penyelidikan Heterogenitas Internal APL**: Analisis ini mengelompokkan 75,42% titik api sebagai APL secara legal agraria. Data turunan untuk membedakan secara pasti antara tanah adat, transmigrasi, dan kebun swadaya di dalam APL memerlukan pemetaan partisipatif tingkat desa yang berada di luar cakupan data satelit provinsi saat ini.

---

## 4. Conclusion

1. **Status Manuskrip**: Manuskrip memiliki kualitas substansi ilmiah, analisis spasial, dan data empiris yang sangat tinggi (43.937 titik api riil, model Machine Learning tanpa koordinat yang terkalibrasi, interpretasi TreeSHAP autentik, dan analisis tenurial 812 poligon konsesi).
2. **Hambatan Utama Submisi**: Hambatan tersisa bersifat prosedural dan redaksional:
   - Abstrak kepanjangan (384 kata $\to$ harus $\le 250$ kata).
   - Kata kunci terlalu banyak (10 $\to$ harus $\le 7$).
   - Inkonsistensi minor pada berkas `manuscript_draft.md`.
   - Diperlukannya penajaman diksi geografi spasial (Hukum Tobler, transferabilitas spasial, ruang hampa tata kelola APL) di Pendahuluan, Pembahasan, dan Surat Pengantar.
3. **Dokumentasi Lengkap**: Analisis komprehensif bagian demi bagian dan usulan teks pengganti konkret telah didokumentasikan di:  
   `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/explorer_ag_survey_2/analysis.md`

---

## 5. Verification Method

Implementer atau agen pemeriksa independen dapat memverifikasi temuan ini dengan menjalankan:

1. **Verifikasi Jumlah Kata Abstrak**:
   ```bash
   /opt/anaconda3/envs/karhutla_env/bin/python -c '
   with open("manuscript/sections/00_abstract.tex") as f:
       text = f.read()
   import re
   body = text.split(r"\begin{abstract}")[1].split(r"\textbf{Keywords:}")[0]
   words = [w for w in re.sub(r"\\[a-zA-Z]+|[^a-zA-Z0-9\s-]", " ", body).split() if w]
   print("Current Abstract Words:", len(words))
   '
   # Menghasilkan ~384 kata (kondisi saat ini) vs batas 250 kata.
   ```

2. **Verifikasi Jumlah Titik Api Ekstrem Data Riil**:
   ```bash
   /opt/anaconda3/envs/karhutla_env/bin/python -c '
   import pandas as pd
   df = pd.read_csv("data/processed/karhutla_kalteng_real_2026.csv")
   print("Total rows:", len(df))
   print("Severe fires (frp_mw >= 12.0):", (df["frp_mw"] >= 12.0).sum())
   '
   # Verifikasi bahwa total = 43.937 dan severe fires = 6.648.
   ```

3. **Verifikasi Kompiler Tectonic**:
   ```bash
   /opt/homebrew/bin/tectonic --version
   ```

4. **Kondisi Invalidasi (Invalidation Conditions)**:
   - Jika *Applied Geography* secara resmi mengizinkan abstrak $> 250$ kata atau kata kunci $> 7$ (faktanya: pedoman *Guide for Authors* melarangnya).
   - Jika data mentah `karhutla_kalteng_real_2026.csv` menunjukkan angka titik api ekstrem selain 6.648.
