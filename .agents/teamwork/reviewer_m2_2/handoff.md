# Laporan Telaah Sejawat & Adversarial Review (Reviewer 2 - Milestone 2)
**Naskah Publikasi LaTeX Scopus Q1: Analisis Spasiotemporal Karhutla Kalteng**

---

## 1. Observation (Pengamatan Faktual)

### 1.1. Status Integritas Figur Ilmiah (01_ s.d. 07_)
- **Keberadaan Berkas Fisik**:
  - `output/figures/01_tren_tahunan_el_nino.png` (256.196 bytes) — ADA.
  - `output/figures/02_heatmap_musiman_bulan.png` (207.114 bytes) — ADA.
  - `output/figures/03_peringkat_kabupaten_terparah.png` (267.669 bytes) — ADA.
  - `output/figures/04_analisis_gambut_dan_kanal.png` (331.385 bytes) — ADA.
  - `output/figures/05_status_konsesi_esg.png` (257.957 bytes) — ADA.
  - `output/figures/06_evaluasi_model_ml.png` (335.653 bytes) — ADA.
  - `output/figures/07_shap_feature_importance.png` (521.558 bytes) — ADA.
- **Penyematan dalam Kode LaTeX (`manuscript/sections/03_results.tex`)**:
  - `Figure 1`: baris 33--38, `\includegraphics[width=0.92\textwidth]{01_tren_tahunan_el_nino.png}`, `\label{fig:decadal_trend}`, dirujuk pada baris 7 via `Figure~\ref{fig:decadal_trend}`.
  - `Figure 2`: baris 44--49, `\includegraphics[width=0.92\textwidth]{02_heatmap_musiman_bulan.png}`, `\label{fig:daily_dynamics}`, dirujuk pada baris 42 via `Figure~\ref{fig:daily_dynamics}`.
  - `Figure 3`: baris 82--87, `\includegraphics[width=0.92\textwidth]{03_peringkat_kabupaten_terparah.png}`, `\label{fig:regency_ranking}`, dirujuk pada baris 56 via `Figure~\ref{fig:regency_ranking}`.
  - `Figure 4`: baris 96--101, `\includegraphics[width=0.92\textwidth]{04_analisis_gambut_dan_kanal.png}`, `\label{fig:peat_canal_analysis}`, dirujuk pada baris 94 via `Figure~\ref{fig:peat_canal_analysis}`.
  - `Figure 5`: baris 119--124, `\includegraphics[width=0.92\textwidth]{05_status_konsesi_esg.png}`, `\label{fig:concession_status}`, dirujuk pada baris 117 via `Figure~\ref{fig:concession_status}`.
  - `Figure 6`: baris 168--173, `\includegraphics[width=0.92\textwidth]{06_evaluasi_model_ml.png}`, `\label{fig:model_evaluation}`, dirujuk pada baris 138 via `Figure~\ref{fig:model_evaluation}`.
  - `Figure 7`: baris 211--216, `\includegraphics[width=0.92\textwidth]{07_shap_feature_importance.png}`, `\label{fig:shap_importance}`, dirujuk pada baris 184 via `Figure~\ref{fig:shap_importance}`.
- **Ketiadaan Diagram ASCII Art**:
  - Penelusuran pola ASCII art (`+---`, `|   |`, `----+`, `===>`) pada seluruh berkas `.tex` di `manuscript/` menghasilkan 0 kemunculan. Naskah 100% menggunakan grafik PNG beresolusi tinggi (300 DPI) asli hasil pipeline analisis data.

### 1.2. Formulasi Matematika & Tabel Standar Scopus Q1
- **Persamaan 1 s.d. 5**:
  - **Persamaan 1** (`manuscript/sections/02_materials_methods.tex`: baris 53--56, `\label{eq:canal_dist}`): Formulasi jarak Euclidean minimum ke verteks vektor kanal eks-PLG dalam proyeksi metrik UTM Zona 49S ($EPSG:32749$):
    $$d_{\text{canal}, i} = \min_{j \in \{1, \dots, M\}} \left\| \mathbf{p}_i - \mathbf{c}_j \right\|_2 = \min_{j} \sqrt{(x_i - u_j)^2 + (y_i - v_j)^2}$$
    Lengkap dengan indikator lanskap biner zonasi eks-PLG (`eq:ex_plg`, baris 60--66).
  - **Persamaan 2** (`manuscript/sections/02_materials_methods.tex`: baris 84--87, `\label{eq:fwi}`): Indeks Bahaya Kebakaran terkalibrasi adaptasi Canadian FWI / BMKG:
    $$\text{FWI}_i = 0.35\,T_{\text{max}, i} + 1.35\,D_{\text{spell}, i} - 0.22\,P_{\text{7d}, i} + 0.22\,(100 - \text{RH}_{\text{mean}, i}) + 0.25\,W_{\text{max}, i}$$
  - **Persamaan 3** (`manuscript/sections/02_materials_methods.tex`: baris 147--153, `\label{eq:target}`): Target biner intensitas radiasi ekstrim ($FRP \ge 12.0\text{ MW}$), dilengkapi dengan formulasi inverse class weighting (`eq:class_weight`, baris 157--160, $w_1 \approx 3.3045, w_0 \approx 0.5891$).
  - **Persamaan 4** (`manuscript/sections/02_materials_methods.tex`: baris 189--192, `\label{eq:spatial_cv}`): Partisi spasial formal Spatial Block Cross-Validation ($\mathcal{D} = \bigcup_{k=1}^K \mathcal{D}_k, \mathcal{D}_k \cap \mathcal{D}_l = \emptyset$) dengan rincian alokasi 5 fold per kabupaten.
  - **Persamaan 5** (`manuscript/sections/02_materials_methods.tex`: baris 209--212, `\label{eq:shap}`): Dekomposisi aditif nilai Shapley eksak algoritma TreeSHAP ($f(\mathbf{x}) = \phi_0 + \sum_{j=1}^M \phi_j(\mathbf{x})$).
- **Format Tabel**:
  - Kelima tabel (`tab:feature_inventory`, `tab:decadal_sipongi`, `tab:regency_distribution`, `tab:model_comparison`, `tab:shap_ranking`) 100% menggunakan format `booktabs` (`\toprule`, `\midrule`, `\bottomrule`) tanpa garis vertikal (`|`).

### 1.3. Bibliografi dan Cakupan Literatur Primer 2021--2025
- Berkas `manuscript/references.bib` memuat tepat 40 entri BibTeX bereputasi tinggi.
- 100% dari 40 entri BibTeX disitasi aktif dalam teks (0 undefined keys, 0 unused keys).
- Cakupan literatur primer 2021--2025 mencakup:
  - Meyer & Pebesma (2021, *Nature Communications*) — Area of Applicability & spatial cross-validation.
  - Wadoux et al. (2021, *Ecological Modelling*) — Spatial prediction & CV debate.
  - Dadap et al. (2021, *Nature Communications*) — Peatland water table satellite remote sensing.
  - Graham et al. (2022, *Scientific Reports*) — Peatland hydrological restoration & fire.
  - Schroeder et al. (2021, *Remote Sensing of Environment*) — VIIRS 375m active fire algorithm.
  - Kiely et al. (2021, *Atmospheric Chemistry and Physics*) — Peat fire emissions & air quality.
  - Putranto et al. (2023, *Land Use Policy*) — Peatland land tenure governance in Central Kalimantan.

### 1.4. Temuan Kritis Adversarial (Uji Kompilasi Riil & Tipografi)
- **Error Kompilasi Fatal pada `manuscript/main.tex`**:
  Saat diuji kompilasi nyata menggunakan compiler LaTeX modern (`/opt/homebrew/bin/tectonic main.tex` dari direktori `manuscript/`), kompilasi **GAGAL TOTAL** dengan pesan galat:
  ```text
  error: main.tex:56: LaTeX Error: Undefined color 'blue!70!black'.
  error: halted on potentially-recoverable error as specified
  ```
  **Akar Masalah**: Pada `main.tex` baris 13:
  `\usepackage[colorlinks=true,linkcolor=blue!70!black,citecolor=blue!70!black,urlcolor=blue!70!black]{hyperref}`
  Sintaks pencampuran warna (`blue!70!black`) adalah fitur dari paket `xcolor`. Namun, `main.tex` **TIDAK memuat `\usepackage{xcolor}`**, sehingga saat perintah `\url{...}` dieksekusi di baris 56, TeX engine menghentikan kompilasi karena warna tidak terdefinisi.
- **Konfirmasi Solusi Uji**:
  Setelah membuat salinan uji di `.agents/teamwork/reviewer_m2_2/test_build/` dan menambahkan `\usepackage{xcolor}` di atas `hyperref`, naskah berhasil dikompilasi sempurna menjadi dokumen PDF setebal **24 halaman** (`main.pdf`, 2.236.950 bytes).
- **Overfull `\hbox` pada Tabel & Persamaan Panjang**:
  Hasil log kompilasi menunjukkan teks meluap melampaui margin kertas A4 pada elemen-elemen berikut:
  1. `sections/02_materials_methods.tex:136`: Overfull `\hbox` (180.85 pt) pada Tabel 1 (`tab:feature_inventory`) karena kolom ke-4 dan ke-5 tidak memiliki pembatas lebar (`p{...}`).
  2. `sections/02_materials_methods.tex:172`: Overfull `\hbox` (105.12 pt) pada Persamaan 6 (`eq:features_a`) karena daftar 15 variabel prediktor ditulis mendatar dalam satu baris panjang.
  3. `sections/03_results.tex:29`: Overfull `\hbox` (126.62 pt) pada Tabel 2 (`tab:decadal_sipongi`).
  4. `sections/03_results.tex:80`: Overfull `\hbox` (106.58 pt) pada Tabel 3 (`tab:regency_distribution`).
  5. `sections/03_results.tex:166`: Overfull `\hbox` (208.98 pt) pada Tabel 4 (`tab:model_comparison`).
  6. `sections/03_results.tex:209`: Overfull `\hbox` (44.53 pt) pada Tabel 5 (`tab:shap_ranking`).

---

## 2. Logic Chain (Rantai Inferensi Logis)

1. **Premis 1 (Standar Publikasi Scopus Q1)**: Sebuah naskah publikasi LaTeX dikatakan *publication-ready* hanya jika naskah tersebut dapat dikompilasi secara deterministik (*zero fatal error*) oleh TeX engine standar, dan tabel/persamaannya tertata rapi dalam batas margin cetak jurnal.
2. **Premis 2 (Otentisitas & Bebas Pelanggaran Integritas)**:
   - Pengujian `tests/test_empirical_metrics.py` memverifikasi 100% metrik (Holdout ROC-AUC Model A 0.7956 vs Model B 0.7527, Spatial CV F1 0.0583 vs 0.1399, matriks konfusi TN=6586, FP=2737, FN=568, TP=1094, 75.4% APL, 16.6% Sawit, 8.0% PBPH, jarak kanal 14.946 m) sepenuhnya otentik dan selaras dengan hasil eksekusi model nyata.
   - Tidak ditemukan pemalsuan data, hardcoded cheat, maupun implementasi fasad (ASCII art telah dihilangkan total).
3. **Premis 3 (Galat Kompilasi TeX)**:
   - Karena `\usepackage{xcolor}` tidak dideklarasikan di `main.tex`, compiler TeX tidak dapat menyelesaikan definisi warna `blue!70!black` pada paket `hyperref`.
   - Ini mengakibatkan proses pembentukan PDF terhenti seketika (*aborted*).
   - Selain itu, ketiadaan batasan lebar kolom spesifik (`p{...}`) pada tabel menyebabkan teks tabel terpotong di tepi kanan halaman cetak (overfull hbox hingga 208 pt).
4. **Deduksi**:
   - Meskipun substansi ilmiah, metodologi, dan data empiris naskah sangat unggul dan memenuhi kriteria Scopus Q1, naskah `manuscript/main.tex` yang ada saat ini secara teknis *tidak dapat dikompilasi* sebelum `\usepackage{xcolor}` ditambahkan, dan tabelnya harus diperbaiki agar tidak meluap keluar margin.

---

## 3. Caveats (Batasan Telaah)

- Pengujian kompilasi TeX dilakukan menggunakan TeX engine modern `tectonic` yang kompatibel dengan XeTeX/pdfTeX. Pada lingkungan TeX Live lengkap yang memuat `xcolor` melalui paket lain secara implisit (misal jika `xcolor` dimuat oleh dokumen kelas tertentu), galat tersebut mungkin tidak muncul, namun pada dokumen kelas standar `article`, deklarasi eksplisit `\usepackage{xcolor}` adalah keharusan mutlak portabilitas.
- Reviewer tidak melakukan modifikasi langsung pada berkas naskah asli di `manuscript/` karena mematuhi batas peran review (*Review-only: do NOT modify implementation code*).

---

## 4. Conclusion & Findings (Vonis Akhir)

**Vonis Akhir**: **`REQUEST_CHANGES`**

### Daftar Temuan (Actionable Findings):

#### [Critical - Must Fix] Temuan 1: Ketiadaan `\usepackage{xcolor}` Menggagalkan Kompilasi TeX
- **Lokasi**: `manuscript/main.tex` (baris 3--14).
- **Masalah**: Penggunaan `blue!70!black` pada argumen `hyperref` memicu galat fatal: `LaTeX Error: Undefined color 'blue!70!black'` saat perintah `\url{...}` dipanggil pada baris 56.
- **Rekomendasi Perbaikan**: Tambahkan `\usepackage{xcolor}` pada *preamble* `manuscript/main.tex` sebelum deklarasi `hyperref`.

#### [Major - Should Fix] Temuan 2: Overfull `\hbox` pada Seluruh Tabel dan Persamaan 6
- **Lokasi**:
  - `manuscript/sections/02_materials_methods.tex` (Tabel 1 baris 112 dan Persamaan 6 baris 170).
  - `manuscript/sections/03_results.tex` (Tabel 2 baris 14, Tabel 3 baris 63, Tabel 4 baris 145, dan Tabel 5 baris 191).
- **Masalah**: Kolom deskripsi naratif pada tabel didefinisikan dengan tipe `l` (left-aligned tak terbatas), sehingga teks membentang hingga 208 pt (~7,3 cm) keluar dari batas kertas A4. Persamaan 6 juga melebihi margin kanan sebesar 105 pt.
- **Rekomendasi Perbaikan**:
  1. Ganti kolom deskripsi dengan kolom berukuran tetap, misalnya `p{6cm}` atau gunakan lingkungan `tabularx`.
  2. Pecah Persamaan 6 (`eq:features_a`) menjadi dua baris menggunakan lingkungan `\begin{split}` atau `multline`.

---

## 5. Verification Method (Metode Verifikasi Ulang)

Untuk memverifikasi bahwa perubahan telah berhasil diterapkan oleh Agen Penulis/Penyusun:

1. **Verifikasi Statis Berkas**:
   ```bash
   /opt/anaconda3/envs/karhutla_env/bin/python tests/verify_latex.py
   ```
2. **Verifikasi Kompilasi TeX Nyata**:
   ```bash
   cd /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/manuscript
   /opt/homebrew/bin/tectonic main.tex
   ```
   *Kondisi Keberhasilan*: Perintah selesai dengan kode keluar 0 (`exit code 0`), menghasilkan berkas `manuscript/main.pdf` tanpa galat `Undefined color`.
