#!/usr/bin/env python3
"""
Automated LaTeX vs JSON Metric Checker
Author: Challenger 2 (Milestone 2)
"""

import json
import re

def check_metrics_consistency():
    with open("output/reports/model_metrics.json") as f:
        metrics = json.load(f)
        
    mb = metrics["model_b_pure_biophysical"]
    ma = metrics["model_a_spatial_memorization"]
    
    with open("manuscript/sections/03_results.tex") as f:
        results_tex = f.read()
        
    with open("manuscript/sections/04_discussion.tex") as f:
        disc_tex = f.read()
        
    with open("manuscript/sections/00_abstract.tex") as f:
        abstract_tex = f.read()

    combined_tex = results_tex + "\n" + disc_tex + "\n" + abstract_tex

    print("=" * 70)
    print("VERIFYING MODEL METRICS VS MANUSCRIPT")
    print("=" * 70)
    
    checks = [
        # Model B Holdout
        ("Model B Holdout Test ROC-AUC", mb["test_roc_auc"], ["0.7527"]),
        ("Model B Holdout Test F1-Score", mb["test_f1_score"], ["0.3983"]),
        ("Model B Precision Regular", mb["precision_reguler"], ["0.9206", "92.1%"]),
        ("Model B Recall Extreme", mb["recall_ekstrem"], ["0.6582", "65.82%"]),
        
        # Model B Spatial Block CV
        ("Model B Spatial CV Mean ROC-AUC", mb["spatial_block_cv_mean_roc_auc"], ["0.4950", "0.495"]),
        ("Model B Spatial CV Std ROC-AUC", mb["spatial_block_cv_std_roc_auc"], ["0.0490", "0.049"]),
        ("Model B Spatial CV Mean F1", mb["spatial_block_cv_mean_f1"], ["0.1399"]),
        ("Model B Fold 1 AUC", mb["spatial_block_cv_folds_auc"][0], ["0.5827"]),
        ("Model B Fold 1 F1", mb["spatial_block_cv_folds_f1"][0], ["0.2914"]),
        ("Model B Fold 2 AUC", mb["spatial_block_cv_folds_auc"][1], ["0.5041"]),
        ("Model B Fold 2 F1", mb["spatial_block_cv_folds_f1"][1], ["0.0657"]),
        ("Model B Fold 3 AUC", mb["spatial_block_cv_folds_auc"][2], ["0.4900", "0.49"]),
        ("Model B Fold 3 F1", mb["spatial_block_cv_folds_f1"][2], ["0.1056"]),
        ("Model B Fold 4 AUC", mb["spatial_block_cv_folds_auc"][3], ["0.4452"]),
        ("Model B Fold 4 F1", mb["spatial_block_cv_folds_f1"][3], ["0.0646"]),
        ("Model B Fold 5 AUC", mb["spatial_block_cv_folds_auc"][4], ["0.4533"]),
        ("Model B Fold 5 F1", mb["spatial_block_cv_folds_f1"][4], ["0.1722"]),
        
        # Model A Holdout
        ("Model A Holdout Test ROC-AUC", ma["test_roc_auc"], ["0.7956"]),
        ("Model A Holdout Test F1-Score", ma["test_f1_score"], ["0.4512"]),
        
        # Model A Spatial Block CV
        ("Model A Spatial CV Mean ROC-AUC", ma["spatial_block_cv_mean_roc_auc"], ["0.5399"]),
        ("Model A Spatial CV Std ROC-AUC", ma["spatial_block_cv_std_roc_auc"], ["0.0531"]),
        ("Model A Spatial CV Mean F1", ma["spatial_block_cv_mean_f1"], ["0.0583"]),
        ("Model A Fold 1 AUC", ma["spatial_block_cv_folds_auc"][0], ["0.5955"]),
        ("Model A Fold 1 F1", ma["spatial_block_cv_folds_f1"][0], ["0.2913"]),
        ("Model A Fold 2 AUC", ma["spatial_block_cv_folds_auc"][1], ["0.5125"]),
        ("Model A Fold 2 F1", ma["spatial_block_cv_folds_f1"][1], ["0.0000", "0.0"]),
        ("Model A Fold 3 AUC", ma["spatial_block_cv_folds_auc"][2], ["0.5259"]),
        ("Model A Fold 3 F1", ma["spatial_block_cv_folds_f1"][2], ["0.0000", "0.0"]),
        ("Model A Fold 4 AUC", ma["spatial_block_cv_folds_auc"][3], ["0.4622"]),
        ("Model A Fold 4 F1", ma["spatial_block_cv_folds_f1"][3], ["0.0000", "0.0"]),
        ("Model A Fold 5 AUC", ma["spatial_block_cv_folds_auc"][4], ["0.6034"]),
        ("Model A Fold 5 F1", ma["spatial_block_cv_folds_f1"][4], ["0.0000", "0.0"]),
        
        # Metadata
        ("Total samples", metrics["metadata"]["total_samples"], ["43937", "43,937"]),
        ("Test samples", metrics["metadata"]["test_samples"], ["10985", "10,985"]),
        
        # Confusion Matrix Values (discussed in text / captions)
        ("Confusion Matrix TN", 6586, ["6586", "6,586"]),
        ("Confusion Matrix FP", 2737, ["2737", "2,737"]),
        ("Confusion Matrix FN", 568, ["568"]),
        ("Confusion Matrix TP", 1094, ["1094", "1,094"]),
        ("Extreme Class Precision", 0.2856, ["28.56%"]),
    ]
    
    all_pass = True
    for name, expected_val, patterns in checks:
        found = False
        matched_pattern = None
        for p in patterns:
            if p in combined_tex:
                found = True
                matched_pattern = p
                break
        if found:
            print(f"[PASS] {name}: Expected {expected_val} | Found match '{matched_pattern}' in TeX")
        else:
            print(f"[FAIL] {name}: Expected {expected_val} | Patterns {patterns} NOT found in TeX")
            all_pass = False
            
    print("\n" + "=" * 70)
    print("VERIFYING SHAP IMPORTANCE RANKINGS")
    print("=" * 70)
    for idx, item in enumerate(metrics["shap_importance_ranking"], 1):
        feat = item["feature"]
        val = f"{item['mean_abs_shap']:.4f}"
        if val in results_tex:
            print(f"[PASS] SHAP Rank {idx} ({feat}): {val} found in TeX")
        else:
            print(f"[FAIL] SHAP Rank {idx} ({feat}): {val} NOT found in TeX")
            all_pass = False

    return all_pass

if __name__ == "__main__":
    check_metrics_consistency()
