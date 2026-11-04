# Laporan Hasil Exploratory Data Analysis (EDA) Terkalibrasi
## Investigasi Spasiotemporal Karhutla Kalimantan Tengah (Episode Krisis Oktober 2026)

### 1. Integritas Data & Metodologi
- **Cakupan Spasial**: 100% dipotong (*spatial clip*) terhadap batas administrasi resmi 14 Kabupaten/Kota Provinsi Kalimantan Tengah.
- **Titik Observasi Riil**: 43,937 titik panas sensor VIIRS & MODIS (NASA FIRMS 5–12 Oktober 2026).
- **Perhitungan Jarak Kanal**: Dihitung terproyeksi (UTM 49S) ke vektor garis (*LineString*) saluran primer eks-PLG Blok A, B, C, D.
- **Penautan Izin Konsesi**: *Point-in-polygon* terhadap 627 sertifikat HGU Sawit BPN dan 185 izin PBPH Kehutanan KLHK.
- **Tren Historis**: Data resmi luasan kebakaran Kementerian Kehutanan (SiPongi KLHK 2018–2026).

### 2. Temuan Kunci Sains Data
1. **Dominasi Area Non-Konsesi (APL / Lahan Terbuka)**:
   Sebanyak **75.4%** titik api berada di luar area konsesi berizin resmi. Ini mematahkan mitos bahwa karhutla 100% dipicu oleh pembukaan lahan oleh korporasi.
2. **Proporsi Konsesi Berizin**:
   Konsesi Sawit (HGU) mencakup **16.6%** dan Konsesi Kehutanan (PBPH) mencakup **8.0%** titik api.
3. **Ekosistem Gambut sebagai Episentrum**:
   Sebanyak **74.3%** kebakaran terjadi di atas rawa gambut. Median jarak ke poros saluran kanal di lanskap eks-PLG adalah **14,946 meter**.
4. **Wilayah Paling Rawan**:
   3 Kabupaten terparah: Seruyan (21.3%), Pulang Pisau (16.3%), Kapuas (14.4%).
