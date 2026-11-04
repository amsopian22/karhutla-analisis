#!/usr/bin/env python3
"""
Test Harness & Adversarial Oracle for Manuscript Empirical Metrics Verification
Author: Challenger 2 (Milestone 2)
"""

import json
import os
import re
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GroupKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    confusion_matrix,
    roc_auc_score,
    f1_score,
    precision_score,
    recall_score
)
from scipy.stats import mannwhitneyu

def run_empirical_audit():
    print("=" * 80)
    print("STARTING COMPREHENSIVE EMPIRICAL AUDIT")
    print("=" * 80)
    
    # 1. Load Ground Truth JSON Reports
    with open("output/reports/model_metrics.json") as f:
        metrics_json = json.load(f)
    with open("output/reports/eda_summary.json") as f:
        eda_json = json.load(f)
    with open("output/reports/transboundary_haze_summary.json") as f:
        haze_json = json.load(f)
        
    print("[OK] Loaded JSON reports successfully.")
    
    # 2. Load Master Processed Dataset
    csv_path = "data/processed/karhutla_kalteng_2019_2026.csv"
    df = pd.read_csv(csv_path, low_memory=False)
    print(f"[OK] Loaded dataset: {len(df):,} rows.")
    
    # 3. Load SiPongi Data
    sipongi_path = "data/raw/sipongi_luas_karhutla_kalteng_2018_2026.csv"
    if os.path.exists(sipongi_path):
        df_sipongi = pd.read_csv(sipongi_path)
        print(f"[OK] Loaded SiPongi data: {len(df_sipongi)} rows.")
    else:
        df_sipongi = None
        print("[WARN] SiPongi data not found.")
        
    audit_results = {}
    
    # -------------------------------------------------------------
    # AUDIT SECTION 1: DATASET TOTALS & SPATIAL CLIPPING
    # -------------------------------------------------------------
    total_samples = len(df)
    audit_results["total_samples"] = {
        "expected": 43937,
        "actual": total_samples,
        "match": total_samples == 43937
    }
    
    # Check raw vs clipped
    raw_path = "data/raw/firms_real_kalteng_latest_7d.csv"
    if os.path.exists(raw_path):
        df_raw = pd.read_csv(raw_path, low_memory=False)
        raw_count = len(df_raw)
        clipped_out = raw_count - total_samples
        clipped_out_pct = (clipped_out / raw_count) * 100
        audit_results["clipping"] = {
            "raw_count": raw_count,
            "clipped_out": clipped_out,
            "clipped_out_pct": round(clipped_out_pct, 2)
        }
    
    # -------------------------------------------------------------
    # AUDIT SECTION 2: REGENCY HOTSPOT DISTRIBUTION
    # -------------------------------------------------------------
    reg_counts = df["kabupaten_kota"].value_counts()
    reg_pcts = (reg_counts / total_samples) * 100
    audit_results["regency_distribution"] = {}
    for reg, count in reg_counts.items():
        audit_results["regency_distribution"][reg] = {
            "count": int(count),
            "pct": round(float(reg_pcts[reg]), 2)
        }
        
    top3_count = reg_counts.iloc[:3].sum()
    top3_pct = (top3_count / total_samples) * 100
    audit_results["top3_regencies"] = {
        "count": int(top3_count),
        "pct": round(float(top3_pct), 2)
    }
    
    # -------------------------------------------------------------
    # AUDIT SECTION 3: PEATLAND STRATIFICATION & CANAL DISTANCES
    # -------------------------------------------------------------
    # Tipe lahan
    peat_types = df["tipe_lahan"].value_counts()
    is_peat = df["tipe_lahan"] != "Tanah Mineral"
    peat_count = is_peat.sum()
    mineral_count = (~is_peat).sum()
    peat_pct = (peat_count / total_samples) * 100
    mineral_pct = (mineral_count / total_samples) * 100
    
    audit_results["peat_mineral"] = {
        "peat_count": int(peat_count),
        "peat_pct": round(float(peat_pct), 2),
        "mineral_count": int(mineral_count),
        "mineral_pct": round(float(mineral_pct), 2)
    }
    
    # Peat depth detail
    audit_results["peat_depth_strata"] = {}
    for t, cnt in peat_types.items():
        audit_results["peat_depth_strata"][t] = {
            "count": int(cnt),
            "pct": round(float((cnt / total_samples) * 100), 2)
        }
    
    # Deep + Very Deep (> 200 cm)
    deep_mask = df["tipe_lahan"].isin(["Gambut Dalam (1-3m)", "Gambut Dalam (2-3m)", "Gambut Sangat Dalam (>3m)"])
    # Let's see actual categories in tipe_lahan
    audit_results["tipe_lahan_unique"] = list(df["tipe_lahan"].unique())
    
    # Canal distances in ex-PLG
    # In process_real_data.py, ex_plg landscape is Pulang Pisau, Kapuas, Kota Palangka Raya
    ex_plg_mask = df["kabupaten_kota"].isin(["Pulang Pisau", "Kapuas", "Kota Palangka Raya"])
    df_ex_plg = df[ex_plg_mask]
    median_canal_all = df_ex_plg["jarak_kanal_m"].median()
    
    # Severe vs regular
    severe_mask = df_ex_plg["frp_mw"] >= 12.0
    median_canal_severe = df_ex_plg[severe_mask]["jarak_kanal_m"].median()
    median_canal_regular = df_ex_plg[~severe_mask]["jarak_kanal_m"].median()
    
    u_stat, p_val = mannwhitneyu(df_ex_plg[severe_mask]["jarak_kanal_m"],
                                 df_ex_plg[~severe_mask]["jarak_kanal_m"])
    
    audit_results["canal_distances"] = {
        "ex_plg_count": len(df_ex_plg),
        "median_all": float(median_canal_all),
        "median_severe": float(median_canal_severe),
        "median_regular": float(median_canal_regular),
        "mann_whitney_p": float(p_val)
    }
    
    # -------------------------------------------------------------
    # AUDIT SECTION 4: LAND TENURE & CONCESSIONS
    # -------------------------------------------------------------
    tenure_counts = df["status_konsesi"].value_counts()
    tenure_pcts = (tenure_counts / total_samples) * 100
    audit_results["tenure"] = {}
    for ten, cnt in tenure_counts.items():
        audit_results["tenure"][ten] = {
            "count": int(cnt),
            "pct": round(float(tenure_pcts[ten]), 2)
        }
        
    # Specific corporate entities
    # In spatial_join_concessions.py, let's see which columns exist for company name
    company_cols = [c for c in df.columns if "nama" in c.lower() or "perusahaan" in c.lower() or "konsesi" in c.lower() or "unit" in c.lower() or "pemegang" in c.lower()]
    print("Potential company columns:", company_cols)
    
    # -------------------------------------------------------------
    # AUDIT SECTION 5: MODEL B & MODEL A CONFUSION MATRIX & METRICS
    # -------------------------------------------------------------
    bundle = joblib.load("output/models/karhutla_rf_model.joblib")
    df_encoded = df.copy()
    for col in ["tipe_lahan", "tutupan_lahan", "status_konsesi", "kabupaten_kota"]:
        df_encoded[col] = bundle["label_encoders"][col].transform(df[col].astype(str))
        
    df_encoded["target_severe_fire"] = (df["frp_mw"] >= 12.0).astype(int)
    y = df_encoded["target_severe_fire"]
    indices = np.arange(len(df_encoded))
    train_idx, test_idx = train_test_split(indices, test_size=0.25, random_state=42, stratify=y)
    
    y_test = y.iloc[test_idx]
    
    # Model B
    model_b = bundle["model"]
    X_b = df_encoded[bundle["features"]]
    y_pred_b = model_b.predict(X_b.iloc[test_idx])
    y_proba_b = model_b.predict_proba(X_b.iloc[test_idx])[:, 1]
    
    cm_b = confusion_matrix(y_test, y_pred_b)
    tn_b, fp_b, fn_b, tp_b = cm_b.ravel()
    
    audit_results["model_b_holdout"] = {
        "TN": int(tn_b),
        "FP": int(fp_b),
        "FN": int(fn_b),
        "TP": int(tp_b),
        "ROC_AUC": round(float(roc_auc_score(y_test, y_proba_b)), 4),
        "F1": round(float(f1_score(y_test, y_pred_b)), 4),
        "precision_reg": round(float(precision_score(y_test, y_pred_b, pos_label=0)), 4),
        "recall_ext": round(float(recall_score(y_test, y_pred_b, pos_label=1)), 4),
        "precision_ext": round(float(precision_score(y_test, y_pred_b, pos_label=1)), 4),
        "recall_reg": round(float(recall_score(y_test, y_pred_b, pos_label=0)), 4)
    }
    
    # Model A
    model_a = bundle["model_a_spatial"]
    X_a = df_encoded[bundle["features_a"]]
    y_pred_a = model_a.predict(X_a.iloc[test_idx])
    y_proba_a = model_a.predict_proba(X_a.iloc[test_idx])[:, 1]
    
    cm_a = confusion_matrix(y_test, y_pred_a)
    tn_a, fp_a, fn_a, tp_a = cm_a.ravel()
    
    audit_results["model_a_holdout"] = {
        "TN": int(tn_a),
        "FP": int(fp_a),
        "FN": int(fn_a),
        "TP": int(tp_a),
        "ROC_AUC": round(float(roc_auc_score(y_test, y_proba_a)), 4),
        "F1": round(float(f1_score(y_test, y_pred_a)), 4),
        "precision_reg": round(float(precision_score(y_test, y_pred_a, pos_label=0)), 4),
        "recall_ext": round(float(recall_score(y_test, y_pred_a, pos_label=1)), 4),
        "precision_ext": round(float(precision_score(y_test, y_pred_a, pos_label=1)), 4),
        "recall_reg": round(float(recall_score(y_test, y_pred_a, pos_label=0)), 4)
    }
    
    # -------------------------------------------------------------
    # AUDIT SECTION 6: TEMPORAL DIURNAL / DAILY COUNTS
    # -------------------------------------------------------------
    daily_counts = df["acq_date"].value_counts().sort_index()
    audit_results["daily_counts"] = {str(k): int(v) for k, v in daily_counts.items()}
    
    return audit_results, metrics_json, eda_json

if __name__ == "__main__":
    results, m_json, e_json = run_empirical_audit()
    print("\n" + "=" * 40 + " AUDIT SUMMARY " + "=" * 40)
    print(json.dumps(results, indent=2))
