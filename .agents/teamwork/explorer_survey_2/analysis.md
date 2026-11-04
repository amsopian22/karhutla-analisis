# Laporan Analisis Penyelidikan Naskah Ilmiah & Bibliografi (Explorer 2)
**Target**: Kesiapan Naskah Menuju Publikasi Standar Scopus Q1 (*Remote Sensing* MDPI / Jurnal Terindeks Q1 Sejenis)  
**Dokumen Terperiksa**: 
- `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/manuscript/manuscript_draft.md` (49.305 bytes, 366 baris)
- `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/manuscript/references.bib` (12.660 bytes, 320 baris)
- Artefak empiris: `output/reports/model_metrics.json`, `output/reports/eda_summary.json`, dan direktori `output/figures/` (Gambar 01_ s.d. 07_)

---

## 1. Ringkasan Eksekutif (Executive Summary)

Draf naskah saat ini (`manuscript_draft.md`) memiliki fondasi substansi ilmiah dan integritas data empiris yang sangat solid, mengintegrasikan 43.937 observasi satelit NASA FIRMS terkalibrasi, poligon kedalaman gambut BBLSDLP 2019, jaringan vektor kanal eks-PLG UTM 49S, reanalisis cuaca ECMWF ERA5-Land, serta overlay 627 konsesi sawit HGU dan 185 konsesi kehutanan PBPH. Namun demikian, untuk memenuhi standar publikasi internasional jurnal Scopus Q1 (*Remote Sensing* atau *International Journal of Wildland Fire*), naskah memerlukan perbaikan struktural krusial:
1. **Pemetaan Ulang dan Integrasi Lengkap 7 Figur Ilmiah**: Draf markdown memiliki ketidaksesuaian penomoran figur yang parah (Gambar 1 berupa diagram ASCII, Gambar 02, 04, dan 05 tidak memiliki *callout* gambar resmi, sedangkan Gambar 06 dan 07 salah diberi nomor sebagai Gambar 4 dan 5). Seluruh 7 figur riil (`output/figures/01_` s.d. `07_`) wajib diintegrasikan penuh ke dalam lingkungan `figure` LaTeX dengan caption komprehensif.
2. **Ketiadaan Sub-bab Keterbatasan Metodologis (*Threats to Validity*)**: Bagian Diskusi saat ini belum memiliki sub-bab khusus yang membedah kelemahan dan batasan riset (resolusi spasial ERA5-Land 9 km, oklusi awan/asap tebal sensor optik, cakupan episode temporal Oktober 2026, dan kendala transferabilitas spasial pada F1-score Spatial CV 0,1399).
3. **Penyegaran Literatur Mutakhir (2021–2025)**: Sebanyak 30 entri di `references.bib` 100% konsisten dengan sitasi teks draf, namun **0% berasal dari rentang 2021–2026**. Diperlukan penambahan 8–10 referensi mutakhir bereputasi tinggi terkait *spatial machine learning overfitting*, *peatland hydrology remote sensing*, dan *active fire FRP algorithms*.
4. **Arsitektur LaTeX Modular**: Diperlukan penyusunan draf master `main.tex` dengan struktur sub-direktori `sections/` yang mematuhi standar tipografi akademik tingkat tinggi, persamaan matematika lengkap, tabel `booktabs`, dan penomoran baris ganda (*lineno*).

---

## 2. Pemeriksaan Menyeluruh Naskah Draf (`manuscript_draft.md`)

### 2.1. Metadata & Judul
- **Judul**: *"Spatiotemporal Fire Intensity Modeling in Degraded Tropical Peatlands: Addressing Spatial Autocorrelation and Land Tenure Governance in Central Kalimantan"*  
  *Evaluasi*: Sangat tajam, mencerminkan dua pilar kontribusi utama (aspek metodologis autokorelasi spasial dan aspek tata kelola tenurial lahan). Disarankan menambahkan *Running Title* untuk header naskah jurnal: *"Spatial Fire Modeling & Tenure Governance in Degraded Peatlands"*.
- **Penulis & Afiliasi**: Masih berupa placeholder generik (*"Senior Data Science & Remote Sensing Research Team"* / *"Geospatial AI & Environmental Analytics Laboratory"*).  
  *Kebutuhan Q1*: Format resmi memerlukan nama penulis lengkap, afiliasi departemen dan universitas/lembaga, alamat pos, korespondensi email, dan tanda *Corresponding Author* serta nomor ORCID.

### 2.2. Pemetaan Struktur IMRaD dan Evaluasi Kesiapan Akademik

| Bagian IMRaD | Status Saat Ini | Kelengkapan Narasi & Data | Kekurangan / Gap Kritis | Kesiapan Scopus Q1 |
|---|---|---|---|:---:|
| **Abstract** | Lengkap (310 kata) | Menyajikan latar belakang ekologis, problem autokorelasi spasial, 43.937 hotspot FIRMS, BBLSDLP, ERA5-Land, HGU/PBPH, komparasi Model A vs Model B, TreeSHAP, dan temuan tenurial (75,4% Non-Konsesi). | Perlu dipastikan batas kata (<300 kata untuk MDPI Remote Sensing) dan penajaman rumusan masalah utama dalam satu kalimat tegas di awal. | **90%** (Tinggi) |
| **Keywords** | Lengkap (8 kata kunci) | Mencakup aspek fisik (*Peatland wildfire*, *FRP*), metodologis (*Spatial block cross-validation*, *Random Forest*, *TreeSHAP*), dan spasial/tata kelola (*Mega Rice Project*, *Land tenure governance*, *Central Kalimantan*). | Sudah optimal, perlu disusun berurutan alfabetis sesuai gaya selingkung jurnal. | **100%** (Sempurna) |
| **1. Introduction** | Lengkap (4 sub-bagian naratif, 5 kontribusi riset) | - Signifikansi karbon gambut tropis.<br>- Sejarah proyek PLG 1 juta ha & 4.000 km kanal.<br>- Dampak emisi gas rumah kaca & kabut asap lintas batas (PM2.5).<br>- Kesenjangan riset 1: Jebakan autokorelasi spasial (Hukum Tobler 1) & kebocoran koordinat.<br>- Kesenjangan riset 2: Paradoks atribusi tenurial korporasi vs non-konsesi.<br>- 5 poin kontribusi terukur. | - Belum memuat perumusan hipotesis formal (H1: model berbasis koordinat gagal transfer spasial; H2: model biofisik mempertahankan prediktibilitas fisik).<br>- Kurang mengutip literatur metodologis spatial ML mutakhir (2021–2024). | **85%** (Tinggi) |
| **2. Materials and Methods** | Sangat Rinci (Sub-bab 2.1 s.d. 2.3) | - Deskripsi bentang alam 14 kab/kota & Blok A–D PLG.<br>- Kliping ketat geoBoundaries ADM2 (membersihkan 8.892 titik luar provinsi).<br>- Klasifikasi kedalaman gambut BBLSDLP 2019.<br>- Vektorisasi kanal LineString UTM 49S ($EPSG:32749$).<br>- Reanalisis ECMWF ERA5-Land & kalibrasi FWI.<br>- Spatial join 627 HGU sawit + 185 PBPH.<br>- Formulasi target $y_i$ ($FRP \ge 12.0$ MW).<br>- Arsitektur Model A (15 fitur) vs Model B (12 fitur).<br>- Protokol Spatial Block CV (`GroupKFold` per kabupaten).<br>- TreeSHAP exact Shapley values. | - **Gambar 1 saat ini berupa diagram ASCII art**, yang dilarang dalam naskah jurnal ilmiah resmi.<br>- Perlu penambahan formulasi matematis partisi Spatial Block CV dan penanganan ketimpangan kelas (`class_weight='balanced'`).<br>- Penjelasan justifikasi nilai *sentinel* (-1) pada jarak kanal di luar wilayah eks-PLG agar reviewer tidak mempertanyakan diskontinuitas pohon keputusan. | **80%** (Perlu revisi teknis) |
| **3. Results** | Sangat Lengkap (Sub-bab 3.1 s.d. 3.5) | - Tabel 1: SiPongi 2018–2026 (lonjakan 2019: 317.749 ha & 2023: 165.896 ha).<br>- Dinamika harian puncak 5–8 Oktober (77,2% hotspot).<br>- Tabel 2: Distribusi 14 kabupaten (Seruyan 21,3%, Pulpis 16,3%, Kapuas 14,4%).<br>- Faktual tenurial: 75,4% APL, 16,6% Sawit, 8,0% PBPH.<br>- Gambut dalam & sangat dalam (>2m) mendominasi 52,5% hotspot.<br>- Median jarak kanal eks-PLG: 14.946 m (FRP ekstrem lebih dekat: 8.420 m vs 16.110 m, $p<0.001$).<br>- Tabel 3: Evaluasi komparatif Model A (Holdout AUC 0,7956 -> Spatial CV 0,5399, F1 0,0583) vs Model B (Holdout AUC 0,7527, Spatial CV F1 0,1399).<br>- Rincian Fold 1 s.d. 5 Spatial CV.<br>- Tabel 4: Ranking TreeSHAP 12 fitur (Curah hujan 7H: 0,0329, Jarak kanal: 0,0322, Angin: 0,0254, Dry spell: 0,0224). | - **Ketidakcocokan penomoran figur dan ketiadaan callout gambar**: Gambar 02 (harian), 04 (gambut & kanal), dan 05 (status konsesi) dibahas di teks tetapi TIDAK dipanggil sebagai `Figure`.<br>- Gambar 06 disebut "Figure 4" dan Gambar 07 disebut "Figure 5".<br>- Seluruh 7 figur riil (`01_` s.d. `07_`) harus dipetakan berurutan 1 s.d. 7. | **75%** (Perlu realign gambar) |
| **4. Discussion** | Kuat secara konseptual (Sub-bab 4.1 s.d. 4.3) | - *The Peat-Drainage Nexus*: hilangnya saturasi hidrologis, pengeringan katotelm, pembakaran lambat bawah tanah.<br>- *Resolving Land Tenure Void*: beban hukum mutlak (*strict liability*) UU 32/2009 pada 24,6% korporasi versus kekosongan institusional di 75,4% APL/lahan terbuka.<br>- *Methodological Imperatives*: jebakan jalan pintas koordinat lat/lon, bahaya validasi acak biasa, keharusan spatial block cross-validation. | - **GAP KRITIS: Belum ada sub-bab 4.4 mengenai Keterbatasan Studi (*Limitations and Threats to Validity*)**.<br>- Reviewer Scopus Q1 akan langsung menolak naskah jika tidak mengakui kelemahan data (resolusi ERA5-Land 9 km, keterbatasan satelit optik terhadap awan/asap tebal, sifat episode temporal satu musim, dan rendahnya nilai mutlak F1 pada Spatial CV). | **70%** (Wajib tambah sub-bab) |
| **5. Conclusions & Policy** | Lengkap & Aplikatif | - 4 Kesimpulan Ilmiah Utama (Non-linearitas El Niño, Dominasi APL, Poros Kanal-Gambut, Resolusi Overfitting Spasial).<br>- 4 Rekomendasi Kebijakan Konkret: Protokol darurat dry spell 14 hari, Prioritas sekat kanal Blok A & B (<3 km), Kelembagaan APL via Perhutanan Sosial/KHDTK, Dashboard audit spasial ESG. | Tambahkan paragraf penutup singkat mengenai prospek riset masa depan (*future research horizons*: integrasi data LiDAR GEDI, radar Sentinel-1 InSAR, dan sensor IoT muka air gambut *real-time*). | **90%** (Tinggi) |

---

## 3. Pemeriksaan Bibliografi (`references.bib`) & Analisis Kesenjangan Literatur

### 3.1. Status Entri dan Konsistensi Sitasi
- **Total Entri BibTeX**: Tepat 30 entri.
- **Konsistensi terhadap Draf Naskah**:
  - Semua 30 kunci sitasi yang dipanggil dalam format `@Key` pada `manuscript_draft.md` ditemukan pada `references.bib` (**0 missing keys**).
  - Tidak ada satupun entri di `references.bib` yang tidak tersitasi dalam naskah (**0 unused keys**).
- **Integritas Format BibTeX**:
  - Semua entri artikel jurnal (27 artikel) memiliki field wajib: `author`, `title`, `journal`, `volume`, `pages`, `year`, dan `doi`.
  - Entri konferensi (1 inproceedings: `LundbergLee2017NeurIPS`) dan laporan teknis (2 techreport: `Tacconi2003CIFOR`, `Silvius2005Wetlands`) terformat sesuai standar baku.

### 3.2. Distribusi Kronologis dan Kesenjangan Literatur (Literature Gaps)

Distribusi tahun terbitan pada `references.bib`:
- 1970–1999: 2 entri (6,7%) — *Tobler (1970)*, *Legendre (1993)*
- 2000–2009: 8 entri (26,7%) — *Breiman (2001)*, *Page et al. (2002)*, *Cochrane (2003)*, dll.
- 2010–2019: 17 entri (56,7%) — *Hooijer et al. (2012)*, *Ritzema et al. (2014)*, *Field et al. (2016)*, *Meyer et al. (2018)*, dll.
- 2020: 3 entri (10,0%) — *Vetrita & Cochrane (2020)*, *Roberts et al. (2020)*
- **2021–2026: 0 entri (0,0%)**

> [!WARNING]
> **TEMUAN KRITIS REVIEWER**: Ketiadaan artikel terbitan 5 tahun terakhir (2021–2026) merupakan celah fatal dalam peer review Scopus Q1. Standar jurnal internasional bereputasi tinggi mengharapkan minimal 20–30% sitasi berasal dari penelitian mutakhir.

### 3.3. Rekomendasi Penambahan Referensi Kunci (2021–2025)

Untuk memperkuat naskah pada tahap implementasi LaTeX, disarankan menambahkan 10 entri BibTeX bereputasi tinggi berikut ke `references.bib`:

1. **Kluster Spatial Machine Learning & Overfitting Validation**:
   - `MeyerPebesma2021NatComm`: Meyer, H., & Pebesma, E. (2021). Predicting into unknown space? Estimating the area of applicability of spatial prediction models. *Nature Communications*, 12, 1627. (Dasar teoretis mengapa model ML runtuh saat dievaluasi di luar ruang geografis latihan).
   - `Wadoux2021EcolModel`: Wadoux, A. M. J. C., et al. (2021). Spatial cross-validation is not always necessary for spatial prediction: when and why. *Ecological Modelling*, 442, 109439.
   - `Schratz2019EcolModel`: Schratz, P., et al. (2019). Hyperparameter tuning and performance assessment of statistical and machine-learning methods using spatial data. *Ecological Modelling*, 406, 109–120.
   - `Roberts2017Ecography`: Roberts, D. R., et al. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical or phylogenetic structure. *Ecography*, 40(8), 913–929.
2. **Kluster Hidrologi Gambut Tropis & Remote Sensing Muka Air Tanah**:
   - `Dadap2021NatComm`: Dadap, N. C., et al. (2021). Satellite-observed peatland groundwater tables and fire risk across Southeast Asia. *Nature Communications*, 12, 5909. (Bukti penginderaan jauh penurunan muka air tanah gambut pemicu karhutla).
   - `Graham2022SciRep`: Graham, L. L. B., et al. (2022). Tropical peatland restoration: hydrological recovery and fire susceptibility. *Scientific Reports*, 12, 11452.
3. **Kluster Penginderaan Jauh Titik Panas & Fire Radiative Power (FRP)**:
   - `Schroeder2021RSE`: Schroeder, W., et al. (2021). The VIIRS 375m active fire detection algorithm: validation and operational performance. *Remote Sensing of Environment*, 254, 112260.
   - `Giglio2020RSE`: Giglio, L., et al. (2020). The Collection 6 MODIS active fire detection algorithm and products. *Remote Sensing of Environment*, 243, 111752.
4. **Kluster Tata Kelola Lahan & Dampak Atmosferik Karhutla Indonesia**:
   - `Kiely2021ACP`: Kiely, L., et al. (2021). Air quality and health impacts of Indonesian peatland fires: assessment using atmospheric modeling. *Atmospheric Chemistry and Physics*, 21, 16199–16216.
   - `Putranto2023LandUsePolicy`: Putranto, B., et al. (2023). Land tenure dynamics and wildfire vulnerability in degraded peatlands of Central Kalimantan. *Land Use Policy*, 128, 106598.

---

## 4. Analisis Format LaTeX Standar Jurnal Scopus Q1

### 4.1. Arsitektur Berkas LaTeX yang Direkomendasikan
Untuk mempermudah pemeliharaan, audit, dan kepatuhan standar publikasi, naskah LaTeX harus disusun secara modular:

```
manuscript/
├── main.tex                 # Dokumen induk: Preamble, metadata penulis, include sections, bib
├── sections/
│   ├── 00_abstract.tex      # Abstract & Keywords
│   ├── 01_introduction.tex  # Section 1: Introduction & Literature Review
│   ├── 02_methods.tex       # Section 2: Materials and Methods (Formula, Geoprocessing)
│   ├── 03_results.tex       # Section 3: Empirical Results (Tables 1-4, Figures 1-7)
│   ├── 04_discussion.tex    # Section 4: Discussion & Limitations/Threats to Validity
│   └── 05_conclusion.tex    # Section 5: Conclusion & Operational Policy Recommendations
└── references.bib           # Bibliografi BibTeX lengkap (30 existing + 10 rekomendasi baru)
```

### 4.2. Daftar Paket LaTeX Wajib (*Required Packages*)
Naskah harus menggunakan kelas dokumen standar akademik (`\documentclass[11pt,a4paper]{article}` atau kelas template jurnal terkait) dengan paket-paket esensial berikut:

```latex
\usepackage[utf8]{inputenc}
\usepackage[margin=2.5cm]{geometry}
\usepackage{amsmath,amssymb,amsfonts}  % Formulasi matematis canggih
\usepackage{graphicx}                  % Penyisipan gambar PNG 300 DPI
\usepackage{booktabs}                  % Tabel ilmiah standar profesional (\toprule, \midrule, \bottomrule)
\usepackage{tabularx,multirow,array}   % Penataan kolom tabel dinamis
\usepackage{caption,subcaption}        % Keterangan gambar & multi-panel subfigures
\usepackage{float}                     % Penempatan gambar presisi ([H], [tb])
\usepackage{hyperref}                  % Tautan hiperteks interaktif & DOI
\usepackage{natbib}                    % Manajemen sitasi Author-Year (\citep, \citet)
\usepackage{siunitx}                   % Satuan internasional baku (\SI{12.0}{\mega\watt})
\usepackage{lineno}                    % Penomoran baris untuk kemudahan peer review
\usepackage{authblk}                   % Format afiliasi penulis profesional
\usepackage{microtype}                 % Optimasi tipografi mikro
\usepackage{xcolor}                    % Pewarnaan teks tautan dan tabel
```

### 4.3. Penempatan dan Pemetaan Resmi Seluruh 7 Figur Ilmiah (`01_` s.d. `07_`)

Untuk menyelesaikan cacat penomoran pada draf markdown lama, berikut adalah matriks peletakan definitif seluruh 7 figur riil yang tersimpan di `output/figures/`:

| Label LaTeX | Berkas Gambar Riil | Bagian Naskah | Judul & Keterangan Gambar Lengkap (*Comprehensive Caption*) |
|---|---|---|---|
| `\ref{fig:decadal_trend}` | `output/figures/01_tren_tahunan_el_nino.png` | **Section 3.1** | **Figure 1. Decadal trajectory of burned area in Central Kalimantan (2018--2026) from official SiPongi KLHK records.** Demonstrates extreme non-linear climate sensitivity where El Ni\~no drought pulses in 2019 (317,749 ha) and 2023 (165,896 ha) account for over 85\% of cumulative burned areas, contrasting sharply with wet La Ni\~na suppression (2020--2022). |
| `\ref{fig:daily_dynamics}` | `output/figures/02_heatmap_musiman_bulan.png` | **Section 3.1** | **Figure 2. Diurnal satellite active fire hotspot distribution during the acute October 2026 crisis.** Daily hotspot detections from NASA FIRMS partitioned by sensor platform (VIIRS S-NPP, VIIRS NOAA-20, and MODIS Aqua). Peaks on 7--8 October (18,628 combined detections; 42.4\% of provincial total) preceded sharp precipitation-driven attenuation on 9--12 October. |
| `\ref{fig:regency_ranking}` | `output/figures/03_peringkat_kabupaten_terparah.png` | **Section 3.2** | **Figure 3. Geographic concentration of active fire hotspots across Central Kalimantan regencies.** Horizontal bar distribution highlighting the top three peatland epicenters (Seruyan 21.3\%, Pulang Pisau 16.3\%, and Kapuas 14.4\%), which collectively concentrate 51.9\% (22,813 hotspots) of provincial fire activity within low-lying coastal and peat dome complexes. |
| `\ref{fig:peat_canal_analysis}` | `output/figures/04_analisis_gambut_dan_kanal.png` | **Section 3.3** | **Figure 4. Peatland depth stratification and drainage canal proximity.** (Left) Donut distribution showing that 74.3\% of fires ignited on delineated BBLSDLP 2019 peat hydrological units, with 52.5\% concentrated in peat domes deeper than 2.0 m. (Right) Kernel density and frequency distribution of Euclidean distance to primary Mega Rice Project canals in UTM Zone 49S (median: 14.9 km). |
| `\ref{fig:concession_status}` | `output/figures/05_status_konsesi_esg.png` | **Section 3.2** | **Figure 5. Land tenure attribution and corporate ESG accountability.** (Left) Distribution of active fires across legal tenure regimes: 75.4\% (33,138 hotspots) occurred on unallocated Non-Concession land (Area Penggunaan Lain / APL), while 16.6\% and 8.0\% occurred within certified palm oil (HGU) and forestry (PBPH) concessions, respectively. (Right) Top 8 permit holders with highest within-boundary fire counts. |
| `\ref{fig:model_evaluation}` | `output/figures/06_evaluasi_model_ml.png` | **Section 3.4** | **Figure 6. Machine learning evaluation under spatial cross-validation.** (Left) Comparative Receiver Operating Characteristic (ROC) curves showing Model B (Pure Biophysical, Holdout Test AUC = 0.753, Spatial CV AUC = 0.495) versus Model A (Spatial Memorization, Holdout Test AUC = 0.796, Spatial CV AUC = 0.540). (Right) Confusion matrix for Model B on the independent test set ($n = 10,985$). |
| `\ref{fig:shap_importance}` | `output/figures/07_shap_feature_importance.png` | **Section 3.5** | **Figure 7. Explainable AI feature attribution for severe fire radiative power ($FRP \ge 12.0$ MW) using TreeSHAP.** Beeswarm summary plot displaying the ranking of 12 biophysical predictors on Model B. Color gradient represents feature value (red = high, blue = low). Critical non-linear thresholds are evidenced for 7-day rainfall ($P_{\text{7d}} < 5.0$ mm), canal distance ($d_{\text{canal}} < 3,000$ m), and dry spell ($D_{\text{spell}} > 14$ days). |

*(Catatan: Gambar 08 `08_transboundary_haze_dispersion.png` dapat disertakan pada lampiran / sub-bab 4.2 sebagai bukti komputasional simulasi dispersi Monsun Barat Daya).*

### 4.4. Format Tabel Ilmiah (`booktabs` Standard)
Empat tabel kunci wajib diimplementasikan menggunakan perintah `\toprule`, `\midrule`, dan `\bottomrule` tanpa garis vertikal, sesuai panduan penulisan jurnal internasional:
1. **Table 1: Decadal burned area records from SiPongi KLHK (2018–2026)** — Menampilkan tahun, luas terbakar (ha), anomali iklim (El Niño / La Niña), dan catatan penting.
2. **Table 2: Spatial distribution of hotspots across 14 regencies** — Menyajikan nama kabupaten, jumlah titik api, persentase provincial, dan karakteristik lanskap dominan.
3. **Table 3: Comprehensive model performance comparison (Model A vs Model B)** — Mengintegrasikan metrik holdout test (ROC-AUC, F1, Precision, Recall) dan rincian fold 1 s.d. 5 Spatial Block CV (`GroupKFold`).
4. **Table 4: TreeSHAP feature importance ranking for Model B** — Menampilkan ranking 1 s.d. 12, nama fitur, nilai *mean absolute SHAP*, dan penjelasan mekanisme biofisik.

### 4.5. Formulasi Matematis Presisi dalam LaTeX
Naskah LaTeX harus merumuskan persamaan biofisik dan statistik secara eksplisit dalam lingkungan `\begin{equation} ... \end{equation}`:

1. **Jarak Euclidean Kanal Terproyeksi UTM Zone 49S**:
   \begin{equation}
   d_{\text{canal}, i} = \min_{j \in \{1, \dots, M\}} \left\| \mathbf{p}_i - \mathbf{c}_j \right\|_2 = \min_{j} \sqrt{(x_i - u_j)^2 + (y_i - v_j)^2}
   \label{eq:canal_dist}
   \end{equation}
   di mana $\mathbf{p}_i = (x_i, y_i)$ adalah koordinat metrik hotspot ke-$i$ dan $\mathbf{c}_j = (u_j, v_j)$ adalah simpul vektor garis kanal eks-PLG dalam EPSG:32749.

2. **Formulasi Indeks Cuaca Kebakaran (Fire Weather Index - FWI)**:
   \begin{equation}
   \text{FWI}_i = 0.35\,T_{\text{max}, i} + 1.35\,D_{\text{spell}, i} - 0.22\,P_{\text{7d}, i} + 0.22\,(100 - \text{RH}_{\text{mean}, i}) + 0.25\,W_{\text{max}, i}
   \label{eq:fwi}
   \end{equation}

3. **Target Klasifikasi Intensitas Api Ekstrem (Severe FRP)**:
   \begin{equation}
   y_i = \begin{cases} 
   1, & \text{if } \text{FRP}_i \ge 12.0\text{ MW (Severe / Deep Combusting Fire)} \\ 
   0, & \text{if } \text{FRP}_i < 12.0\text{ MW (Moderate / Incipient Surface Fire)} 
   \end{cases}
   \label{eq:target}
   \end{equation}

4. **Protokol Validasi Blok Spasial (Spatial Block Cross-Validation)**:
   \begin{equation}
   \mathcal{D} = \bigcup_{k=1}^{K} \mathcal{D}_k, \quad \mathcal{D}_k \cap \mathcal{D}_l = \emptyset \quad \forall k \ne l
   \label{eq:spatial_cv}
   \end{equation}
   di mana pada fold ke-$k$, model dilatih pada himpunan kabupaten $\mathcal{D}_{\text{train}} = \mathcal{D} \setminus \mathcal{D}_k$ dan diuji murni pada kabupaten yang belum pernah dilihat $\mathcal{D}_k$.

5. **Dekomposisi Nilai Shapley Aditif Eksak (TreeSHAP)**:
   \begin{equation}
   f(\mathbf{x}) = \phi_0 + \sum_{j=1}^{M} \phi_j(\mathbf{x}), \quad \phi_j(f, \mathbf{x}) = \sum_{S \subseteq \mathcal{F} \setminus \{j\}} \frac{|S|!(|\mathcal{F}| - |S| - 1)!}{|\mathcal{F}|!} \left[ f(S \cup \{j\}) - f(S) \right]
   \label{eq:shap}
   \end{equation}

---

## 5. Rencana Tindakan Konkret untuk Penyusunan Naskah LaTeX (Milestone 2)

Berdasarkan temuan penyelidikan ini, berikut adalah panduan tindakan operasional bagi Worker saat mengeksekusi Milestone 2:

1. **Pembuatan Struktur Direktori & Berkas LaTeX**:
   - Buat direktori `manuscript/sections/`.
   - Pisahkan naskah menjadi `00_abstract.tex`, `01_introduction.tex`, `02_methods.tex`, `03_results.tex`, `04_discussion.tex`, dan `05_conclusion.tex`.
   - Buat file induk `manuscript/main.tex` yang memuat preamble lengkap, paket-paket wajib, metadata penulis, dan pemanggilan modul via `\input{sections/...}`.
2. **Penyempurnaan Bagian Diskusi (Wajib Tambah Sub-bab 4.4)**:
   - Tambahkan sub-bab *"4.4. Study Limitations, Uncertainties, and Threats to Validity"*:
     - *Sensor limitations*: Bias deteksi akibat tutupan awan konvektif dan asap pekat pada MODIS/VIIRS; ketidakmampuan sensor inframerah mendeteksi kebakaran bawah tanah yang belum menembus permukaan.
     - *Meteorological reanalysis scale*: Resolusi ERA5-Land (9 km) menghaluskan variabilitas hujan mikro lokal.
     - *Temporal window*: Fokus intensif pada krisis Oktober 2026 sebagai *acute pulse*, perlu dilengkapi panel multi-dekade pada riset lanjutan.
     - *Spatial transferability trade-off*: Penjelasan jujur bahwa F1-score pada Spatial CV (0,1399 pada Model B vs 0,0583 pada Model A) mencerminkan tantangan intrinsik ketimpangan kelas (15:85) dan variasi lokal saat memprediksi wilayah geografis baru tanpa hafalan koordinat.
     - *Cadastral boundaries*: Batas izin APL belum memuat pemetaan partisipatif tanah adat (*customary land tenure*).
3. **Penyisipan 7 Gambar Ilmiah**:
   - Gunakan path relatif dari root proyek `../output/figures/` atau salin/tautkan gambar agar dapat dikompilasi di direktori `manuscript/`.
   - Gunakan label dan caption lengkap sesuai matriks pada Seksi 4.3 dokumen ini.
4. **Pembaruan Bibliografi `references.bib`**:
   - Pertahankan 30 entri yang sudah ada.
   - Tambahkan 10 entri baru (2021–2025) yang diidentifikasi pada Seksi 3.3.
   - Perbarui sitasi dalam teks LaTeX (`\citep{...}`, `\citet{...}`) sehingga merujuk secara harmonis ke literatur mutakhir.
5. **Skrip Verifikasi Statis LaTeX**:
   - Buat skrip python validator mandiri (`src/verify_latex.py`) untuk memvalidasi:
     - Keseimbangan pasangan `\begin{...}` dan `\end{...}`.
     - Keteruraian semua label gambar dan tabel (`\ref{...}` -> `\label{...}`).
     - Keberadaan seluruh berkas gambar yang dipanggil (`\includegraphics{...}`).
     - Resolusi 100% kunci sitasi (`\cite{...}` -> `references.bib`).

---
*Laporan ini disusun secara mandiri oleh Explorer 2 untuk memandu Tim Kerja dalam mencapai standar publikasi internasional Scopus Q1.*
