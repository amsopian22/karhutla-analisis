# Analisis Karhutla (Kebakaran Hutan dan Lahan) Kalimantan Tengah

Proyek investigasi, pemodelan Machine Learning (*Spatial Cross-Validation*), dan analisis dispersi atmosferik terkait kebakaran hutan dan lahan (Karhutla) di **Provinsi Kalimantan Tengah**, episentrum karhutla lahan gambut tropis di Indonesia.

Proyek ini dibangun dari sudut pandang **Senior Data Scientist & Geospasial** dengan memadukan observasi satelit (**NASA FIRMS MODIS & VIIRS**), data resmi **SiPongi Kementerian Kehutanan / KLHK (2018–2026)**, biofisik rawa gambut, vektor poros kanal drainase eks-PLG (UTM 49S), iklim mikro dinamis BMKG, serta batas hukum konsesi lahan perkebunan sawit (HGU) dan kehutanan (PBPH).

---

## 📁 Struktur Direktori Repositori

```
karhutla-analisis/
├── AGENTS.md                                # Panduan operasional & handover teknis untuk Agen AI
├── README.md                                # Dokumentasi utama repositori
├── PROJECT_SUMMARY.md                       # Laporan eksekutif lengkap & audit ilmiah
├── manuscript/                              # NASKAH JURNAL ILMIAH (Scopus Q1/Q2 IMRAD)
│   ├── manuscript_draft.md                  # Draf lengkap manuskrip akademik bahasa Inggris
│   └── references.bib                       # 30 sitasi bibtex bereputasi tinggi
├── data/
│   ├── raw/                                 # Data mentah referensi
│   │   ├── firms_real_kalteng_latest_7d.csv # Data mentah NASA FIRMS dalam bounding box (52.829 titik)
│   │   ├── batas_kabupaten_kalteng.geojson  # Poligon batas resmi 14 Kabupaten/Kota Kalteng (geoBoundaries ADM2)
│   │   ├── peta_gambut_kalteng_bblsdlp.geojson # Poligon resmi stratifikasi kedalaman gambut BBLSDLP/KHG 2019
│   │   ├── era5_weather_kalteng_october.csv # Data reanalisis atmosferik riil ECMWF ERA5-Land (14 kabupaten)
│   │   ├── jaringan_kanal_plg_kalteng.geojson # Vektor garis (LineString) poros kanal eks-PLG
│   │   ├── sipongi_luas_karhutla_kalteng_2018_2026.csv # Data resmi luasan kebakaran SiPongi KLHK
│   │   ├── konsesi_sawit_kalteng_real.geojson # Poligon riil HGU Sawit Kalteng (627 izin)
│   │   └── konsesi_kehutanan_pbph_real.geojson # Poligon riil PBPH Kehutanan Nasional (185 Kalteng)
│   └── processed/
│       ├── karhutla_kalteng_2019_2026.csv   # DATASET MASTER: 43.937 titik valid hasil kliping batas resmi Kalteng
│       ├── karhutla_kalteng_real_2026.csv   # Dataset terproses episode 2026 (43.937 titik)
│       └── transboundary_pm25_haze_2026.csv # Data simulasi dispersi PM2.5 atmosferik Monsun Barat Daya
├── app.py                                   # WEB APP DASHBOARD: Streamlit Dashboard + Speedometer Risiko
├── output/
│   ├── figures/                             # Visualisasi infografis ramah pengguna (300 DPI)
│   │   ├── 01_tren_tahunan_el_nino.png      # Gambar 1: Tren SiPongi KLHK (2018–2026) & El Niño
│   │   ├── 02_heatmap_musiman_bulan.png     # Gambar 2: Dinamika harian NASA FIRMS Oktober 2026
│   │   ├── 03_peringkat_kabupaten_terparah.png # Gambar 3: 8 Kabupaten terparah (Focal Colors)
│   │   ├── 04_analisis_gambut_dan_kanal.png # Gambar 4: Ekosistem gambut BBLSDLP (74,3%) & jarak kanal eks-PLG
│   │   ├── 05_status_konsesi_esg.png        # Gambar 5: Distribusi izin lahan (75,4% Non-Konsesi vs Sawit & PBPH)
│   │   ├── 06_evaluasi_model_ml.png         # Gambar 6: Kurva ROC komparasi Model A vs B & Matriks Konfusi
│   │   ├── 07_shap_feature_importance.png   # Gambar 7: SHAP Beeswarm Plot Asli (shap.TreeExplainer)
│   │   ├── 08_transboundary_haze_dispersion.png # Gambar 8: Modul tambahan edukasi dispersi aerosol PM2.5
│   │   └── peta_interaktif_karhutla_kalteng.html # Peta interaktif Folium (multi-layer, garis kanal, legenda)
│   ├── models/
│   │   └── karhutla_rf_model.joblib         # Model Random Forest, Encoders, & Spatial CV Metrics
│   └── reports/
│       ├── eda_report.md                    # Laporan naratif temuan EDA terkalibrasi
│       ├── eda_summary.json                 # Metrik statistik ringkasan EDA
│       ├── model_metrics.json               # Metrik evaluasi model Random Forest & Spatial CV
│       └── transboundary_haze_summary.json  # Data kalkulasi dispersi asap regional 2026
└── src/
    ├── download_era5_weather.py             # Pengunduh data cuaca reanalisis ERA5-Land ECMWF
    ├── generate_bblsdlp_peatland.py         # Pembangun poligon resmi gambut BBLSDLP/KHG 2019
    ├── process_real_data.py                 # PROSESOR: Kliping 14 Kab/Kota, vektor kanal UTM 49S, cuaca ERA5
    ├── spatial_join_concessions.py          # SPATIAL JOIN: Penaut spasial ke 627 HGU sawit & 185 PBPH
    ├── eda_kalteng.py                       # VISUALISASI: Gambar 01 - 05 gaya infografis modern
    ├── train_model.py                       # MACHINE LEARNING: Komparasi 2 Model, Spatial Block CV & TreeSHAP
    ├── generate_map.py                      # PETA INTERAKTIF: Folium dengan layer kanal & legenda mengambang
    └── transboundary_haze_analysis.py       # DISPERSI ASAP: Gambar 08 model atmosferik Monsun
```

---

## 🐍 Lingkungan Kerja (Conda Environment)

Seluruh analisis dijalankan pada lingkungan conda terisolasi:
```bash
conda activate karhutla_env
```

Untuk mereproduksi seluruh pipeline dari awal:
```bash
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

# 7. Menjalankan Web App Dashboard Interaktif Streamlit
streamlit run app.py
```

---

## 🔍 Temuan Kunci Utama (Key Insights)

1. **Dominasi Area Non-Konsesi (75,4%)**:
   - Sebanyak **75,4%** (33.138 titik api) berada di luar konsesi berizin resmi (di Area Penggunaan Lain / Lahan Terbuka / Gambut Terlantar).
   - Konsesi Sawit (HGU) mencakup **16,6%** (7.276 titik) dan Konsesi Kehutanan (PBPH) mencakup **8,0%** (3.523 titik).
2. **Episentrum Spasial Terpusat pada Eks-PLG**:
   - Tiga kabupaten teratas secara konsisten menyumbang **52,0%** kebakaran di Kalteng: **Seruyan (21,3%)**, **Pulang Pisau (16,3%)**, dan **Kapuas (14,4%)**. Wilayah Pulang Pisau dan Kapuas beririsan langsung dengan kanal-kanal peninggalan eks-Proyek Lahan Gambut (PLG) 1 Juta Hektar.
3. **Ekosistem Gambut & Pengeringan Kanal**:
   - **74,3%** (32.643 titik api) terjadi di atas ekosistem rawa gambut resmi (BBLSDLP 2019 / SK.130 MenLHK), dengan 52,5% berada di kubah gambut dalam (> 2 meter). Kanal eks-PLG tanpa sekat menguras air tanah, memicu kebakaran bawah tanah (*subsurface smoldering*).
4. **Pembuktian Bahaya Memorisasi Spasial (Spatial Block CV)**:
   - Komparasi dua model membuktikan bahwa model yang mengikutsertakan koordinat (`Model A`) mengalami *spatial memorization overfitting*: AUC tampak tinggi pada random split (0.7956) namun anjlok ke 0.5399 (F1-score kolaps ke 0.0583) pada Spatial Block CV.
   - Model Biofisik Murni (`Model B`) mempertahankan generalisasi proses fisik (Holdout AUC: 0.7527, Recall Api Ekstrem: 65,8%, Spatial CV F1-score: 0.1399 atau 2,4x lebih tinggi dari Model A).
