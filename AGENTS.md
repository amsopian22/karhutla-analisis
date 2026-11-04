# PANDUAN PENGEMBANGAN DAN HANDOVER AGEN AI (AGENTS.md)
# Proyek: Analisis Spasiotemporal Karhutla Kalimantan Tengah

Dokumen ini adalah instruksi operasional, konteks arsitektur, dan panduan teknis bagi setiap Agen AI yang melanjutkan pekerjaan pada repositori ini di sesi berikutnya.

---

## 1. Aturan Lingkungan & Eksekusi (Environment Rules)

> [!IMPORTANT]
> **ATURAN WAJIB PENGGUNAAN CONDA**:
> 1. Proyek ini berjalan pada lingkungan conda khusus: **`karhutla_env`** (Python 3.10).
> 2. Jalankan perintah Python melalui python binary di environment ini:
>    ```bash
>    /opt/anaconda3/envs/karhutla_env/bin/python <script.py>
>    # atau aktifkan conda
>    conda activate karhutla_env
>    ```
> 3. Jangan menginstal paket secara global atau menggunakan environment `base`.
> 4. Seluruh komunikasi dan penjelasan kepada pengguna **WAJIB menggunakan Bahasa Indonesia** yang terstruktur, berbasis data, dan berbobot *Senior Data Scientist*.

---

## 2. Struktur Proyek & Inventaris Berkas (File Inventory)

```
karhutla-analisis/
├── AGENTS.md                                # [DOKUMEN INI] Panduan teknis & handover agen AI
├── README.md                                # Dokumentasi publik proyek
├── PROJECT_SUMMARY.md                       # Ringkasan eksekutif hasil analisis & audit ilmiah
├── data/
│   ├── raw/                                 # DATA MENTAH
│   │   ├── firms_real_kalteng_latest_7d.csv # Data mentah NASA FIRMS dalam bounding box (52.829 titik)
│   │   ├── batas_kabupaten_kalteng.geojson  # Poligon batas resmi 14 Kabupaten/Kota Kalteng (geoBoundaries ADM2)
│   │   ├── jaringan_kanal_plg_kalteng.geojson # Vektor garis (LineString) poros kanal eks-PLG Blok A, B, C, D
│   │   ├── sipongi_luas_karhutla_kalteng_2018_2026.csv # Data resmi luasan kebakaran SiPongi KLHK
│   │   ├── konsesi_sawit_kalteng_real.geojson # Poligon riil HGU Perkebunan Sawit Kalteng (627 izin)
│   │   └── konsesi_kehutanan_pbph_real.geojson # Poligon riil PBPH Kehutanan Nasional (185 Kalteng)
│   └── processed/
│       ├── karhutla_kalteng_2019_2026.csv   # DATASET MASTER: 43.937 titik valid hasil kliping batas resmi Kalteng
│       ├── karhutla_kalteng_real_2026.csv   # Dataset terproses episode 2026 (43.937 titik)
│       └── transboundary_pm25_haze_2026.csv # Data simulasi dispersi PM2.5 atmosferik Monsun Barat Daya
├── app.py                                   # WEB APP DASHBOARD: Streamlit Dashboard + Gauge Meter Simulator
├── output/
│   ├── figures/                             # Visualisasi infografis ramah pengguna (300 DPI)
│   │   ├── 01_tren_tahunan_el_nino.png      # Gambar 1: Tren SiPongi KLHK (2018–2026) & El Niño
│   │   ├── 02_heatmap_musiman_bulan.png     # Gambar 2: Dinamika harian NASA FIRMS Oktober 2026
│   │   ├── 03_peringkat_kabupaten_terparah.png # Gambar 3: 8 Kabupaten terparah (Focal Colors)
│   │   ├── 04_analisis_gambut_dan_kanal.png # Gambar 4: Ekosistem gambut & jarak vektor garis kanal eks-PLG
│   │   ├── 05_status_konsesi_esg.png        # Gambar 5: Distribusi izin lahan (75,4% Non-Konsesi vs Sawit & PBPH)
│   │   ├── 06_evaluasi_model_ml.png         # Gambar 6: Kurva ROC (AUC 0.7845) & Matriks Konfusi
│   │   ├── 07_shap_feature_importance.png   # Gambar 7: Faktor paling mempengaruhi risiko (ramah awam)
│   │   ├── 08_transboundary_haze_dispersion.png # Gambar 8: Simulasi dispersi aerosol PM2.5 & Monsun
│   │   └── peta_interaktif_karhutla_kalteng.html # Peta interaktif Folium (multi-layer, garis kanal, legenda)
│   ├── models/
│   │   └── karhutla_rf_model.joblib         # Model Random Forest, Encoders, & Spatial CV Metrics
│   └── reports/
│       ├── eda_report.md                    # Laporan naratif temuan EDA terkalibrasi
│       ├── eda_summary.json                 # Metrik statistik ringkasan EDA
│       ├── model_metrics.json               # Metrik evaluasi model Random Forest & Spatial CV
│       └── transboundary_haze_summary.json  # Data kalkulasi dispersi asap regional 2026
└── src/
    ├── download_real_data.py                # PENGUNDUH data satelit & batas
    ├── process_real_data.py                 # PROSESOR: Kliping 14 Kab/Kota, vektor kanal UTM 49S, cuaca BMKG
    ├── spatial_join_concessions.py          # SPATIAL JOIN: Penaut spasial ke 627 HGU sawit & 185 PBPH
    ├── eda_kalteng.py                       # VISUALISASI: Gambar 01 - 05 gaya infografis modern
    ├── train_model.py                       # MACHINE LEARNING: Random Forest, Spatial Block CV (GroupKFold)
    ├── generate_map.py                      # PETA INTERAKTIF: Folium dengan layer kanal & legenda mengambang
    └── transboundary_haze_analysis.py       # DISPERSI ASAP: Gambar 08 model atmosferik Monsun
```

---

## 3. Alur Kerja & Eksekusi Pipeline (Step-by-Step Runbook)

Untuk mereproduksi seluruh pipeline dari awal secara berurutan:

```bash
conda activate karhutla_env

# 1. Pemrosesan data titik api riil, kliping batas 14 kabupaten, dan jarak garis kanal eks-PLG
python src/process_real_data.py

# 2. Tautkan spasial ke poligon konsesi sawit (HGU) & kehutanan (PBPH)
python src/spatial_join_concessions.py

# 3. Eksekusi Exploratory Data Analysis & visualisasi Gambar 01-05
python src/eda_kalteng.py

# 4. Latih model Machine Learning Random Forest dengan Spatial Block Cross-Validation (Gambar 06-07)
python src/train_model.py

# 5. Generate analisis dispersi asap lintas batas (Gambar 08)
python src/transboundary_haze_analysis.py

# 6. Render peta interaktif HTML dengan layer kanal dan legenda mengambang
python src/generate_map.py

# 7. Jalankan Web App Dashboard Interaktif Streamlit
streamlit run app.py
```

---

## 4. Pelajaran Teknis & Solusi Masalah (*Troubleshooting & Pitfalls*)

1. **Integritas Batas Administrasi**:
   - Selalu gunakan `data/raw/batas_kabupaten_kalteng.geojson` untuk memotong titik koordinat. Jangan hanya mengandalkan bounding box persegi karena akan memasukkan titik api di Kalsel dan Kalbar.
2. **Perhitungan Jarak Kanal**:
   - Jarak kanal dihitung menggunakan jarak minimum ke vektor `LineString` saluran primer eks-PLG di `data/raw/jaringan_kanal_plg_kalteng.geojson` yang diproyeksikan ke sistem koordinat meter `EPSG:32749` (UTM Zone 49S).
3. **Validasi Model Machine Learning (Spatial Block CV & Spatial Memorization)**:
   - Random cross-validation biasa memberikan skor yang terlalu optimis karena autokorelasi spasial (Model A: Test ROC-AUC 0.7956 vs Spatial CV 0.5399, F1 0.0583).
   - Model utama saat ini adalah **Model B (Pure Biophysical)** tanpa koordinat, divalidasi menggunakan `GroupKFold` per kabupaten dengan Holdout Test **ROC-AUC: 0.7527** (Recall Ekstrem 65,8%, Precision Reguler 92,1%) dan mempertahankan rata-rata **F1-Score: 0.1399** (2,4x lebih tinggi dari Model A) pada Spatial Block CV.
4. **Peringatan Glyph Emoji pada Matplotlib**:
   - Hindari penggunaan emoji Unicode di teks anotasi Matplotlib. Gunakan penanda teks biasa seperti `[RINGKASAN CEPAT]` untuk mencegah *UserWarning: Glyph missing from font*.
