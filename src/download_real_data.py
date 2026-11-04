"""
Skrip Pengunduh Data Riil Karhutla Kalimantan Tengah
Sumber:
1. NASA FIRMS (Fire Information for Resource Management System) - NRT Active Fires
2. SiPongi KLHK (Sistem Pemantauan Karhutla Kemenhut/KLHK) - Rekapitulasi Luas Kebakaran
"""

import os
import urllib.request
import pandas as pd

RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

# 1. Bounding box Kalimantan Tengah
# Latitude: 0.8 N s/d -3.6 S, Longitude: 110.7 E s/d 115.9 E
KALTENG_BBOX = {
    'min_lat': -3.6,
    'max_lat': 0.8,
    'min_lon': 110.7,
    'max_lon': 115.9
}

print("=" * 60)
print("1. Mengunduh data titik api riil dari satelit NASA FIRMS...")
print("=" * 60)

firms_urls = {
    'VIIRS_SNPP': 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_SouthEast_Asia_7d.csv',
    'VIIRS_NOAA20': 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-20-viirs-c2/csv/J1_VIIRS_C2_SouthEast_Asia_7d.csv',
    'MODIS': 'https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_SouthEast_Asia_7d.csv'
}

kalteng_frames = []

for sensor, url in firms_urls.items():
    try:
        print(f"Mengunduh data {sensor}...")
        df = pd.read_csv(url)
        # Filter batas koordinat Kalteng
        filtered = df[
            (df['latitude'] >= KALTENG_BBOX['min_lat']) &
            (df['latitude'] <= KALTENG_BBOX['max_lat']) &
            (df['longitude'] >= KALTENG_BBOX['min_lon']) &
            (df['longitude'] <= KALTENG_BBOX['max_lon'])
        ].copy()
        filtered['sensor_source'] = sensor
        print(f" -> Berhasil: {len(df):,} titik SE Asia, {len(filtered):,} titik di area Kalimantan Tengah")
        kalteng_frames.append(filtered)
    except Exception as e:
        print(f" -> Gagal mengunduh {sensor}: {e}")

if kalteng_frames:
    firms_real_df = pd.concat(kalteng_frames, ignore_index=True)
    firms_out = os.path.join(RAW_DIR, "firms_real_kalteng_latest_7d.csv")
    firms_real_df.to_csv(firms_out, index=False)
    print(f"\n[OK] Data riil FIRMS berhasil disimpan: {firms_out}")
    print(f"Total titik api riil tersimpan: {len(firms_real_df):,} baris")
    print(f"Rentang tanggal: {firms_real_df['acq_date'].min()} s/d {firms_real_df['acq_date'].max()}")

print("\n" + "=" * 60)
print("2. Menyimpan data rekapitulasi resmi SiPongi KLHK (2018–2026)...")
print("=" * 60)

sipongi_data = {
    'tahun': [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026],
    'luas_terbakar_ha': [
        47432.57,
        317749.00,
        7681.00,
        3653.00,
        1554.00,
        165896.44,
        11459.89,
        4803.97,
        7634.46
    ],
    'catatan': [
        'Kondisi normal kering',
        'El Nino Kuat (Puncak Krisis 2019)',
        'La Nina (Musim Basah)',
        'La Nina (Musim Basah)',
        'Tahun sangat basah (Terendah)',
        'El Nino Moderat (Lonjakan Signifikan)',
        'Kondisi Netral',
        'Kondisi Netral',
        'Data berjalan resmi per pertengahan tahun (SiPongi Kemenhut)'
    ]
}

sipongi_df = pd.DataFrame(sipongi_data)
sipongi_out = os.path.join(RAW_DIR, "sipongi_luas_karhutla_kalteng_2018_2026.csv")
sipongi_df.to_csv(sipongi_out, index=False)
print(f"[OK] Data resmi SiPongi KLHK berhasil disimpan: {sipongi_out}")
print(sipongi_df.to_string(index=False))
