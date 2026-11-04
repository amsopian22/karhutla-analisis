"""
src/generate_temporal_figure.py

Generates Figure 5: Consolidated Temporal Dynamics:
  (a) Decadal Burned Area Trajectory (2018-2026) from Official SiPongi KLHK Records and ENSO Cycles.
  (b) Diurnal Active Fire Dynamics & Sensor Detections during the Acute October 2026 Peatland Crisis.

Academic Q1 standard (300 DPI, clean typography, coordinated color palette).
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

def generate_figure(output_path="output/figures/05_tren_temporal_dan_harian.png"):
    print(f"Generating Figure 5: Consolidated Temporal Dynamics -> {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 1. Load data
    sipongi_path = "data/raw/sipongi_luas_karhutla_kalteng_2018_2026.csv"
    sdf = pd.read_csv(sipongi_path)
    
    df = pd.read_csv("data/processed/karhutla_kalteng_2019_2026.csv", low_memory=False)
    df["acq_date"] = pd.to_datetime(df["acq_date"])
    total_records = len(df)
    
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6.2), dpi=300)
    
    # -------------------------------------------------------------------------
    # PANEL (a): Decadal Burned Area (2018-2026) & El Niño Drought Anomalies
    # -------------------------------------------------------------------------
    bar_colors = []
    for yr in sdf["tahun"]:
        if yr in [2019, 2023]:
            bar_colors.append("#dc2626") # Vivid Red for El Nino Disasters
        elif yr in [2020, 2021, 2022]:
            bar_colors.append("#94a3b8") # Neutral Slate Gray for Wet La Nina Years
        else:
            bar_colors.append("#f97316") # Orange for Moderate / Transition Years
            
    bars = ax1.bar(sdf["tahun"], sdf["luas_terbakar_ha"], color=bar_colors, width=0.55,
                   edgecolor="#1e293b", linewidth=0.8, alpha=0.92)
    
    ax1.set_title("(a) Decadal Trajectory: Climate Drought Cycles Drive >85% of Burned Area (2018–2026)\n"
                  "Official SiPongi Ministry of Environment and Forestry (KLHK) Records",
                  fontsize=10, fontweight="bold", pad=10, loc="left", color="#0f172a", linespacing=1.3)
    ax1.set_xlabel("Observation Year", fontsize=9, fontweight="bold", labelpad=6)
    ax1.set_ylabel("Burned Area Extent (Hectares)", fontsize=9, fontweight="bold", labelpad=6)
    ax1.set_xticks(sdf["tahun"])
    ax1.tick_params(labelsize=8.5)
    ax1.grid(axis="y", linestyle="--", alpha=0.5)
    ax1.set_ylim(0, 380000)
    
    for bar in bars:
        height = bar.get_height()
        yr = sdf.loc[bars.index(bar), "tahun"]
        if yr not in [2019, 2023]:
            ax1.annotate(f"{height:,.0f} ha",
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 4), textcoords="offset points",
                         ha="center", va="bottom", fontsize=7.5, fontweight="bold", color="#1e293b")
        
    # Annotate El Nino events outside bar
    ax1.annotate("Strong El Niño 2019\n(317,749 ha Burned)", xy=(2019, 317749), xytext=(2017.9, 342000),
                 arrowprops=dict(facecolor='#991b1b', shrink=0.08, width=1.0, headwidth=5),
                 fontweight='bold', color='#991b1b', fontsize=8)
    ax1.annotate("Moderate El Niño 2023\n(165,896 ha Burned)", xy=(2023, 165896), xytext=(2021.1, 230000),
                 arrowprops=dict(facecolor='#991b1b', shrink=0.08, width=1.0, headwidth=5),
                 fontweight='bold', color='#991b1b', fontsize=8)
    
    summary_box = dict(boxstyle="round,pad=0.5", facecolor="#f8fafc", edgecolor="#cbd5e1", alpha=0.95)
    ax1.text(0.64, 0.52, "[DECIDED CLIMATE PATTERNS]\n• El Niño triggers catastrophic pulses.\n• 2020–2022 wet La Niña suppression.\n• Over 85% area burned in 2019 & 2023.",
             transform=ax1.transAxes, fontsize=8, verticalalignment="top", bbox=summary_box, color="#1e293b", linespacing=1.35)
    
    # -------------------------------------------------------------------------
    # PANEL (b): Diurnal Satellite Dynamics during Acute October 2026 Crisis
    # -------------------------------------------------------------------------
    df_daily = df.copy()
    df_daily["tgl_label"] = df_daily["acq_date"].dt.strftime("%d %b")
    daily_sensor = df_daily.groupby(["tgl_label", "satellite"]).size().unstack(fill_value=0)
    
    # Sort chronologically
    unique_dates = df_daily.sort_values("acq_date")["tgl_label"].unique()
    daily_sensor = daily_sensor.reindex(unique_dates)
    
    daily_sensor.plot(kind="bar", stacked=True, ax=ax2, color=["#dc2626", "#ea580c", "#f59e0b"],
                      edgecolor="#1e293b", linewidth=0.7, alpha=0.9)
    
    ax2.set_title(f"(b) Diurnal Pulse: Extreme Fire Concentration in Early October 2026\n"
                  f"Total: {total_records:,} Hotspots (VIIRS SNPP/NOAA-20 and MODIS Aqua) across Central Kalimantan",
                  fontsize=10, fontweight="bold", pad=10, loc="left", color="#0f172a", linespacing=1.3)
    ax2.set_xlabel("Observation Date (October 2026)", fontsize=9, fontweight="bold", labelpad=6)
    ax2.set_ylabel("Number of Active Fire Hotspots", fontsize=9, fontweight="bold", labelpad=6)
    ax2.legend(title="Satellite Sensor", loc="upper right", fontsize=8, title_fontsize=8.5, frameon=True)
    ax2.tick_params(axis="x", rotation=0, labelsize=8.5)
    ax2.tick_params(axis="y", labelsize=8.5)
    ax2.grid(axis="y", linestyle="--", alpha=0.5)
    ax2.set_ylim(0, 9500)
    
    # Annotation for convective rain transition
    ax2.annotate("Onset of Convective Rainfall\n(Abrupt Hotspot Suppression)", xy=(4, 2500), xytext=(4.2, 5600),
                 arrowprops=dict(facecolor='#0369a1', shrink=0.08, width=1.0, headwidth=5),
                 fontweight='bold', color='#0369a1', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Successfully generated: {output_path} ({os.path.getsize(output_path):,} bytes)")

if __name__ == "__main__":
    generate_figure()
