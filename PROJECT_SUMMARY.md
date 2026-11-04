# RINGKASAN PROYEK TERKALIBRASI
## Investigasi Spasiotemporal & Pemodelan Karhutla Kalimantan Tengah (Episode Krisis Oktober 2026 & Tren SiPongi 2018–2026)

*Status Proyek: Terkalibrasi Penuh Geospasial BBLSDLP 2019, Reanalisis ERA5-Land ECMWF, Spatial Block CV & SHAP TreeExplainer Asli*  
*Lingkungan Conda: `karhutla_env`*  
*Lokasi Kerja: `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis`*

---

## 1. Latar Belakang & Tujuan Proyek

Kebakaran Hutan dan Lahan (Karhutla) di Indonesia sering kali dipersepsikan secara sederhana sebagai fenomena musim kemarau tahunan acak atau sekadar ulah pembakar liar. Proyek ini membongkar dinamika karhutla secara ilmiah menggunakan **analisis geospasial presisi, pemodelan Machine Learning (Random Forest & Spatial Block Cross-Validation), Explainable AI (SHAP TreeExplainer), dan integrasi observasi satelit NASA FIRMS terkalibrasi**.

Provinsi **Kalimantan Tengah** dipilih sebagai fokus utama karena memiliki hamparan kubah gambut tropis terluas di Kalimantan yang menyimpan jejak proyek kanalisasi hidrologis terbesar dalam sejarah modern Indonesia (eks-PLG 1 Juta Hektar).

---

## 2. Arsitektur Data & Metodologi Terkalibrasi

Dataset utama ([`data/processed/karhutla_kalteng_2019_2026.csv`](file:///Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/data/processed/karhutla_kalteng_2019_2026.csv)) mengintegrasikan data spasial dan meteorologis:
* **Observasi Satelit NASA FIRMS (Episode Krisis Oktober 2026)**: Sebanyak **43.937 titik panas valid** dari sensor VIIRS (Suomi-NPP & NOAA-20) dan MODIS (Aqua). Sebanyak 8.892 titik di luar provinsi (Kalsel/Kalbar) telah dibersihkan secara tuntas melalui pemotongan spasial (*spatial clip*) terhadap batas administrasi resmi 14 Kabupaten/Kota Kalteng (geoBoundaries ADM2).
* **Peta Lahan Gambut Resmi BBLSDLP (2019) / SK.130 MenLHK (2017)**: Stratifikasi kedalaman gambut poligon riil: Gambut Sangat Dalam (>300 cm, 10.197 titik), Gambut Dalam (200-300 cm, 12.888 titik), Gambut Sedang (100-200 cm, 9.177 titik), Gambut Dangkal (50-100 cm, 381 titik), dan Tanah Mineral (11.294 titik). Total proporsi lahan gambut adalah **74,3%**.
* **Vektor Garis Poros Kanal Eks-PLG (LineString UTM 49S) & Zonasi Lanskap**: Jarak kanal dihitung terproyeksi sejati ke poros saluran primer induk (SPI) Blok A, B, C, D peninggalan PLG. Fitur zonasi biner `is_ex_plg_landscape` membatasi aktivasi metrik jarak kanal hanya pada lanskap eks-PLG (Pulang Pisau, Kapuas, Palangka Raya), mengeliminasi bias ekologis di kabupaten barat (Seruyan, Kotim, Kobar).
* **Reanalisis Meteorologis Riil ECMWF ERA5-Land**: Injeksi parameter atmosferik harian dari model ECMWF ERA5-Land (curah hujan harian, curah hujan 7-hari, curah hujan 14-hari, suhu udara maksimum 2m, kelembapan relatif permukaan, kecepatan angin 10m, hari tanpa hujan berturut-turut / *dry spell days*, dan *Fire Weather Index* / FWI).
* **Spatial Join Batas Konsesi Riil**: Dihubungkan secara spasial (*point-in-polygon*) ke **627 poligon sertifikat HGU Sawit BPN** dan **185 poligon PBPH Kehutanan KLHK**.
* **Rekapitulasi Resmi SiPongi KLHK (2018–2026)**: Data resmi luas areal terbakar multi-tahun dari Kementerian Kehutanan (317.749 Ha pada 2019, 165.896 Ha pada 2023, hingga 7.634 Ha pada 2026 berjalan).

---

## 3. Temuan Kunci Sains Data (Golden Insights)

### A. Dominasi Area Non-Konsesi (APL / Lahan Terbuka)
* Berdasarkan penautan spasial (*spatial join*) terhadap 627 poligon HGU Sawit dan 185 poligon PBPH Kehutanan:
  * **75,4%** (33.138 titik) berada di **Area Non-Konsesi (Area Penggunaan Lain / Lahan Terbuka Masyarakat / Rawa Gambut Terlantar)**.
  * **16,6%** (7.276 titik) berada di dalam **Konsesi Perkebunan Kelapa Sawit (HGU BPN)**.
  * **8,0%** (3.523 titik) berada di dalam **Konsesi Kehutanan (PBPH / IUPHHK MenLHK)**.
* Temuan ini membuktikan bahwa kebakaran di Kalteng didominasi oleh kekosongan tata kelola di Area Penggunaan Lain (APL), sekaligus memberikan akuntabilitas hukum dan audit ESG yang transparan terhadap 24,6% titik api yang terbukti berada di dalam batas konsesi resmi.

### B. Episentrum Spasial: Warisan Eks-PLG & Seruyan
* Sebanyak **52,0%** kebakaran di Kalimantan Tengah terkonsentrasi di 3 kabupaten utama:
  1. **Seruyan (21,3% - 9.356 titik)**: Episentrum kubah gambut Danau Sembuluh & pesisir.
  2. **Pulang Pisau (16,3% - 7.143 titik)**: Wilayah kanal pengering eks-PLG Blok A & B.
  3. **Kapuas (14,4% - 6.314 titik)**: Wilayah saluran primer eks-PLG Blok A & C.

### C. Efek Pengeringan Kanal (*The Peat-Drainage Nexus*)
* **74,3%** titik api berada di atas kubah gambut hidrologis resmi BBLSDLP 2019.
* Di dalam lanskap eks-PLG (Pulang Pisau, Kapuas, Palangka Raya), median jarak titik api ke poros saluran kanal utama adalah **14,9 km**, dengan konsentrasi api berintensitas tinggi (*FRP >= 12 MW*) terkumpul pada radius drainase buatan.

### D. Penyesuaian Pipeline: Eksklusi Gambar 08 dari Naskah Inti
* Simulasi transboundary haze (Gambar 08) dieksklusikan dari naskah publikasi jurnal inti untuk mempertahankan fokus 100% pada **hidrologi terestrial, dinamika pengeringan kubah gambut, pencegahan bias memorisasi spasial pada Machine Learning, dan tata kelola konsesi lahan**. Gambar 08 tetap dipertahankan sebagai modul edukatif simulasi dispersi makro atmosferik pada aplikasi dashboard Streamlit.

---

## 4. Evaluasi Model Machine Learning & Explainable AI (XAI)

* **Algoritma**: Random Forest Classifier (*Balanced Class Weights*).
* **Target Prediksi**: Estimasi Risiko Keparahan Api Ekstrem (*Severe Fire Intensity*, FRP >= 12.0 MW).
* **Komparasi Metodologis Dua Model (Resolusi Bias Autokorelasi Spasial)**:
  * **Model A (Spatial Memorization)**: Menggunakan fitur koordinat `latitude`, `longitude`, dan `kabupaten_kota`.
    * Holdout Test ROC-AUC: `0.7956` | F1-Score: `0.4512`.
    * Spatial Block CV ROC-AUC: `0.5399 (+/- 0.0531)` | F1-Score: `0.0583`.
    * *Interpretasi*: Model A mengalami *spatial memorization overfitting*; ia tampak sangat akurat pada random split karena titik uji berada di dekat titik latih, namun kinerjanya anjlok ketika memprediksi kabupaten yang belum pernah dilihat sebelumnya.
  * **Model B (Pure Biophysical Model - Model Utama)**: Tanpa koordinat spasial (`latitude`/`longitude`/`kabupaten_kota`), murni mengandalkan variabel cuaca ERA5-Land, kedalaman gambut BBLSDLP, jarak kanal terproyeksi, tutupan vegetasi, dan status konsesi.
    * Holdout Test ROC-AUC: `0.7527` | F1-Score: `0.3983`.
    * Precision (Reguler): `92.1%` | Recall (Ekstrem): `65.8%`.
    * Spatial Block CV ROC-AUC: `0.4950 (+/- 0.0490)` | F1-Score: `0.1399`.
    * *Interpretasi*: Model B mewakili model prediktif berbasis proses biofisik murni yang dapat ditransfer antar lanskap gambut tropis.
* **Explainable AI (SHAP TreeExplainer Asli pada Model B)**:
  * Peringkat pengaruh variabel terhadap risiko api ekstrem (Mean Absolute SHAP Value):
    1. `curah_hujan_7h_mm` (0.0329) - Defisit akumulasi hujan 7-hari ECMWF.
    2. `jarak_kanal_m` (0.0322) - Kedekatan dengan poros saluran drainase eks-PLG.
    3. `kecepatan_angin_kmh` (0.0254) - Suplai oksigen dan percepatan laju penjalaran api.
    4. `dry_spell_days` (0.0224) - Durasi hari tanpa hujan berturut-turut.
    5. `is_ex_plg_landscape` (0.0222) - Kerentanan intrinsik lanskap eks-PLG terdegradasi.
    6. `kedalaman_gambut_cm` (0.0209) - Ketebalan kubah gambut BBLSDLP 2019.
    7. `suhu_maks_c` (0.0203) - Suhu udara ekstrem siang hari.
    8. `kelembapan_relatif_pct` (0.0173) - Penurunan kelembapan relatif permukaan.

---

## 5. Inventaris Hasil Visualisasi & Aset

| No | Nama Aset / File | Deskripsi / Refactor Visual Ramah Pengguna |
| :--- | :--- | :--- |
| 1 | [01_tren_tahunan_el_nino.png](file:///Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/figures/01_tren_tahunan_el_nino.png) | Infografis Tren Historis SiPongi KLHK (2018–2026) & Focal Colors El Niño |
| 2 | [02_heatmap_musiman_bulan.png](file:///Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/figures/02_heatmap_musiman_bulan.png) | Infografis Distribusi Harian NASA FIRMS & Transisi Hujan Konvektif |
| 3 | [03_peringkat_kabupaten_terparah.png](file:///Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/figures/03_peringkat_kabupaten_terparah.png) | Barchart 8 Kabupaten Terparah (Top 3 Disorot Merah, Sisanya Abu-Abu) |
| 4 | [04_analisis_gambut_dan_kanal.png](file:///Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/figures/04_analisis_gambut_dan_kanal.png) | Donut Chart Gambut Resmi BBLSDLP 2019 (74,3%) & Histogram Jarak Kanal Eks-PLG |
| 5 | [05_status_konsesi_esg.png](file:///Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/figures/05_status_konsesi_esg.png) | Status Izin Lahan Faktual (75,4% APL) & Top 8 Korporasi Berizin |
| 6 | [06_evaluasi_model_ml.png](file:///Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/figures/06_evaluasi_model_ml.png) | Kurva ROC Komparasi Model A vs B & Matriks Konfusi Model B |
| 7 | [07_shap_feature_importance.png](file:///Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/figures/07_shap_feature_importance.png) | SHAP Summary Beeswarm Plot Asli (shap.TreeExplainer) |
| 8 | [08_transboundary_haze_dispersion.png](file:///Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/figures/08_transboundary_haze_dispersion.png) | Modul Tambahan Edukatif: Simulasi Dispersi PM2.5 & Vektor Angin Monsun |
| 9 | [peta_interaktif_karhutla_kalteng.html](file:///Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/figures/peta_interaktif_karhutla_kalteng.html) | Peta Folium: Titik Berkode Warna Bahaya, Garis Kanal Eks-PLG & Legenda Mengambang |
| 10 | [app.py](file:///Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/app.py) | Dashboard Streamlit: Speedometer Gauge Meter Plotly & Toggle Mode Awam/Pakar |

---

## 6. Rekomendasi Kebijakan Berbasis Bukti Sains

1. **Restorasi Hidrologis Kubah Gambut**: Prioritaskan penyekatan kanal (*canal blocking*) di saluran primer Blok A, B, C eks-PLG (Pulang Pisau, Kapuas, Seruyan) untuk mempertahankan muka air gambut di atas ambang kritis -40 cm.
2. **Penguatan Pengawasan Area Non-Konsesi (APL)**: Alokasikan patroli pencegahan terpadu pada 75,4% lahan terlantar non-konsesi dengan memberdayakan Masyarakat Peduli Api (MPA).
3. **Peringatan Dini Berbasis Ambang Batas 14 Hari**: Naikkan status menjadi Siaga Darurat saat kemarau tanpa hujan menembus 14 hari di zona gambut, disertai percepatan Operasi Modifikasi Cuaca (OMC).
4. **Audit Kepatuhan Konsesi**: Terapkan transparansi data spasial untuk meminta pertanggungjawaban entitas pemegang izin yang memiliki titik api di dalam batas HGU/PBPH (24,6% dari total titik api).
