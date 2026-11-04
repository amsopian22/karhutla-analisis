"""
Pemodelan Prediktif Spasiotemporal & Explainable AI (Random Forest + SHAP TreeExplainer)
Komparasi Dua Model: Model Hafalan Spasial (Model A) vs Model Biofisik Murni (Model B)
Dengan Validasi Silang Blok Spasial (Spatial Block Cross-Validation per Kabupaten).

Pembaruan Metodologis (Resolusi Celah 3):
1. Target Prediksi: Estimasi Risiko Intensitas Api Ekstrem (FRP >= 12.0 MW).
2. Komparasi Dua Model:
   - Model A (Spatial Memorization): Melibatkan Latitude, Longitude, dan Kabupaten.
   - Model B (Pure Biophysical): Tanpa Latitude/Longitude/Kabupaten, berbasis proses biofisik murni
     (Curah Hujan ERA5, Dry Spell, Suhu, Kelembapan, Angin, Kedalaman Gambut BBLSDLP, Kanal PLG, Konsesi).
3. Validasi Ganda:
   - Evaluasi Random / Stratified Test Split (75:25).
   - Validasi Silang Blok Spasial (Spatial Block CV via GroupKFold 5-Fold per Kabupaten).
4. Explainable AI (XAI):
   - Eksekusi SHAP TreeExplainer Asli (shap.TreeExplainer) pada Model B.
   - Pembuatan Gambar 07: SHAP Summary Beeswarm Plot yang sah dan informatif.
   - Pembuatan Gambar 06: Komparasi Kurva ROC Spasial & Matriks Konfusi.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold, train_test_split
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
    confusion_matrix,
    roc_curve,
    f1_score,
    precision_score,
    recall_score
)
import shap

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["figure.dpi"] = 300
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

def train_karhutla_model(csv_path="data/processed/karhutla_kalteng_2019_2026.csv",
                         output_fig_dir="output/figures",
                         output_report_dir="output/reports",
                         output_model_dir="output/models"):
    
    os.makedirs(output_fig_dir, exist_ok=True)
    os.makedirs(output_report_dir, exist_ok=True)
    os.makedirs(output_model_dir, exist_ok=True)
    
    print("=" * 70)
    print("1. MEMUAT DATASET TERKALIBRASI & PENETAPAN TARGET PREDIKSI")
    print("=" * 70)
    df = pd.read_csv(csv_path, low_memory=False)
    
    # Target: Api Ekstrem Berenergi Radiasi Tinggi (FRP >= 12.0 MW)
    df["target_severe_fire"] = (df["frp_mw"] >= 12.0).astype(int)
    pos_rate = df["target_severe_fire"].mean() * 100
    print(f"Total Sampel: {len(df):,} titik api. Proporsi Api Ekstrem (FRP >= 12 MW): {pos_rate:.1f}%")
    
    # Label Encoding Kolom Kategori
    categorical_cols = ["tipe_lahan", "tutupan_lahan", "status_konsesi", "kabupaten_kota"]
    label_encoders = {}
    df_encoded = df.copy()
    for col in categorical_cols:
        le = LabelEncoder()
        df_encoded[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le
        
    y = df_encoded["target_severe_fire"]
    groups = df["kabupaten_kota"]
    
    # -------------------------------------------------------------------------
    # DEFINISI FITUR UNTUK DUA MODEL
    # -------------------------------------------------------------------------
    # Model A: Baseline Hafalan Koordinat (Termasuk Lat/Lon dan Kabupaten)
    features_a = [
        "latitude", "longitude",
        "kedalaman_gambut_cm", "jarak_kanal_m", "is_ex_plg_landscape",
        "curah_hujan_7h_mm", "suhu_maks_c", "kelembapan_relatif_pct",
        "kecepatan_angin_kmh", "dry_spell_days", "fwi_score",
        "kabupaten_kota", "tipe_lahan", "tutupan_lahan", "status_konsesi"
    ]
    
    # Model B: Model Biofisik Murni (TANPA Lat/Lon dan TANPA Kabupaten) - MODEL UTAMA
    features_b = [
        "kedalaman_gambut_cm", "jarak_kanal_m", "is_ex_plg_landscape",
        "curah_hujan_7h_mm", "suhu_maks_c", "kelembapan_relatif_pct",
        "kecepatan_angin_kmh", "dry_spell_days", "fwi_score",
        "tipe_lahan", "tutupan_lahan", "status_konsesi"
    ]
    
    X_a = df_encoded[features_a]
    X_b = df_encoded[features_b]
    
    print(f"\nModel A (Spatial Memorization): {len(features_a)} fitur (dengan Lat/Lon/Kabupaten)")
    print(f"Model B (Pure Biophysical):      {len(features_b)} fitur (tanpa Lat/Lon/Kabupaten)")
    
    # -------------------------------------------------------------------------
    # 2. VALIDASI SILANG BLOK SPASIAL (SPATIAL BLOCK CV: GroupKFold per Kabupaten)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("2. SPATIAL BLOCK CROSS-VALIDATION (GroupKFold 5-Fold per Kabupaten)")
    print("=" * 70)
    gkf = GroupKFold(n_splits=5)
    
    # Kumpulkan daftar kabupaten per fold
    fold_kabs = []
    for _, val_idx in gkf.split(X_a, y, groups):
        val_kabs = sorted(df.iloc[val_idx]["kabupaten_kota"].unique().tolist())
        fold_kabs.append(val_kabs)

    # Evaluasi Model A di Spatial Block CV
    spatial_aucs_a, spatial_f1s_a = [], []
    for fold, (train_idx, val_idx) in enumerate(gkf.split(X_a, y, groups)):
        clf_a = RandomForestClassifier(
            n_estimators=100, max_depth=9, min_samples_split=6,
            class_weight="balanced", random_state=42 + fold, n_jobs=-1
        )
        clf_a.fit(X_a.iloc[train_idx], y.iloc[train_idx])
        y_val_proba_a = clf_a.predict_proba(X_a.iloc[val_idx])[:, 1]
        y_val_pred_a = clf_a.predict(X_a.iloc[val_idx])
        
        spatial_aucs_a.append(roc_auc_score(y.iloc[val_idx], y_val_proba_a))
        spatial_f1s_a.append(f1_score(y.iloc[val_idx], y_val_pred_a, zero_division=0))
        
    # Evaluasi Model B di Spatial Block CV
    spatial_aucs_b, spatial_f1s_b = [], []
    for fold, (train_idx, val_idx) in enumerate(gkf.split(X_b, y, groups)):
        clf_b = RandomForestClassifier(
            n_estimators=100, max_depth=9, min_samples_split=6,
            class_weight="balanced", random_state=42 + fold, n_jobs=-1
        )
        clf_b.fit(X_b.iloc[train_idx], y.iloc[train_idx])
        y_val_proba_b = clf_b.predict_proba(X_b.iloc[val_idx])[:, 1]
        y_val_pred_b = clf_b.predict(X_b.iloc[val_idx])
        
        spatial_aucs_b.append(roc_auc_score(y.iloc[val_idx], y_val_proba_b))
        spatial_f1s_b.append(f1_score(y.iloc[val_idx], y_val_pred_b, zero_division=0))
        
    print(f"Hasil Spatial Block CV (5-Fold):")
    print(f" -> Model A (Dengan Lat/Lon): Mean ROC-AUC = {np.mean(spatial_aucs_a):.4f} (+/- {np.std(spatial_aucs_a):.4f}), F1 = {np.mean(spatial_f1s_a):.4f}")
    print(f" -> Model B (Biofisik Murni): Mean ROC-AUC = {np.mean(spatial_aucs_b):.4f} (+/- {np.std(spatial_aucs_b):.4f}), F1 = {np.mean(spatial_f1s_b):.4f}")
    
    # -------------------------------------------------------------------------
    # 3. EVALUASI HOLDOUT TEST SET (Stratified 75:25 Split)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("3. EVALUASI STRATIFIED HOLDOUT TEST SET (75:25 SPLIT)")
    print("=" * 70)
    indices = np.arange(len(df_encoded))
    train_idx, test_idx = train_test_split(indices, test_size=0.25, random_state=42, stratify=y)
    
    # Train Model A pada Holdout
    model_a = RandomForestClassifier(
        n_estimators=150, max_depth=10, min_samples_split=6,
        class_weight="balanced", random_state=42, n_jobs=-1
    )
    model_a.fit(X_a.iloc[train_idx], y.iloc[train_idx])
    y_test_proba_a = model_a.predict_proba(X_a.iloc[test_idx])[:, 1]
    y_test_pred_a = model_a.predict(X_a.iloc[test_idx])
    
    auc_test_a = roc_auc_score(y.iloc[test_idx], y_test_proba_a)
    f1_test_a = f1_score(y.iloc[test_idx], y_test_pred_a)
    
    # Train Model B pada Holdout
    model_b = RandomForestClassifier(
        n_estimators=150, max_depth=10, min_samples_split=6,
        class_weight="balanced", random_state=42, n_jobs=-1
    )
    model_b.fit(X_b.iloc[train_idx], y.iloc[train_idx])
    y_test_proba_b = model_b.predict_proba(X_b.iloc[test_idx])[:, 1]
    y_test_pred_b = model_b.predict(X_b.iloc[test_idx])
    
    auc_test_b = roc_auc_score(y.iloc[test_idx], y_test_proba_b)
    f1_test_b = f1_score(y.iloc[test_idx], y_test_pred_b)
    prec_reg_b = precision_score(y.iloc[test_idx], y_test_pred_b, pos_label=0)
    rec_ext_b = recall_score(y.iloc[test_idx], y_test_pred_b, pos_label=1)
    
    print(f"Hasil Testing Set (10.985 titik):")
    print(f" • Model A (Spatial Memorization): ROC-AUC = {auc_test_a:.4f}, F1 = {f1_test_a:.4f}")
    print(f" • Model B (Pure Biophysical):      ROC-AUC = {auc_test_b:.4f}, F1 = {f1_test_b:.4f}")
    print(f"   - Precision Reguler (Model B): {prec_reg_b*100:.1f}%")
    print(f"   - Recall Ekstrem (Model B):    {rec_ext_b*100:.1f}%")
    
    # -------------------------------------------------------------------------
    # 4. GAMBAR 06: KOMPARASI KURVA ROC & MATRIKS KONFUSI (MODEL EVALUATION)
    # -------------------------------------------------------------------------
    print("\n4. Menghasilkan visualisasi Gambar 06 (Evaluasi Model & Komparasi)...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    
    # Kurva ROC Komparasi
    fpr_b, tpr_b, _ = roc_curve(y.iloc[test_idx], y_test_proba_b)
    fpr_a, tpr_a, _ = roc_curve(y.iloc[test_idx], y_test_proba_a)
    
    ax1.plot(fpr_b, tpr_b, color="#dc2626", lw=2.6,
             label=f"Model B - Pure Biophysical (Test AUC = {auc_test_b:.3f} | Spatial CV = {np.mean(spatial_aucs_b):.3f})")
    ax1.plot(fpr_a, tpr_a, color="#2563eb", lw=1.8, linestyle="--",
             label=f"Model A - Spatial Memory (Test AUC = {auc_test_a:.3f} | Spatial CV = {np.mean(spatial_aucs_a):.3f})")
    ax1.plot([0, 1], [0, 1], color="#94a3b8", lw=1.2, linestyle=":", label="Random Guess (AUC = 0.500)")
    
    ax1.set_xlim([0.0, 1.0])
    ax1.set_ylim([0.0, 1.05])
    ax1.set_xlabel("False Positive Rate (1 - Specificity)", fontsize=10, fontweight="bold")
    ax1.set_ylabel("True Positive Rate (Sensitivity / Recall)", fontsize=10, fontweight="bold")
    ax1.set_title("ROC Curves: Pure Biophysical Model vs. Spatial Memorization", fontsize=11.5, fontweight="bold", pad=12)
    ax1.legend(loc="lower right", frameon=True, fontsize=8.5)
    ax1.grid(True, linestyle="--", alpha=0.5)
    
    # Matriks Konfusi Model B
    cm_b = confusion_matrix(y.iloc[test_idx], y_test_pred_b)
    sns.heatmap(cm_b, annot=True, fmt=",d", cmap="Reds", cbar=False, ax=ax2,
                xticklabels=["Predicted Regular", "Predicted Severe"],
                yticklabels=["Actual Regular", "Actual Severe"],
                annot_kws={"size": 11, "fontweight": "bold"})
    ax2.set_title(f"Model B Confusion Matrix on Test Set ({len(test_idx):,} Samples)", fontsize=11.5, fontweight="bold", pad=12)
    ax2.set_xlabel("Predicted Class (AI Classification)", fontsize=10, fontweight="bold")
    ax2.set_ylabel("Ground Truth (Satellite Observation)", fontsize=10, fontweight="bold")

    plt.tight_layout()
    fig6_path = os.path.join(output_fig_dir, "06_evaluasi_model_ml.png")
    plt.savefig(fig6_path)
    plt.close()
    print(f" -> Gambar 06 tersimpan: {fig6_path}")
    
    # -------------------------------------------------------------------------
    # 5. EXPLAINABLE AI: SHAP TREEEXPLAINER ASLI PADA MODEL B (GAMBAR 07)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("5. MENGHITUNG NILAI SHAP SEJATI (shap.TreeExplainer) PADA MODEL B")
    print("=" * 70)
    
    # Sample representatif test set untuk kalkulasi SHAP yang cepat dan stabil
    sample_size = min(2500, len(test_idx))
    np.random.seed(42)
    sample_sub_idx = np.random.choice(test_idx, size=sample_size, replace=False)
    X_shap_sample = X_b.loc[sample_sub_idx].copy()
    
    # English feature names for peer-reviewed journal publication
    feature_rename = {
        "kedalaman_gambut_cm": "Peat Dome Thickness (cm)",
        "jarak_kanal_m": "Distance to Primary Canal (m)",
        "is_ex_plg_landscape": "Ex-PLG Landscape Corridor",
        "curah_hujan_7h_mm": "7-Day Cumulative Rainfall (mm)",
        "suhu_maks_c": "Maximum Air Temperature (°C)",
        "kelembapan_relatif_pct": "Relative Air Humidity (%)",
        "kecepatan_angin_kmh": "Maximum Wind Speed (km/h)",
        "dry_spell_days": "Consecutive Dry Spell (days)",
        "fwi_score": "Fire Weather Index (FWI Score)",
        "tipe_lahan": "Peatland Soil Depth Class",
        "tutupan_lahan": "Vegetation Land Cover Class",
        "status_konsesi": "Cadastral Concession Tenure"
    }
    
    X_shap_display = X_shap_sample.rename(columns=feature_rename)
    
    print(f"Menghitung SHAP Values pada {sample_size:,} sampel uji...")
    explainer = shap.TreeExplainer(model_b)
    shap_explanation = explainer(X_shap_sample)
    
    # SHAP beeswarm untuk kelas 1 (Severe Fire)
    # Berikan nama fitur dalam Bahasa Inggris
    shap_explanation.feature_names = [feature_rename.get(f, f) for f in features_b]
    
    fig = plt.figure(figsize=(11.5, 6.2))
    # Ambil nilai SHAP untuk kelas positif (indeks 1)
    shap_class1 = shap_explanation[:, :, 1]
    
    shap.plots.beeswarm(shap_class1, max_display=12, show=False)
    plt.title("Biophysical Drivers of Severe Fire Radiative Power (TreeSHAP Summary)",
              fontsize=12.5, fontweight="bold", pad=16, loc="left", color="#0f172a")
    plt.xlabel("SHAP Value (Impact on Log-Odds for Severe Fire FRP >= 12 MW)", fontsize=9.5, fontweight="bold")
    
    plt.tight_layout()
    fig7_path = os.path.join(output_fig_dir, "07_shap_feature_importance.png")
    plt.savefig(fig7_path, bbox_inches="tight")
    plt.close()
    print(f" -> Gambar 07 (SHAP Summary Beeswarm) tersimpan: {fig7_path}")
    
    # -------------------------------------------------------------------------
    # 6. SIMPAN MODEL BUNDLE & LAPORAN METRIK KE JSON
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("6. MENYIMPAN MODEL BUNDLE & LAPORAN METRIK KOMPARATIF")
    print("=" * 70)
    
    # Rata-rata absolut SHAP per fitur
    mean_abs_shap = np.mean(np.abs(shap_class1.values), axis=0)
    shap_ranking = sorted(
        zip(features_b, [feature_rename[f] for f in features_b], mean_abs_shap),
        key=lambda x: x[2], reverse=True
    )
    
    model_bundle = {
        "model": model_b,  # Model B sebagai model utama
        "model_a_spatial": model_a,
        "features": features_b,
        "features_a": features_a,
        "label_encoders": label_encoders,
        "mean_spatial_auc_model_b": round(float(np.mean(spatial_aucs_b)), 4),
        "mean_spatial_auc_model_a": round(float(np.mean(spatial_aucs_a)), 4),
        "mean_spatial_f1_model_b": round(float(np.mean(spatial_f1s_b)), 4),
        "mean_spatial_f1_model_a": round(float(np.mean(spatial_f1s_a)), 4),
        "test_auc_model_b": round(float(auc_test_b), 4),
        "test_auc_model_a": round(float(auc_test_a), 4)
    }
    
    model_file = os.path.join(output_model_dir, "karhutla_rf_model.joblib")
    joblib.dump(model_bundle, model_file)
    print(f"Model bundle tersimpan ke: {model_file}")
    
    metrics = {
        "model_b_pure_biophysical": {
            "description": "Model Utama Tanpa Koordinat Spasial (Lat/Lon/Kabupaten)",
            "features": features_b,
            "test_roc_auc": round(float(auc_test_b), 4),
            "test_f1_score": round(float(f1_test_b), 4),
            "precision_reguler": round(float(prec_reg_b), 4),
            "recall_ekstrem": round(float(rec_ext_b), 4),
            "spatial_block_cv_mean_roc_auc": round(float(np.mean(spatial_aucs_b)), 4),
            "spatial_block_cv_std_roc_auc": round(float(np.std(spatial_aucs_b)), 4),
            "spatial_block_cv_mean_f1": round(float(np.mean(spatial_f1s_b)), 4),
            "spatial_block_cv_folds_auc": [round(float(s), 4) for s in spatial_aucs_b],
            "spatial_block_cv_folds_f1": [round(float(s), 4) for s in spatial_f1s_b],
            "spatial_block_cv_folds_detail": [
                {
                    "fold": i + 1,
                    "test_regencies": fold_kabs[i],
                    "roc_auc": round(float(spatial_aucs_b[i]), 4),
                    "f1_score": round(float(spatial_f1s_b[i]), 4)
                }
                for i in range(len(spatial_aucs_b))
            ]
        },
        "model_a_spatial_memorization": {
            "description": "Baseline Model Hafalan Spasial (Dengan Lat/Lon/Kabupaten)",
            "features": features_a,
            "test_roc_auc": round(float(auc_test_a), 4),
            "test_f1_score": round(float(f1_test_a), 4),
            "spatial_block_cv_mean_roc_auc": round(float(np.mean(spatial_aucs_a)), 4),
            "spatial_block_cv_std_roc_auc": round(float(np.std(spatial_aucs_a)), 4),
            "spatial_block_cv_mean_f1": round(float(np.mean(spatial_f1s_a)), 4),
            "spatial_block_cv_folds_auc": [round(float(s), 4) for s in spatial_aucs_a],
            "spatial_block_cv_folds_f1": [round(float(s), 4) for s in spatial_f1s_a],
            "spatial_block_cv_folds_detail": [
                {
                    "fold": i + 1,
                    "test_regencies": fold_kabs[i],
                    "roc_auc": round(float(spatial_aucs_a[i]), 4),
                    "f1_score": round(float(spatial_f1s_a[i]), 4)
                }
                for i in range(len(spatial_aucs_a))
            ]
        },
        "shap_importance_ranking": [
            {"feature": f[0], "label": f[1], "mean_abs_shap": round(float(f[2]), 4)}
            for f in shap_ranking
        ],
        "metadata": {
            "total_samples": len(df),
            "test_samples": len(test_idx),
            "target": "Severe Fire Intensity (FRP >= 12.0 MW)",
            "weather_source": "ECMWF ERA5-Land Reanalysis",
            "peat_source": "BBLSDLP Kementan (2019) / SK.130 MenLHK"
        }
    }
    
    metrics_path = os.path.join(output_report_dir, "model_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=4)
    print(f"Laporan metrik tersimpan ke: {metrics_path}")
    
    print("\nTabel Peringkat Pengaruh Fitur (SHAP Values Asli):")
    for r in shap_ranking:
        print(f" • {r[1]}: {r[2]:.4f}")

if __name__ == "__main__":
    train_karhutla_model()
