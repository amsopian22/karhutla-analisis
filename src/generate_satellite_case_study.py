"""
src/generate_satellite_case_study.py

Generates Figure 3: High-Resolution Satellite Forensic Analysis at the Ex-PLG Canal Nexus.
Panels:
  (a) True-Color Optical Satellite Imagery Mosaic (Esri World Imagery) of Dadahup / Block A ex-PLG.
  (b) Spatial Overlay of Primary Canal Vectors, Multi-Ring Buffer Corridors (1km, 3km, 5km), and Active Fires.
  (c) Cross-Sectional Distance Decay Profile & TreeSHAP 3,000-meter Critical Corridor Tipping Point.
"""

import os
import math
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Rectangle, Patch
from matplotlib.lines import Line2D
from shapely.geometry import box
from PIL import Image

def add_north_arrow(ax, x=0.92, y=0.88, arrow_len=0.07):
    ax.annotate('N', xy=(x, y + arrow_len), xytext=(x, y),
                xycoords='axes fraction', textcoords='axes fraction',
                ha='center', va='bottom', fontsize=10, fontweight='bold',
                color='white',
                arrowprops=dict(facecolor='white', edgecolor='#0f172a', width=2.0, headwidth=6, headlength=8, shrink=0))

def add_scale_bar(ax, lon_start, lat_start, length_km=10, unit="km", text_color="white"):
    lat_rad = np.radians(lat_start)
    km_per_deg_lon = 111.32 * np.cos(lat_rad)
    deg_len = length_km / km_per_deg_lon
    half_deg = deg_len / 2.0
    h = 0.015
    
    rect1 = Rectangle((lon_start, lat_start), half_deg, h, facecolor="#0f172a", edgecolor="white", lw=0.8, zorder=10)
    rect2 = Rectangle((lon_start + half_deg, lat_start), half_deg, h, facecolor="white", edgecolor="#0f172a", lw=0.8, zorder=10)
    ax.add_patch(rect1)
    ax.add_patch(rect2)
    
    halo = [pe.withStroke(linewidth=2.5, foreground='#0f172a' if text_color == 'white' else 'white')]
    ax.text(lon_start, lat_start - 0.025, "0", ha='center', va='top', fontsize=7.5, fontweight='bold', color=text_color, path_effects=halo, zorder=11)
    ax.text(lon_start + half_deg, lat_start - 0.025, f"{int(length_km/2)}", ha='center', va='top', fontsize=7.5, fontweight='bold', color=text_color, path_effects=halo, zorder=11)
    ax.text(lon_start + deg_len, lat_start - 0.025, f"{length_km} {unit}", ha='center', va='top', fontsize=7.5, fontweight='bold', color=text_color, path_effects=halo, zorder=11)

def generate_figure(output_path="output/figures/03_analisis_citra_satelit_kanal.png"):
    print(f"Generating Figure 3: Satellite Case Study & Canal Forensic -> {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 1. Load satellite mosaic
    mosaic_path = "data/raw/satellite_dadahup_mosaic.jpg"
    assert os.path.exists(mosaic_path), f"Satellite mosaic {mosaic_path} missing!"
    img = Image.open(mosaic_path)
    
    # Exact geographic bounds of the mosaic from tile calculation
    bounds = [114.2578125, -2.8113711933311296, 114.9609375, -2.2845506602369627]
    extent = [bounds[0], bounds[2], bounds[1], bounds[3]] # [lon_min, lon_max, lat_min, lat_max]
    
    # 2. Load layers
    kanal = gpd.read_file("data/raw/jaringan_kanal_plg_kalteng.geojson")
    df = pd.read_csv("data/processed/karhutla_kalteng_2019_2026.csv", low_memory=False)
    
    # Filter hotspots within mosaic bounds
    mask = ((df['longitude'] >= bounds[0]) & (df['longitude'] <= bounds[2]) & 
            (df['latitude'] >= bounds[1]) & (df['latitude'] <= bounds[3]))
    sub_df = df[mask].copy()
    
    # 3. Create Multi-Ring Buffers in UTM Zone 49S
    focus_box = box(*bounds)
    kanal_focus = kanal.clip(focus_box)
    u1 = kanal_utm.buffer(1000).union_all() if hasattr(kanal_utm, 'union_all') else kanal_utm.buffer(1000).unary_union
    u3 = kanal_utm.buffer(3000).union_all() if hasattr(kanal_utm, 'union_all') else kanal_utm.buffer(3000).unary_union
    u5 = kanal_utm.buffer(5000).union_all() if hasattr(kanal_utm, 'union_all') else kanal_utm.buffer(5000).unary_union
    
    buf_1km = gpd.GeoDataFrame(geometry=[u1], crs='EPSG:32749').to_crs(epsg=4326)
    buf_3km = gpd.GeoDataFrame(geometry=[u3], crs='EPSG:32749').to_crs(epsg=4326)
    buf_5km = gpd.GeoDataFrame(geometry=[u5], crs='EPSG:32749').to_crs(epsg=4326)
    
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
    
    fig = plt.figure(figsize=(16, 10.5), dpi=300)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.4, 1.0], width_ratios=[1.0, 1.0],
                          left=0.06, right=0.96, bottom=0.07, top=0.93, wspace=0.16, hspace=0.25)
    
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[1, :])
    
    halo_white = [pe.withStroke(linewidth=2.5, foreground='white')]
    halo_dark = [pe.withStroke(linewidth=2.5, foreground='#0f172a')]
    
    # -------------------------------------------------------------------------
    # PANEL (a): True-Color Optical Satellite Imagery (Esri World Imagery)
    # -------------------------------------------------------------------------
    ax_a.imshow(img, extent=extent, aspect='auto')
    
    # Trace primary canals with thin subtle cyan line
    kanal_focus.plot(ax=ax_a, color='#38bdf8', linewidth=1.2, alpha=0.85, zorder=3)
    
    # Annotate Dadahup and landscape features
    ax_a.text(114.65, -2.42, "Dadahup Irrigation Scheme\n(Ex-PLG Block A)", fontsize=8.5, fontweight='bold', color='white', ha='center', path_effects=halo_dark, zorder=5)
    ax_a.text(114.35, -2.35, "Kahayan River Corridor", fontsize=8, fontweight='bold', color='#bae6fd', ha='center', path_effects=halo_dark, zorder=5)
    ax_a.text(114.82, -2.70, "Kapuas Murung\nRiver", fontsize=7.5, fontweight='bold', color='#bae6fd', ha='center', path_effects=halo_dark, zorder=5)
    
    ax_a.set_xlim(bounds[0], bounds[2])
    ax_a.set_ylim(bounds[1], bounds[3])
    
    add_north_arrow(ax_a, x=0.92, y=0.88, arrow_len=0.06)
    add_scale_bar(ax_a, lon_start=114.30, lat_start=-2.78, length_km=20, text_color="white")
    
    ax_a.set_title("(a) True-Color Satellite Imagery: Ex-PLG Canal Drainage Nexus (Block A Dadahup)",
                   fontsize=11, fontweight='bold', loc='left', color='#0f172a', pad=8)
    ax_a.set_xlabel("Longitude (°E)", fontsize=8.5, fontweight='bold')
    ax_a.set_ylabel("Latitude (°N/S)", fontsize=8.5, fontweight='bold')
    ax_a.tick_params(labelsize=8)
    ax_a.grid(True, linestyle=':', alpha=0.4, color='white')
    
    # -------------------------------------------------------------------------
    # PANEL (b): Multi-Ring Canal Buffers & Active Fire Clustering
    # -------------------------------------------------------------------------
    # High-contrast dark basemap background
    ax_b.set_facecolor('#0f172a')
    
    # Overlay buffer zones
    buf_5km.plot(ax=ax_b, facecolor='#fef08a', edgecolor='#eab308', linewidth=1.0, alpha=0.25, zorder=2)
    buf_3km.plot(ax=ax_b, facecolor='#fdba74', edgecolor='#f97316', linewidth=1.2, alpha=0.35, zorder=3)
    buf_1km.plot(ax=ax_b, facecolor='#f87171', edgecolor='#ef4444', linewidth=1.4, alpha=0.45, zorder=4)
    
    # Overlay Primary Canal axes
    kanal_focus.plot(ax=ax_b, color='#38bdf8', linewidth=2.2, zorder=5)
    
    # Overlay Hotspots
    regular = sub_df[sub_df['frp_mw'] < 12.0]
    severe = sub_df[sub_df['frp_mw'] >= 12.0]
    
    ax_b.scatter(regular['longitude'], regular['latitude'], s=9.0, color='#facc15', alpha=0.6,
                 label='Regular Fire (FRP < 12 MW)', zorder=6)
    ax_b.scatter(severe['longitude'], severe['latitude'], s=24.0, color='#dc2626', edgecolor='white', linewidth=0.6,
                 label='Extreme Severe Fire (FRP ≥ 12 MW)', zorder=7)
    
    ax_b.set_xlim(bounds[0], bounds[2])
    ax_b.set_ylim(bounds[1], bounds[3])
    
    add_north_arrow(ax_b, x=0.92, y=0.88, arrow_len=0.06)
    add_scale_bar(ax_b, lon_start=114.30, lat_start=-2.78, length_km=20, text_color="white")
    
    legend_elements_b = [
        Line2D([0], [0], color='#38bdf8', lw=2.2, label='Primary Drainage Canal (POROS)'),
        Patch(facecolor='#f87171', edgecolor='#ef4444', alpha=0.5, label='1,000 m Drainage Corridor'),
        Patch(facecolor='#fdba74', edgecolor='#f97316', alpha=0.4, label='3,000 m TreeSHAP Critical Zone'),
        Patch(facecolor='#fef08a', edgecolor='#eab308', alpha=0.3, label='5,000 m Extended Perimeter'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#dc2626', markersize=6, label='Severe Fire (FRP ≥ 12 MW)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#facc15', markersize=4, label='Regular Thermal Anomaly')
    ]
    ax_b.legend(handles=legend_elements_b, loc='lower right', fontsize=7.5, frameon=True, framealpha=0.92, facecolor='#1e293b', labelcolor='white')
    
    ax_b.set_title("(b) Spatial Forensics: Canal Vectors & Multi-Ring Buffer Corridors (1km, 3km, 5km)",
                   fontsize=11, fontweight='bold', loc='left', color='#0f172a', pad=8)
    ax_b.set_xlabel("Longitude (°E)", fontsize=8.5, fontweight='bold')
    ax_b.set_ylabel("Latitude (°N/S)", fontsize=8.5, fontweight='bold')
    ax_b.tick_params(labelsize=8)
    ax_b.grid(True, linestyle='--', alpha=0.25, color='#cbd5e1')
    
    # -------------------------------------------------------------------------
    # PANEL (c): Cross-Sectional Distance Decay Profile & TreeSHAP Tipping Point
    # -------------------------------------------------------------------------
    # Analyze all ex-PLG fires (n = 16,645 in Pulang Pisau, Kapuas, Palangka Raya)
    plg_mask = df['kabupaten_kota'].isin(['Pulang Pisau', 'Kapuas', 'Kota Palangka Raya'])
    plg_df = df[plg_mask].copy()
    
    # Distance in km
    dist_km = plg_df['jarak_kanal_m'] / 1000.0
    
    # Binning by 1 km intervals up to 30 km
    bins = np.arange(0, 31, 1.0)
    bin_centers = (bins[:-1] + bins[1:]) / 2.0
    
    # Calculate counts and severe fraction per bin
    counts, _ = np.histogram(dist_km, bins=bins)
    severe_counts, _ = np.histogram(dist_km[plg_df['frp_mw'] >= 12.0], bins=bins)
    severe_rate = np.divide(severe_counts, counts, out=np.zeros_like(severe_counts, dtype=float), where=counts > 0) * 100.0
    
    # Dual-axis plot
    ax_c.set_facecolor('#f8fafc')
    color_bar = '#3b82f6'
    color_line = '#b91c1c'
    
    # Highlight 0 - 3 km Critical Corridor
    ax_c.axvspan(0, 3.0, color='#fee2e2', alpha=0.7, label='Critical 3,000-m Drainage Zone (TreeSHAP Mean |SHAP| = 0.0322)')
    
    # Bar plot for hotspot frequency
    bars = ax_c.bar(bin_centers, counts, width=0.8, color=color_bar, edgecolor='#1e3a8a', alpha=0.75, label='Active Fire Hotspot Frequency (Left Axis)')
    ax_c.set_xlabel("Metric Geodesic Distance to Nearest Primary Canal Vector (km)", fontsize=9.5, fontweight='bold')
    ax_c.set_ylabel("Active Fire Hotspot Count (n = 16,645)", fontsize=9.5, fontweight='bold', color='#1e3a8a')
    ax_c.tick_params(axis='y', labelcolor='#1e3a8a', labelsize=8.5)
    ax_c.tick_params(axis='x', labelsize=8.5)
    ax_c.set_xlim(0, 30)
    ax_c.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Twin axis for severe fire percentage
    ax_c_twin = ax_c.twinx()
    ax_c_twin.plot(bin_centers, severe_rate, color=color_line, lw=2.4, marker='o', markersize=4.5,
                   label='Severe Fire Probability (FRP ≥ 12 MW %, Right Axis)')
    ax_c_twin.set_ylabel("Severe Fire Rate (FRP ≥ 12.0 MW %)", fontsize=9.5, fontweight='bold', color=color_line)
    ax_c_twin.tick_params(axis='y', labelcolor=color_line, labelsize=8.5)
    ax_c_twin.set_ylim(0, 35)
    
    # Annotate Ex-PLG median distance (14,946 m)
    ax_c.axvline(14.946, color='#0f172a', linestyle='--', lw=1.6, label='Landscape Median Distance (14,946 m / 14.9 km)')
    ax_c.annotate("Ex-PLG Median Distance\n14,946 m (14.9 km)",
                  xy=(14.946, 750), xytext=(17.0, 950),
                  arrowprops=dict(facecolor='#0f172a', shrink=0.08, width=1.0, headwidth=5),
                  fontsize=8.5, fontweight='bold', color='#0f172a')
    
    # Annotate 3,000 m Tipping Point
    ax_c.annotate("TreeSHAP Inflection Threshold (3,000 m)\nSharp Risk Acceleration & Desiccation",
                  xy=(3.0, 1000), xytext=(4.2, 1020),
                  arrowprops=dict(facecolor='#b91c1c', shrink=0.08, width=1.2, headwidth=6),
                  fontsize=8.5, fontweight='bold', color='#b91c1c')
    
    # Combine legends
    lines_1, labels_1 = ax_c.get_legend_handles_labels()
    lines_2, labels_2 = ax_c_twin.get_legend_handles_labels()
    ax_c.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right', fontsize=8.2, frameon=True, framealpha=0.95)
    
    ax_c.set_title("(c) Cross-Sectional Distance Decay Profile & TreeSHAP Non-Linear Drainage Tipping Point in Ex-PLG Landscape",
                   fontsize=11, fontweight='bold', loc='left', color='#0f172a', pad=8)
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Successfully generated: {output_path} ({os.path.getsize(output_path):,} bytes)")

if __name__ == "__main__":
    generate_figure()
