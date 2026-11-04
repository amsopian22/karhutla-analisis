"""
Melakukan Spatial Join antara Titik Api Satelit (NASA FIRMS & Historis)
dengan Poligon Konsesi Riil (HGU Sawit & PBPH Kehutanan) di Kalimantan Tengah.
"""

import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

sawit_geojson = os.path.join(RAW_DIR, "konsesi_sawit_kalteng_real.geojson")
pbph_geojson = os.path.join(RAW_DIR, "konsesi_kehutanan_pbph_real.geojson")
master_csv = os.path.join(PROCESSED_DIR, "karhutla_kalteng_2019_2026.csv")

print("1. Membaca data spasial konsesi riil...")
gdf_sawit = gpd.read_file(sawit_geojson)
gdf_pbph_all = gpd.read_file(pbph_geojson)

# Bounding box Kalteng
kalteng_box = (110.7, -3.6, 115.9, 0.8)
gdf_pbph = gdf_pbph_all.cx[kalteng_box[0]:kalteng_box[2], kalteng_box[1]:kalteng_box[3]].copy()

print(f" -> Konsesi Sawit Riil Kalteng: {len(gdf_sawit)} poligon")
print(f" -> Konsesi Kehutanan (PBPH) Kalteng: {len(gdf_pbph)} poligon")

# Standardisasi kolom sawit
gdf_sawit = gdf_sawit[['name', 'company', 'po_hgu', 'geometry']].copy()
gdf_sawit['company_clean'] = gdf_sawit['company'].fillna(gdf_sawit['name']).str.strip()
gdf_sawit['izin_clean'] = gdf_sawit['po_hgu'].fillna('-').str.strip()
gdf_sawit['tipe_konsesi'] = 'Konsesi Perkebunan Sawit (HGU)'

# Standardisasi kolom PBPH
gdf_pbph = gdf_pbph[['NAMOBJ', 'NO_SK', 'KEGIATAN', 'geometry']].copy()
gdf_pbph['company_clean'] = gdf_pbph['NAMOBJ'].fillna('PBPH Tanpa Nama').str.strip()
gdf_pbph['izin_clean'] = gdf_pbph['NO_SK'].fillna('-').str.strip()
gdf_pbph['tipe_konsesi'] = 'Konsesi Kehutanan (IUPHHK-HTI/HA)'

# 2. Baca master dataset titik api
print(f"\n2. Membaca dataset titik api master: {master_csv}...")
df = pd.read_csv(master_csv, low_memory=False)
print(f"Total titik api: {len(df):,} observasi")

# Konversi titik ke GeoDataFrame
geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
gdf_hotspots = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# 3. Spatial Join dengan Konsesi Sawit
print("3. Melakukan Spatial Join dengan Konsesi Sawit (Point-in-Polygon)...")
join_sawit = gpd.sjoin(gdf_hotspots, gdf_sawit[['company_clean', 'izin_clean', 'tipe_konsesi', 'geometry']], 
                       how="left", predicate="within")
# Hapus duplikat index jika ada overlap batas
join_sawit = join_sawit[~join_sawit.index.duplicated(keep='first')]

# 4. Spatial Join dengan Konsesi Kehutanan PBPH
print("4. Melakukan Spatial Join dengan Konsesi Kehutanan PBPH...")
join_pbph = gpd.sjoin(gdf_hotspots, gdf_pbph[['company_clean', 'izin_clean', 'tipe_konsesi', 'geometry']], 
                      how="left", predicate="within")
join_pbph = join_pbph[~join_pbph.index.duplicated(keep='first')]

# 5. Gabungkan hasil status konsesi faktual
print("5. Menentukan status konsesi faktual dan nama pemegang izin...")
status_konsesi_list = []
nama_konsesi_list = []
no_izin_list = []
tutupan_lahan_list = []

for idx in df.index:
    sawit_match = join_sawit.loc[idx, 'tipe_konsesi'] if idx in join_sawit.index else None
    pbph_match = join_pbph.loc[idx, 'tipe_konsesi'] if idx in join_pbph.index else None
    is_peat = "Gambut" in str(df.loc[idx, 'tipe_lahan'])
    
    if pd.notnull(sawit_match):
        status_konsesi_list.append("Konsesi Perkebunan Sawit (HGU)")
        nama_konsesi_list.append(str(join_sawit.loc[idx, 'company_clean']))
        no_izin_list.append(str(join_sawit.loc[idx, 'izin_clean']))
        tutupan_lahan_list.append("Perkebunan Kelapa Sawit (HGU)")
    elif pd.notnull(pbph_match):
        status_konsesi_list.append("Konsesi Kehutanan (IUPHHK-HTI/HA)")
        nama_konsesi_list.append(str(join_pbph.loc[idx, 'company_clean']))
        no_izin_list.append(str(join_pbph.loc[idx, 'izin_clean']))
        tutupan_lahan_list.append("Konsesi Hutan Tanaman / Alam (PBPH)")
    else:
        status_konsesi_list.append("Non-Konsesi (Area Penggunaan Lain / Komunitas)")
        nama_konsesi_list.append("Non-Konsesi (APL / Lahan Terbuka)")
        no_izin_list.append("-")
        if is_peat:
            tutupan_lahan_list.append("Semak Belukar Rawa Gambut (Eks-PLG)")
        else:
            tutupan_lahan_list.append("Semak Belukar / Lahan Terbuka Mineral")

df['status_konsesi'] = status_konsesi_list
df['nama_konsesi'] = nama_konsesi_list
df['no_izin_sk'] = no_izin_list
df['tutupan_lahan'] = tutupan_lahan_list

# Simpan kembali dataset master dan dataset riil
df.to_csv(master_csv, index=False)
df.to_csv(os.path.join(PROCESSED_DIR, "karhutla_kalteng_real_2026.csv"), index=False)
print(f"\n[SUKSES] Dataset master diperbarui: {master_csv}")
print("Distribusi Faktual Status Konsesi:")
print(df['status_konsesi'].value_counts())
print("\nDistribusi Tutupan Lahan Faktual:")
print(df['tutupan_lahan'].value_counts())
print(f"\nPersentase Non-Konsesi vs Konsesi:")
print((df['status_konsesi'].value_counts(normalize=True) * 100).round(2).to_string())

print("\nTop 10 Perusahaan Sawit dengan Titik Api Terbanyak:")
top_sawit = df[df['status_konsesi'].str.contains("Sawit")]['nama_konsesi'].value_counts().head(10)
print(top_sawit.to_string())

print("\nTop 10 Pemegang Izin Kehutanan dengan Titik Api Terbanyak:")
top_pbph = df[df['status_konsesi'].str.contains("Kehutanan")]['nama_konsesi'].value_counts().head(10)
print(top_pbph.to_string())
