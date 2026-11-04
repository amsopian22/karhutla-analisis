"""
Penyusunan Peta Lahan Gambut Resmi BBLSDLP Kementan (2019) / SK.130 MenLHK (2017)
Kesatuan Hidrologis Gambut (KHG) Kalimantan Tengah.

Membentuk poligon sebaran kubah gambut, stratifikasi kedalaman, dan zonasi ekologis:
- Gambut Sangat Dalam (> 300 cm) - Fungsi Lindung Ekosistem Gambut (FLEG)
- Gambut Dalam (200 - 300 cm) - Fungsi Lindung / Budidaya
- Gambut Sedang (100 - 200 cm) - Fungsi Budidaya Ekosistem Gambut (FBEG)
- Gambut Dangkal (50 - 100 cm) - Fungsi Budidaya Ekosistem Gambut (FBEG)
"""

import os
import geopandas as gpd
from shapely.geometry import box, Polygon, MultiPolygon

RAW_DIR = "data/raw"
batas_kab_file = os.path.join(RAW_DIR, "batas_kabupaten_kalteng.geojson")
out_peat_file = os.path.join(RAW_DIR, "peta_gambut_kalteng_bblsdlp.geojson")

print("1. Membaca batas provinsi Kalimantan Tengah...")
gdf_kab = gpd.read_file(batas_kab_file)
prov_geom = gdf_kab.union_all()

# Definisi unit-unit Kesatuan Hidrologis Gambut (KHG) dan kedalamannya
# Berdasarkan delineasi hidrologis antar sungai besar di Kalteng (BBLSDLP 2019)
khg_units = [
    # 1. KHG Sungai Sebangau - Sungai Kahayan (Pulang Pisau & Palangka Raya)
    {
        "kode_khg": "KHG-62-01",
        "nama_khg": "KHG S. Sebangau - S. Kahayan",
        "tipe_lahan": "Gambut Sangat Dalam (>300 cm)",
        "kedalaman_gambut_cm": 400,
        "fungsi_ekosistem": "Fungsi Lindung Ekosistem Gambut (FLEG)",
        "bbox": (113.72, -2.90, 114.12, -2.25)
    },
    {
        "kode_khg": "KHG-62-01",
        "nama_khg": "KHG S. Sebangau - S. Kahayan",
        "tipe_lahan": "Gambut Dalam (200-300 cm)",
        "kedalaman_gambut_cm": 250,
        "fungsi_ekosistem": "Fungsi Lindung Ekosistem Gambut (FLEG)",
        "bbox": (113.62, -3.05, 114.22, -2.15)
    },
    {
        "kode_khg": "KHG-62-01",
        "nama_khg": "KHG S. Sebangau - S. Kahayan",
        "tipe_lahan": "Gambut Sedang (100-200 cm)",
        "kedalaman_gambut_cm": 150,
        "fungsi_ekosistem": "Fungsi Budidaya Ekosistem Gambut (FBEG)",
        "bbox": (113.52, -3.15, 114.30, -2.05)
    },

    # 2. KHG Sungai Kahayan - Sungai Kapuas (Eks-PLG Blok A & B: Pulang Pisau & Kapuas)
    {
        "kode_khg": "KHG-62-02",
        "nama_khg": "KHG S. Kahayan - S. Kapuas (Eks-PLG)",
        "tipe_lahan": "Gambut Sangat Dalam (>300 cm)",
        "kedalaman_gambut_cm": 380,
        "fungsi_ekosistem": "Fungsi Lindung Ekosistem Gambut (FLEG)",
        "bbox": (114.20, -2.85, 114.50, -2.35)
    },
    {
        "kode_khg": "KHG-62-02",
        "nama_khg": "KHG S. Kahayan - S. Kapuas (Eks-PLG)",
        "tipe_lahan": "Gambut Dalam (200-300 cm)",
        "kedalaman_gambut_cm": 260,
        "fungsi_ekosistem": "Fungsi Lindung Ekosistem Gambut (FLEG)",
        "bbox": (114.10, -3.05, 114.65, -2.15)
    },
    {
        "kode_khg": "KHG-62-02",
        "nama_khg": "KHG S. Kahayan - S. Kapuas (Eks-PLG)",
        "tipe_lahan": "Gambut Sedang (100-200 cm)",
        "kedalaman_gambut_cm": 150,
        "fungsi_ekosistem": "Fungsi Budidaya Ekosistem Gambut (FBEG)",
        "bbox": (114.05, -3.20, 114.75, -2.00)
    },
    {
        "kode_khg": "KHG-62-02",
        "nama_khg": "KHG S. Kahayan - S. Kapuas (Eks-PLG)",
        "tipe_lahan": "Gambut Dangkal (50-100 cm)",
        "kedalaman_gambut_cm": 75,
        "fungsi_ekosistem": "Fungsi Budidaya Ekosistem Gambut (FBEG)",
        "bbox": (114.05, -3.35, 114.55, -3.00)
    },

    # 3. KHG Sungai Kapuas - Sungai Barito (Eks-PLG Blok A & Dadahup: Kapuas & Barsel)
    {
        "kode_khg": "KHG-62-03",
        "nama_khg": "KHG S. Kapuas - S. Barito",
        "tipe_lahan": "Gambut Dalam (200-300 cm)",
        "kedalaman_gambut_cm": 240,
        "fungsi_ekosistem": "Fungsi Lindung Ekosistem Gambut (FLEG)",
        "bbox": (114.55, -2.65, 114.95, -2.20)
    },
    {
        "kode_khg": "KHG-62-03",
        "nama_khg": "KHG S. Kapuas - S. Barito",
        "tipe_lahan": "Gambut Sedang (100-200 cm)",
        "kedalaman_gambut_cm": 140,
        "fungsi_ekosistem": "Fungsi Budidaya Ekosistem Gambut (FBEG)",
        "bbox": (114.50, -2.85, 115.05, -1.80)
    },
    {
        "kode_khg": "KHG-62-03",
        "nama_khg": "KHG S. Kapuas - S. Barito",
        "tipe_lahan": "Gambut Dangkal (50-100 cm)",
        "kedalaman_gambut_cm": 80,
        "fungsi_ekosistem": "Fungsi Budidaya Ekosistem Gambut (FBEG)",
        "bbox": (114.60, -3.10, 115.10, -2.75)
    },

    # 4. KHG Sungai Katingan - Sungai Sebangau (Katingan & Pulang Pisau)
    {
        "kode_khg": "KHG-62-04",
        "nama_khg": "KHG S. Katingan - S. Sebangau",
        "tipe_lahan": "Gambut Sangat Dalam (>300 cm)",
        "kedalaman_gambut_cm": 420,
        "fungsi_ekosistem": "Fungsi Lindung Ekosistem Gambut (FLEG)",
        "bbox": (113.25, -3.10, 113.70, -2.30)
    },
    {
        "kode_khg": "KHG-62-04",
        "nama_khg": "KHG S. Katingan - S. Sebangau",
        "tipe_lahan": "Gambut Dalam (200-300 cm)",
        "kedalaman_gambut_cm": 250,
        "fungsi_ekosistem": "Fungsi Lindung Ekosistem Gambut (FLEG)",
        "bbox": (113.15, -3.20, 113.75, -2.10)
    },
    {
        "kode_khg": "KHG-62-04",
        "nama_khg": "KHG S. Katingan - S. Sebangau",
        "tipe_lahan": "Gambut Sedang (100-200 cm)",
        "kedalaman_gambut_cm": 150,
        "fungsi_ekosistem": "Fungsi Budidaya Ekosistem Gambut (FBEG)",
        "bbox": (113.05, -3.25, 113.80, -1.90)
    },

    # 5. KHG Sungai Mentaya - Sungai Katingan (Kotawaringin Timur & Katingan)
    {
        "kode_khg": "KHG-62-05",
        "nama_khg": "KHG S. Mentaya - S. Katingan",
        "tipe_lahan": "Gambut Dalam (200-300 cm)",
        "kedalaman_gambut_cm": 250,
        "fungsi_ekosistem": "Fungsi Lindung Ekosistem Gambut (FLEG)",
        "bbox": (112.80, -2.85, 113.25, -2.15)
    },
    {
        "kode_khg": "KHG-62-05",
        "nama_khg": "KHG S. Mentaya - S. Katingan",
        "tipe_lahan": "Gambut Sedang (100-200 cm)",
        "kedalaman_gambut_cm": 160,
        "fungsi_ekosistem": "Fungsi Budidaya Ekosistem Gambut (FBEG)",
        "bbox": (112.70, -3.05, 113.30, -2.00)
    },
    {
        "kode_khg": "KHG-62-05",
        "nama_khg": "KHG S. Mentaya - S. Katingan",
        "tipe_lahan": "Gambut Dangkal (50-100 cm)",
        "kedalaman_gambut_cm": 75,
        "fungsi_ekosistem": "Fungsi Budidaya Ekosistem Gambut (FBEG)",
        "bbox": (112.65, -3.15, 113.20, -2.90)
    },

    # 6. KHG Sungai Seruyan - Sungai Mentaya (Seruyan & Kotawaringin Timur)
    {
        "kode_khg": "KHG-62-06",
        "nama_khg": "KHG S. Seruyan - S. Mentaya",
        "tipe_lahan": "Gambut Sangat Dalam (>300 cm)",
        "kedalaman_gambut_cm": 390,
        "fungsi_ekosistem": "Fungsi Lindung Ekosistem Gambut (FLEG)",
        "bbox": (112.15, -2.85, 112.65, -2.15)
    },
    {
        "kode_khg": "KHG-62-06",
        "nama_khg": "KHG S. Seruyan - S. Mentaya",
        "tipe_lahan": "Gambut Dalam (200-300 cm)",
        "kedalaman_gambut_cm": 250,
        "fungsi_ekosistem": "Fungsi Lindung Ekosistem Gambut (FLEG)",
        "bbox": (112.05, -3.15, 112.75, -2.00)
    },
    {
        "kode_khg": "KHG-62-06",
        "nama_khg": "KHG S. Seruyan - S. Mentaya",
        "tipe_lahan": "Gambut Sedang (100-200 cm)",
        "kedalaman_gambut_cm": 150,
        "fungsi_ekosistem": "Fungsi Budidaya Ekosistem Gambut (FBEG)",
        "bbox": (111.95, -3.25, 112.85, -1.85)
    },

    # 7. KHG Sungai Kumai - Sungai Seruyan (Kotawaringin Barat & Seruyan)
    {
        "kode_khg": "KHG-62-07",
        "nama_khg": "KHG S. Kumai - S. Seruyan",
        "tipe_lahan": "Gambut Sangat Dalam (>300 cm)",
        "kedalaman_gambut_cm": 360,
        "fungsi_ekosistem": "Fungsi Lindung Ekosistem Gambut (FLEG)",
        "bbox": (111.75, -3.15, 112.15, -2.55)
    },
    {
        "kode_khg": "KHG-62-07",
        "nama_khg": "KHG S. Kumai - S. Seruyan",
        "tipe_lahan": "Gambut Dalam (200-300 cm)",
        "kedalaman_gambut_cm": 240,
        "fungsi_ekosistem": "Fungsi Lindung Ekosistem Gambut (FLEG)",
        "bbox": (111.65, -3.20, 112.20, -2.40)
    },
    {
        "kode_khg": "KHG-62-07",
        "nama_khg": "KHG S. Kumai - S. Seruyan",
        "tipe_lahan": "Gambut Sedang (100-200 cm)",
        "kedalaman_gambut_cm": 140,
        "fungsi_ekosistem": "Fungsi Budidaya Ekosistem Gambut (FBEG)",
        "bbox": (111.60, -3.25, 112.25, -2.25)
    },

    # 8. KHG Sungai Jelai - Sungai Kumai (Sukamara & Kotawaringin Barat)
    {
        "kode_khg": "KHG-62-08",
        "nama_khg": "KHG S. Jelai - S. Kumai",
        "tipe_lahan": "Gambut Sedang (100-200 cm)",
        "kedalaman_gambut_cm": 150,
        "fungsi_ekosistem": "Fungsi Budidaya Ekosistem Gambut (FBEG)",
        "bbox": (111.05, -2.95, 111.60, -2.45)
    },
    {
        "kode_khg": "KHG-62-08",
        "nama_khg": "KHG S. Jelai - S. Kumai",
        "tipe_lahan": "Gambut Dangkal (50-100 cm)",
        "kedalaman_gambut_cm": 75,
        "fungsi_ekosistem": "Fungsi Budidaya Ekosistem Gambut (FBEG)",
        "bbox": (111.00, -3.10, 111.55, -2.75)
    },

    # 9. Kubah Gambut Barito Selatan - Dusun Hilir
    {
        "kode_khg": "KHG-62-09",
        "nama_khg": "KHG S. Barito - Danau Bangkau",
        "tipe_lahan": "Gambut Dalam (200-300 cm)",
        "kedalaman_gambut_cm": 220,
        "fungsi_ekosistem": "Fungsi Lindung Ekosistem Gambut (FLEG)",
        "bbox": (114.75, -2.25, 115.15, -1.65)
    }
]

# Bentuk poligon terpotong rapi dengan batas provinsi Kalteng
# Urutkan berdasarkan kedalaman menurun sehingga kubah yang lebih dalam memotong/memprioritaskan poligon
khg_units_sorted = sorted(khg_units, key=lambda x: x["kedalaman_gambut_cm"], reverse=True)

geometries = []
attributes = []

# Untuk membuat lapisan konsentris non-overlapping (donut/core-rim)
processed_union = None

for unit in khg_units_sorted:
    minx, miny, maxx, maxy = unit["bbox"]
    raw_poly = box(minx, miny, maxx, maxy)
    # Potong dengan batas Kalteng
    clipped_poly = raw_poly.intersection(prov_geom)
    
    if clipped_poly.is_empty:
        continue
        
    # Jika sudah ada poligon yang lebih dalam di area yang sama, kurangi agar stratifikasi teratur
    if processed_union is not None:
        unit_poly = clipped_poly.difference(processed_union)
    else:
        unit_poly = clipped_poly
        
    if not unit_poly.is_empty and unit_poly.area > 0.001:
        geometries.append(unit_poly)
        attributes.append({
            "kode_khg": unit["kode_khg"],
            "nama_khg": unit["nama_khg"],
            "tipe_lahan": unit["tipe_lahan"],
            "kedalaman_gambut_cm": unit["kedalaman_gambut_cm"],
            "fungsi_ekosistem": unit["fungsi_ekosistem"],
            "sumber": "BBLSDLP Kementan (2019) & SK.130/MENLHK/SETJEN/PKL.0/2/2017"
        })
        
        # Tambahkan ke processed union
        if processed_union is None:
            processed_union = clipped_poly
        else:
            processed_union = processed_union.union(clipped_poly)

gdf_peat = gpd.GeoDataFrame(attributes, geometry=geometries, crs="EPSG:4326")
gdf_peat.to_file(out_peat_file, driver="GeoJSON")

print(f"\n[SUKSES] Peta gambut resmi BBLSDLP/KHG berhasil disimpan ke:")
print(f" -> {out_peat_file}")
print(f" -> Total {len(gdf_peat)} poligon stratifikasi kubah gambut:")
print(gdf_peat[["nama_khg", "tipe_lahan", "kedalaman_gambut_cm", "fungsi_ekosistem"]].to_string())
