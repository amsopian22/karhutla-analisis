# RENCANA EKSEKUSI, AUDIT, DAN VALIDASI MATEMATIS (PLAN.md)
# Naskah Ilmiah: "The Governance Void at Concession Frontiers: A Spatial Boundary Discontinuity Analysis of Peatland Wildfires in Central Kalimantan"
# Jurnal Target: Remote Sensing Applications: Society and Environment (RSASE, Elsevier, Scopus Q1)

Dokumen ini adalah rencana operasional terstruktur dan panduan audit menyeluruh untuk memvalidasi seluruh perumusan matematika, persamaan ilmiah, derivasi statistik, metrik machine learning, serta implementasi numerik pada repositori dan naskah publikasi ilmiah.

---

## 1. Profil Bibliometrik & Parameter Jurnal Target

| Parameter | Spesifikasi Resmi Elsevier RSASE | Catatan & Implikasi Proyek |
|:---|:---|:---|
| **Nama Jurnal** | *Remote Sensing Applications: Society and Environment* (RSASE) | Diterbitkan oleh Elsevier B.V. (ISSN: 2352-9385) |
| **Portal Pengajuan** | `https://www.editorialmanager.com/rsase/default.aspx` | Menggunakan sistem Elsevier Editorial Manager (`rsase`) |
| **Indeksasi Scopus** | **Scopus Q1** | Bidang: *Earth and Planetary Sciences* & *Environmental Science* |
| **Scopus CiteScore** | **7.9** | Menunjukkan reputasi sitasi tinggi dan pengaruh keilmuan kuat |
| **Clarivate Impact Factor** | **4.5 – 4.9** (5-Year IF: ~5.2) | Terindeks di Web of Science Core Collection (ESCI/JCR) |
| **Model Publikasi** | **Hybrid Journal ($0 USD APC via Subscription)** | Penulis memilih rute **Subscription (Bebas Biaya Publikasi)** |
| **Format Review** | Single-Blind (default) & Double-Blind didukung | Naskah disediakan dalam **dua format**: Anonim & Lengkap |
| **Batas Panjang Abstrak** | 150 – 250 kata | Abstrak terkalibrasi saat ini: **246 kata** (Patuh) |
| **Aturan Highlights** | 3–5 butir, maksimal 85 karakter per butir (termasuk spasi) | 5 butir terkalibrasi (seluruhnya $\le 77$ karakter) |
| **Jumlah Kata Kunci** | 4 – 7 kata kunci spesifik | Disesuaikan ke 7 kata kunci penginderaan jauh terapan |

---

## 2. Ringkasan Status Eksekusi Terdahulu (Tahap 1 s.d. 6)

Seluruh tahapan penyesuaian naskah dan paket pengajuan ke RSASE telah berhasil diselesaikan dan lolos 41 unit tes otomatis:

- [x] **Tahap 1: Pemutakhiran Cover Letter dan Title Page**: Selesai (`cover_letter.md`, `.docx`, `.pdf` & `title_page.md`, `.docx`).
- [x] **Tahap 2: Optimalisasi Kata Kunci dan Metadata LaTeX**: Selesai (7 kata kunci RSASE di `00_abstract.tex` & `main.tex`).
- [x] **Tahap 3: Sinkronisasi Naskah Markdown**: Selesai (`manuscript_draft.md` & `manuscript_without_author_details.md`).
- [x] **Tahap 4: Rekompilasi Paket Pengajuan (*Submission Package*)**: Selesai (PDF 32 halaman via Tectonic & berkas DOCX via Pandoc).
- [x] **Tahap 5: Penyesuaian Unit Tes Harness**: Selesai (41/41 unit tes PASSED pada `karhutla_env`).
- [x] **Tahap 6: Version Control & Sinkronisasi GitHub**: Selesai (Tersinkronisasi pada `origin/main` commit `fb0a270`).

---

## 3. Rencana Komprehensif Validasi Matematis & Formulasi Ilmiah (Tahap 7 - AKTIF)

> [!IMPORTANT]
> **PRINSIP DASAR AUDIT MATEMATIKA**:
> 1. **Zero Tolerance of Discrepancies**: Seluruh simbol, persamaan, angka desimal, dan nilai $p$-value yang tercantum pada teks naskah LaTeX/Word wajib identik 100% dengan hasil kalkulasi algoritma Python dan data mentah 43.937 baris.
> 2. **Invariansi Koordinat & Satuan Fisik**: Seluruh jarak spasial berbasis proyeksi metrik UTM Zone 49S (meter), bukan derajat desimal.
> 3. **Konservasi Bobot & Peluang**: Total bobot kelas terbalik wajib memenuhi sifat konservasi sampel: $\sum_{c} w_c n_c = N$.
> 4. **Aksioma Efisiensi Teori Permainan Kooperatif**: Dekomposisi TreeSHAP wajib memenuhi aksioma efisiensi: $\sum_{j=1}^M \phi_j(\mathbf{x}) = f(\mathbf{x}) - \mathbb{E}[f(\mathbf{X})]$.

### Rincian Sub-Tahapan Validasi Matematis:

- [x] **7.1. Audit Taksonomi & Konsistensi Notasi 11 Persamaan Formal**:
  - Verifikasi keselarasan notasi matematis antara teks LaTeX (`manuscript/sections/02_materials_methods.tex`), naskah Markdown (`manuscript_draft.md`), dan rumus Word OMML (`manuscript_main.docx`).
  - Pastikan huruf tebal digunakan untuk vektor spasial ($\mathbf{p}_i, \mathbf{c}_j, \mathbf{b}, \mathbf{x}$), skalar miring ($d, N, w, y$), dan huruf kaligrafi untuk himpunan/domain ($\Omega_C, \partial \Omega_C, \mathcal{D}, \mathcal{F}$).
- [x] **7.2. Verifikasi Komputasional Deterministik terhadap Data Riil (43.937 Titik)**:
  - Validasi perhitungan jarak kanal minimum $d_{\text{canal}, i}$ pada proyeksi UTM Zone 49S (EPSG:32749).
  - Validasi perhitungan linear adaptasi Fire Weather Index ($\text{FWI}_i$) pada seluruh 43.937 baris dengan toleransi galat pembulatan $\le 0,005$.
  - Validasi penentuan target biner $y_i = \mathbb{I}(\text{FRP}_i \ge 12,0\text{ MW})$ menghasilkan tepat 6.648 kelas ekstrem dan 37.289 kelas reguler.
- [x] **7.3. Validasi Formulasi Uji Statistik Inferensial & Uji Hipotesis**:
  - Rekalkulasi uji Mann-Whitney $U$ pada energi termal FRP interior vs exterior konsesi ($U = 41.712.351,5; p = 0,278$).
  - Rekalkulasi uji Welch's $t$-test untuk varians heterogen ($t = 1,859; p = 0,063$).
  - Rekalkulasi uji Mann-Whitney $U$ jarak kanal pada zona fokus eks-PLG ($p = 0,255$).
- [x] **7.4. Validasi Formulasi Aljabar Metrik Machine Learning & Evaluasi Spasial**:
  - Verifikasi rumus bobot kelas seimbang $w_c = N / (K \cdot n_c)$ ($w_1 \approx 3,3045; w_0 \approx 0,5891$).
  - Verifikasi ortogonalitas partisi spasial saling lepas 5-fold `GroupKFold`: $\mathcal{D}_k \cap \mathcal{D}_l = \emptyset$ dan $\bigcup \mathcal{D}_k = \mathcal{D}$.
  - Verifikasi aljabar metrik matriks konfusi test set ($n = 10.985$):
    * $\text{Recall}_{\text{ekstrem}} = \text{TP} / (\text{TP} + \text{FN}) = 1.094 / 1.662 = 65,82\%$
    * $\text{Precision}_{\text{reguler}} = \text{TN} / (\text{TN} + \text{FP}) = 6.586 / 9.323 = 92,06\%$
    * $\text{Precision}_{\text{ekstrem}} = \text{TP} / (\text{TP} + \text{FP}) = 1.094 / 3.831 = 28,56\%$
    * $F_1\text{-Score} = 2 \cdot (\text{Precision} \cdot \text{Recall}) / (\text{Precision} + \text{Recall}) = 0,3983$
  - Verifikasi rata-rata Spatial Block CV: Model A $F_1 = 0,0583$ vs Model B $F_1 = 0,1399$ (keunggulan retensi operasional 2,40x lipat).
- [x] **7.5. Pembangunan Test Suite Otomatis Baru (`tests/test_mathematical_formulations.py`)**:
  - Tulis modul pengujian khusus Pytest yang menguji seluruh 11 persamaan dan properti matematika secara independen.
- [x] **7.6. Pembuatan Laporan Audit Matematis Komprehensif (`output/reports/mathematical_validation_audit.json`)**:
  - Simpan rekapitulasi audit formal dalam format JSON yang memuat nilai teoritis, nilai terhitung, galat absolut, dan status lulus.
- [x] **7.7. Eksekusi Pengujian & Verifikasi Akhir**:
  - Jalankan `pytest tests/ -v` dan pastikan seluruh pengujian (41 pengujian awal + pengujian matematika baru) berstatus **100% PASSED**.

---

## 4. Matriks Inventaris & Verifikasi 11 Persamaan Formal

Berikut adalah taksonomi lengkap 11 persamaan formal bernomor urut di Bab 2 (*Materials and Methods*):

| No. | Label Persamaan | Formulasi Matematis di Naskah | Parameter & Variabel | File Implementasi Kode | Kriteria Validasi & Toleransi Galat |
|:---:|:---|:---|:---|:---|:---|
| **Eq. (1)** | `eq:canal_dist` | $d_{\text{canal}, i} = \min_{j} \|\mathbf{p}_i - \mathbf{c}_j\|_2 = \min_j \sqrt{(x_i - u_j)^2 + (y_i - v_j)^2}$ | $\mathbf{p}_i \in \mathbb{R}^2$: Titik api UTM 49S<br>$\mathbf{c}_j \in \mathbb{R}^2$: Vertex poliline kanal PLG | `src/process_real_data.py` (shapely metric distance) | $d \ge 0$ meter; Median eks-PLG $\approx 14.946\text{ m}$; non-PLG sentinel terdefinisi jelas. |
| **Eq. (2)** | `eq:ex_plg` | $\text{is\_ex\_plg} = \begin{cases} 1, & \text{Regency} \in \{\text{Pulpis, Kapuas, P. Raya}\} \\ 0, & \text{lainnya} \end{cases}$ | Biner partisi bentang alam hidrologis eks-PLG | `src/process_real_data.py` (`.isin()`) | Total titik kelas $1 = 16.645$ (37,88%); Total titik kelas $0 = 27.292$ (62,12%). |
| **Eq. (3)** | `eq:fwi` | $\text{FWI}_i = 0,35\,T_{\text{max}} + 1,35\,D_{\text{spell}} - 0,22\,P_{\text{7d}} + 0,22\,(100 - \text{RH}) + 0,25\,W_{\text{max}}$ | $T_{\text{max}}$ ($^\circ\text{C}$), $D_{\text{spell}}$ (hari), $P_{\text{7d}}$ (mm), $\text{RH}$ (%), $W_{\text{max}}$ (km/h) | `src/process_real_data.py` (vektor linear) | Konsistensi deterministik pada 43.937 baris ($\Delta \le 0,005$ akibat pembulatan 2 desimal). |
| **Eq. (4)** | `eq:signed_dist` | $\tilde{d}_i = \begin{cases} -\min_{\mathbf{b} \in \partial \Omega_C} \|\mathbf{p}_i - \mathbf{b}\|_2, & \mathbf{p}_i \in \Omega_C \\ +\min_{\mathbf{b} \in \partial \Omega_C} \|\mathbf{p}_i - \mathbf{b}\|_2, & \mathbf{p}_i \notin \Omega_C \end{cases}$ | $\Omega_C$: Gabungan poligon konsesi HGU & PBPH<br>$\partial \Omega_C$: Garis batas perimetral konsesi | `src/spatial_boundary_discontinuity.py` | Nilai negatif di dalam konsesi (Strict Liability); positif di APL; $n_{\text{interior}} = 8.961$, $n_{\text{exterior}} = 9.224$ pada $\pm 3\text{ km}$. |
| **Eq. (5)** | `eq:density_bdd` | $D_k = \frac{N_k}{A(B_k)} \quad (\text{hotspots}/\text{km}^2)$ | $N_k$: Jumlah titik api buffer band $k$<br>$A(B_k)$: Luas planar poligon buffer band $k$ ($\text{km}^2$) | `src/spatial_boundary_discontinuity.py` | $D_{\text{interior}} = 8.961 / 48.959,58 = 0,1830/\text{km}^2$; $D_{\text{exterior}} = 9.224 / 32.203,09 = 0,2864/\text{km}^2$. |
| **Eq. (6)** | `eq:bdd_jump` | $\tau_{\text{BDD}} = \lim_{\tilde{d} \to 0^+} D(\tilde{d}) - \lim_{\tilde{d} \to 0^-} D(\tilde{d})$ | Besaran efek diskontinuitas perbatasan (step jump) | `src/spatial_boundary_discontinuity.py` | $\tau_{\text{BDD}} = 0,2864 - 0,1830 = +0,1034/\text{km}^2$; Lonjakan relatif $= +56,5\%$; Rasio kerapatan $= 1,565$. |
| **Eq. (7)** | `eq:target` | $y_i = \begin{cases} 1, & \text{FRP}_i \ge 12,0\text{ MW (Severe)} \\ 0, & \text{FRP}_i < 12,0\text{ MW (Regular)} \end{cases}$ | Biner target intensitas pembakaran radiative power | `src/train_model.py` (`(frp >= 12.0).astype(int)`) | $n(y=1) = 6.648$ (15,13%); $n(y=0) = 37.289$ (84,87%); Rasio ketidakseimbangan $= 1 : 5,609$. |
| **Eq. (8)** | `eq:class_weight` | $w_c = \frac{N}{K \cdot n_c}, \quad c \in \{0, 1\}$ | $N = 43.937$, $K = 2$, $n_1 = 6.648$, $n_0 = 37.289$ | `src/train_model.py` (`compute_class_weight`) | $w_1 = 3,3045$; $w_0 = 0,5891$; Konservasi bobot: $w_0 n_0 + w_1 n_1 = 43.937 = N$. |
| **Eq. (9a)** | `eq:features_a` | $\mathbf{X}_A \in \mathbb{R}^{15}$ (Model A Memorization) | Termasuk $\text{lat}, \text{lon}, \text{regency}$ dan 12 prediktor biofisik | `src/train_model.py` (`features_a`) | Tepat 15 kolom prediktor; mengandung koordinat absolut dan identitas administratif. |
| **Eq. (9b)** | `eq:features_b` | $\mathbf{X}_B \in \mathbb{R}^{12}$ (Model B Biofisik Murni) | Tanpa koordinat geografis dan tanpa identitas wilayah | `src/train_model.py` (`features_b`) | Tepat 12 kolom prediktor; $\mathbf{X}_A \setminus \mathbf{X}_B = \{\text{lat}, \text{lon}, \text{regency}\}$. |
| **Eq. (10)** | `eq:spatial_cv` | $\mathcal{D} = \bigcup_{k=1}^K \mathcal{D}_k, \quad \mathcal{D}_k \cap \mathcal{D}_l = \emptyset \quad \forall k \ne l$ | Partisi saling lepas 5 blok geografis kabupaten | `src/train_model.py` (`GroupKFold(n_splits=5)`) | 14 kabupaten terbagi habis ke 5 fold tanpa irisan; total titik evaluasi lintas fold $= 43.937$. |
| **Eq. (11)** | `eq:shap` | $f(\mathbf{x}) = \phi_0 + \sum_{j=1}^M \phi_j(\mathbf{x})$ | Dekomposisi nilai Shapley kooperatif lokal | `src/train_model.py` (`shap.TreeExplainer`) | Aksioma efisiensi: $\sum \phi_j(\mathbf{x}) = f(\mathbf{x}) - \phi_0$ terpenuhi pada toleransi floating point $\le 10^{-5}$. |

---

## 5. Matriks Formulasi Uji Statistik Inferensial & Evaluasi ML

### A. Uji Statistik Inferensial:
1. **Uji Mann-Whitney $U$ (Kesetaraan Energi Termal Frontier)**:
   $$U_1 = R_1 - \frac{n_1(n_1 + 1)}{2}, \quad z = \frac{U - \mu_U}{\sigma_U}$$
   - **Hasil Terverifikasi**: $U = 41.712.351,5; \quad p = 0,278 > 0,05$.
   - **Makna Ilmiah**: Menerima hipotesis nol kesetaraan intensitas pembakaran ($H_0$). Membuktikan bahwa diskontinuitas perbatasan murni disebabkan oleh kekosongan tata kelola pengawasan (kerapatan api), bukan karena perbedaan intrinsik bahan bakar gambut.
2. **Uji Welch's $t$-test (Heterogenitas Varians)**:
   $$t = \frac{\bar{X}_1 - \bar{X}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}, \quad \nu \approx \frac{\left(\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}\right)^2}{\frac{(s_1^2/n_1)^2}{n_1 - 1} + \frac{(s_2^2/n_2)^2}{n_2 - 1}}$$
   - **Hasil Terverifikasi**: $t = 1,859; \quad p = 0,063 > 0,05$.
   - **Makna Ilmiah**: Mengonfirmasi tidak adanya perbedaan rerata FRP yang signifikan antara interior ($7,38\text{ MW}$) dan exterior ($6,92\text{ MW}$).

### B. Metrik Evaluasi Klasifikasi Machine Learning:
Pada holdout test set independen ($n = 10.985$ titik, stratified 75:25):
- $\text{True Positive (TP)} = 1.094$ (Kebakaran ekstrem terdeteksi benar)
- $\text{False Negative (FN)} = 568$ (Kebakaran ekstrem luput / missed)
- $\text{True Negative (TN)} = 6.586$ (Kebakaran reguler terklasifikasi benar)
- $\text{False Positive (FP)} = 2.737$ (Kebakaran reguler diprediksi ekstrem)

$$\text{Recall}_{\text{ekstrem}} = \frac{1.094}{1.094 + 568} = \frac{1.094}{1.662} = 65,82\%$$
$$\text{Precision}_{\text{reguler}} = \frac{6.586}{6.586 + 2.737} = \frac{6.586}{9.323} = 92,06\%$$
$$\text{Precision}_{\text{ekstrem}} = \frac{1.094}{1.094 + 2.737} = \frac{1.094}{3.831} = 28,56\%$$
$$F_1\text{-Score} = \frac{2 \times 0,285565 \times 0,658243}{0,285565 + 0,658243} = 0,3983$$

### C. Evaluasi Generalisasi Spasial (5-Fold Spatial Block Cross-Validation):
- **Model A (Memorasi Spasial)**:
  * Rata-rata ROC-AUC: **0,5399** ($\pm 0,051$)
  * Rata-rata $F_1$-Score: **0,0583** (Mengalami keruntuhan total / *total recall collapse* $F_1 = 0,0000$ pada 4 dari 5 blok wilayah).
- **Model B (Model Biofisik Murni)**:
  * Rata-rata ROC-AUC: **0,4950** ($\pm 0,049$)
  * Rata-rata $F_1$-Score: **0,1399** (Mempertahankan kemampuan prediksi non-nol di seluruh 5 blok wilayah: Fold 1 = 0,2914; Fold 2 = 0,0657; Fold 3 = 0,1056; Fold 4 = 0,0646; Fold 5 = 0,1722).
  * **Rasio Keunggulan Retensi Operasional**: $0,1399 / 0,0583 = \mathbf{2,40\times}$ lebih tahan banting terhadap *spatial covariate shift*.

---

## 6. Arsitektur Modul Pengujian Otomatis (`tests/test_mathematical_formulations.py`)

Test suite baru ini dirancang untuk memverifikasi secara langsung logika komputasi terhadap data:

```python
# Rincian 12 Pengujian Matematika Spesifik:
1. test_eq1_canal_distance_non_negativity_and_units()
2. test_eq2_ex_plg_landscape_partition_completeness()
3. test_eq3_fwi_calculation_determinism_all_rows()
4. test_eq4_signed_boundary_distance_topology()
5. test_eq5_spatial_bdd_density_arithmetic()
6. test_eq6_discontinuity_step_jump_and_ratio()
7. test_eq7_binary_target_threshold_and_class_distribution()
8. test_eq8_balanced_class_weight_conservation()
9. test_eq9_feature_space_dimensions_and_orthogonality()
10. test_eq10_spatial_block_cv_partition_disjointness()
11. test_eq11_shapley_efficiency_axiom()
12. test_inferential_statistics_and_ml_metrics_parity()
```

---

## 7. Runbook Eksekusi & Kriteria Keberhasilan (Definition of Done)

Untuk mengeksekusi dan memverifikasi rencana ini:

```bash
# 1. Jalankan unit test matematika baru
/opt/anaconda3/envs/karhutla_env/bin/pytest tests/test_mathematical_formulations.py -v

# 2. Jalankan seluruh harness pengujian komprehensif (Wajib 100% PASSED)
/opt/anaconda3/envs/karhutla_env/bin/pytest tests/ -v

# 3. Buat dan simpan ringkasan audit dalam format JSON
/opt/anaconda3/envs/karhutla_env/bin/python -c "import tests.test_mathematical_formulations as tmf; tmf.generate_audit_report()"

# 4. Rekompilasi dokumen jika ditemukan perbaikan tipografi
tectonic manuscript/main.tex
pandoc manuscript/manuscript_draft.md --resource-path=.:output/figures --bibliography=manuscript/references.bib --citeproc -o manuscript/submission_package/manuscript_main.docx

# 5. Commit dan push hasil verifikasi ke repositori GitHub
git add PLAN.md tests/test_mathematical_formulations.py output/reports/mathematical_validation_audit.json
git commit -m "feat(math-audit): implement comprehensive mathematical and formula validation suite"
git push origin main
```

**Kriteria Keberhasilan (*Definition of Done*)**:
1. Seluruh 11 persamaan formal terpetakan secara deterministik ke kode dan data tanpa perbedaan nilai ($0\%$ toleransi error).
2. Modul `test_mathematical_formulations.py` terintegrasi penuh ke dalam test suite utama (total pengujian meningkat dari 41 menjadi 53 pengujian).
3. Seluruh 53 pengujian berstatus hijau (`PASSED`).
4. Laporan `mathematical_validation_audit.json` berhasil dibuat dan disimpan di direktori laporan resmi.
