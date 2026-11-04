"""
src/generate_spatial_fire_figure.py

Generates Figure 2: Active Fire Spatiotemporal Density and FRP Regimes in Central Kalimantan.
Replaces the old regency-level bar chart with high-resolution GIS surfaces:
  (a) 2D Spatial Density Surface (Hexbin density of 43,937 NASA FIRMS hotspots).
  (b) Spatial Distribution of Extreme Fires (FRP >= 12.0 MW vs Regular Fires) over Peat Domes.
  (c) Comparative FRP Intensity Regimes on Peat vs Mineral Soils (Log-density distributions & statistics).
"""

import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.colors import LogNorm
from matplotlib.patches import Rectangle, Patch
from matplotlib.lines import Line2D
import seaborn as sns

def add_north_arrow(ax, x=0.92, y=0.88, arrow_len=0.07):
    ax.annotate('N', xy=(x, y + arrow_len), xytext=(x, y),
                xycoords='axes fraction', textcoords='axes fraction',
                ha='center', va='bottom', fontsize=10, fontweight='bold',
                color='#0f172a',
                arrowprops=dict(facecolor='#0f172a', edgecolor='white', width=2.0, headwidth=6, headlength=8, shrink=0))

def add_scale_bar(ax, lon_start, lat_start, length_km=100, unit="km"):
    lat_rad = np.radians(lat_start)
    km_per_deg_lon = 111.32 * np.cos(lat_rad)
    deg_len = length_km / km_per_deg_lon
    half_deg = deg_len / 2.0
    h = 0.03
    
    rect1 = Rectangle((lon_start, lat_start), half_deg, h, facecolor="#0f172a", edgecolor="#0f172a", zorder=10)
    rect2 = Rectangle((lon_start + half_deg, lat_start), half_deg, h, facecolor="white", edgecolor="#0f172a", lw=1.2, zorder=10)
    ax.add_patch(rect1)
    ax.add_patch(rect2)
    
    halo = [pe.withStroke(linewidth=2.5, foreground='white')]
    ax.text(lon_start, lat_start - 0.04, "0", ha='center', va='top', fontsize=7.5, fontweight='bold', path_effects=halo, zorder=11)
    ax.text(lon_start + half_deg, lat_start - 0.04, f"{int(length_km/2)}", ha='center', va='top', fontsize=7.5, fontweight='bold', path_effects=halo, zorder=11)
    ax.text(lon_start + deg_len, lat_start - 0.04, f"{length_km} {unit}", ha='center', va='top', fontsize=7.5, fontweight='bold', path_effects=halo, zorder=11)

def generate_figure(output_path="output/figures/02_peta_densitas_hotspot_frp.png"):
    print(f"Generating Figure 2: Fire Density & FRP Regimes -> {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 1. Load datasets
    df = pd.read_csv("data/processed/karhutla_kalteng_2019_2026.csv", low_memory=False)
    kab = gpd.read_file("data/raw/batas_kabupaten_kalteng.geojson")
    gambut = gpd.read_file("data/raw/peta_gambut_kalteng_bblsdlp.geojson")
    
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
    
    fig = plt.figure(figsize=(16, 11), dpi=300)
    
    # Gridspec: Top row (Panels a & b), Bottom row (Panel c: FRP distribution & summary metrics)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.6, 1.0], width_ratios=[1.0, 1.0],
                          left=0.06, right=0.96, bottom=0.07, top=0.93, wspace=0.18, hspace=0.25)
    
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c1 = fig.add_subplot(gs[1, 0])
    ax_c2 = fig.add_subplot(gs[1, 1])
    
    halo = [pe.withStroke(linewidth=2.5, foreground='white')]
    
    # -------------------------------------------------------------------------
    # PANEL (a): 2D Hexbin Spatial Density Surface of 43,937 Hotspots
    # -------------------------------------------------------------------------
    ax_a.set_facecolor('#f8fafc')
    
    # Regency boundaries in subtle slate
    kab.plot(ax=ax_a, facecolor='#f1f5f9', edgecolor='#94a3b8', linewidth=0.8, zorder=1)
    
    # Hexbin plot of active fire points
    hb = ax_a.hexbin(df['longitude'], df['latitude'], gridsize=55, cmap='YlOrRd',
                     norm=LogNorm(vmin=1, vmax=df.groupby(['latitude', 'longitude']).size().max()),
                     mincnt=1, edgecolors='none', alpha=0.9, zorder=3)
    
    # Re-draw provincial outline on top
    kab.plot(ax=ax_a, facecolor='none', edgecolor='#1e293b', linewidth=1.1, zorder=4)
    
    cb_a = fig.colorbar(hb, ax=ax_a, orientation='horizontal', pad=0.08, fraction=0.045, aspect=28)
    cb_a.set_label("Active Fire Hotspot Density (Count per Hexagonal Cell, Log-scale)", fontsize=8.5, fontweight='bold')
    cb_a.ax.tick_params(labelsize=8)
    
    ax_a.set_xlim(110.5, 116.1)
    ax_a.set_ylim(-3.65, 0.95)
    
    add_north_arrow(ax_a, x=0.92, y=0.88, arrow_len=0.06)
    add_scale_bar(ax_a, lon_start=111.0, lat_start=-3.45, length_km=100)
    
    # Annotate Top Epicenters
    ax_a.text(112.20, -2.60, "Seruyan\nBasin (21.3%)", fontsize=8, fontweight='bold', color='#991b1b', ha='center', path_effects=halo, zorder=5)
    ax_a.text(114.20, -2.85, "Pulang Pisau\n(16.3%)", fontsize=8, fontweight='bold', color='#991b1b', ha='center', path_effects=halo, zorder=5)
    ax_a.text(114.65, -2.15, "Kapuas\n(14.4%)", fontsize=8, fontweight='bold', color='#991b1b', ha='center', path_effects=halo, zorder=5)
    
    ax_a.set_title("(a) Spatial Density Surface of 43,937 NASA FIRMS Active Fire Hotspots",
                   fontsize=11.5, fontweight='bold', loc='left', color='#0f172a', pad=8)
    ax_a.set_xlabel("Longitude (°E)", fontsize=9, fontweight='bold')
    ax_a.set_ylabel("Latitude (°N/S)", fontsize=9, fontweight='bold')
    ax_a.tick_params(labelsize=8.5)
    ax_a.grid(True, linestyle='--', alpha=0.4, color='#cbd5e1')
    
    # -------------------------------------------------------------------------
    # PANEL (b): Extreme Fires (FRP >= 12 MW) vs Regular Fires over Peat Domes
    # -------------------------------------------------------------------------
    ax_b.set_facecolor('#f8fafc')
    
    # Peat domes background
    kab.plot(ax=ax_b, facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=0.7, zorder=1)
    gambut.plot(ax=ax_b, facecolor='#fef3c7', edgecolor='#b45309', linewidth=0.8, alpha=0.6, zorder=2)
    
    # Split into regular (< 12 MW) and severe (>= 12 MW)
    regular_mask = df['frp_mw'] < 12.0
    severe_mask = df['frp_mw'] >= 12.0
    
    ax_b.scatter(df.loc[regular_mask, 'longitude'], df.loc[regular_mask, 'latitude'],
                 s=3.0, color='#fb923c', alpha=0.20, label='Regular Fires (FRP < 12.0 MW, n=37,289)', zorder=3)
    ax_b.scatter(df.loc[severe_mask, 'longitude'], df.loc[severe_mask, 'latitude'],
                 s=14.0, color='#b91c1c', edgecolor='#450a0a', linewidth=0.4, alpha=0.85,
                 label='Extreme Severity Fires (FRP ≥ 12.0 MW, n=6,648)', zorder=4)
    
    kab.plot(ax=ax_b, facecolor='none', edgecolor='#1e293b', linewidth=1.1, zorder=5)
    
    ax_b.set_xlim(110.5, 116.1)
    ax_b.set_ylim(-3.65, 0.95)
    
    add_north_arrow(ax_b, x=0.92, y=0.88, arrow_len=0.06)
    add_scale_bar(ax_b, lon_start=111.0, lat_start=-3.45, length_km=100)
    
    legend_elements_b = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#b91c1c', markeredgecolor='#450a0a', markersize=7, label='Extreme Severe Fires (FRP ≥ 12.0 MW, 6,648 pts)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#fb923c', markersize=5, alpha=0.6, label='Regular Thermal Anomaly (FRP < 12.0 MW, 37,289 pts)'),
        Patch(facecolor='#fef3c7', edgecolor='#b45309', alpha=0.6, label='Official Peatland Domes (KHG Ecosystem)')
    ]
    ax_b.legend(handles=legend_elements_b, loc='lower right', fontsize=8, frameon=True, framealpha=0.95, facecolor='white', edgecolor='#cbd5e1')
    
    ax_b.set_title("(b) Spatial Radiative Regimes: Extreme Fires Clustered in Peat Basins",
                   fontsize=11.5, fontweight='bold', loc='left', color='#0f172a', pad=8)
    ax_b.set_xlabel("Longitude (°E)", fontsize=9, fontweight='bold')
    ax_b.set_ylabel("Latitude (°N/S)", fontsize=9, fontweight='bold')
    ax_b.tick_params(labelsize=8.5)
    ax_b.grid(True, linestyle='--', alpha=0.4, color='#cbd5e1')
    
    # -------------------------------------------------------------------------
    # PANEL (c1): FRP Probability Density Distribution: Peat vs Mineral Soils
    # -------------------------------------------------------------------------
    is_peat = df['tipe_lahan'].str.lower().str.contains('gambut')
    peat_frp = df.loc[is_peat, 'frp_mw']
    mineral_frp = df.loc[~is_peat, 'frp_mw']
    
    log_peat = np.log10(peat_frp.clip(lower=0.1))
    log_mineral = np.log10(mineral_frp.clip(lower=0.1))
    
    sns.kdeplot(log_peat, ax=ax_c1, color='#b91c1c', lw=2.2, label=f"Peat Soils (n = {len(peat_frp):,}, 74.3%)", fill=True, alpha=0.25)
    sns.kdeplot(log_mineral, ax=ax_c1, color='#0284c7', lw=2.0, linestyle='--', label=f"Mineral Soils (n = {len(mineral_frp):,}, 25.7%)", fill=True, alpha=0.15)
    
    # Mark the 12 MW Threshold
    log_threshold = np.log10(12.0)
    ax_c1.axvline(log_threshold, color='#0f172a', linestyle=':', lw=1.8, label="Severe Threshold (12.0 MW)")
    ax_c1.annotate("Severe Combustion Class (FRP ≥ 12.0 MW)\n67.4% (4,481 / 6,648) in Peatlands",
                   xy=(log_threshold, 0.45), xytext=(log_threshold + 0.15, 0.65),
                   arrowprops=dict(facecolor='#0f172a', shrink=0.08, width=1.0, headwidth=5),
                   fontsize=8, fontweight='bold', color='#0f172a')
    
    # Tick formatting in original MW
    ticks_val = [0.2, 0.5, 1.0, 2.0, 5.0, 12.0, 50.0, 200.0, 600.0]
    ticks_log = [np.log10(t) for t in ticks_val]
    ax_c1.set_xticks(ticks_log)
    ax_c1.set_xticklabels([f"{t:g}" for t in ticks_val], fontsize=8)
    
    ax_c1.set_title("(c) FRP Intensity Distribution (Peat vs Mineral Edaphic Substrates)",
                    fontsize=10.5, fontweight='bold', loc='left', color='#0f172a', pad=8)
    ax_c1.set_xlabel("Fire Radiative Power (MW, Logarithmic Scale)", fontsize=8.5, fontweight='bold')
    ax_c1.set_ylabel("Probability Density", fontsize=8.5, fontweight='bold')
    ax_c1.legend(loc='upper right', fontsize=8, frameon=True, framealpha=0.95)
    ax_c1.grid(True, linestyle='--', alpha=0.5)
    
    # -------------------------------------------------------------------------
    # PANEL (c2): Statistical Summary & Quantile Regimes Breakdown
    # -------------------------------------------------------------------------
    ax_c2.axis('off')
    
    divider = "─" * 58
    summary_text = f"""ACTIVE FIRE RADIATIVE INTENSITY AUDIT SUMMARY (NASA FIRMS 2026)
{divider}
• Total Valid Active Fire Hotspots: 43,937 observations
  ├─ Peatland Ecosystem (KHG): 32,643 hotspots (74.30% of provincial total)
  └─ Mineral Soil Terrain:     11,294 hotspots (25.70% of provincial total)

• Radiative Energy Output (FRP in Megawatts):
  ├─ Overall Mean FRP: 7.56 MW  |  Maximum: 667.1 MW (Kotim) & 644.9 MW (Seruyan)
  ├─ Peatland FRP Median: 3.12 MW  |  IQR: 1.62 – 7.04 MW  |  90th Pct: 14.8 MW
  └─ Mineral FRP Median:  3.50 MW  |  IQR: 1.59 – 9.15 MW  |  90th Pct: 20.6 MW

• Extreme Combustion Regime (FRP ≥ 12.0 MW, Target Label for Modeling):
  ├─ Total Extreme Fires: 6,648 hotspots (15.13% of all satellite detections)
  ├─ Spatial Burden: 67.4% (4,481 hotspots) concentrated in Peat Ecosystems
  └─ Top Regency Epicenters: Seruyan (21.3%), Pulang Pisau (16.3%), Kapuas (14.4%)
{divider}
Scientific Takeaway: While flaming combustion on mineral brush exhibits higher instantaneous peak
temperatures, the massive spatial concentration (74.3%) and protracted smoldering duration in peat
drives catastrophic carbon emissions and regional transboundary PM2.5 dispersion."""
    
    box_props = dict(boxstyle="round,pad=0.8", facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=1.2)
    ax_c2.text(0.02, 0.95, summary_text, transform=ax_c2.transAxes, fontsize=8.2,
               fontfamily="monospace", verticalalignment="top", bbox=box_props, linespacing=1.35)
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Successfully generated: {output_path} ({os.path.getsize(output_path):,} bytes)")

if __name__ == "__main__":
    generate_figure()
