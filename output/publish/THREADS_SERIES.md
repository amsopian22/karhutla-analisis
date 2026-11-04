# Rangkaian Utas Threads / X (8-Post Thread Series)

Rangkaian postingan ini dirancang dengan gaya *storytelling* santai, visual, dan memikat untuk audiens Threads & X. Setiap post dilengkapi panduan lampiran visual dari folder `output/figures/`.

---

### Post 1 (The Viral Hook) 🧵👇
Sebagai Data Scientist, saya menganalisis 18.000 titik api kebakaran hutan (Karhutla) di Kalimantan Tengah dari 2019 sampai 2026.

Kami gabungkan data satelit NASA, data resmi Kementerian Kehutanan, peta gambut, dan batas konsesi perusahaan.

Ini 4 anomali data paling mengejutkan yang kami temukan: 🧵👇

📸 *Lampirkan Gambar: `output/figures/01_tren_tahunan_el_nino.png` atau rekaman layar singkat `peta_interaktif_karhutla_kalteng.html`.*

---

### Post 2 (Anomali 1: Siklus El Niño yang Brutal)
Fakta pertama: Karhutla di Kalteng punya siklus 'Boom-and-Bust'.

Sebanyak 79% titik api selama 8 tahun HANYA menumpuk di 2 tahun El Niño: 2019 dan 2023.

Saat tahun basah La Niña (2020-2022), kebakaran turun lebih dari 85%. Api di Kalteng sangat sensitif terhadap anomali suhu samudra Pasifik.

---

### Post 3 (Anomali 2024–2026: Jeda Basah Lalu Re-Eskalasi Krisis!)
Data resmi SiPongi Kemenhut mencatat:
- 2024–2025: Sempat anjlok drastis di fase basah (luas terbakar Kalteng turun ke 3.405 Ha di 2024 dan 1.115 Ha di 2025).
- TAPI 2026: Terjadi re-eskalasi tajam! Luas karhutla nasional Jan–Jul 2026 menembus 202.004 Ha (+80% dibanding periode sama 2023).
- Di Kalteng per Okt 2026: 3.750+ titik api aktif terdeteksi satelit, menjadikan Kalteng episentrum #1 nasional!

Kenapa meledak lagi di 2026? Biomassa 2 tahun basah mengering serentak akibat kemarau kilat (Fuel Load Trap).

📸 *Lampirkan Gambar: `output/figures/02_heatmap_musiman_bulan.png`*

---

### Post 4 (Anomali 2: Episentrum Spasial Eks-PLG)
Kebakaran tidak terjadi acak. Lebih dari 55% titik api dan energi radiasi pelepasan api (FRP) berulang di 3 kabupaten:
1. Pulang Pisau (21,8%)
2. Kotawaringin Timur (18,1%)
3. Kapuas (15,6%)

Kawasan ini beririsan langsung dengan proyek ambisius era 90-an: eks-PLG 1 Juta Hektar.

📸 *Lampirkan Gambar: `output/figures/03_peringkat_kabupaten_terparah.png`*

---

### Post 5 (Anomali 3: Efek Mematikan Kanal Drainase < 1.000 Meter)
Ini temuan paling krusial:
- 73,5% api terjadi di lahan gambut.
- 78,5% api gambut terjadi dalam radius < 1 km dari kanal drainase buatan!

Kanal buatan menguras air kubah gambut alami. Saat kemarau, gambut kering menjadi bahan bakar bawah tanah (smoldering) yang menyala berhari-hari dan menghasilkan kabut asap pekat.

📸 *Lampirkan Gambar: `output/figures/04_analisis_gambut_dan_kanal.png`*

---

### Post 6 (Anomali 4: Plot Twist Status Konsesi!)
Banyak yang mengira sebagian besar karhutla terjadi di dalam konsesi kebun sawit korporasi.

Fakta data spasial:
- 53,7% justru di Area Non-Konsesi (APL / Lahan Terbuka Terlantar)!
- Konsesi Sawit: 27,2%
- Konsesi HTI: 14,1%

Tanah terbuka tak bertuan yang minim penjagaan dan patroli adalah kantong api terbesar.

---

### Post 7 (Kenapa Asap 2026 Sampai ke Singapura & Malaysia?)
Banyak yang heran: Kenapa kabut asap bisa melintasi lautan sampai ke Singapura & Malaysia?

Ada 2 penyebab fisika atmosfer:
1. Api gambut membakar bawah tanah (smoldering) tanpa oksigen cukup, melepaskan partikel PM2.5 4-10x lebih pekat dari kebakaran biasa.
2. Angin Monsun Barat Daya (Mei - awal Okt 2026) meniupkan asap langsung dari Sumatera & Kalimantan menuju Selat Malaka & Semenanjung Malaysia!

Untungnya, per 9-12 Oktober 2026 ini kita masuk fase peralihan monsun: angin melemah dan hujan mulai turun meredakan jerebu.

📸 *Lampirkan Gambar: `output/figures/08_transboundary_haze_dispersion.png`*

---

### Post 8 (Faktor Penentu Menurut Machine Learning & SHAP)
Kami latih model AI XGBoost dengan validasi out-of-time (Train: 2019-2023, Test: 2024-2026). Skor ROC-AUC mencapai 0,87+.

Menggunakan SHAP explainability, 2 faktor utama penentu risiko kebakaran ekstrem adalah:
1. Jarak ke kanal drainase (semakin dekat = risiko melonjak).
2. Hari tanpa hujan > 14 hari berturut-turut.

📸 *Lampirkan Gambar: `output/figures/07_shap_feature_importance.png`*

---

### Post 9 (Solusi & Link Lengkap)
Kesimpulan data:
Karhutla bisa dicegah jika fokus diarahkan pada:
1. Penyekatan kanal (canal blocking) di radius 1 km eks-PLG.
2. Sistem siaga otomatis saat 14 hari tanpa hujan.
3. Patroli berbasis AI di lahan terbuka non-konsesi.

Analisis lengkap, grafik interaktif, dan kodenya ada di Medium & GitHub saya:
🔗 [Link Artikel Medium]
🔗 [Link GitHub Repository]

Bagikan jika bermanfaat! 🔄
