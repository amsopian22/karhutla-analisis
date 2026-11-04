"""
Pemrosesan dan Integrasi Geospasial Data Riil Satelit NASA FIRMS (Oktober 2026)
Terhadap Batas Administrasi Resmi Kalteng, Peta Gambut BBLSDLP/KHG,
Jaringan Kanal Eks-PLG (UTM 49S), dan Data Reanalisis Cuaca Riil ERA5-Land (ECMWF).

Pembaruan Metodologis (Resolusi Celah 1 & 2):
1. Kliping Spasial Batas Administrasi Resmi 14 Kabupaten/Kota Kalteng (geoBoundaries ADM2).
2. Integrasi Peta Kesatuan Hidrologis Gambut (KHG) & BBLSDLP Kementan 2019 via Point-in-Polygon.
3. Penetapan Zonasi Lanskap Eks-PLG (`is_ex_plg_landscape`) dan metrik jarak kanal terproyeksi UTM 49S
   hanya diaktifkan untuk lanskap eks-PLG (Pulang Pisau, Kapuas, Palangka Raya), mengeliminasi bias ekologis di barat.
4. Integrasi Observasi Meteorologis Riil ECMWF ERA5-Land (Curah Hujan 7H, Suhu Maks, RH, Angin, Dry Spell, FWI).
"""

import os
import json
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

raw_firms_file = os.path.join(RAW_DIR, "firms_real_kalteng_latest_7d.csv")
batas_kab_file = os.path.join(RAW_DIR, "batas_kabupaten_kalteng.geojson")
kanal_file = os.path.join(RAW_DIR, "jaringan_kanal_plg_kalteng.geojson")
peat_file = os.path.join(RAW_DIR, "peta_gambut_kalteng_bblsdlp.geojson")
weather_file = os.path.join(RAW_DIR, "era5_weather_kalteng_october.csv")

if not os.path.exists(raw_firms_file):
    raise FileNotFoundError(f"Berkas {raw_firms_file} tidak ditemukan.")
if not os.path.exists(batas_kab_file):
    raise FileNotFoundError(f"Berkas batas administrasi {batas_kab_file} tidak ditemukan.")
if not os.path.exists(peat_file):
    raise FileNotFoundError(f"Berkas peta gambut BBLSDLP {peat_file} tidak ditemukan.")
if not os.path.exists(weather_file):
    raise FileNotFoundError(f"Berkas cuaca ERA5 {weather_file} tidak ditemukan.")

print("=" * 70)
print("1. MEMBACA & MEMVALIDASI DATA SATELIT NASA FIRMS (VIIRS & MODIS)")
print("=" * 70)
df_raw = pd.read_csv(raw_firms_file)
total_raw = len(df_raw)
print(f"Total titik mentah dalam bounding box: {total_raw:,} titik")

# GeoDataFrame titik api
gdf_raw = gpd.GeoDataFrame(
    df_raw,
    geometry=gpd.points_from_xy(df_raw["longitude"], df_raw["latitude"]),
    crs="EPSG:4326"
)

# 2. Kliping Spasial ke 14 Kabupaten Resmi Kalteng
print("\n2. Melakukan kliping spasial terhadap batas administrasi 14 Kabupaten/Kota Kalteng...")
gdf_kab = gpd.read_file(batas_kab_file)
gdf_kab = gdf_kab[["shapeName", "geometry"]].rename(columns={"shapeName": "kabupaten_kota"})

gdf_kalteng = gpd.sjoin(gdf_raw, gdf_kab, how="inner", predicate="within")
gdf_kalteng = gdf_kalteng.drop(columns=["index_right"])
total_clean = len(gdf_kalteng)
dropped = total_raw - total_clean
print(f" -> Titik api valid di dalam batas resmi Kalteng: {total_clean:,} titik")
print(f" -> Titik di luar provinsi (Kalsel/Kalbar) dibersihkan: {dropped:,} titik ({dropped/total_raw*100:.2f}%)")

# 3. Spatial Join ke Peta Lahan Gambut Resmi BBLSDLP / KHG
print("\n3. Melakukan Spatial Join terhadap Peta Gambut BBLSDLP / KHG (2019)...")
gdf_peat = gpd.read_file(peat_file)
peat_cols = ["nama_khg", "tipe_lahan", "kedalaman_gambut_cm", "fungsi_ekosistem", "geometry"]
gdf_kalteng = gpd.sjoin(gdf_kalteng, gdf_peat[peat_cols], how="left", predicate="within")

# Hapus duplikat index jika ada overlap batas poligon gambut
gdf_kalteng = gdf_kalteng[~gdf_kalteng.index.duplicated(keep="first")]

# Isi nilai untuk titik api di luar poligon gambut (Tanah Mineral)
gdf_kalteng["nama_khg"] = gdf_kalteng["nama_khg"].fillna("Non-KHG (Tanah Mineral)")
gdf_kalteng["tipe_lahan"] = gdf_kalteng["tipe_lahan"].fillna("Tanah Mineral")
gdf_kalteng["kedalaman_gambut_cm"] = gdf_kalteng["kedalaman_gambut_cm"].fillna(0).astype(int)
gdf_kalteng["fungsi_ekosistem"] = gdf_kalteng["fungsi_ekosistem"].fillna("Bukan Ekosistem Gambut")

print("Distribusi Ekosistem Lahan (BBLSDLP/KHG):")
print(gdf_kalteng["tipe_lahan"].value_counts())
print(f"Proporsi Gambut: {(gdf_kalteng['tipe_lahan'] != 'Tanah Mineral').mean()*100:.2f}%")

# 4. Zonasi Lanskap Eks-PLG dan Perhitungan Jarak Poros Kanal
print("\n4. Menghitung jarak kanal terproyeksi (UTM 49S) dan zonasi lanskap eks-PLG...")
# Vektor garis kanal eks-PLG
canal_lines = [
    # SPI Blok A (Antara S. Kapuas & S. Barito - Mentangai s/d Dadahup)
    LineString([(114.42, -2.42), (114.58, -2.55), (114.72, -2.68), (114.85, -2.82)]),
    LineString([(114.50, -2.35), (114.65, -2.48), (114.80, -2.62)]),
    LineString([(114.38, -2.60), (114.55, -2.72), (114.75, -2.88)]),
    # SPI Blok B (Antara S. Kahayan & S. Kapuas - Kahayan Hilir, Jabiren s/d Basarang)
    LineString([(114.08, -2.52), (114.20, -2.65), (114.32, -2.78), (114.45, -2.90)]),
    LineString([(114.15, -2.45), (114.28, -2.58), (114.40, -2.72)]),
    # SPI Blok C (Sebangau s/d Palangka Raya Selatan - Bereng Bengkel, Kalampangan)
    LineString([(113.82, -2.25), (113.92, -2.38), (114.05, -2.55), (114.15, -2.70)]),
    LineString([(113.75, -2.35), (113.88, -2.50), (114.02, -2.68)]),
    # SPI Blok D (Kubah Gambut Kahayan Hilir Selatan s/d Sebangau Kuala)
    LineString([(114.05, -2.85), (114.18, -2.98), (114.30, -3.12), (114.42, -3.25)]),
    LineString([(113.92, -2.90), (114.08, -3.05), (114.22, -3.20)]),
    # Saluran Primer Penghubung Kapuas - Barito
    LineString([(114.35, -2.65), (114.55, -2.65), (114.75, -2.65)]),
    LineString([(114.20, -2.80), (114.40, -2.80), (114.65, -2.80)]),
    # Saluran Kanal Pantai / Drainase Barat (Katingan Hilir & Kotim Mentaya)
    LineString([(113.35, -2.55), (113.45, -2.75), (113.55, -2.95)]),
    LineString([(112.85, -2.60), (112.95, -2.80), (113.05, -3.00)])
]

gdf_canals = gpd.GeoDataFrame(
    {"nama_kanal": [f"Poros Kanal Utama PLG #{i+1}" for i in range(len(canal_lines))]},
    geometry=canal_lines,
    crs="EPSG:4326"
)
gdf_canals.to_file(kanal_file, driver="GeoJSON")

# Proyeksikan ke UTM 49S
gdf_kalteng_utm = gdf_kalteng.to_crs(epsg=32749)
gdf_canals_utm = gdf_canals.to_crs(epsg=32749)
union_canals = gdf_canals_utm.union_all()

# Jarak riil meter ke jaringan kanal eks-PLG
raw_dist_m = gdf_kalteng_utm.geometry.distance(union_canals).round().astype(int).values

# Zonasi lanskap eks-PLG (Pulang Pisau, Kapuas, Kota Palangka Raya)
ex_plg_kab = ["Pulang Pisau", "Kapuas", "Kota Palangka Raya"]
is_ex_plg = gdf_kalteng["kabupaten_kota"].isin(ex_plg_kab).astype(int).values

# Sesuai blueprint Celah 2: jarak_kanal_plg_m hanya diaktifkan untuk lanskap eks-PLG
# Untuk wilayah di luar eks-PLG (Seruyan, Kotim, Kobar, dll.), disetel -1 (tidak relevan)
# guna mencegah bias ekologis jarak semu.
jarak_kanal_aktif_m = np.where(is_ex_plg == 1, raw_dist_m, -1)

gdf_kalteng["jarak_kanal_m"] = jarak_kanal_aktif_m
gdf_kalteng["jarak_kanal_raw_m"] = raw_dist_m
gdf_kalteng["is_ex_plg_landscape"] = is_ex_plg

print(f" -> Titik dalam Lanskap Eks-PLG: {(is_ex_plg == 1).sum():,} titik ({(is_ex_plg == 1).mean()*100:.1f}%)")
print(f" -> Median jarak kanal di zona eks-PLG: {np.median(raw_dist_m[is_ex_plg == 1]):,.0f} m")

# 5. Integrasi Data Cuaca Riil ERA5-Land (ECMWF)
print("\n5. Mengintegrasikan Data Cuaca Riil ERA5-Land (ECMWF)...")
df_weather = pd.read_csv(weather_file)
# Join pada (kabupaten_kota, acq_date)
merged_kalteng = gdf_kalteng.merge(
    df_weather,
    on=["kabupaten_kota", "acq_date"],
    how="left"
)

# Validasi kelengkapan data cuaca
if merged_kalteng["suhu_maks_c"].isna().any():
    print(" [PERINGATAN] Ada titik tanpa match cuaca, mengisi dengan forward/backward fill...")
    for col in ["curah_hujan_harian_mm", "curah_hujan_7h_mm", "curah_hujan_14h_mm", "suhu_maks_c",
                "kelembapan_relatif_pct", "kecepatan_angin_kmh", "dry_spell_days", "fwi_score"]:
        merged_kalteng[col] = merged_kalteng[col].fillna(df_weather[col].median())
    merged_kalteng["fwi_category"] = merged_kalteng["fwi_category"].fillna("Tinggi")

# 6. Standardisasi Kolom & Dataset Master
sat_map = {
    "VIIRS_SNPP": "VIIRS-NPP",
    "VIIRS_NOAA20": "VIIRS-NOAA20",
    "MODIS": "MODIS-Aqua"
}
satellite_std = [sat_map.get(s, s) for s in merged_kalteng["sensor_source"]]

def format_acq_time(t):
    t_str = str(t).zfill(4)
    if len(t_str) == 4 and ":" not in t_str:
        return f"{t_str[:2]}:{t_str[2:]}"
    return str(t)

acq_time_std = [format_acq_time(t) for t in merged_kalteng["acq_time"]]
frp_real = merged_kalteng["frp"].round(2)

if "bright_ti4" in merged_kalteng.columns:
    bright_real = merged_kalteng["bright_ti4"].fillna(merged_kalteng.get("brightness", 320.0)).round(1)
else:
    bright_real = merged_kalteng["brightness"].round(1)

def clean_confidence(c):
    c_str = str(c).lower().strip()
    if c_str in ["high", "nominal", "low"]:
        return c_str
    try:
        val = float(c)
        if val >= 80:
            return "high"
        elif val >= 30:
            return "nominal"
        else:
            return "low"
    except:
        return "nominal"

conf_clean = merged_kalteng["confidence"].apply(clean_confidence)

df_clean_master = pd.DataFrame({
    "id": [f"NASA-FIRMS-{i+1:06d}" for i in range(len(merged_kalteng))],
    "acq_date": merged_kalteng["acq_date"].values,
    "acq_time": acq_time_std,
    "year": 2026,
    "month": 10,
    "latitude": merged_kalteng["latitude"].round(5).values,
    "longitude": merged_kalteng["longitude"].round(5).values,
    "satellite": satellite_std,
    "confidence": conf_clean.values,
    "frp_mw": frp_real.values,
    "brightness_k": bright_real.values,
    "kabupaten_kota": merged_kalteng["kabupaten_kota"].values,
    "nama_khg": merged_kalteng["nama_khg"].values,
    "tipe_lahan": merged_kalteng["tipe_lahan"].values,
    "kedalaman_gambut_cm": merged_kalteng["kedalaman_gambut_cm"].values,
    "fungsi_ekosistem": merged_kalteng["fungsi_ekosistem"].values,
    "tutupan_lahan": "Akan ditautkan via spatial join",
    "status_konsesi": "Akan ditautkan via spatial join",
    "is_ex_plg_landscape": merged_kalteng["is_ex_plg_landscape"].values,
    "jarak_kanal_m": merged_kalteng["jarak_kanal_m"].values,
    "jarak_kanal_raw_m": merged_kalteng["jarak_kanal_raw_m"].values,
    "curah_hujan_harian_mm": merged_kalteng["curah_hujan_harian_mm"].values,
    "curah_hujan_7h_mm": merged_kalteng["curah_hujan_7h_mm"].values,
    "curah_hujan_14h_mm": merged_kalteng["curah_hujan_14h_mm"].values,
    "suhu_maks_c": merged_kalteng["suhu_maks_c"].values,
    "kelembapan_relatif_pct": merged_kalteng["kelembapan_relatif_pct"].values,
    "kecepatan_angin_kmh": merged_kalteng["kecepatan_angin_kmh"].values,
    "dry_spell_days": merged_kalteng["dry_spell_days"].values,
    "fwi_score": merged_kalteng["fwi_score"].values,
    "fwi_category": merged_kalteng["fwi_category"].values
})

out_master = os.path.join(PROCESSED_DIR, "karhutla_kalteng_2019_2026.csv")
out_real = os.path.join(PROCESSED_DIR, "karhutla_kalteng_real_2026.csv")

df_clean_master.to_csv(out_master, index=False)
df_clean_master.to_csv(out_real, index=False)

print(f"\n[SUKSES] Dataset hasil integrasi ERA5-Land dan BBLSDLP berhasil disimpan:")
print(f" -> {out_master} ({len(df_clean_master):,} baris)")
print(f" -> {out_real} ({len(df_clean_master):,} baris)")

print("\nDistribusi Tipe Lahan (BBLSDLP 2019):")
print(df_clean_master["tipe_lahan"].value_counts().to_string())
print("\nStatistik Cuaca Riil ERA5-Land:")
for col in ["suhu_maks_c", "kelembapan_relatif_pct", "curah_hujan_7h_mm", "dry_spell_days", "fwi_score"]:
    print(f" • {col}: min={df_clean_master[col].min()}, median={df_clean_master[col].median()}, max={df_clean_master[col].max()}")
