# LAPORAN VERIFIKASI ADVERSASIAL METRIK EMPIRIS (CHALLENGER 2)
**Milestone**: M2 (Naskah Publikasi LaTeX Scopus Q1)  
**Target Pengujian**: Naskah LaTeX di `manuscript/sections/` terhadap data empiris riil di `output/reports/model_metrics.json`, `output/reports/eda_summary.json`, `data/processed/karhutla_kalteng_2019_2026.csv`, dan `output/figures/`.  
**Vonis Akhir**: **REQUEST_CHANGES** (Ditemukan 4 ketidaksesuaian empiris kritis akibat sisa teks draf lama yang bertentangan dengan dataset master dan figur ilmiah).

---

## 1. Observation (Pengamatan Faktual)

Pengujian dilakukan menggunakan orakel uji otomatis (`tests/verify_empirical_metrics.py` dan `tests/check_latex_metrics.py`) yang dieksekusi langsung pada lingkungan conda `karhutla_env` (`Python 3.10`).

### A. Metrik yang Terverifikasi 100% Konsisten (PASS)
1. **Model B (Pure Biophysical)**:
   - Holdout Test ROC-AUC: `0.7527` (Tabel 4, Baris 150 `03_results.tex`, Abstrak Baris 2). Sesuai dengan `model_metrics.json` (`0.7527`).
   - Holdout Test $F_1$-Score: `0.3983` (Tabel 4, Baris 151 `03_results.tex`, Baris 48 `04_discussion.tex`). Sesuai dengan `model_metrics.json` (`0.3983`).
   - Precision Reguler: `92.1%` / `0.9206` (Tabel 4, Baris 152 `03_results.tex`, Baris 178 `03_results.tex`). Sesuai dengan `model_metrics.json` (`0.9206`).
   - Recall Ekstrem: `65.82%` / `0.6582` (Tabel 4, Baris 153 `03_results.tex`, Baris 178 `03_results.tex`). Sesuai dengan `model_metrics.json` (`0.6582`).
   - Spatial Block CV Mean ROC-AUC: `0.4950` ($\pm 0.0490$) (Tabel 4, Baris 155 `03_results.tex`). Sesuai dengan `model_metrics.json` (`0.495` / `0.049`).
   - Spatial Block CV Mean $F_1$-Score: `0.1399` (Tabel 4, Baris 156 `03_results.tex`, Baris 178 `03_results.tex`). Sesuai dengan `model_metrics.json` (`0.1399`).
   - Rincian 5 Folds Model B (Tabel 4, Baris 159–163 `03_results.tex`):
     - Fold 1 (Seruyan): AUC `0.5827`, $F_1$: `0.2914`.
     - Fold 2 (Pulang Pisau dkk): AUC `0.5041`, $F_1$: `0.0657`.
     - Fold 3 (Kapuas dkk): AUC `0.4900`, $F_1$: `0.1056`.
     - Fold 4 (Katingan, Palangka Raya): AUC `0.4452`, $F_1$: `0.0646`.
     - Fold 5 (Kobar, Kotim): AUC `0.4533`, $F_1$: `0.1722`.
     Semuanya 100% identik dengan `model_metrics.json`.
2. **Model A (Spatial Memorization)**:
   - Holdout Test ROC-AUC: `0.7956` (Tabel 4, Baris 150 `03_results.tex`). Sesuai `model_metrics.json`.
   - Holdout Test $F_1$-Score: `0.4512` (Tabel 4, Baris 151 `03_results.tex`). Sesuai `model_metrics.json`.
   - Spatial Block CV Mean ROC-AUC: `0.5399` ($\pm 0.0531$) (Tabel 4, Baris 155 `03_results.tex`). Sesuai `model_metrics.json`.
   - Spatial Block CV Mean $F_1$-Score: `0.0583` (Tabel 4, Baris 156 `03_results.tex`). Sesuai `model_metrics.json`.
   - Rincian 5 Folds Model A (Tabel 4, Baris 159–163 `03_results.tex`):
     - Fold 1: AUC `0.5955`, $F_1$: `0.2913`.
     - Fold 2: AUC `0.5125`, $F_1$: `0.0000`.
     - Fold 3: AUC `0.5259`, $F_1$: `0.0000`.
     - Fold 4: AUC `0.4622`, $F_1$: `0.0000`.
     - Fold 5: AUC `0.6034`, $F_1$: `0.0000`.
     Semuanya 100% identik dengan `model_metrics.json`.
3. **Matriks Konfusi Model B pada Test Set ($n = 10.985$)**:
   - Dihitung langsung dari model bundle `output/models/karhutla_rf_model.joblib`:
     $$\begin{bmatrix} \text{TN} = 6.586 & \text{FP} = 2.737 \\ \text{FN} = 568 & \text{TP} = 1.094 \end{bmatrix}$$
   - Nilai $\text{TN} = 6.586$, $\text{FP} = 2.737$, $\text{TP} = 1.094$ tertulis eksplisit di `03_results.tex` (Baris 178) dan `04_discussion.tex` (Baris 48). Keempat sel ditampilkan secara utuh pada Gambar 6 (`06_evaluasi_model_ml.png`).
4. **TreeSHAP Feature Importance Ranking (12 Fitur)**:
   - Nilai Mean Absolute SHAP di Tabel 5 (`03_results.tex`, Baris 195–206) terverifikasi 100% cocok dengan `model_metrics.json`:
     1. Curah Hujan 7H: `0.0329`
     2. Jarak Kanal: `0.0322`
     3. Kecepatan Angin: `0.0254`
     4. Dry Spell: `0.0224`
     5. Lanskap Eks-PLG: `0.0222`
     6. Kedalaman Gambut: `0.0209`
     7. Suhu Maks: `0.0203`
     8. Kelembapan Relatif: `0.0173`
     9. Tipe Lahan Gambut: `0.0171`
     10. FWI Indeks: `0.0170`
     11. Status Konsesi: `0.0094`
     12. Tutupan Lahan: `0.0094`
5. **Agregat Makro EDA & Tenurial**:
   - Total hotspot Kalteng terkliping resmi: `43.937` titik.
   - Hotspot di lahan gambut: `32.643` titik (`74.30%` / `74.3%`).
   - Hotspot di tanah mineral: `11.294` titik (`25.70%` / `25.7%`).
   - Stratifikasi kedalaman gambut:
     - Gambut Dalam (200–300 cm): `12.888` titik (`29.33%`).
     - Gambut Sangat Dalam (>300 cm): `10.197` titik (`23.21%`).
     - Gambut Sedang (100–200 cm): `9.177` titik (`20.89%`).
     - Gambut Dangkal (50–100 cm): `381` titik (`0.87%`).
     - Gambut $>2$ meter: `23.085` titik (`52.54%` / `52.5%`).
   - Status konsesi:
     - Non-Konsesi (APL): `33.138` titik (`75.42%` / `75.4%`).
     - Perkebunan Sawit (HGU): `7.276` titik (`16.56%` / `16.6%`).
     - Kehutanan (PBPH): `3.523` titik (`8.02%` / `8.0%`).
   - Median jarak kanal lanskap eks-PLG: `14.946` meter.
   - Peringkat Korporasi: PT Rimba Makmur Utama (`964`), PT Sangkowong Sinta (`954`), PT Nusantara Raya Solusi (`522`), PT Graha Inti Jaya (`472`), PT Bulau Sawit Bajenta (`343`).

---

### B. Temuan Ketidaksesuaian Empiris & Anomali (FAIL / CRITICAL DISCREPANCIES)

Terdapat 4 ketidaksesuaian faktual yang ditemukan pada berkas `manuscript/sections/03_results.tex`:

#### 1. Kesalahan Faktual Distribusi Kabupaten pada Tabel 2 (`03_results.tex`, Baris 67–75)
- **Teks Naskah Saat Ini**:
  ```latex
  Kotawaringin Timur & 5,821 & 13.25% & Mentaya river basin; intensive oil palm plantation belt \\
  Katingan & 5,108 & 11.63% & Katingan-Sebangau basin; Tanjung Puting buffer zone \\
  Kotawaringin Barat & 4,219 & 9.60% & Kumai-Jelai coastal peat complex; agricultural frontier \\
  Barito Selatan & 2,894 & 6.59% & Dusun Hilir peatlands; transition to Barito river alluvium \\
  Kota Palangka Raya & 1,488 & 3.39% & Peri-urban peat fringe; Kalampangan and Sebangau lowlands \\
  Other 6 Regencies & 1,594 & 3.63% & Northern mineral uplands (Murung Raya, Gunung Mas, etc.) \\
  ```
- **Fakta Empiris Dataset Master (`data/processed/karhutla_kalteng_2019_2026.csv`) & Gambar 3 (`03_peringkat_kabupaten_terparah.png`)**:
  - Peringkat 4 adalah **Katingan**: `6.106` titik (`13.90%`), BUKAN `5.108` (`11.63%`).
  - Peringkat 5 adalah **Kotawaringin Timur**: `4.627` titik (`10.53%`), BUKAN `5.821` (`13.25%`).
  - Peringkat 6 adalah **Kotawaringin Barat**: `4.256` titik (`9.69%`), BUKAN `4.219` (`9.60%`).
  - Peringkat 7 adalah **Kota Palangka Raya**: `3.188` titik (`7.26%`), BUKAN `1.488` (`3.39%`).
  - Peringkat 8 adalah **Barito Selatan**: `992` titik (`2.26%`), BUKAN `2.894` (`6.59%`).
  - Gabungan 6 Kabupaten Lainnya (**Other 6 Regencies**): Lamandau (`773`; 1,76%) + Sukamara (`481`; 1,09%) + Gunung Mas (`407`; 0,93%) + Barito Timur (`227`; 0,52%) + Murung Raya (`44`; 0,10%) + Barito Utara (`23`; 0,05%) = **`1.955` titik (`4.45%`)**, BUKAN `1.594` (`3.63%`).
- **Dampak**: Tabel 2 bertentangan secara langsung dengan grafik batang pada Gambar 3 (`03_peringkat_kabupaten_terparah.png`) yang berada tepat di bawahnya, dan teks pada Baris 89 yang menyebut "1,594 hotspots (3.63%)" menjadi salah.

#### 2. Angka Dinamika Temporal Harian Hasil Draf Fiktif (`03_results.tex`, Baris 47 & 51)
- **Teks Naskah Saat Ini**:
  - Baris 47 (Kapsi Gambar 2): *"Thermal anomalies peaked sharply on 7--8 October (18,628 hotspots; 42.4% of total detections)..."*
  - Baris 51 (Paragraf 3.1): *"the four-day window between 5 October and 8 October accounted for 33,942 hotspots (77.2% of provincial detections). The crisis peaked on 7 October with 9,859 hotspots and 8 October with 8,769 hotspots... reducing detections to 3,128 on 9 October and 2,712 by 12 October."*
- **Fakta Empiris Dataset Master & Gambar 2 (`02_heatmap_musiman_bulan.png`)**:
  - `05 Oct 2026`: 7.390 titik
  - `06 Oct 2026`: 5.330 titik
  - `07 Oct 2026`: **8.290** titik (BUKAN 9.859)
  - `08 Oct 2026`: **7.377** titik (BUKAN 8.769)
  - `09 Oct 2026`: **2.366** titik (BUKAN 3.128)
  - `10 Oct 2026`: 3.904 titik
  - `11 Oct 2026`: 7.196 titik
  - `12 Oct 2026`: **2.084** titik (BUKAN 2.712)
  - Akumulasi 7–8 Oktober: $8.290 + 7.377 =$ **`15.667` titik (`35.66%`)**, BUKAN 18.628 (42,4%).
  - Akumulasi 5–8 Oktober: $7.390 + 5.330 + 8.290 + 7.377 =$ **`28.387` titik (`64.61%`)**, BUKAN 33.942 (77,2%).
- **Dampak**: Angka pada narasi naskah disalin dari `manuscript_draft.md` lama dan berkontradiksi langsung dengan diagram batang Gambar 2 (`02_heatmap_musiman_bulan.png`).

#### 3. Klaim Median Jarak Kanal Univariat yang Tidak Valid (`03_results.tex`, Baris 112)
- **Teks Naskah Saat Ini**:
  - Baris 112: *"Crucially, severe high-energy fires ($\text{FRP} \ge 12.0$\,MW) exhibited significantly closer proximity to canals (median: 8,420\,m) compared to regular-intensity fires (median: 16,110\,m; Mann-Whitney $U$ test, $p < 0.001$)."*
- **Fakta Empiris Dataset Master (`df_ex_plg`, $n = 16.645$)**:
  - Median jarak kanal keseluruhan di lanskap eks-PLG: `14.946 m` (VALID).
  - Median jarak kanal api ekstrem ($\text{FRP} \ge 12$ MW): **`17.085 m`** (BUKAN 8.420 m).
  - Median jarak kanal api reguler ($\text{FRP} < 12$ MW): **`14.571 m`** (BUKAN 16.110 m).
  - Nilai p-value uji Mann-Whitney $U$: **$p = 0.2545$** (BUKAN $p < 0.001$).
- **Dampak**: Secara univariat sederhana, median jarak kanal api ekstrem tidak lebih dekat dan tidak signifikan secara Mann-Whitney. Pengaruh kanal terhadap api ekstrem adalah fenomena non-linear multivariabel yang dibuktikan secara sah oleh TreeSHAP (peringkat 2, bobot SHAP 0,0322 dengan lonjakan log-odds pada koridor $<3$ km). Klaim univariat median 8.420 m vs 16.110 m ($p < 0.001$) adalah fabrikasi draft lama yang harus diganti atau dihapus agar tidak menjadi sasaran empuk penolakan reviewer Scopus Q1.

#### 4. Nilai Recall Holdout Model A di Tabel 4 (`03_results.tex`, Baris 153)
- **Teks Naskah Saat Ini**:
  - Tabel 4 Baris 153: `Recall (Severe Class, FRP >= 12) & 62.4\% & \textbf{65.82\%} & Model B captures higher proportion of severe fires \\`
- **Fakta Empiris Model Riil (`karhutla_rf_model.joblib`)**:
  - Recall kelas ekstrem Model A pada holdout test set adalah **`66.37%`** ($\text{TP}=1.103, \text{FN}=559$; $1.103 / 1.662 = 0.6637$), BUKAN `62.4%`.
- **Dampak**: Pada random holdout test set, Model A justru memiliki Recall yang sedikit lebih tinggi (66,37% vs 65,82%) karena mengalami *spatial memorization* / kebocoran data spasial di mana data uji berada di lingkungan spasial yang sama dengan data latih. Klaim bahwa Model B mengungguli Model A pada holdout test recall adalah keliru; keunggulan Model B terletak pada validasi silang spasial (**Spatial Block CV**) di mana $F_1$ Model B mencapai `0.1399` (konsisten di seluruh 5 fold) sementara Model A anjlok total ke `0.0000` di 4 fold.

---

## 2. Logic Chain (Rantai Logika Pembuktian)

1. **Premis 1 (Integritas Data Ilmiah)**: Standar jurnal Scopus Q1 mewajibkan korespondensi 100% antara data tabular, teks naskah, grafik figur, dan dataset terproses.
2. **Observasi 1**: Eksekusi pengujian pada `data/processed/karhutla_kalteng_2019_2026.csv` membuktikan bahwa jumlah titik api per kabupaten untuk Katingan adalah 6.106 dan Kotim adalah 4.627. Angka ini secara visual terpasang pada Gambar 3 (`03_peringkat_kabupaten_terparah.png`).
3. **Observasi 2**: Tabel 2 pada `03_results.tex` mencantumkan Kotim 5.821 dan Katingan 5.108. Ini merupakan angka draf lama yang tidak sinkron dengan dataset master.
4. **Observasi 3**: Pengamatan harian satelit pada dataset menunjukkan puncak krisis 7–8 Oktober adalah 15.667 titik (35,66%) dan 5–8 Oktober adalah 28.387 titik (64,61%). Kapsi Gambar 2 dan paragraf 3.1 di `03_results.tex` menulis 18.628 (42,4%) dan 33.942 (77,2%).
5. **Observasi 4**: Uji statistik Mann-Whitney pada `df_ex_plg` menghasilkan $p = 0.2545$ dengan median jarak kanal api ekstrem 17.085 m vs reguler 14.571 m, membantah klaim 8.420 m vs 16.110 m ($p < 0.001$).
6. **Kesimpulan Logis**: Terdapat sisa teks (*residual draft artifacts*) yang terbawa dari `manuscript_draft.md` ke dalam `03_results.tex` yang secara objektif tidak sinkron dengan dataset riil dan gambar ilmiah. Oleh karena itu, naskah tidak dapat disetujui (REQUEST_CHANGES) sampai tim penulis memperbarui baris-baris tersebut dengan angka empiris yang benar.

---

## 3. Caveats (Batasan dan Asumsi)

1. **Model Inti & Metrik Utama**: Seluruh metrik inti Machine Learning (ROC-AUC holdout 0,7956 vs 0,7527; Spatial CV 0,5399 vs 0,4950; F1 spatial 0,0583 vs 0,1399; seluruh 5 fold, nilai SHAP 12 fitur, dan proporsi APL 75,4%) telah terbukti **100% sahih, akurat, dan tidak mengalami smoothing**.
2. **Karakter Kesalahan**: Keempat ketidaksesuaian yang ditemukan bukan merupakan manipulasi data yang disengaja, melainkan *copy-paste artifact* dari draf narasi awal (`manuscript_draft.md`) sebelum data riil difinalisasi.
3. **Cakupan Perbaikan**: Perbaikan hanya diperlukan pada berkas `manuscript/sections/03_results.tex` (Tabel 2, Paragraf 3.1 & Kapsi Gambar 2, Baris 112, dan Tabel 4 Baris 153). Bagian Abstract, Introduction, Materials & Methods, Discussion, dan Conclusions sudah bebas dari kesalahan tersebut.

---

## 4. Conclusion & Actionable Recommendations (Kesimpulan & Rekomendasi Aksi)

**Vonis Akhir**: **`REQUEST_CHANGES`**

Tim Penulis (Milestone 2) WAJIB melakukan perbaikan berikut pada `manuscript/sections/03_results.tex`:

1. **Perbaiki Tabel 2 & Paragraf Terkait (`03_results.tex`, Baris 67–75 dan Baris 89)**:
   - Ganti baris Kotim s.d. Other 6 dengan data riil:
     - `Katingan`: 6,106 (13.90%)
     - `Kotawaringin Timur`: 4,627 (10.53%)
     - `Kotawaringin Barat`: 4,256 (9.69%)
     - `Kota Palangka Raya`: 3,188 (7.26%)
     - `Barito Selatan`: 992 (2.26%)
     - `Other 6 Regencies`: 1,955 (4.45%) [Lamandau 773, Sukamara 481, Gunung Mas 407, Barito Timur 227, Murung Raya 44, Barito Utara 23].
   - Perbarui Baris 89 dari `1,594 hotspots (3.63%)` menjadi `1,955 hotspots (4.45%)`.
2. **Perbaiki Kapsi Gambar 2 dan Paragraf 3.1 (`03_results.tex`, Baris 47 & 51)**:
   - Ganti `18,628 hotspots (42.4%)` menjadi `15,667 hotspots (35.7%)`.
   - Ganti `33,942 hotspots (77.2%)` menjadi `28,387 hotspots (64.6%)`.
   - Ganti rincian puncak: `7 October with 8,290 hotspots and 8 October with 7,377 hotspots... reducing detections to 2,366 on 9 October and 2,084 by 12 October`.
3. **Koreksi Paragraf Jarak Kanal Univariat (`03_results.tex`, Baris 112)**:
   - Hapus klaim fiktif median 8.420 m vs 16.110 m dan $p < 0.001$.
   - Ganti dengan penekanan pada temuan empiris sahih:
     *"While univariate median canal distance across all ex-PLG fires stood at 14,946\,m, multivariable TreeSHAP feature attribution identified canal proximity as the second most influential predictor (mean $|\text{SHAP}| = 0.0322$), with severe fire risk accelerating sharply within a 3,000-meter corridor along primary drainage channels."*
4. **Koreksi Recall Model A pada Tabel 4 (`03_results.tex`, Baris 153)**:
   - Ubah nilai Model A dari `62.4%` menjadi `66.37%` (atau `66.4%`), dengan catatan metodologis:
     *"Model A exhibits slightly higher holdout recall due to spatial autocorrelation memorization, but collapses under spatial cross-validation."*

---

## 5. Verification Method (Metode Verifikasi Independen)

Untuk memverifikasi secara independen seluruh temuan dalam laporan ini:

1. **Jalankan skrip audit empiris komprehensif**:
   ```bash
   /opt/anaconda3/envs/karhutla_env/bin/python tests/verify_empirical_metrics.py
   ```
2. **Jalankan skrip pencocokan metrik LaTeX otomatis**:
   ```bash
   /opt/anaconda3/envs/karhutla_env/bin/python tests/check_latex_metrics.py
   ```
3. **Kondisi Invalidasi (Invalidation Conditions)**:
   Laporan ini dapat dibatalkan jika tim penulis membuktikan bahwa dataset master yang digunakan bukan `data/processed/karhutla_kalteng_2019_2026.csv` atau jika model bundle yang dilatih bukan `output/models/karhutla_rf_model.joblib`. Namun karena kedua berkas ini adalah artefak resmi yang ditetapkan dalam `PROJECT.md` dan `AGENTS.md`, temuan ini bersifat definitif.
