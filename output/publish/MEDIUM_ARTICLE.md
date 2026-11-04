# Mengapa Hutan Gambut Terus Terbakar? Investigasi Spasiotemporal Karhutla Kalimantan Tengah (2019-2026)

*Topik: Geospatial Data Science, Analisis Kebijakan Lingkungan, Explainable AI, ESG Analytics, Dispersi Atmosfer*

---

![Animasi Peta Interaktif Karhutla Kalimantan Tengah](output/figures/animasi_peta_interaktif_karhutla.gif)

> Dokumen Visual Peta Interaktif:
> * Animasi di atas menampilkan navigasi spasial 52.829 titik observasi satelit NASA FIRMS, lapisan densitas heatmap FRP, penelusuran wilayah eks-PLG, atribut izin konsesi, dan citra satelit resolusi tinggi.
> * [Tonton Video Demonstrasi Full HD (MP4)](output/figures/video_peta_interaktif_karhutla.mp4)
> * [Buka Peta Interaktif di Browser (HTML)](output/figures/peta_interaktif_karhutla_kalteng.html)

---

## Pendahuluan: Membaca Struktur di Balik Titik Panas

Saat musim kemarau tiba, pemberitaan di media sering mengulang kalimat yang sama: titik panas melonjak dan kabut asap kembali menyebar. Kebakaran hutan dan lahan kerap diperlakukan sebagai peristiwa musiman acak atau semata ulah pembakar liar.

Catatan satelit dan data biofisik tanah menunjukkan struktur persoalan yang berbeda. Saat koordinat api dihubungkan dengan sebaran kubah gambut, riwayat kanalisasi, arah angin monsun, dan peta konsesi resmi, kebakaran memperlihatkan pola spasial yang berulang dan terikat pada kondisi hidrologis tertentu.

Laporan ini menyajikan analisis terhadap 52.829 titik observasi satelit NASA FIRMS di Kalimantan Tengah selama Oktober 2026, yang dikonfirmasi dengan rekapitulasi luasan resmi SiPongi Kementerian Lingkungan Hidup dan Kehutanan (KLHK) periode 2018 sampai 2026. Kami menautkan data titik api dengan 627 poligon sertifikat Hak Guna Usaha (HGU) sawit, 185 poligon Perizinan Berusaha Pemanfaatan Hutan (PBPH), peta Kesatuan Hidrologis Gambut (KHG), jaringan kanal buatan, data partikulat PM2.5, serta model klasifikasi Random Forest dan SHAP.

Berikut temuan faktual dan analisis teknisnya.

---

## 1. Siklus Iklim dan Eskalasi 2026

Pemeriksaan pertama menguji korelasi antara kejadian kebakaran dan anomali iklim regional. Menggunakan data luasan resmi SiPongi KLHK dan deteksi satelit, fluktuasi kebakaran mengikuti siklus kekeringan makro.

![Grafik 1: Tren Tahunan Luas Karhutla Resmi SiPongi KLHK](output/figures/01_tren_tahunan_el_nino.png)

### Ringkasan Data:
* Konsentrasi Tahun Kering: Luasan kebakaran terbesar terjadi pada fase kemarau panjang, yaitu 2019 (El Nino kuat) seluas 317.749 hektare dan 2023 (El Nino moderat) seluas 165.896 hektare.
* Penurunan pada Fase Basah (2024-2025): Luasan kebakaran di Kalimantan Tengah turun menjadi 3.405 hektare pada 2024 dan 1.115 hektare pada 2025 selama pengaruh La Nina.
* Eskalasi 2026: Memasuki 2026, akumulasi kebakaran kembali meningkat. Data SiPongi mencatat luas karhutla nasional Januari sampai Juli 2026 mencapai 202.004,30 hektare, naik 80 persen dibandingkan periode yang sama pada 2023 (111.871 hektare). Di Kalimantan Tengah, satelit NASA FIRMS merekam 52.829 titik panas aktif sepanjang Oktober 2026.
* Akumulasi Bahan Bakar Kering: Dua tahun basah berturut-turut memicu pertumbuhan vegetasi semak dan pakis rawa. Saat musim kemarau kilat tiba pada 2026, biomassa tersebut mengering cepat dan menjadi bahan bakar siap bakar dalam volume besar.

![Grafik 2: Distribusi Harian Observasi Sensor NASA FIRMS](output/figures/02_heatmap_musiman_bulan.png)

Grafik harian menunjukkan bahwa titik api terkonsentrasi pada rentang hari dengan kelembapan relatif terendah, dengan deteksi sensor VIIRS (Suomi-NPP dan NOAA-20) mencapai ribuan titik per hari.

---

## 2. Konsentrasi Spasial di Wilayah Eks-PLG

Berdasarkan batas administrasi dan bentang hidrologis, titik api di Kalimantan Tengah tidak menyebar rata di seluruh wilayah seluas 153.564 kilometer persegi, melainkan mengelompok di kabupaten tertentu.

![Grafik 3: Peringkat Kabupaten Terparah dan Akumulasi Titik Api](output/figures/03_peringkat_kabupaten_terparah.png)

Tiga kabupaten mencatat jumlah titik api tertinggi:
1. Kabupaten Pulang Pisau: 14,3 persen
2. Kabupaten Kotawaringin Barat: 13,7 persen
3. Kabupaten Seruyan: 13,0 persen  
(Disusul Kabupaten Kapuas dan Kotawaringin Timur).

### Konteks Wilayah Eks-PLG
Pulang Pisau dan Kapuas mencakup area eks Proyek Pembukaan Lahan Gambut (PLG) Satu Juta Hektar yang dibangun pada dekade 1990-an melalui Keppres Nomor 82 Tahun 1995. Proyek tersebut membuat jaringan kanal primer, sekunder, dan tersier selebar 5 hingga 25 meter yang memotong kubah gambut alami. Saluran drainase ini mengalirkan air keluar kubah dan menyebabkan penurunan muka air tanah gambut saat kemarau.

> Sumber Rujukan Data Spasial:
> * Batas Kesatuan Hidrologis Gambut (KHG): Peta penetapan fungsi ekosistem gambut nasional SK.129/MENLHK/SETJEN/KUM.1/2/2017.
> * Jaringan Kanal: Peta inventarisasi kanal Badan Restorasi Gambut dan Mangrove (BRGM) serta peta teknis kanal Blok A, B, C, dan D eks-PLG.
> * Koordinat Titik Api: 52.829 titik observasi satelit NASA FIRMS (VIIRS 375m dan MODIS).

---

## 3. Dinamika Biofisik Gambut dan Jarak Kanal

Analisis spasial membuktikan korelasi kuat antara jenis tanah, ketebalan lapisan gambut, dan jarak ke saluran drainase buatan.

![Grafik 4: Distribusi Lahan Gambut dan Radius Kanal Drainase](output/figures/04_analisis_gambut_dan_kanal.png)

### Fakta Data:
* 79,6 persen titik api berada di ekosistem lahan gambut, sebagian besar pada gambut dalam (1 hingga 3 meter) dan gambut sangat dalam (lebih dari 3 meter).
* Sebagian besar titik api gambut berada dalam radius kurang dari 1.000 meter dari saluran kanal eks-PLG.
* Nilai rata-rata Fire Radiative Power (FRP) tercatat 7,64 MW. Api di lahan gambut berkanal membakar material organik di bawah permukaan tanah tanpa nyala api terbuka (smoldering), sehingga pembakaran bertahan lebih lama dan sulit dipadamkan dari permukaan.

Gambut alami menahan air seperti spons. Ketika kanal buatan memotong kubah gambut tanpa sekat pengatur air, air terus terkuras ke sungai. Saat hari tanpa hujan berlangsung lebih dari 10 hari, muka air tanah dapat turun melampaui batas kritis minus 40 sentimeter dari permukaan (ambang batas baku kerusakan ekosistem gambut berdasarkan Peraturan Pemerintah Nomor 57 Tahun 2016 juncto PP 71 Tahun 2014, serta studi hidrologi gambut tropis Hooijer et al., 2012 dan Wösten et al., 2008). Penurunan muka air tanah di bawah ambang ini mengeringkan lapisan atas gambut hingga kadar airnya merosot, mengubahnya menjadi bahan bakar padat yang mudah tersulut dan memicu pembakaran bawah permukaan yang persisten.

---

## 4. Status Penguasaan Lahan Berdasarkan Peta Izin Resmi

Pengujian spasial (point-in-polygon) terhadap 627 sertifikat HGU perkebunan sawit dan 185 izin PBPH kehutanan menghasilkan rincian berikut:

![Grafik 5: Distribusi Titik Panas Berdasarkan Status Konsesi Lahan](output/figures/05_status_konsesi_esg.png)

* 73,1 persen titik api berada di Area Non-Konsesi (Area Penggunaan Lain atau APL): Area ini mencakup lahan semak rawa tak bertuan, eks proyek PLG, lahan tidur tanpa pengelola definitif, serta kawasan di dekat permukiman dan rintisan jalan.
* 15,0 persen berada di dalam konsesi Hak Guna Usaha (HGU) kelapa sawit.
* 12,0 persen berada di dalam konsesi perizinan kehutanan (PBPH tanaman industri dan restorasi ekosistem).

### Implikasi untuk Pengawasan Lapangan:
1. Pada 27,0 persen titik api yang berada di dalam konsesi berizin, koordinat dan nama entitas pemegang hak tercatat di dalam basis data spasial. Informasi ini menjadi bahan audit bagi penegak hukum dan verifikasi sarana pemadam mandiri perusahaan.
2. Pada 73,1 persen titik api di area non-konsesi, tingginya angka kebakaran menandakan kekosongan pengawasan harian di lahan-lahan gambut terlantar yang tidak dikelola secara aktif oleh korporasi maupun masyarakat adat.

---

## 5. Pemodelan Machine Learning dan Analisis SHAP

Kami melatih model klasifikasi untuk memperkirakan probabilitas kebakaran berintensitas tinggi menggunakan 52.829 baris data observasi satelit.

### Spesifikasi Model:
* Dataset: 52.829 titik observasi satelit NASA FIRMS.
* Pembagian Data: Stratified train-test split dengan rasio 75:25 (39.621 data latih dan 13.208 data uji).
* Algoritma: Random Forest Classifier dengan penyeimbang bobot kelas (class_weight='balanced').
* Hasil Evaluasi pada Data Uji:
  * ROC-AUC: 0,7491
  * F1-Score: 0,4038
  * Precision (kebakaran reguler): 91 persen
  * Recall (kebakaran intensitas tinggi): 59 persen

![Grafik 6: Evaluasi Model Machine Learning Kurva ROC dan Confusion Matrix](output/figures/06_evaluasi_model_ml.png)

### Analisis Pengaruh Fitur (SHAP):
Pemeriksaan kontribusi fitur menggunakan SHAP TreeExplainer mengidentifikasi variabel yang paling memengaruhi hasil prediksi:

![Grafik 7: SHAP Beeswarm Plot Atribusi Fitur Penentu Karhutla](output/figures/07_shap_feature_importance.png)

1. Jarak ke Kanal Eks-PLG: Variabel ini memiliki bobot pengaruh tertinggi; kedekatan lokasi terhadap saluran drainase (< 1.000 meter) meningkatkan probabilitas terjadinya kebakaran intensif.
2. Kedalaman Gambut: Lapisan gambut di atas 3 meter meningkatkan persistensi pembakaran bawah tanah.
3. Posisi Geografis (Lintang dan Bujur): Menangkap klaster spasial pada kubah gambut bagian selatan provinsi.
4. Status Konsesi dan Tutupan Lahan: Area non-konsesi bertutupan semak rawa terdegradasi mencatat frekuensi kebakaran tertinggi.

---

## 6. Pola Dispersi Asap Lintas Batas (Oktober 2026)

Selama Agustus hingga awal Oktober 2026, partikulat asap dari kebakaran gambut melintasi batas wilayah menuju Semenanjung Malaysia, Sarawak, dan Singapura. Analisis terhadap konsentrasi PM2.5 harian dan vektor angin troposfer menjelaskan proses transportasi atmosfer tersebut.

![Grafik 8: Dispersi Asap Lintas Batas dan Vektor Angin Monsun](output/figures/08_transboundary_haze_dispersion.png)

Tiga faktor yang menjelaskan pergerakan asap:
1. Karakteristik Partikulat Gambut: Pembakaran gambut tanpa pasokan oksigen cukup menghasilkan partikel halus PM2.5 dalam jumlah 4 hingga 10 kali lipat lebih banyak per hektare dibanding pembakaran hutan tanah mineral. Partikel karbon organik ini berukuran sangat kecil, ringan, dan stabil melayang di lapisan batas atmosfer.
2. Koridor Angin Monsun Barat Daya: Pada periode kemarau, angin bertiup konsisten dari arah barat daya ke timur laut dengan kecepatan 18 hingga 22 km/jam. Pola aliran ini membawa asap dari Sumatera melintasi Selat Malaka menuju Singapura dalam 12 hingga 18 jam, serta dari Kalimantan Barat dan Kalimantan Tengah menuju Sarawak dalam 24 hingga 36 jam (koefisien korelasi r = 0,91).
3. Transisi Musim pada Pertengahan Oktober: Memasuki pertengahan Oktober 2026, kecepatan angin monsun melemah dan mulai berganti arah, disertai kenaikan frekuensi hujan lokal yang menurunkan konsentrasi aerosol di wilayah regional secara bertahap.

---

## 7. Batasan Metodologi dan Validasi Lanjutan

Penyusunan analisis ini mencatat beberapa batasan teknis:
1. Keterbatasan Sensor Satelit: Sensor termal MODIS dan VIIRS terhalang oleh awan tebal dan kepulan asap pekat, sehingga jumlah titik api yang tercatat cenderung berada di bawah jumlah kejadian sebenarnya di lapangan.
2. Data Sekat Kanal: Jarak kanal dihitung secara geometris dari peta jaringan saluran statis, belum mencerminkan status hidrologis apakah suatu kanal telah disekat permanen atau sekatnya mengalami kerusakan.
3. Pelacakan Titik Sulut: Data snapshot harian satelit belum dapat membuktikan arah perambatan awal, apakah api bermula dari area non-konsesi lalu merambat ke izin perkebunan atau sebaliknya. Verifikasi lanjutan membutuhkan data citra per jam dari satelit geostasioner Himawari-9.
4. Perbedaan Titik Panas dan Luas Terbakar: Jumlah titik api tidak selalu berbanding lurus dengan luas hektare terbakar, karena satu titik bara gambut dapat terdeteksi berulang kali oleh sensor satelit dalam beberapa hari.

---

## 8. Rekomendasi Kebijakan Berbasis Data

Berdasarkan hasil pemetaan spasial dan model prediktif, kami merumuskan empat langkah prioritas:

1. Prioritas Penyekatan Kanal di Zona Penyangga: Restorasi hidrologis melalui sekat kanal perlu difokuskan pada radius 1.000 meter dari kubah gambut di Pulang Pisau, Seruyan, dan Kapuas sebelum musim kemarau dimulai agar tinggi muka air tetap terjaga.
2. Patroli Terjadwal di Area Non-Konsesi (APL): Pengawasan lapangan perlu diperluas ke lahan-lahan terbuka tanpa pengelola aktif dengan melibatkan Masyarakat Peduli Api (MPA) melalui program insentif ekonomi restorasi gambut.
3. Ambang Peringatan Dini Berdasarkan Hari Tanpa Hujan: Satuan tugas pencegahan tidak perlu menunggu deteksi titik api di satelit. Ketika pos pengamatan cuaca mencatat 14 hari berturut-turut tanpa hujan di atas kubah gambut berkanal, status siaga darurat dan operasi modifikasi cuaca perlu segera diaktifkan.
4. Keterbukaan Data Spasial Konsesi: Penyediaan peta batas izin konsesi yang terintegrasi dengan pemantauan satelit harian penting untuk mendukung verifikasi lapangan dan penegakan regulasi lingkungan yang objektif.

---

## Kesimpulan

Kebakaran hutan dan lahan di Kalimantan Tengah memiliki keterkaitan langsung dengan kondisi bentang alam hasil modifikasi manusia. Hubungan antara kekeringan iklim makro, drainase kubah gambut peninggalan proyek eks-PLG, status penguasaan lahan di area non-konsesi, dan arah angin monsun membentuk rantai penyebab utama timbulnya kabut asap.

Pengendalian karhutla yang efektif memerlukan intervensi terarah: memulihkan hidrologi kanal gambut, menutup celah pengawasan di lahan tak bertuan, dan menerapkan sistem peringatan dini berbasis ambang batas cuaca.

---
*Kode analisis, dataset terproses, model prediksi, dan visualisasi spasial tersimpan di dalam repositori proyek.*
