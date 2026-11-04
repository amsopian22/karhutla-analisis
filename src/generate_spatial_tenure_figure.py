"""
src/generate_spatial_tenure_figure.py

Generates Figure 4: Cadastral Land Tenure Governance & Concession Accountability Audit.
Replaces the old concession bar chart with comprehensive GIS spatial overlays:
  (a) Provincial Tenurial Overlay: 627 Oil Palm (HGU) and 185 Commercial Forestry (PBPH) Concessions vs 43,937 Hotspots (75.4% APL).
  (b) Concession Boundary Corridor Zoom (Seruyan Basin): Illustrating fire clustering directly outside certified concession boundaries (governance void).
  (c) Corporate Accountability Ranking: Top 8 corporate concession entities with highest active fire detections (ESG compliance monitoring).
"""

import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Rectangle, Patch
from matplotlib.lines import Line2D
from shapely.geometry import box

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

def generate_figure(output_path="output/figures/04_peta_tenurial_konsesi_esg.png"):
    print(f"Generating Figure 4: Spatial Tenurial Audit & Concessions -> {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 1. Load layers
    kab = gpd.read_file("data/raw/batas_kabupaten_kalteng.geojson")
    sawit = gpd.read_file("data/raw/konsesi_sawit_kalteng_real.geojson")
    pbph_all = gpd.read_file("data/raw/konsesi_kehutanan_pbph_real.geojson")
    df = pd.read_csv("data/processed/karhutla_kalteng_2019_2026.csv", low_memory=False)
    
    # Clip PBPH to Kalteng box
    kalteng_box = (110.7, -3.6, 115.9, 0.8)
    pbph = pbph_all.cx[kalteng_box[0]:kalteng_box[2], kalteng_box[1]:kalteng_box[3]].copy()
    
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
    
    fig = plt.figure(figsize=(16, 11), dpi=300)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.5, 1.0], width_ratios=[1.1, 0.9],
                          left=0.06, right=0.96, bottom=0.07, top=0.93, wspace=0.25, hspace=0.28)
    
    ax_a = fig.add_subplot(gs[0, :])   # Panel (a) spans full top row
    ax_b = fig.add_subplot(gs[1, 0])   # Panel (b) Zoom corridor
    ax_c = fig.add_subplot(gs[1, 1])   # Panel (c) Corporate ranking
    
    halo = [pe.withStroke(linewidth=2.5, foreground='white')]
    
    # -------------------------------------------------------------------------
    # PANEL (a): Provincial Spatial Tenurial Map & Hotspot Distribution
    # -------------------------------------------------------------------------
    ax_a.set_facecolor('#f8fafc')
    
    # Regency boundaries
    kab.plot(ax=ax_a, facecolor='#f1f5f9', edgecolor='#cbd5e1', linewidth=0.8, zorder=1)
    
    # Corporate Concessions
    pbph.plot(ax=ax_a, facecolor='#06b6d4', edgecolor='#0891b2', linewidth=0.6, alpha=0.45, zorder=2)
    sawit.plot(ax=ax_a, facecolor='#f59e0b', edgecolor='#d97706', linewidth=0.6, alpha=0.50, zorder=3)
    
    # Hotspots colored by tenure status
    apl_pts = df[df['status_konsesi'] == "Non-Konsesi (Area Penggunaan Lain / Komunitas)"]
    sawit_pts = df[df['status_konsesi'] == "Konsesi Perkebunan Sawit (HGU)"]
    pbph_pts = df[df['status_konsesi'] == "Konsesi Kehutanan (IUPHHK-HTI/HA)"]
    
    # Plot non-concession fires in red/crimson
    ax_a.scatter(apl_pts['longitude'], apl_pts['latitude'], s=4.0, color='#dc2626', alpha=0.35, zorder=4)
    # Plot corporate sawit fires in dark amber
    ax_a.scatter(sawit_pts['longitude'], sawit_pts['latitude'], s=5.0, color='#b45309', alpha=0.65, zorder=5)
    # Plot forestry fires in deep cyan
    ax_a.scatter(pbph_pts['longitude'], pbph_pts['latitude'], s=5.0, color='#0e7490', alpha=0.65, zorder=6)
    
    kab.plot(ax=ax_a, facecolor='none', edgecolor='#1e293b', linewidth=1.1, zorder=7)
    
    # Zoom box for Panel (b) (Seruyan / Danau Sembuluh corridor)
    zoom_box_bounds = (112.15, -3.10, 112.75, -2.45)
    zoom_rect = Rectangle((zoom_box_bounds[0], zoom_box_bounds[1]),
                          zoom_box_bounds[2] - zoom_box_bounds[0],
                          zoom_box_bounds[3] - zoom_box_bounds[1],
                          linewidth=1.8, edgecolor='#b91c1c', facecolor='none', linestyle='--', zorder=8)
    ax_a.add_patch(zoom_rect)
    ax_a.text(zoom_box_bounds[0] + 0.05, zoom_box_bounds[3] + 0.05, "Seruyan Concession Interface [Panel (b)]",
              fontsize=8.5, fontweight='bold', color='#b91c1c', path_effects=halo, zorder=9)
    
    ax_a.set_xlim(110.5, 116.1)
    ax_a.set_ylim(-3.65, 0.95)
    
    add_north_arrow(ax_a, x=0.94, y=0.88, arrow_len=0.06)
    add_scale_bar(ax_a, lon_start=111.0, lat_start=-3.45, length_km=100)
    
    legend_elements_a = [
        Patch(facecolor='#f59e0b', edgecolor='#d97706', alpha=0.6, label='627 Oil Palm Concessions (HGU Riil)'),
        Patch(facecolor='#06b6d4', edgecolor='#0891b2', alpha=0.5, label='185 Commercial Forestry Concessions (PBPH)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#dc2626', markersize=6, alpha=0.8,
               label=f'Fires in Non-Concession / APL ({len(apl_pts):,} pts, 75.4%)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#b45309', markersize=6,
               label=f'Fires inside Oil Palm HGU ({len(sawit_pts):,} pts, 16.6%)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#0e7490', markersize=6,
               label=f'Fires inside Forestry PBPH ({len(pbph_pts):,} pts, 8.0%)'),
        Line2D([0], [0], color='#b91c1c', lw=1.8, linestyle='--', label='Concession Boundary Interface Zoom')
    ]
    ax_a.legend(handles=legend_elements_a, loc='upper left', fontsize=8.2, frameon=True, framealpha=0.95, facecolor='white', edgecolor='#cbd5e1')
    
    ax_a.set_title("(a) Cadastral Land Tenure Overlay: 75.4% of Active Fires Ignited on Unallocated Non-Concession Land (APL)",
                   fontsize=11.5, fontweight='bold', loc='left', color='#0f172a', pad=8)
    ax_a.set_xlabel("Longitude (°E)", fontsize=9, fontweight='bold')
    ax_a.set_ylabel("Latitude (°N/S)", fontsize=9, fontweight='bold')
    ax_a.tick_params(labelsize=8.5)
    ax_a.grid(True, linestyle='--', alpha=0.4, color='#cbd5e1')
    
    # -------------------------------------------------------------------------
    # PANEL (b): Detailed Zoom of Seruyan Concession Boundary Corridor
    # -------------------------------------------------------------------------
    ax_b.set_facecolor('#f8fafc')
    
    corridor_geom = box(*zoom_box_bounds)
    sawit_zoom = sawit.clip(corridor_geom)
    pbph_zoom = pbph.clip(corridor_geom)
    kab_zoom = kab.clip(corridor_geom)
    
    mask_b = ((df['longitude'] >= zoom_box_bounds[0]) & (df['longitude'] <= zoom_box_bounds[2]) &
              (df['latitude'] >= zoom_box_bounds[1]) & (df['latitude'] <= zoom_box_bounds[3]))
    df_zoom = df[mask_b]
    
    kab_zoom.plot(ax=ax_b, facecolor='#f1f5f9', edgecolor='#94a3b8', linewidth=1.0, zorder=1)
    pbph_zoom.plot(ax=ax_b, facecolor='#06b6d4', edgecolor='#0891b2', linewidth=1.4, alpha=0.4, zorder=2)
    sawit_zoom.plot(ax=ax_b, facecolor='#f59e0b', edgecolor='#b45309', linewidth=1.4, alpha=0.4, zorder=3)
    
    # Separate hotspots in zoom
    apl_z = df_zoom[df_zoom['status_konsesi'] == "Non-Konsesi (Area Penggunaan Lain / Komunitas)"]
    sawit_z = df_zoom[df_zoom['status_konsesi'] == "Konsesi Perkebunan Sawit (HGU)"]
    pbph_z = df_zoom[df_zoom['status_konsesi'] == "Konsesi Kehutanan (IUPHHK-HTI/HA)"]
    
    ax_b.scatter(apl_z['longitude'], apl_z['latitude'], s=12.0, color='#dc2626', alpha=0.65, label=f'APL / Community Land ({len(apl_z):,})', zorder=4)
    ax_b.scatter(sawit_z['longitude'], sawit_z['latitude'], s=14.0, color='#b45309', edgecolor='white', linewidth=0.5, label=f'Inside Oil Palm HGU ({len(sawit_z):,})', zorder=5)
    ax_b.scatter(pbph_z['longitude'], pbph_z['latitude'], s=14.0, color='#0e7490', edgecolor='white', linewidth=0.5, label=f'Inside Forestry PBPH ({len(pbph_z):,})', zorder=6)
    
    ax_b.set_xlim(zoom_box_bounds[0], zoom_box_bounds[2])
    ax_b.set_ylim(zoom_box_bounds[1], zoom_box_bounds[3])
    
    add_north_arrow(ax_b, x=0.90, y=0.86, arrow_len=0.08)
    
    # Scale bar for 20 km
    lat_rad = np.radians(-2.9)
    km_per_deg_lon = 111.32 * np.cos(lat_rad)
    deg_len = 20.0 / km_per_deg_lon
    rect_sb = Rectangle((112.20, -3.05), deg_len, 0.015, facecolor="#0f172a", edgecolor="white", zorder=10)
    ax_b.add_patch(rect_sb)
    ax_b.text(112.20 + deg_len/2, -3.07, "20 km", ha='center', va='top', fontsize=7.5, fontweight='bold', path_effects=halo, zorder=11)
    
    ax_b.set_title("(b) Concession Boundary Interface: Fire Clustering\nOutside Certified Land (Seruyan Basin)",
                   fontsize=10, fontweight='bold', loc='left', color='#0f172a', pad=8)
    ax_b.set_xlabel("Longitude (°E)", fontsize=8.5, fontweight='bold')
    ax_b.set_ylabel("Latitude (°N/S)", fontsize=8.5, fontweight='bold')
    ax_b.tick_params(labelsize=8)
    ax_b.grid(True, linestyle='--', alpha=0.4, color='#cbd5e1')
    ax_b.legend(loc='upper left', fontsize=7.8, frameon=True, framealpha=0.92, facecolor='white', edgecolor='#cbd5e1')
    
    # -------------------------------------------------------------------------
    # PANEL (c): Top 8 Concession Entities with Highest Active Fire Hotspots
    # -------------------------------------------------------------------------
    corp_df = df[df["nama_konsesi"] != "Non-Konsesi (APL / Lahan Terbuka)"]
    top_corp = corp_df["nama_konsesi"].value_counts().head(8).sort_values(ascending=True)
    
    # Color bars by license type
    # Check if entity is PBPH or Sawit
    bar_colors = []
    for comp in top_corp.index:
        sample_status = df.loc[df['nama_konsesi'] == comp, 'status_konsesi'].iloc[0]
        if "Kehutanan" in sample_status or "PBPH" in sample_status or "RIMBA" in comp:
            bar_colors.append('#0891b2') # Teal for PBPH
        else:
            bar_colors.append('#f59e0b') # Amber for Sawit HGU
            
    bars = ax_c.barh(top_corp.index, top_corp.values, color=bar_colors, edgecolor='#1e293b', linewidth=0.7, alpha=0.9)
    ax_c.set_title("(c) Top 8 Concession Entities with Thermal Detections (ESG Compliance)",
                   fontsize=10.5, fontweight='bold', loc='left', color='#0f172a', pad=8)
    ax_c.set_xlabel("Hotspots within Demarcated Boundary", fontsize=8.5, fontweight='bold')
    ax_c.tick_params(labelsize=8)
    ax_c.grid(axis='x', linestyle='--', alpha=0.5)
    
    for bar in bars:
        width = bar.get_width()
        pct = (width / len(df)) * 100
        ax_c.text(width + 12, bar.get_y() + bar.get_height()/2, f"{width:,} ({pct:.1f}%)",
                  va='center', fontsize=8, fontweight='bold', color='#0f172a')
        
    legend_elements_c = [
        Patch(facecolor='#f59e0b', edgecolor='#1e293b', label='Oil Palm Concession (HGU)'),
        Patch(facecolor='#0891b2', edgecolor='#1e293b', label='Forestry Concession (PBPH / Restoration)')
    ]
    ax_c.legend(handles=legend_elements_c, loc='lower right', fontsize=8, frameon=True, framealpha=0.95)
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Successfully generated: {output_path} ({os.path.getsize(output_path):,} bytes)")

if __name__ == "__main__":
    generate_figure()
