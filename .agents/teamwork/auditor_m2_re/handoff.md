# Forensic Audit Report: Milestone 2 Re-evaluasi (Naskah Publikasi LaTeX Scopus Q1)

**Work Product**: `manuscript/` (`main.tex`, `sections/*.tex`, `references.bib`, `main.pdf`), `tests/verify_latex.py`, `output/reports/model_metrics.json`, `output/reports/eda_summary.json`  
**Profile**: General Project (Integrity Mode: Demo)  
**Auditor**: Forensic Auditor (Re-evaluasi Gate Milestone 2)  
**Verdict**: **CLEAN** (Lolos Gate Milestone 2 Tanpa Syarat)

---

## 1. Observation (Observasi Langsung)

Berikut adalah data observasi berbasis eksekusi alat, analisis statis, verifikasi empiris komputasional mandiri, dan penelaahan berkas PDF hasil kompilasi:

### Observasi 1.1: Verifikasi Remediasi Pelanggaran 1 (Tabel Distribusi Kabupaten pada `03_results.tex` dan `main.pdf`)
Sebelumnya, auditor mendeteksi deviasi ribuan titik pada 6 kabupaten di Tabel 2 (dalam berkas lengkap menjadi Tabel 3). Berdasarkan pemeriksaan langsung pada `manuscript/sections/03_results.tex` baris 67--75 dan ekstraksi teks `manuscript/main.pdf` via `/opt/homebrew/bin/pdftotext`:

| Kabupaten / Kota | Angka Naskah Pasca-Remediasi (`03_results.tex` & `main.pdf`) | Data Faktual Master (`karhutla_kalteng_2019_2026.csv`) | Visual Gambar 03 (`03_peringkat_kabupaten_terparah.png`) | Selisih | Status Audit |
|---|:---:|:---:|:---:|:---:|:---:|
| **Seruyan** | 9,356 (21.29%) | 9,356 (21.29%) | 9,356 (21.3%) | 0 | **PASS** |
| **Pulang Pisau** | 7,143 (16.26%) | 7,143 (16.26%) | 7,143 (16.3%) | 0 | **PASS** |
| **Kapuas** | 6,314 (14.37%) | 6,314 (14.37%) | 6,314 (14.4%) | 0 | **PASS** |
| **Katingan** | 6,106 (13.90%) [Rank 4] | 6,106 (13.90%) [Rank 4] | 6,106 (13.9%) [Rank 4] | 0 | **PASS** |
| **Kotawaringin Timur** | 4,627 (10.53%) [Rank 5] | 4,627 (10.53%) [Rank 5] | 4,627 (10.5%) [Rank 5] | 0 | **PASS** |
| **Kotawaringin Barat** | 4,256 (9.69%) [Rank 6] | 4,256 (9.69%) [Rank 6] | 4,256 (9.7%) [Rank 6] | 0 | **PASS** |
| **Kota Palangka Raya** | 3,188 (7.26%) [Rank 7] | 3,188 (7.26%) [Rank 7] | 3,188 (7.3%) [Rank 7] | 0 | **PASS** |
| **Barito Selatan** | 992 (2.26%) [Rank 8] | 992 (2.26%) [Rank 8] | 992 (2.3%) [Rank 8] | 0 | **PASS** |
| **Other 6 Regencies** | 1,955 (4.45%) | 1,955 (4.45%) | 1,955 (4.5%) *(Lamandau: 773, Sukamara: 481, Gumas: 407, Bartim: 227, Mura: 44, Barut: 23)* | 0 | **PASS** |
| **Total** | **43,937 (100.00%)** | **43,937 (100.00%)** | **43,937 (100.0%)** | **0** | **PASS** |

- Teks naratif pendukung pada baris 89: *"The top three jurisdictions---Seruyan (21.29\%), Pulang Pisau (16.26\%), and Kapuas (14.37\%)---accounted for 51.92\% (22,813 hotspots)... six northern interior regencies... collectively generated only 1,955 hotspots (4.45\%)"* $\rightarrow$ **IDENTIK 100%**.

---

### Observasi 1.2: Verifikasi Remediasi Pelanggaran 2 (Dinamika Harian Bagian 3.1 & Keterangan Gambar 02)
Sebelumnya, naskah memuat angka mentah *unclipped bounding box* (9.859, 8.769, 18.628, 33.942, 3.128, 2.712). Pada naskah terkini (`03_results.tex` baris 47 dan 51 serta `main.pdf`):

| Parameter Dinamika Harian | Teks Naskah Terkini (`03_results.tex` & `main.pdf`) | Data Faktual Terkliping Kalteng (`karhutla_kalteng_2019_2026.csv`) | Visual Gambar 02 (`02_heatmap_musiman_bulan.png`) | Selisih | Status Audit |
|---|:---:|:---:|:---:|:---:|:---:|
| **Puncak 7 Oktober** | 8,290 | 8,290 (18.87%) | 8,290 | 0 | **PASS** |
| **Puncak 8 Oktober** | 7,377 | 7,377 (16.79%) | 7,377 | 0 | **PASS** |
| **Total Puncak 7--8 Oktober** | 15,667 (35.66%) | 15,667 (35.66%) | 15,667 | 0 | **PASS** |
| **Total Window 5--8 Oktober** | 28,387 (64.61%) | 28,387 (64.61%) | 28,387 | 0 | **PASS** |
| **Penurunan 9 Oktober** | 2,366 | 2,366 (5.38%) | 2,366 | 0 | **PASS** |
| **Akhir 12 Oktober** | 2,084 | 2,084 (4.74%) | 2,084 | 0 | **PASS** |

- Kutipan verbatim `03_results.tex` baris 47: `\caption{\textbf{Diurnal dynamics and satellite sensor distribution of active fire hotspots during the acute October 2026 crisis in Central Kalimantan.} Thermal anomalies peaked sharply on 7--8 October (15,667 hotspots; 35.66\% of total provincial detections) under extreme fuel desiccation, followed by precipitous suppression on 9--12 October due to localized convective precipitation.}`
- Kutipan verbatim `03_results.tex` baris 51: `Temporal distribution revealed extreme temporal concentration: the four-day window between 5 October and 8 October accounted for 28,387 hotspots (64.61\% of provincial detections). The crisis peaked on 7 October with 8,290 hotspots and 8 October with 7,377 hotspots... reducing detections to 2,366 on 9 October and 2,084 by 12 October.` $\rightarrow$ **IDENTIK 100%**.

---

### Observasi 1.3: Audit Ketiadaan Manipulasi Data Baru & Konsistensi Eksperimen
Seluruh metrik pemodelan Machine Learning dan data biofisik diverifikasi langsung terhadap `output/reports/model_metrics.json` dan data mentah:
1. **Model B (Pure Biophysical)**:
   - Holdout Test ROC-AUC: `0.7527`, $F_1$: `0.3983`, Presisi Reguler: `92.1%`, Recall Ekstrem: `65.82%`, Presisi Ekstrem: `28.56%`.
   - Matriks Konfusi ($n=10.985$): $\text{TN}=6.586, \text{FP}=2.737, \text{FN}=568, \text{TP}=1.094$.
   - Spatial Block CV Mean ROC-AUC: `0.4950` ($\pm$0.0490), Mean $F_1$: `0.1399`.
   - Rincian Folds 1 s.d. 5: Seruyan (AUC 0.5827, $F_1$ 0.2914), Fold 2 (AUC 0.5041, $F_1$ 0.0657), Fold 3 (AUC 0.4900, $F_1$ 0.1056), Fold 4 (AUC 0.4452, $F_1$ 0.0646), Fold 5 (AUC 0.4533, $F_1$ 0.1722). Seluruh 5 fold bernilai positif.
2. **Model A (Baseline Hafalan Spasial)**:
   - Holdout Test ROC-AUC: `0.7956`, $F_1$: `0.4512`.
   - Spatial Block CV Mean ROC-AUC: `0.5399` ($\pm$0.0531), Mean $F_1$: `0.0583`.
   - Folds 2, 3, 4, 5: $F_1 = 0.0000$ (kegagalan total di 4 fold akibat menghafal koordinat geodetik).
3. **TreeSHAP Attributions (12 Fitur)**:
   - Curah hujan 7H (0.0329), Jarak kanal (0.0322), Angin (0.0254), Dry spell (0.0224), Eks-PLG (0.0222), Kedalaman gambut (0.0209), Suhu maks (0.0203), Kelembapan (0.0173), Tipe tanah (0.0171), FWI (0.0170), Status konsesi (0.0094), Tutupan lahan (0.0094).
4. **Data Tenurial & Biofisik Gambut**:
   - Non-Konsesi (APL): 33.138 (75.42%); Sawit (HGU): 7.276 (16.56%); Kehutanan (PBPH): 3.523 (8.02%).
   - Entitas teratas: PT Rimba Makmur Utama (964), PT Sangkowong Sinta (954), PT Nusantara Raya Solusi (522), PT Graha Inti Jaya (472), PT Bulau Sawit Bajenta (343).
   - Peat depth: Gambut Dalam (12.888 / 29.33%), Mineral (11.294 / 25.70%), Gambut Sangat Dalam (10.197 / 23.21%), Sedang (9.177 / 20.89%), Dangkal (381 / 0.87%). Total gambut: 32.643 (74.30%).
   - Jarak kanal eks-PLG ($n=16.645$): Median 14.946 m (~14.9 km).
   - Historis SiPongi KLHK (2018--2026): Cocok 100% per tahun.

---

### Observasi 1.4: Audit Transparansi Keterbatasan Metodologis (Section 4.4)
Berkas `manuscript/sections/04_discussion.tex` baris 31--59 memuat sub-bab eksplisit *"Study Limitations, Uncertainties, and Threats to Validity"* yang mencakup 5 domain limitasi saintifik:
1. **Sensors & Smoldering Combustion Physics (4.4.1)**: Keterbatasan orbit satelit polar (2--4 lintasan/hari), tutupan awan/asap tebal, serta perbedaan fisika pembakaran menyala (*flaming* $>800$\,K) versus membara bawah tanah (*smoldering* 500--700\,K) pada lapisan katotelm sehingga FRP memodelkan emisi radiatif permukaan, bukan massa gambut bawah tanah yang terbakar.
2. **ERA5 Scale Mismatch & Ecological Fallacy (4.4.2)**: Resolusi reanalisis ERA5-Land ($0.1^\circ \approx 9$\,km) diagregasikan harian per kabupaten, tidak dapat menangkap hujan konvektif lokal di kabupaten luas seperti Kapuas ($>15.000\,\text{km}^2$).
3. **Temporal Scope of Acute Crisis (4.4.3)**: Data dibatasi pada pulsa krisis 8 hari (5--12 Oktober 2026) transisi kemarau ekstrem ke hujan; model memerlukan adaptasi domain untuk musim basah La Niña atau awal musim kemarau.
4. **Spatial Transferability, Covariate Shift & Class Imbalance (4.4.4)**: Mengakui secara jujur performa Spatial CV ROC-AUC 0.4950 dan $F_1$ 0.1399 akibat *covariate shift* lanskap kanal eks-PLG versus Seruyan, serta rasio ketidakseimbangan kelas 1:5.6 yang memicu 2.737 *false positives* (presisi kelas ekstrem 28.56%). Membahas *loss asymmetry* dan merumuskan mitigasi praktis *Multi-Tier Risk Stratification Protocol (Waspada, Siaga, Awas)* untuk mencegah *alert fatigue*.
5. **Cadastral Boundary Resolution & APL Heterogeneity (4.4.5)**: Mengakui heterogenitas lahan APL yang mencakup tanah adat, transmigrasi, kebun swadaya bersertifikat SHM, dan lahan terlantar yang memerlukan pemetaan partisipatif tingkat desa.

---

### Observasi 1.5: Validasi Statis Sintaks LaTeX dan Integritas Sitasi
- Eksekusi `/opt/anaconda3/envs/karhutla_env/bin/python tests/verify_latex.py`:
  - Hasil: **Exit code 0, 0 Error, 0 Warning**.
  - Keseimbangan lingkungan `\begin{...}` dan `\end{...}`: 100% seimbang (0 mismatch).
  - Sitasi: 40 entri BibTeX di `references.bib`, 40 kunci disitir di teks naskah (100% resolusi, 0 undefined keys, 0 unused keys).
  - Referensi silang: 51 label unik, 21 referensi silang `\ref{...}` terselesaikan sempurna ke `\label{...}`.
  - Integrasi gambar: Seluruh 7 figur ilmiah (`01_` s.d. `07_`) terverifikasi ada dan disisipkan dengan `\includegraphics`.
  - Persamaan 1--5 dan Tabel 1--5 terverifikasi lengkap.

---

### Observasi 1.6: Pengujian Kompilasi Dokumen PDF
- Kompiler `/opt/homebrew/bin/tectonic` mengeksekusi kompilasi `manuscript/main.tex`:
  - Hasil: Exit code 0, kompilasi berhasil penuh.
  - Berkas luaran: `manuscript/main.pdf` berukuran **2.239.749 bytes (~2.14 MB)**.
  - Ekstraksi teks menggunakan `pdftotext` membuktikan bahwa seluruh perbaikan numerik telah ter-render secara utuh pada dokumen PDF siap publikasi.

---

## 2. Logic Chain (Rantai Logika Pembuktian)

1. **Evaluasi Terhadap Syarat Ground Truth (`ORIGINAL_REQUEST.md`)**:
   - Syarat utama integritas: *"The team must NOT: modify real empirical metrics from experiment results, copy external text without valid citations, or omit methodological limitations in the discussion."*
   - Pada audit sebelumnya, ditemukan 2 cacat empiris (inkonsistensi data kabupaten di Tabel 2 dan data dinamika harian mentah di Bagian 3.1).
2. **Evaluasi Perbaikan Empiris**:
   - Observasi 1.1 membuktikan bahwa Tabel 2 (distribusi kabupaten) telah disinkronkan 100% dengan dataset master `karhutla_kalteng_2019_2026.csv` dan grafik Gambar 03. Urutan peringkat Katingan (Rank 4, 6.106) dan Kotim (Rank 5, 4.627) kini tepat, serta Palangka Raya (3.188) dan Barito Selatan (992) sesuai data faktual.
   - Observasi 1.2 membuktikan bahwa narasi Bagian 3.1 dan caption Gambar 02 telah disinkronkan 100% dengan angka terkliping resmi Kalteng (puncak 7 Okt: 8.290; puncak 8 Okt: 7.377; total 7--8 Okt: 15.667 / 35.66%; window 5--8 Okt: 28.387 / 64.61%).
3. **Evaluasi Ketiadaan Manipulasi Lanjutan**:
   - Observasi 1.3 membuktikan bahwa seluruh metrik Machine Learning (Model A vs Model B), matriks konfusi, spatial cross-validation, 12 peringkat TreeSHAP, stratifikasi kedalaman gambut, dan kepemilikan konsesi bersesuaian sempurna dengan berkas eksperimen riil tanpa fabrikasi apapun.
4. **Evaluasi Transparansi & Keterbatasan Metodologis**:
   - Observasi 1.4 membuktikan bahwa Section 4.4 membahas seluruh limitasi (resolusi satelit, smoldering, ERA5 scale mismatch, temporal scope, spatial block CV collapse pada Model A, presisi 28.56% akibat class imbalance, serta heterogenitas APL) secara jujur dan ilmiah sesuai standar reviewer Scopus Q1.
5. **Evaluasi Kelayakan Publikasi & Kompilasi**:
   - Observasi 1.5 dan 1.6 membuktikan integritas sintaks LaTeX 100% valid (0 error) dan dokumen `main.pdf` berhasil dikompilasi secara nyata dengan layout profesional.
6. **Kesimpulan Deduktif**:
   Seluruh kriteria integritas forensik terpenuhi dan semua temuan pelanggaran terdahulu telah diremediasi secara sempurna. Tidak ada satu pun cek yang gagal.

---

## 3. Caveats (Batasan dan Asumsi)

No caveats. Seluruh verifikasi telah dilakukan secara komputasional langsung terhadap kode sumber, data primer CSV/JSON, visualisasi PNG, skrip LaTeX, dan berkas PDF terkompilasi.

---

## 4. Conclusion (Kesimpulan & Vonis)

**VONIS: CLEAN**

Naskah publikasi LaTeX Milestone 2 (`manuscript/`) telah memenuhi seluruh standar integritas forensik ilmiah dan kriteria akseptasi `ORIGINAL_REQUEST.md`:
1. Kontradiksi empiris pada Tabel 2 dan Bagian 3.1 telah diperbaiki 100% sesuai data master.
2. Tidak ditemukan manipulasi angka baru atau fabrikasi hasil eksperimen.
3. Keterbatasan metodologis diungkapkan secara jujur, transparan, dan berbobot *Senior Journal Reviewer* pada Sub-bab 4.4.
4. Seluruh 40 sitasi terhubung secara valid ke `references.bib` tanpa ada undefined/ghost citations.
5. Naskah berhasil dikompilasi menjadi dokumen PDF berstandar Scopus Q1 (`manuscript/main.pdf`).

Milestone 2 secara resmi dinyatakan **LULUS (CLEAN)** dan siap dilanjutkan ke tahapan berikutnya.

---

## 5. Verification Method (Metode Verifikasi Independen)

Untuk mereproduksi hasil verifikasi audit ini:

```bash
# 1. Jalankan pengujian validasi statis LaTeX (memastikan 0 error)
/opt/anaconda3/envs/karhutla_env/bin/python tests/verify_latex.py

# 2. Verifikasi kesesuaian nilai kabupaten pada naskah terhadap data master CSV
/opt/anaconda3/envs/karhutla_env/bin/python -c "
import pandas as pd
df = pd.read_csv('data/processed/karhutla_kalteng_2019_2026.csv', low_memory=False)
vc = df['kabupaten_kota'].value_counts()
for k, v in vc.items():
    print(f'{k}: {v:,} ({v/len(df)*100:.2f}%)')
"

# 3. Verifikasi dinamika harian pada naskah terhadap data master CSV
/opt/anaconda3/envs/karhutla_env/bin/python -c "
import pandas as pd
df = pd.read_csv('data/processed/karhutla_kalteng_2019_2026.csv', low_memory=False)
print(df['acq_date'].value_counts().sort_index())
"

# 4. Verifikasi kompilasi dokumen PDF
cd manuscript && /opt/homebrew/bin/tectonic main.tex
```

Kondisi Invalidasi: Jika terdapat perbedaan angka antara naskah dan output skrip verifikasi di atas, vonis CLEAN ini batal demi integritas ilmiah.
