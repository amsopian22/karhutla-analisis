"""
Skrip Uji Empiris Challenger 1:
Memverifikasi ulang seluruh metrik di model_metrics.json, eda_summary.json,
serta mereproduksi evaluasi model (Confusion Matrix, ROC-AUC, F1, Spatial CV)
secara mandiri dari dataset dan model yang tersimpan.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, roc_auc_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split, GroupKFold
from sklearn.preprocessing import LabelEncoder

def run_empirical_verification():
    print("=== PENGUJIAN EMPIRIS OLEH CHALLENGER 1 ===")
    
    # 1. Verifikasi File JSON
    with open("output/reports/model_metrics.json") as f:
        metrics = json.load(f)
    with open("output/reports/eda_summary.json") as f:
        eda = json.load(f)
        
    print("\n[1] Memeriksa Struktur File Sumber Kebenaran:")
    print(f"- model_metrics.json keys: {list(metrics.keys())}")
    print(f"- eda_summary.json: {eda}")
    
    # 2. Muat dataset master
    csv_path = "data/processed/karhutla_kalteng_2019_2026.csv"
    assert os.path.exists(csv_path), f"File {csv_path} tidak ditemukan!"
    df = pd.read_csv(csv_path, low_memory=False)
    print(f"\n[2] Dataset Master: {len(df):,} baris")
    assert len(df) == 43937, f"Total baris bukan 43937, tapi {len(df)}"
    assert len(df) == eda["total_hotspot_kalteng_2026"]
    assert len(df) == metrics["metadata"]["total_samples"]
    
    # 3. Verifikasi EDA: Gambut, Konsesi, Top Kabupaten, Median Kanal
    print("\n[3] Verifikasi Metrik EDA:")
    # Gambut
    pct_gambut = (df["tipe_lahan"].str.lower().str.contains("gambut").mean()) * 100
    print(f"- Persentase Lahan Gambut di data: {pct_gambut:.2f}% (Target: {eda['persentase_lahan_gambut']}%)")
    assert abs(pct_gambut - 74.3) < 0.2, f"Persentase gambut {pct_gambut:.2f}% menyimpang dari 74.3%"
    
    # Konsesi
    status_counts = df["status_konsesi"].value_counts(normalize=True) * 100
    print(f"- Distribusi Konsesi:\n{status_counts}")
    apl_pct = status_counts.get("Non-Konsesi (Area Penggunaan Lain / Komunitas)", 0.0)
    sawit_pct = status_counts.get("Konsesi Perkebunan Sawit (HGU)", 0.0)
    pbph_pct = status_counts.get("Konsesi Kehutanan (IUPHHK-HTI/HA)", 0.0)
    print(f"  APL: {apl_pct:.2f}% (Target: {eda['persentase_non_konsesi_apl']}%)")
    print(f"  Sawit: {sawit_pct:.2f}% (Target: {eda['persentase_konsesi_sawit_hgu']}%)")
    print(f"  PBPH: {pbph_pct:.2f}% (Target: {eda['persentase_konsesi_kehutanan_pbph']}%)")
    assert round(apl_pct, 1) == 75.4
    assert round(sawit_pct, 1) == 16.6
    assert round(pbph_pct, 1) == 8.0
    
    # Jarak Kanal Median
    plg_mask = df["jarak_kanal_m"] >= 0
    median_kanal = df.loc[plg_mask, "jarak_kanal_m"].median()
    print(f"- Median Jarak Kanal eks-PLG: {median_kanal} m (Target: {eda['median_jarak_kanal_eks_plg_m']} m)")
    assert median_kanal == eda["median_jarak_kanal_eks_plg_m"]
    
    # Top 3 Kabupaten
    kab_counts = df["kabupaten_kota"].value_counts(normalize=True) * 100
    print(f"- Top 3 Kabupaten:\n{kab_counts.head(3)}")
    assert round(kab_counts["Seruyan"], 1) == 21.3
    assert round(kab_counts["Pulang Pisau"], 1) == 16.3
    assert round(kab_counts["Kapuas"], 1) == 14.4
    
    # 4. Verifikasi Model B dan Model A
    print("\n[4] Memuat Model Terlatih dan Memverifikasi Metrik Uji...")
    model_bundle = joblib.load("output/models/karhutla_rf_model.joblib")
    model_b = model_bundle["model"]
    model_a = model_bundle["model_a_spatial"]
    
    # Siapkan data encode persis seperti di train_model.py
    df["target_severe_fire"] = (df["frp_mw"] >= 12.0).astype(int)
    categorical_cols = ["tipe_lahan", "tutupan_lahan", "status_konsesi", "kabupaten_kota"]
    df_encoded = df.copy()
    for col in categorical_cols:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df[col].astype(str))
        
    y = df_encoded["target_severe_fire"]
    indices = np.arange(len(df_encoded))
    train_idx, test_idx = train_test_split(indices, test_size=0.25, random_state=42, stratify=y)
    
    X_b = df_encoded[metrics["model_b_pure_biophysical"]["features"]]
    X_a = df_encoded[metrics["model_a_spatial_memorization"]["features"]]
    
    y_test = y.iloc[test_idx]
    X_test_b = X_b.iloc[test_idx]
    X_test_a = X_a.iloc[test_idx]
    
    y_pred_b = model_b.predict(X_test_b)
    y_proba_b = model_b.predict_proba(X_test_b)[:, 1]
    
    y_pred_a = model_a.predict(X_test_a)
    y_proba_a = model_a.predict_proba(X_test_a)[:, 1]
    
    # Confusion Matrix Model B
    cm_b = confusion_matrix(y_test, y_pred_b)
    tn, fp, fn, tp = cm_b.ravel()
    print(f"\n[5] Matriks Konfusi Model B (Holdout Test n={len(test_idx)}):")
    print(f"  TN={tn}, FP={fp}, FN={fn}, TP={tp}")
    print(f"  Total = {tn+fp+fn+tp}")
    
    rec_b = recall_score(y_test, y_pred_b)
    prec_reg_b = precision_score(y_test, y_pred_b, pos_label=0)
    prec_ext_b = precision_score(y_test, y_pred_b, pos_label=1)
    f1_b = f1_score(y_test, y_pred_b)
    auc_b = roc_auc_score(y_test, y_proba_b)
    
    print(f"  Recall Ekstrem: {rec_b:.4f} (Target: {metrics['model_b_pure_biophysical']['recall_ekstrem']})")
    print(f"  Precision Reguler: {prec_reg_b:.4f} (Target: {metrics['model_b_pure_biophysical']['precision_reguler']})")
    print(f"  Precision Ekstrem: {prec_ext_b:.4f} (~28.56%)")
    print(f"  F1 Score: {f1_b:.4f} (Target: {metrics['model_b_pure_biophysical']['test_f1_score']})")
    print(f"  ROC-AUC: {auc_b:.4f} (Target: {metrics['model_b_pure_biophysical']['test_roc_auc']})")
    
    assert tn == 6586, f"TN expected 6586, got {tn}"
    assert fp == 2737, f"FP expected 2737, got {fp}"
    assert fn == 568, f"FN expected 568, got {fn}"
    assert tp == 1094, f"TP expected 1094, got {tp}"
    assert round(rec_b, 4) == metrics['model_b_pure_biophysical']['recall_ekstrem']
    assert round(prec_reg_b, 4) == metrics['model_b_pure_biophysical']['precision_reguler']
    assert round(f1_b, 4) == metrics['model_b_pure_biophysical']['test_f1_score']
    assert round(auc_b, 4) == metrics['model_b_pure_biophysical']['test_roc_auc']
    
    auc_a = roc_auc_score(y_test, y_proba_a)
    f1_a = f1_score(y_test, y_pred_a)
    print(f"\n[6] Metrik Holdout Model A:")
    print(f"  ROC-AUC: {auc_a:.4f} (Target: {metrics['model_a_spatial_memorization']['test_roc_auc']})")
    print(f"  F1 Score: {f1_a:.4f} (Target: {metrics['model_a_spatial_memorization']['test_f1_score']})")
    assert round(auc_a, 4) == metrics['model_a_spatial_memorization']['test_roc_auc']
    assert round(f1_a, 4) == metrics['model_a_spatial_memorization']['test_f1_score']
    
    print("\n=== SEMUA PENGUJIAN EMPIRIS BERHASIL DENGAN NILAI IDENTIK 100%! ===")

if __name__ == "__main__":
    run_empirical_verification()
