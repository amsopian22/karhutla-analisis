# Forensic Audit Report: Milestone 2 (Naskah Publikasi LaTeX Scopus Q1)

**Work Product**: `manuscript/` (`main.tex`, `sections/*.tex`, `references.bib`), `tests/verify_latex.py`, `output/reports/model_metrics.json`  
**Profile**: General Project (Integrity Mode: Demo)  
**Auditor**: Forensic Auditor (Milestone 2)  
**Verdict**: **INTEGRITY VIOLATION** (Pekerjaan Ditolak Sementara untuk Sinkronisasi Metrik Empiris)

---

## 1. Observation (Observasi Langsung)

Berikut adalah temuan langsung berbasis eksekusi alat, pembacaan berkas sumber kebenaran (*ground truth*), dan verifikasi komputasi mandiri:

### Observasi 1.1: Hasil Validasi Statis Sintaks LaTeX (`tests/verify_latex.py`)
- Perintah eksekusi: `/opt/anaconda3/envs/karhutla_env/bin/python tests/verify_latex.py`
- Hasil: Exit code 0, 0 Error, 0 Warning.
- Verifikasi lingkungan: Lingkungan `\begin{...}` dan `\end{...}` 100% seimbang (0 mismatch).
- Verifikasi sitasi: 40 entri BibTeX di `references.bib` terdefinisi penuh, dan seluruh 40 kunci disitir secara aktif di naskah (0 undefined citation keys).
- Verifikasi referensi silang: 51 label unik terdefinisi, seluruh 12 `\ref{...}` terselesaikan sempurna ke `\label{...}`.
- Verifikasi berkas figur: Seluruh 7 figur ilmiah (`01_` s.d. `07_`) ada di disk dan disisipkan dengan perintah `\includegraphics`.
- Verifikasi persamaan dan tabel: Persamaan 1--5, Tabel 1--4, serta Sub-bab 4.4 terdeteksi lengkap.

### Observasi 1.2: Verifikasi Metrik Model Pembelajaran Mesin (Model B vs Model A)
Membandingkan nilai di `manuscript/sections/03_results.tex` (Tabel 3 dan Tabel 4) terhadap sumber kebenaran `output/reports/model_metrics.json`:
- **Model B (Holdout Test)**:
  - ROC-AUC: `0.7527` (Tabel 3 baris 150) vs `0.7527` (`model_metrics.json` baris 18) $\rightarrow$ **IDENTIK**.
  - $F_1$-Score: `0.3983` (Tabel 3 baris 151) vs `0.3983` (`model_metrics.json` baris 19) $\rightarrow$ **IDENTIK**.
  - Precision Reguler: `92.1%` (Tabel 3 baris 152) vs `0.9206` (`model_metrics.json` baris 20) $\rightarrow$ **IDENTIK**.
  - Recall Ekstrem: `65.82%` (Tabel 3 baris 153) vs `0.6582` (`model_metrics.json` baris 21) $\rightarrow$ **IDENTIK**.
  - Matriks Konfusi ($n=10.985$): $\text{TN}=6.586, \text{FP}=2.737, \text{FN}=568, \text{TP}=1.094$ (baris 171) $\rightarrow$ **IDENTIK**.
- **Model B (Spatial Block Cross-Validation)**:
  - Mean ROC-AUC: `0.4950` ($\pm$0.0490) (Tabel 3 baris 155) vs `0.495` / `0.049` (`model_metrics.json` baris 22-23) $\rightarrow$ **IDENTIK**.
  - Mean $F_1$-Score: `0.1399` (Tabel 3 baris 156) vs `0.1399` (`model_metrics.json` baris 24) $\rightarrow$ **IDENTIK**.
  - Folds 1 s.d. 5 AUC & $F_1$: Seruyan (AUC 0.5827, $F_1$ 0.2914), Fold 2 (AUC 0.5041, $F_1$ 0.0657), Fold 3 (AUC 0.4900, $F_1$ 0.1056), Fold 4 (AUC 0.4452, $F_1$ 0.0646), Fold 5 (AUC 0.4533, $F_1$ 0.1722) (Tabel 3 baris 159-163) $\rightarrow$ **IDENTIK**.
- **Model A (Baseline Hafalan Spasial)**:
  - Holdout ROC-AUC: `0.7956`, $F_1$: `0.4512` $\rightarrow$ **IDENTIK**.
  - Spatial Block CV Mean ROC-AUC: `0.5399` ($\pm$0.0531), Mean $F_1$: `0.0583` $\rightarrow$ **IDENTIK**.
  - Spatial Block CV Folds 2, 3, 4, 5: $F_1 = 0.0000$ di 4 fold $\rightarrow$ **IDENTIK**.
- **TreeSHAP Rankings (Tabel 4)**:
  - Seluruh 12 fitur (Curah hujan 7H: 0.0329, Jarak kanal: 0.0322, Angin: 0.0254, Dry spell: 0.0224, Eks-PLG: 0.0222, Kedalaman gambut: 0.0209, Suhu maks: 0.0203, Kelembapan: 0.0173, Tipe tanah: 0.0171, FWI: 0.0170, Status konsesi: 0.0094, Tutupan lahan: 0.0094) cocok 100% dengan `model_metrics.json` baris 181-241 $\rightarrow$ **IDENTIK**.

### Observasi 1.3: Verifikasi Status Tenurial, Biofisik Gambut, dan Historis SiPongi
- **Status Tenurial Konsesi**:
  - Non-Konsesi (APL): 33.138 titik (75,42%)
  - Sawit (HGU): 7.276 titik (16,56%)
  - Kehutanan (PBPH): 3.523 titik (8,02%)
  - Entitas korporasi teratas: PT Rimba Makmur Utama (964), PT Sangkowong Sinta (954), PT Nusantara Raya Solusi (522), PT Graha Inti Jaya (472), PT Bulau Sawit Bajenta (343)
  - Hasil audit: Seluruhnya cocok persis dengan eksekusi spatial join di dataset master.
- **Stratifikasi Kedalaman Gambut**:
  - Gambut Dalam (200--300 cm): 12.888 (29,33%)
  - Tanah Mineral: 11.294 (25,70%)
  - Gambut Sangat Dalam (>300 cm): 10.197 (23,21%)
  - Gambut Sedang (100--200 cm): 9.177 (20,89%)
  - Gambut Dangkal (50--100 cm): 381 (0.87%)
  - Hasil audit: Cocok 100% dengan `df['tipe_lahan'].value_counts()`.
- **Historis SiPongi (Tabel 1)**:
  - 2018 (47.432,57 ha), 2019 (317.749,00 ha), 2020 (7.681,00 ha), 2021 (3.653,00 ha), 2022 (1.554,00 ha), 2023 (165.896,44 ha), 2024 (11.459,89 ha), 2025 (4.803,97 ha), 2026 (7.634,46 ha).
  - Hasil audit: Cocok 100% dengan `data/raw/sipongi_luas_karhutla_kalteng_2018_2026.csv`.

---

### Observasi 1.4: [PELANGGARAN FORENSIK 1] Inkonsistensi Empiris dan Kontradiksi pada Tabel 2 (`03_results.tex`) vs Gambar 03 & Dataset Riil
Pada berkas `manuscript/sections/03_results.tex` baris 63--79 (Tabel 2), disajikan sebaran titik api per kabupaten/kota. Ketika diaudit silang terhadap dataset riil `data/processed/karhutla_kalteng_2019_2026.csv` dan grafik infografis Gambar 03 (`output/figures/03_peringkat_kabupaten_terparah.png`), ditemukan deviasi angka yang sangat masif pada 6 kabupaten:

| Kabupaten / Kota | Dilaporkan di Tabel 2 (Naskah) | Data Faktual Dataset Master (`karhutla_kalteng_2019_2026.csv`) | Angka di Gambar 03 (`03_peringkat_kabupaten_terparah.png`) | Selisih Titik (Tabel 2 vs Riil) | Status Audit |
|---|:---:|:---:|:---:|:---:|:---:|
| **Seruyan** | 9.356 (21,29%) | 9.356 (21,29%) | 9.356 (21,3%) | 0 | PASS |
| **Pulang Pisau** | 7.143 (16,26%) | 7.143 (16,26%) | 7.143 (16,3%) | 0 | PASS |
| **Kapuas** | 6.314 (14,37%) | 6.314 (14,37%) | 6.314 (14,4%) | 0 | PASS |
| **Katingan** | **5.108 (11,63%) [Rank 5]** | **6.106 (13,90%) [Rank 4]** | **6.106 (13,9%) [Rank 4]** | **-998 titik** | **VIOLATION** |
| **Kotawaringin Timur** | **5.821 (13,25%) [Rank 4]** | **4.627 (10,53%) [Rank 5]** | **4.627 (10,5%) [Rank 5]** | **+1.194 titik** | **VIOLATION** |
| **Kotawaringin Barat** | **4.219 (9,60%)** | **4.256 (9,69%)** | **4.256 (9,7%)** | **-37 titik** | **VIOLATION** |
| **Kota Palangka Raya** | **1.488 (3,39%) [Rank 8]** | **3.188 (7,26%) [Rank 7]** | **3.188 (7,3%) [Rank 7]** | **-1.700 titik** | **VIOLATION** |
| **Barito Selatan** | **2.894 (6,59%) [Rank 7]** | **992 (2,26%) [Rank 8]** | **992 (2,3%) [Rank 8]** | **+1.902 titik** | **VIOLATION** |
| **Other 6 Regencies** | **1.594 (3,63%)** | **1.955 (4,45%)** | *(Lamandau: 773, Sukamara: 481, Gumas: 407, Bartim: 227, Mura: 44, Barut: 23)* | **-361 titik** | **VIOLATION** |
| **Total** | **43.937 (100,00%)** | **43.937 (100,00%)** | *(Total Kliping Resmi Kalteng)* | **0** | **Total cocok, rincian manipulatif/salah** |

**Bukti Forensik**:
- Pada Tabel 2 naskah, urutan peringkat kabupaten ke-4 dan ke-5 tertukar (Kotim ditaruh di peringkat 4 dengan 5.821, Katingan di peringkat 5 dengan 5.108). Padahal di Gambar 03 dan data riil, Katingan adalah peringkat 4 dengan 6.106 titik (13,9%) dan Kotim adalah peringkat 5 dengan 4.627 titik (10,5%).
- Barito Selatan dilaporkan 2.894 titik (meledak hampir 3x lipat dari kenyataan 992 titik), sementara Kota Palangka Raya dilaporkan hanya 1.488 titik (terpangkas lebih dari separuh dari kenyataan 3.188 titik).
- Teks naratif naskah mengutip Gambar 3 (`\ref{fig:regency_ranking}`), namun isi Tabel 2 bertentangan secara telanjang dengan angka visual batang yang tertera di Gambar 3 itu sendiri.

---

### Observasi 1.5: [PELANGGARAN FORENSIK 2] Penggunaan Angka Bounding Box Mentah pada Teks Bagian 3.1 & Keterangan Gambar 02
Pada berkas `manuscript/sections/03_results.tex` baris 46--52, tertulis narasi dinamika harian:
> Baris 47: *"Thermal anomalies peaked sharply on 7--8 October (18,628 hotspots; 42.4% of total detections)..."*
> Baris 51: *"the four-day window between 5 October and 8 October accounted for 33,942 hotspots (77.2% of provincial detections). The crisis peaked on 7 October with 9,859 hotspots and 8 October with 8,769 hotspots... reducing detections to 3,128 on 9 October and 2,712 by 12 October."*

Ketika diverifikasi terhadap data mentah `data/raw/firms_real_kalteng_latest_7d.csv` ($n = 52.829$) vs data master terkliping Kalteng `data/processed/karhutla_kalteng_2019_2026.csv` ($n = 43.937$) dan visualisasi Gambar 02 (`02_heatmap_musiman_bulan.png`):

| Parameter Harian | Dilaporkan pada Teks Naskah | Data Faktual Mentah Bounding Box (`firms_real_...csv`, $n=52.829$) | Data Faktual Terkliping Kalteng (`karhutla_kalteng_...csv`, $n=43.937$) | Angka pada Gambar 02 (`02_heatmap_musiman_bulan.png`) | Status Audit |
|---|:---:|:---:|:---:|:---:|:---:|
| Puncak 7 Oktober | 9.859 | 9.859 | **8.290** | **~8.290** | **VIOLATION (Teks pakai data mentah luar Kalteng)** |
| Puncak 8 Oktober | 8.769 | 8.769 | **7.377** | **~7.377** | **VIOLATION (Teks pakai data mentah luar Kalteng)** |
| Total 7--8 Oktober | 18.628 (42,4%) | 18.628 | **15.667 (35,66%)** | **15.667** | **VIOLATION (Numerator mentah dibagi total kliping)** |
| Total 5--8 Oktober | 33.942 (77,2%) | 33.942 | **28.387 (64,61%)** | **28.387** | **VIOLATION (Numerator mentah dibagi total kliping)** |
| Penurunan 9 Oktober | 3.128 | 3.128 | **2.366** | **~2.366** | **VIOLATION** |
| Akhir 12 Oktober | 2.712 | 2.712 | **2.084** | **~2.084** | **VIOLATION** |

**Bukti Forensik**:
Grafik batang di Gambar 02 memplot data riil terkliping Kalteng dengan benar (total 43.937; puncak 7 Okt = 8.290, 8 Okt = 7.377). Namun narasi teks naskah dan caption Gambar 02 menyalin teks mentah dari `manuscript_draft.md` yang menggunakan angka *unclipped bounding box* (termasuk titik api di Kalsel dan Kalbar). Akibatnya, narasi teks dan grafik di Gambar 02 saling bertentangan secara frontal.

---

## 2. Logic Chain (Rantai Logika Pembuktian)

1. **Premis Mandat Utama (`ORIGINAL_REQUEST.md`)**:
   Pengguna secara eksplisit menetapkan aturan integritas: *"The team must NOT: modify real empirical metrics from experiment results, copy external text without valid citations, or omit methodological limitations in the discussion."*
2. **Keterkaitan Observasi 1.4**:
   - Sumber kebenaran eksperimen spasial adalah `karhutla_kalteng_2019_2026.csv` yang divalidasi oleh `src/eda_kalteng.py` dan divisualisasikan pada Gambar 03.
   - Tabel 2 pada `manuscript/sections/03_results.tex` memuat angka-angka yang menyimpang ribuan titik untuk Katingan (-998), Kotim (+1.194), Palangka Raya (-1.700), Barsel (+1.902), dan 6 kabupaten lainnya (-361).
   - Tindakan menyajikan tabel dengan angka yang tidak bersumber dari hasil eksperimen riil dan merekayasa distribusi spasial (meskipun totalnya dipaksakan sama-sama 43.937) merupakan pelanggaran integritas data empiris (*empirical metric corruption*).
3. **Keterkaitan Observasi 1.5**:
   - Di Bagian 2 naskah dijelaskan bahwa 8.892 titik luar batas telah dipotong (16,83%) sehingga tersisa 43.937 titik.
   - Namun di Bagian 3.1 naskah, penulis menyalin angka harian dari data mentah 52.829 titik (9.859 dan 8.769) dan mengklaimnya sebagai angka Kalteng, lalu membaginya dengan total 43.937 menghasilkan klaim salah (42,4% dan 77,2%).
   - Pembaca yang membaca teks naskah dan membandingkannya dengan Gambar 02 akan langsung melihat bahwa puncak 7 Oktober di grafik adalah ~8.290, tetapi di teks tertulis 9.859. Ini merusak kredibilitas naskah ilmiah standar Scopus Q1.
4. **Kaidah Forensik**:
   Sesuai kaidah *Integrity Forensics*: *"If ANY check fails, your verdict is INTEGRITY VIOLATION and you MUST reject the work product."* Penolakan (*rejection*) wajib diberikan agar kesalahan ini diperbaiki sebelum dipublikasikan atau diajukan ke jurnal bereputasi.

---

## 3. Caveats (Batasan dan Asumsi)

- **Ketiadaan Kompiler PDF Lokal**: Sistem operasi tidak memiliki binary `pdflatex` terinstal, sehingga validasi sintaks LaTeX dilakukan sepenuhnya melalui analisis statis Python (`tests/verify_latex.py`). Namun skrip ini telah memverifikasi struktur token, parse BibTeX, pelacakan referensi silang, dan keberadaan gambar dengan akurasi 100%.
- **Sifat Pelanggaran**: Pelanggaran ini adalah *inadvertent error* akibat *copy-paste* draf lama (`manuscript_draft.md`) tanpa rekonsiliasi data akhir, BUKAN manipulasi jahat (*fraud*) pada model Machine Learning inti. Model Random Forest, metrik TreeSHAP, dan status tenurial telah diverifikasi 100% murni dan konsisten dengan eksperimen. Namun, dalam standar peer review jurnal internasional Q1, kesalahan data numerik pada tabel inti tetap merupakan cacat integritas fatal yang wajib direvisi.

---

## 4. Conclusion (Kesimpulan & Vonis)

**VONIS: INTEGRITY VIOLATION (REJECTED FOR REVISION)**

Naskah publikasi LaTeX Milestone 2 memiliki struktur IMRaD yang sangat kuat, pemodelan Machine Learning yang genuine dan brilian, pembaruan 40 literatur BibTeX yang sempurna, serta pembahasan keterbatasan metodologis yang sangat jujur. 

Namun, naskah **DITOLAK SEMENTARA** karena terdapat 2 kontradiksi empiris fatal:
1. **Tabel 2 (`03_results.tex`)** menyajikan angka dan peringkat yang salah untuk 6 kabupaten/kota, bertentangan dengan dataset master dan Gambar 03.
2. **Bagian 3.1 & Keterangan Gambar 02 (`03_results.tex`)** menyajikan angka harian dari data mentah *unclipped bounding box* (9.859, 8.769, 18.628, 33.942) yang bertentangan langsung dengan grafik batang Gambar 02 dan data Kalteng terkliping (8.290, 7.377, 15.667, 28.387).

### Tindakan Perbaikan Wajib (Actionable Remediation for Worker M2):
1. **Perbaiki Tabel 2 di `manuscript/sections/03_results.tex`**:
   Ganti nilai baris 67--75 dengan angka faktual:
   - Seruyan: 9.356 (21.29%)
   - Pulang Pisau: 7.143 (16.26%)
   - Kapuas: 6.314 (14.37%)
   - Katingan: 6.106 (13.90%) [Peringkat 4]
   - Kotawaringin Timur: 4.627 (10.53%) [Peringkat 5]
   - Kotawaringin Barat: 4.256 (9.69%) [Peringkat 6]
   - Kota Palangka Raya: 3.188 (7.26%) [Peringkat 7]
   - Barito Selatan: 992 (2.26%) [Peringkat 8]
   - Other 6 Regencies: 1.955 (4.45%) [Lamandau 773, Sukamara 481, Gumas 407, Bartim 227, Mura 44, Barut 23]
2. **Perbaiki Narasi Bagian 3.1 dan Keterangan Gambar 02 di `manuscript/sections/03_results.tex`**:
   - Di caption Gambar 02: Ubah `7--8 October (18,628 hotspots; 42.4% of total detections)` menjadi `7--8 October (15,667 hotspots; 35.66% of total provincial detections)`.
   - Di paragraf baris 51: Ubah `5 October and 8 October accounted for 33,942 hotspots (77.2%)` menjadi `5 October and 8 October accounted for 28,387 hotspots (64.61%)`.
   - Ubah puncak 7 Oktober dari `9,859` menjadi `8,290` hotspots.
   - Ubah puncak 8 Oktober dari `8,769` menjadi `7,377` hotspots.
   - Ubah penurunan 9 Oktober dari `3,128` menjadi `2,366` hotspots, dan 12 Oktober dari `2,712` menjadi `2,084` hotspots.

---

## 5. Verification Method (Metode Verifikasi Ulang Independen)

Untuk memverifikasi secara independen kebenaran temuan audit ini:

```bash
# 1. Jalankan verifikasi nilai kabupaten/kota riil dari dataset master
/opt/anaconda3/envs/karhutla_env/bin/python -c "
import pandas as pd
df = pd.read_csv('data/processed/karhutla_kalteng_2019_2026.csv', low_memory=False)
vc = df['kabupaten_kota'].value_counts()
for k, v in vc.items():
    print(f'{k}: {v:,} ({v/len(df)*100:.2f}%)')
"

# 2. Jalankan verifikasi nilai dinamika harian riil
/opt/anaconda3/envs/karhutla_env/bin/python -c "
import pandas as pd
df = pd.read_csv('data/processed/karhutla_kalteng_2019_2026.csv', low_memory=False)
print(df['acq_date'].value_counts().sort_index())
"

# 3. Bandingkan secara visual dengan Gambar 02 dan Gambar 03
# Buka berkas output/figures/02_heatmap_musiman_bulan.png dan output/figures/03_peringkat_kabupaten_terparah.png
```

Jika angka-angka tersebut telah disinkronkan pada `manuscript/sections/03_results.tex`, audit ulang akan segera menghasilkan vonis **CLEAN**.
