# AUDIT LAPORAN & REKOMENDASI TEKSTUAL MANUSKRIP UNTUK *APPLIED GEOGRAPHY* (ELSEVIER)

**Target Jurnal:** *Applied Geography* (Elsevier, Impact Factor: 7.4, CiteScore: 8.3, Scopus Q1)  
**Judul Manuskrip:** *Spatiotemporal Fire Intensity Modeling in Degraded Tropical Peatlands: Addressing Spatial Autocorrelation and Land Tenure Governance in Central Kalimantan*  
**Penulis:** Ahmad Sopian & Rahmi Susanti  
**Tanggal Audit:** 4 November 2026  
**Auditor:** `explorer_ag_survey_2` (Teamwork Explorer Agent)  

---

## 1. Ringkasan Eksekutif & Reframing Cakupan (Context & Scope Reframing)

### 1.1. Konteks Penolakan *Ecological Modelling* & Rasionalisasi Reorientasi ke *Applied Geography*
Manuskrip ini sebelumnya menerima penolakan awal (*out-of-scope desk rejection*) dari jurnal *Ecological Modelling*. Analisis forensik editorial menunjukkan penyebab fundamental:
* *Ecological Modelling* berfokus secara ketat pada pemodelan proses biologis dan simulasi mekanistik dinamika ekosistem murni (misalnya dinamika populasi, siklus biokimia, jaring-jaring makanan, atau fisiologi vegetasi).
* Manuskrip ini bukan simulasi proses ekologi murni, melainkan sebuah studi terapan tingkat tinggi dalam **Geografi Spasial Terapan (Applied Spatial Geography)**, **Sains Informasi Geografis (GIScience)**, **Penginderaan Jauh (Remote Sensing)**, **Tata Kelola Tenurial Lahan (Land Tenure Governance)**, dan **Mitigasi Bencana Lingkungan Hidup**.

Oleh karena itu, Elsevier's *Applied Geography* (IF: 7.4, CiteScore: 8.3, Scopus Q1) adalah rumah publikasi yang ideal. Namun, manuskrip harus **diorientasikan ulang secara tegas (reframed)** dari sekadar eksperimen *machine learning* generik menjadi sebuah kontribusi geografi spasial terapan yang kokoh.

### 1.2. Empat Jangkar Tematik Utama (Thematic Anchors) untuk *Applied Geography*

1. **Hukum Pertama Tobler & Mitigasi Autokorelasi Spasial (Tobler's First Law & Spatial Autocorrelation)**:
   * Menjelaskan bahwa prinsip *"everything is related to everything else, but near things are more related than distant things"* (Tobler, 1970) mendasari fenomena kebakaran hutan dan lahan gambut.
   * Mendemonstrasikan secara empiris jebakan **hafalan spasial (spatial memorization)**: ketika koordinat geodetik (`latitude`, `longitude`) dimasukkan sebagai fitur prediktor dalam Model A, pohon keputusan (*decision trees*) memecah ruang koordinat secara langsung. Hal ini menghasilkan ilusi akurasi semu pada validasi acak (Holdout ROC-AUC = 0.7956), namun mengalami keruntuhan katastropik saat diuji pada wilayah geografis baru melalui *Spatial Block Cross-Validation* (ROC-AUC runtuh ke 0.5399, dan $F_1$-score jatuh ke 0.0000 pada 4 dari 5 lipatan spasial).
   * Membuktikan bahwa Model B (*Pure Biophysical Model*), yang dilatih murni berbasis variabel fisik tanpa koordinat, mempertahankan kemampuan generalisasi lintas blok spasial (Spatial CV mean $F_1 = 0.1399$, retensi 2,4 kali lebih tinggi dibanding Model A).

2. **Geografi Tenurial Lahan & Ruang Hampa Tata Kelola (Land Tenure Geography & Governance Void)**:
   * Mengungkap temuan spasial krusial bahwa **75,42% (33.138 titik api)** kebakaran terjadi di lahan Non-Konsesi (**Area Penggunaan Lain / APL**), bukan di dalam konsesi korporasi formal.
   * Menjelaskan geografi politik di balik fenomena ini: pasca-pembatalan Proyek Lahan Gambut (PLG) sejuta hektar tahun 1999, ratusan ribu hektar kubah gambut terdegradasi berstatus tanah negara bebas tanpa administrator definitif (*open-access regimes*), memicu perambahan spekulatif, pembukaan lahan liar, dan kebakaran tanpa penanggung jawab hukum.
   * Menempatkan 24,58% titik api di konsesi korporasi (Sawit HGU 16,56%, Kehutanan PBPH 8,02%) dalam konteks hukum *strict liability* (Pasal 88 UU No. 32/2009) dan audit ESG berbasis spasial, sehingga meluruskan narasi publik yang selama ini terpolarisasi.

3. **Vektor Kanal Drainase & Peluruhan Jarak Spasial (Canal Drainage Vectors & Distance Decay)**:
   * Memetakan 13 poros vektor garis kanal primer (Saluran Primer Induk / SPI) eks-PLG Blok A, B, C, dan D yang diproyeksikan secara metrik pada sistem proyeksi **WGS 84 / UTM Zone 49S (EPSG:32749)**.
   * Mengidentifikasi efek peluruhan jarak spasial (*distance decay effect*): intensitas radiasi termal (*Fire Radiative Power* / FRP) melonjak drastis dalam koridor 3.000 meter dari kanal primer (peringkat ke-2 pengaruh fitur TreeSHAP, mean $|\text{SHAP}| = 0.0322$).

4. **Perencanaan Spasial Terapan & Kebijakan Intervensi (Applied Spatial Planning & Policy)**:
   * Mentransformasikan temuan ambang batas TreeSHAP menjadi rekomendasi kebijakan tata ruang dan mitigasi bencana:
     - Protokol peringatan dini siaga darurat saat hari tanpa hujan berturut-turut mencapai ambang 12–14 hari.
     - Zonasi prioritas pembasahan kembali (*rewetting*) dan sekat kanal (*canal blocking*) dalam radius 3 km dari kanal eks-PLG.
     - Penataan tenurial APL terlantar melalui skema Perhutanan Sosial (*Social Forestry*) atau Kesatuan Pengelolaan Hutan (KPH).

---

## 2. Audit Kepatuhan Pedoman Penulis *Applied Geography* (Editorial Guidelines Compliance)

Berdasarkan audit terprogram terhadap berkas manuskrip saat ini, ditemukan beberapa pelanggaran batas pedoman editorial yang **wajib diperbaiki** sebelum submisi:

| Parameter Pedoman | Ketentuan *Applied Geography* | Kondisi Berkas Saat Ini | Status Kepatuhan | Tindakan Perbaikan Diperlukan |
| :--- | :--- | :--- | :--- | :--- |
| **Panjang Abstrak** | Maksimal 250 kata (*strictly $\le 250$ words*) | `00_abstract.tex`: **384 kata**<br>`manuscript_draft.md`: **369 kata** | ❌ **PELANGGARAN KRITIS** (+134 kata) | Ringkas abstrak menjadi $\le 246$ kata tanpa menghilangkan metrik empiris kuantitatif. |
| **Jumlah Kata Kunci (Keywords)** | 1 hingga 7 kata kunci (*1--7 keywords*) | `00_abstract.tex`: **10 kata kunci**<br>`manuscript_draft.md`: **9 kata kunci** | ❌ **PELANGGARAN** (+3 kata kunci) | Pangkas menjadi tepat 7 kata kunci yang berbobot geografi spasial terapan. |
| **Format Highlights** | 3--5 poin, masing-masing maks 85 karakter (termasuk spasi) | `highlights.md`: 5 poin<br>Karakter: 76, 80, 75, 76, 77 | ✅ **PATUH** | Format patuh; sempurnakan redaksi agar lebih menonjolkan aspek geografi terapan. |
| **Target Journal pada Draf** | *Applied Geography* | `manuscript_draft.md` baris 10: *Remote Sensing of Environment / IJWF / MDPI* | ❌ **INKONSISTENSI** | Perbarui header draf markdown ke *Applied Geography*. |
| **Jumlah Titik Api Ekstrem ($n$)** | 6.648 titik (FRP $\ge 12.0$ MW) | `manuscript_draft.md` baris 128: `$n = 6,634$`<br>`02_materials_methods.tex`: 6.648 | ❌ **INKONSISTENSI DATA** | Samakan draf markdown menjadi 6.648 sesuai data riil. |
| **Format Pernyataan CRediT** | Standar Elsevier CRediT | `credit_statement.md` & `main.tex` | ✅ **PATUH** | Format CRediT sudah mencakup seluruh peran penulis. |
| **Deklarasi Kepentingan (COI)** | Formulir Elsevier Declaration of Interest | `declaration_of_interest.md` | ✅ **PATUH** | Sudah tersedia dan lengkap. |
| **Ketersediaan Data (Data Availability)** | Tautan repositori publik terbuka | GitHub: `amsopian22/karhutla-analisis` | ✅ **PATUH** | Repositori publik aktif dan transparan. |

---

## 3. Audit Mutu Bahasa Inggris Akademik & Gaya Penulisan Ilmiah (Academic English & Tone Audit)

### 3.1. Penilaian Kualitas Penulisan
Secara keseluruhan, draf manuskrip ditulis dengan tata bahasa yang baik, namun audit mendalam menemukan beberapa area yang memerlukan penyempurnaan gaya bahasa akademik standar tinggi (*High-Impact Academic English*):

1. **Pengurangan Konstruksi Pasif yang Berlebihan (*Passive Voice Saturation*)**:
   * *Temuan:* Pada beberapa paragraf metodologi dan hasil, kalimat pasif bertumpuk secara berulang (misal: *"Active fires were clipped... distance was calculated... models were trained... SHAP values were extracted"*).
   * *Rekomendasi:* Variasikan struktur kalimat menggunakan frasa aktif berbasis agen dan tindakan substantif (misal: *"Automated spatial clipping against official administrative boundaries eliminated 8,892 peripheral detections..."*).

2. **Presisi Terminologi Geografi Spasial (*Precision of Spatial Geographic Terminology*)**:
   * *Temuan:* Istilah seperti *"spatial shortcuts"* atau *"spatial memorization"* perlu diperkuat dengan terminologi GIScience yang diakui secara luas, seperti **"spatial non-stationarity"**, **"spatial autocorrelation leakage"**, **"geographical domain shift"**, dan **"areal spatial interpolation failure"**.
   * *Temuan:* Istilah *"Non-concession land"* harus selalu diperjelas dalam konteks hukum agraria Indonesia sebagai **"unallocated State Other Utilization Areas (*Area Penggunaan Lain* / APL)"** untuk menghindari kerancuan bagi pembaca internasional.

3. **Kejelasan Transisi dan Kepadatan Prosa (*Flow, Conciseness, and Coherence*)**:
   * Hindari kalimat majemuk yang terlalu panjang (lebih dari 45 kata dalam satu tarikan kalimat) yang berisiko mengaburkan pesan utama bagi penelaah (*peer reviewers*).
   * Pertahankan nada objektif, berbasis data (*evidence-based*), dan hindari kata-kata bernada sensasional seperti *"catastrophicly"* (salah ketik; seharusnya *"catastrophically"*, atau lebih baik diganti dengan *"drastically"* / *"precipitously"*).

---

## 4. Analisis & Usulan Perbaikan Tekstual Bagian demi Bagian (Section-by-Section Proposals)

### 4.1. Bagian 0: Judul, Abstrak, Kata Kunci, dan Highlights

#### A. Abstrak (Abstract)
* **Status Masalah:** Abstrak saat ini memiliki panjang 384 kata di berkas LaTeX dan 369 kata di draf markdown, melanggar batas maksimal 250 kata Elsevier *Applied Geography*.
* **Usulan Teks Pengganti (Tepat 246 Kata):**

```latex
\begin{abstract}
\noindent
Tropical peatlands in Southeast Asia are globally vital carbon pools destabilized by artificial drainage networks and recurring wildfires. Operational fire hazard prediction in applied spatial geography faces two critical challenges: unmitigated spatial autocorrelation causing coordinate-dependent machine learning models to overfit local clusters (spatial memorization), and empirical ambiguity regarding land tenure culpability. We analyzed 43,937 verified satellite active fire detections (NASA FIRMS: VIIRS 375\,m and MODIS Aqua) during the October 2026 crisis in Central Kalimantan, Indonesia, integrated with official peat depth inventories (BBLSDLP), metric primary canal vectors (UTM Zone 49S), ECMWF ERA5-Land atmospheric reanalysis, and 812 cadastral concession overlays. Under 5-fold Spatial Block Cross-Validation (\texttt{GroupKFold} by regency), a Random Forest baseline incorporating geodetic coordinates (Model~A) suffered spatial memorization collapse, with mean ROC-AUC dropping from 0.7956 to 0.5399 and $F_1$-score falling to 0.0000 across four of five folds. Conversely, a pure biophysical model excluding coordinates (Model~B) preserved generalizability across unseen regions (holdout ROC-AUC: 0.7527; extreme fire recall: 65.8\%; spatial CV mean $F_1 = 0.1399$, a 2.4-fold retention over Model~A). TreeSHAP attribution identified key non-linear thresholds: 7-day rainfall deficit $< 5.0$\,mm, canal proximity within 3.0\,km, and dry spells $> 14$\,days. Cadastral overlays revealed that 75.4\% of hotspots occurred on unallocated Non-Concession public land (\textit{Area Penggunaan Lain}, APL), exposing a spatial governance vacuum on abandoned state peatlands, while corporate concessions accounted for 24.6\%. These findings demonstrate that wildfire mitigation requires institutional administration over unallocated APL peatlands alongside corporate oversight, guided by spatially generalizable biophysical early-warning thresholds.

\vspace{0.4em}
\noindent\textbf{Keywords:}\ \ \textit{Applied spatial geography; Tropical peatlands; Spatial autocorrelation; Spatial block cross-validation; Land tenure governance; Wildfire intensity modeling; Mega Rice Project.}
\end{abstract}
```

* **Evaluasi Perbaikan:** 
  - Panjang kata berkurang dari 384 menjadi **246 kata** (patuh penuh pada batas $\le 250$ kata).
  - Mempertahankan seluruh angka statistik krusial (43.937 titik api, 75,4% APL vs 24,6% konsesi, Model A runtuh ke 0.5399 AUC & 0.0000 F1, Model B Spatial F1 0.1399, ambang batas TreeSHAP < 5 mm hujan, 3 km kanal, 14 hari kemarau).
  - Kata kunci dipangkas dari 10 menjadi tepat **7 kata kunci** dengan penekanan pada geografi spasial terapan.

#### B. Research Highlights (`manuscript/highlights.md`)
* **Status Masalah:** 5 butir saat ini sudah $\le 85$ karakter, namun narasinya dapat dipertajam agar lebih mencerminkan kontribusi geografi dan hukum Tobler.
* **Usulan Teks Pengganti:**

```markdown
# RESEARCH HIGHLIGHTS

* 43,937 active fire detections analyzed across degraded Borneo peatlands. (74 chars)
* Coordinate-based ML collapses under Spatial Block CV via Tobler's First Law. (78 chars)
* Pure biophysical Random Forest retains 2.4-fold higher spatial CV F1-score. (75 chars)
* 75.4% of fires occur on unallocated public lands (APL), revealing tenure void. (80 chars)
* Explainable AI reveals critical 3 km canal corridor and 14-day drought trigger. (81 chars)
```

---

### 4.2. Bagian 1: Pendahuluan (Introduction)

#### A. Titik Kritis yang Perlu Ditingkatkan
1. **Penyelarasan dengan Epistemologi Geografi Spasial Terapan:**
   * Di baris 10--15 `sections/01_introduction.tex`, pengenalan masalah autokorelasi spasial harus secara eksplisit mengaitkan Hukum Pertama Tobler dengan problem ekstrapolasi geografis (*geographic transferability*) dan area keberlakuan model (*Area of Applicability* / AOA, Meyer & Pebesma, 2021).
2. **Penguatan Teoretis Geografi Tenurial Lahan:**
   * Masalah atribusi tenurial harus dihubungkan dengan literatur geografi politik mengenai teritorialisasi (*territorialization*, Vandergeest & Peluso, 1995; Peluso & Lund, 2011) dan dikotomi spasial antara Kawasan Hutan Negara (*State Forest Estate*) dan Area Penggunaan Lain (APL).
3. **Formulasi Hipotesis Spasial yang Lebih Tajam:**
   * Rumusan hipotesis $H_1$ dan $H_2$ perlu menonjolkan aspek kegagalan transferabilitas ruang geografis (*geographical domain transfer failure*).

#### B. Usulan Revisi Teks (Paragraf 4 hingga Hipotesis):

* **Teks Eksisting (Baris 10--20 `01_introduction.tex`):**
> *"Operational wildfire risk prediction and policy interventions in tropical peatlands face two main challenges: First, spatial autocorrelation creates spatial memorization in machine learning models... Second, debates over land tenure culpability remain polarized..."*

* **Usulan Revisi Teks Berkualitas Tinggi (*Proposed Revision*):**
```latex
In the domain of applied spatial geography and environmental hazard management, operational wildfire prediction and land governance encounter two unresolved impasses:

First, unmitigated spatial autocorrelation induces insidious spatial memorization in geospatial machine learning algorithms. Supervised classifiers, including Random Forests, gradient-boosted ensembles, and deep neural architectures, are increasingly deployed for spatial wildfire susceptibility and active combustion mapping \citep{Breiman2001ML}. However, terrestrial environmental processes strictly operate under Tobler's First Law of Geography: everything is related to everything else, but near things are more related than distant things \citep{Tobler1970EconGeogr, Legendre1993Ecology}. When spatial hazard models ingest geodetic coordinates (\texttt{latitude} and \texttt{longitude}) or administrative unit labels as independent predictors, recursive tree partitioning algorithms exploit spatial coordinates as empirical shortcuts, memorizing historical spatial clusters rather than learning underlying biophysical combustion mechanics \citep{Meyer2018EcolModel, Dormann2007Ecography}. Under standard random cross-validation, spatial autocorrelation between geographically proximate training and validation samples causes severe data leakage \citep{Roberts2017Ecography, Wadoux2021EcolModel}. Consequently, while such coordinate-dependent models report deceptively high predictive skill within sampled neighborhoods, their transferability collapses precipitously when deployed across out-of-sample administrative jurisdictions or unfamiliar peat dome systems \citep{MeyerPebesma2021NatComm, Schratz2019EcolModel}.

Second, the geographical political economy of land tenure culpability remains clouded by empirical ambiguity and contentious public discourse. Academic and policy debates surrounding Indonesian peatland wildfires frequently bifurcate between attributing ignitions primarily to corporate concessionaires expanding industrial monocultures \citep{Tacconi2003CIFOR, Carlson2012PNAS} versus smallholder agricultural clearance and illegal forest encroachment \citep{Cattau2016GCB}. This polarization stems from the historical state territorialization of Indonesia's land estate, which partitioned the landscape into the State Forest Estate (\textit{Kawasan Hutan}) and Other Utilization Areas (\textit{Area Penggunaan Lain}, APL). In post-Mega Rice Project Central Kalimantan, vast expanses of drained peatlands were excised from the forest estate but left without designated concessionaires or institutional managers, fostering an ambiguous open-access spatial regime. Spatially explicit cadastral overlays intersecting high-resolution satellite active fire detections with audited concession boundaries remain exceptionally rare in peer-reviewed geographical literature, leaving the actual spatial distribution of fire across tenure regimes largely unquantified \citep{Putranto2023LandUsePol}.

To resolve these pressing methodological and governance questions, this study presents an empirical investigation of the wildfire crisis in Central Kalimantan. Utilizing 43,937 satellite active fire observations from NASA FIRMS during the acute October 2026 fire pulse, we test two central geographical hypotheses:
\begin{enumerate}
    \item[$\mathbf{H_1}$:] \textit{Incorporating geodetic coordinates into tree-based wildfire intensity models induces severe spatial memorization, producing inflated performance under random cross-validation due to spatial autocorrelation, but triggering catastrophic performance collapse under spatially disjoint block cross-validation due to geographical transfer failure.}
    \item[$\mathbf{H_2}$:] \textit{A pure biophysical feature architecture free from spatial coordinates generalizes across distinct geographical blocks by learning transferable environmental, hydrological, and edaphic combustion thresholds.}
\end{enumerate}
```

---

### 4.3. Bagian 2: Data & Metodologi (Materials and Methods)

#### A. Titik Kritis yang Perlu Ditingkatkan
1. **Ketegasan Landasan Geodesi dan Proyeksi Spasial:**
   * Menjelaskan secara eksplisit mengapa re-proyeksi koordinat dari derajat geografis WGS 84 (EPSG:4326) ke sistem proyeksi bidang datar bergradien metrik **WGS 84 / UTM Zone 49S (EPSG:32749)** mutlak diperlukan untuk menghindari distorsi jarak geodesik pada lintang ekuator.
2. **Topologi Jaringan Kanal Eks-PLG:**
   * Merinci 13 vektor sumbu kanal primer (Saluran Primer Induk / SPI) sebagai infrastruktur linier artifisial yang memotong kubah gambut ombrogenik.
3. **Justifikasi Geografis Pemartisian Lipatan Spasial (`GroupKFold` per Kabupaten):**
   * Menjelaskan mengapa pengelompokan 14 kabupaten/kota menjadi 5 lipatan spasial adalah representasi valid dari uji transferabilitas regional (memisahkan kubah gambut pesisir barat Seruyan, koridor kanal eks-PLG di Pulang Pisau dan Kapuas, serta dataran mineral pedalaman utara).

#### B. Usulan Penyempurnaan Teks Metodologi:
* Pastikan Persamaan (68) dan penanganan nilai sentinal kanal ($d_{\text{canal}} = -1$) dijelaskan dengan landasan zonasi bentang alam (*landscape zoning principle*) yang mencegah bias ekologis di wilayah kabupaten barat yang tidak memiliki kanal eks-PLG.

---

### 4.4. Bagian 3: Hasil (Results)

#### A. Titik Kritis yang Perlu Ditingkatkan
1. **Penegasan Pola Spasial Konsentrasi Titik Api:**
   * Menonjolkan bahwa 51,92% titik api terkonsentrasi hanya di 3 kabupaten gambut selatan (Seruyan 21,29%, Pulang Pisau 16,26%, Kapuas 14,37%), sementara 6 kabupaten mineral pedalaman hanya menyumbang 4,45%. Ini adalah pola *core-periphery environmental hazard* yang khas dalam geografi.
2. **Geografi Efek Koridor Perbatasan Konsesi (*Boundary Interface Dynamics*):**
   * Menjelaskan Gambar 4b (*Seruyan basin zoom-in*): kebakaran mengelompok secara intensif tepat di luar garis batas terluar konsesi HGU pada lahan masyarakat/APL tak bertuan. Ini membuktikan fenomena *leakage* dan kekosongan patroli di zona transisi.
3. **Analisis Rinci Runtuhnya Model A pada Lipatan Spasial (Tabel 3):**
   * Uraikan secara tegas bahwa Model A mencatatkan $F_1 = 0.0000$ pada Lipatan 2, 3, 4, dan 5! Pohon keputusan sama sekali gagal memprediksi api ekstrem pada kabupaten baru karena pohon tersebut memotong koordinat lintang/bujur yang tidak ada di wilayah uji. Sebaliknya, Model B mempertahankan nilai $F_1 > 0$ di seluruh 5 lipatan (rata-rata $F_1 = 0.1399$).

---

### 4.5. Bagian 4: Pembahasan (Discussion)

#### A. Titik Kritis yang Perlu Ditingkatkan
1. **Analisis Mendalam "Ruang Hampa Tata Kelola" (*The APL Institutional Vacuum*):**
   * Bagian 4.2 harus diperkaya dengan analisis geografi kelembagaan:
     - Korporasi HGU dan PBPH memikul tanggung jawab mutlak (*strict liability* Pasal 88 UU No. 32/2009), memiliki posko damkar mandiri, menara pantau, dan ancaman pencabutan izin usaha.
     - Lahan APL eks-PLG pasca-1999 tidak memiliki pemegang izin maupun badan pengelola permanen seperti KPH. Akibatnya, lahan tersebut mengalami tragedi ruang bersama (*tragedy of the open-access commons*). Penegakan hukum kehutanan tidak dapat menjangkau APL, sementara pemerintah kabupaten kekurangan anggaran dan personel damkar.
2. **Kritik Metodologis untuk Komunitas Geografi & Sains Informasi Geografis:**
   * Bagian 4.3 harus menyampaikan seruan tegas (*methodological imperative*) kepada editor dan penelaah jurnal geografi untuk tidak menerima manuskrip bahaya lingkungan (*wildfire, landslide, flood*) yang memasukkan koordinat spasial tanpa melakukan uji *Spatial Block Cross-Validation*.
3. **Protokol Tiga Tingkat Siaga Spasial Terapan:**
   * Operasionalisasi Model B ke dalam 3 tier probabilitas (*Advisory* 0.30--0.50, *Watch* 0.50--0.70, *Warning* $\ge 0.70$) untuk memitigasi *alert fatigue* tim pemadam darat.

---

### 4.6. Bagian 5: Kesimpulan & Implikasi Kebijakan (Conclusions & Policy Implications)

#### A. Titik Kritis yang Perlu Ditingkatkan
1. **Integrasi Perencanaan Tata Ruang Spasial (*Spatial Planning Integration*):**
   * Mengaitkan rekomendasi sekat kanal koridor 3.000 m langsung dengan revisi Rencana Tata Ruang Wilayah Provinsi (RTRWP) Kalimantan Tengah dan Rencana Perlindungan dan Pengelolaan Ekosistem Gambut (RPPEG).
2. **Resolusi Tenurial Lahan APL:**
   * Rekomendasi konkret pengalihan lahan APL terlantar menjadi skema Hutan Kemasyarakatan (HKm) atau Hutan Desa (HD) dalam program Perhutanan Sosial (*Social Forestry*), yang memberikan hak tenurial legal kepada komunitas lokal dengan kewajiban menjaga dari api.

---

### 4.7. Audit Surat Pengantar (Cover Letter Audit — `manuscript/cover_letter.md`)

* **Kesesuaian Target:** Surat pengantar sudah ditujukan kepada Editor-in-Chief *Applied Geography*.
* **Area Peningkatan Bahasa & Narasi:**
  1. Pada paragraf pertama, jelaskan secara eksplisit mengapa manuskrip ini memiliki relevansi tinggi dengan ruang lingkup *Applied Geography*:
     > *"Given Applied Geography’s core commitment to utilizing geospatial analysis, GIScience, and spatial modeling to resolve pressing human-environment resource dilemmas, this manuscript directly addresses the spatial methodological traps and land governance challenges underpinning Southeast Asia's recurrent peatland wildfire crises."*
  2. Jelaskan secara diplomatis penolakan sebelumnya dari *Ecological Modelling*: naskah sebelumnya ditolak tanpa penelaahan (*desk rejection*) murni karena ketidakcocokan ruang lingkup (*out-of-scope*), di mana jurnal tersebut mengkhususkan diri pada simulasi biologis-ekologis spesifik, sedangkan kontribusi utama manuskrip ini adalah **metodologi geografi spasial terapan, autokorelasi spasial, sains informasi geografis, dan tata kelola tenurial lahan**.

---

## 5. Matriks Inkonsistensi & Sinkronisasi Antar-Berkas

| Item / Metrik | Berkas `manuscript_draft.md` | Berkas `sections/*.tex` & `main.tex` | Sumber Data Riil / Benar | Rekomendasi Sinkronisasi |
| :--- | :--- | :--- | :--- | :--- |
| **Target Journal Header** | Baris 10: *Remote Sensing of Environment / IJWF / MDPI* | `main.tex` metadata: *Applied Geography* | *Applied Geography* (Elsevier) | Ganti baris 10 `draft.md` menjadi *Applied Geography*. |
| **Kata Kunci (Keywords)** | 9 kata kunci | 10 kata kunci | Maksimal 7 kata kunci | Tetapkan 7 kata kunci standar di kedua berkas. |
| **Panjang Abstrak** | 369 kata | 384 kata | Maksimal 250 kata | Ganti dengan draf abstrak 246 kata di kedua berkas. |
| **Jumlah Api Ekstrem ($n$)** | Baris 128: `$n = 6,634$` | Baris 163 `02_materials_methods.tex`: 6.648 | $n = 6.648$ ($FRP \ge 12.0$ MW) | Ubah 6.634 menjadi 6.648 pada `draft.md`. |
| **Penomoran Gambar** | Konflik penomoran (Gambar 4 & 5 muncul ganda di markdown) | Menggunakan label otomatis `\ref{fig:...}` | Penomoran sekuensial Gambar 1--7 | Perbaiki teks penomoran gambar pada markdown `draft.md`. |

---

## 6. Rekomendasi Langkah Kerja Konkret untuk Tim Pelaksana (Actionable Implementation Plan)

1. **Sinkronisasi Abstrak & Kata Kunci:**
   * Terapkan draf abstrak 246 kata pada `manuscript/sections/00_abstract.tex` dan `manuscript/manuscript_draft.md`.
   * Terapkan 7 kata kunci baku pada kedua berkas.
2. **Penyempurnaan Reframing Geografi pada `sections/01_introduction.tex`:**
   * Perbarui paragraf autokorelasi spasial, hukum Tobler, dan latar belakang tenurial politik APL sesuai usulan revisi.
3. **Penyelarasan Draf Markdown (`manuscript_draft.md`):**
   * Sinkronkan angka $n=6.648$, header *Applied Geography*, dan urutan penomoran gambar.
4. **Kompilasi Dokumen & Validasi:**
   * Kompilasi ulang `main.tex` menggunakan `/opt/homebrew/bin/tectonic` untuk menghasilkan `main.pdf` yang sempurna.
   * Ekspor dokumen submisi Word (`manuscript_main.docx`, `highlights.docx`, `cover_letter.docx`) yang selaras dan terbebas dari markup mentah.
