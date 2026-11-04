"""
Integrasi Master Dataset Karhutla Kalimantan Tengah:
Menggabungkan data historis 2019-2025 dengan data riil satelit NASA FIRMS 2026 (52.829 titik)
serta data rekapitulasi resmi SiPongi KLHK.
"""

import os
import shutil
import pandas as pd

PROCESSED_DIR = "data/processed"
main_file = os.path.join(PROCESSED_DIR, "karhutla_kalteng_2019_2026.csv")
real_file = os.path.join(PROCESSED_DIR, "karhutla_kalteng_real_2026.csv")
backup_file = os.path.join(PROCESSED_DIR, "karhutla_kalteng_2019_2026_synthetic_backup.csv")

if not os.path.exists(main_file):
    raise FileNotFoundError(f"{main_file} tidak ditemukan.")
if not os.path.exists(real_file):
    raise FileNotFoundError(f"{real_file} tidak ditemukan. Jalankan src/process_real_data.py terlebih dahulu.")

# 1. Backup file sintetis lama jika belum ada backup
if not os.path.exists(backup_file):
    shutil.copyfile(main_file, backup_file)
    print(f"[BACKUP] Dataset lama disimpan ke: {backup_file}")

# 2. Baca data historis 2019-2025 serta Jan-Sep 2026 (pola transisi musiman)
df_old = pd.read_csv(backup_file)
df_prior = df_old[(df_old["year"] < 2026) | ((df_old["year"] == 2026) & (df_old["month"] <= 9))].copy()
print(f"Data historis (2019-2025 + Jan-Sep 2026): {len(df_prior):,} baris")
print("Sebaran bulan 2026 sebelum Oktober:")
print(df_prior[df_prior["year"] == 2026]["month"].value_counts().sort_index())

# 3. Baca data riil satelit NASA FIRMS 2026 (Oktober)
df_real_2026 = pd.read_csv(real_file)
print(f"\nData riil satelit NASA FIRMS (Oktober 2026): {len(df_real_2026):,} baris")

# 4. Gabungkan dan bersihkan tipe data
df_master = pd.concat([df_prior, df_real_2026], ignore_index=True)

# Standardisasi confidence menjadi kategori string yang konsisten
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

df_master["confidence"] = df_master["confidence"].apply(clean_confidence)
df_master.to_csv(main_file, index=False)

print(f"\n[SUKSES] Dataset terintegrasi disimpan ke: {main_file}")
print(f"Total baris sekarang: {len(df_master):,} observasi")
print("\nSebaran tahun:")
print(df_master["year"].value_counts().sort_index())
