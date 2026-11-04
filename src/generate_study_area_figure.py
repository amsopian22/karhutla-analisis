"""
src/generate_study_area_figure.py

Generates Figure 1: Comprehensive Study Area Map & Spatial Block Cross-Validation Partitioning.
Panels:
  (a) Regional Inset: Central Kalimantan within Borneo and Maritime Southeast Asia.
  (b) Provincial Map: 14 Regencies colored by 5-fold Spatial Block CV with 24 KHG Peat Units overlay.
  (c) Focal Zoom: Degraded ex-PLG Landscape showing 13 primary canal vectors, Sebangau NP, and Block zones.

Complies with Q1 academic cartographic standards (300 DPI, metric scale bar, north arrow, graticules).
"""

import os
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Rectangle, FancyArrowPatch, Patch
from matplotlib.lines import Line2D
from shapely.geometry import box

def add_north_arrow(ax, x=0.92, y=0.88, arrow_len=0.08):
    """Draws a clean cartographic north arrow."""
    ax.annotate('N', xy=(x, y + arrow_len), xytext=(x, y),
                xycoords='axes fraction', textcoords='axes fraction',
                ha='center', va='bottom', fontsize=11, fontweight='bold',
                color='#0f172a',
                arrowprops=dict(facecolor='#0f172a', edgecolor='white', width=2.5, headwidth=8, headlength=10, shrink=0))

def add_scale_bar(ax, lon_start, lat_start, length_km=50, unit="km"):
    """
    Draws a metric scale bar on an unprojected geographic axis (EPSG:4326)
    around lat -2.5 to -3.0 deg. (1 deg lon ~ 111.19 * cos(lat) km)
    """
    lat_rad = np.radians(lat_start)
    km_per_deg_lon = 111.32 * np.cos(lat_rad)
    deg_len = length_km / km_per_deg_lon
    
    # Alternating black/white bar
    half_deg = deg_len / 2.0
    h = 0.025
    
    # Left segment (0 - 25 km)
    rect1 = Rectangle((lon_start, lat_start), half_deg, h, facecolor="#0f172a", edgecolor="#0f172a", zorder=10)
    # Right segment (25 - 50 km)
    rect2 = Rectangle((lon_start + half_deg, lat_start), half_deg, h, facecolor="white", edgecolor="#0f172a", lw=1.2, zorder=10)
    ax.add_patch(rect1)
    ax.add_patch(rect2)
    
    # Text labels
    halo = [pe.withStroke(linewidth=2.5, foreground='white')]
    ax.text(lon_start, lat_start - 0.04, "0", ha='center', va='top', fontsize=8, fontweight='bold', path_effects=halo, zorder=11)
    ax.text(lon_start + half_deg, lat_start - 0.04, f"{int(length_km/2)}", ha='center', va='top', fontsize=8, fontweight='bold', path_effects=halo, zorder=11)
    ax.text(lon_start + deg_len, lat_start - 0.04, f"{length_km} {unit}", ha='center', va='top', fontsize=8, fontweight='bold', path_effects=halo, zorder=11)

def generate_figure(output_path="output/figures/01_peta_wilayah_studi_spatial_cv.png"):
    print(f"Generating Figure 1: Study Area & Spatial CV Partition -> {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 1. Load geospatial layers
    kab = gpd.read_file("data/raw/batas_kabupaten_kalteng.geojson")
    gambut = gpd.read_file("data/raw/peta_gambut_kalteng_bblsdlp.geojson")
    kanal = gpd.read_file("data/raw/jaringan_kanal_plg_kalteng.geojson")
    land = gpd.read_file("data/raw/ne_50m_land.geojson")
    
    # GroupKFold Fold Definitions
    fold_map = {
        'Seruyan': 'Fold 1 (Seruyan)',
        'Barito Timur': 'Fold 2 (East & North Flank)',
        'Barito Utara': 'Fold 2 (East & North Flank)',
        'Lamandau': 'Fold 2 (East & North Flank)',
        'Murung Raya': 'Fold 2 (East & North Flank)',
        'Pulang Pisau': 'Fold 2 (East & North Flank)',
        'Barito Selatan': 'Fold 3 (Central & Delta)',
        'Gunung Mas': 'Fold 3 (Central & Delta)',
        'Kapuas': 'Fold 3 (Central & Delta)',
        'Sukamara': 'Fold 3 (Central & Delta)',
        'Katingan': 'Fold 4 (Sebangau Corridor)',
        'Kota Palangka Raya': 'Fold 4 (Sebangau Corridor)',
        'Kotawaringin Barat': 'Fold 5 (West Peat Basin)',
        'Kotawaringin Timur': 'Fold 5 (West Peat Basin)'
    }
    
    fold_colors = {
        'Fold 1 (Seruyan)': '#38bdf8',               # Vivid Sky Blue
        'Fold 2 (East & North Flank)': '#34d399',     # Mint Emerald
        'Fold 3 (Central & Delta)': '#fbbf24',        # Warm Amber
        'Fold 4 (Sebangau Corridor)': '#a78bfa',      # Soft Violet
        'Fold 5 (West Peat Basin)': '#f472b6'         # Rose / Pink
    }
    
    kab['fold_name'] = kab['shapeName'].map(fold_map)
    kab['color'] = kab['fold_name'].map(fold_colors)
    
    # Set up matplotlib figure with 3 panels
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
    
    fig = plt.figure(figsize=(16, 9.5), dpi=300)
    
    # Create gridspec layout:
    # Left column: Panel (a) Regional Inset [top], Panel (c) ex-PLG Zoom [bottom]
    # Right column: Panel (b) Provincial Map (spans full height)
    gs = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.25], height_ratios=[1.0, 1.3],
                          left=0.05, right=0.98, bottom=0.06, top=0.93, wspace=0.18, hspace=0.25)
    
    ax_a = fig.add_subplot(gs[0, 0])
    ax_c = fig.add_subplot(gs[1, 0])
    ax_b = fig.add_subplot(gs[:, 1])
    
    halo = [pe.withStroke(linewidth=2.5, foreground='white')]
    halo_dark = [pe.withStroke(linewidth=2.5, foreground='#0f172a')]
    
    # -------------------------------------------------------------------------
    # PANEL (a): Regional Inset (Borneo & Maritime Southeast Asia)
    # -------------------------------------------------------------------------
    ax_a.set_facecolor('#e0f2fe') # Pale ocean
    sea_box = box(95.0, -11.0, 126.0, 8.5)
    land_clipped = land.clip(sea_box)
    land_clipped.plot(ax=ax_a, facecolor='#f1f5f9', edgecolor='#94a3b8', linewidth=0.6)
    
    # Highlight Central Kalimantan
    kalteng_union = kab.union_all() if hasattr(kab, 'union_all') else kab.unary_union
    kalteng_gdf = gpd.GeoDataFrame(geometry=[kalteng_union], crs="EPSG:4326")
    kalteng_gdf.plot(ax=ax_a, facecolor='#ef4444', edgecolor='#991b1b', linewidth=1.2, zorder=5)
    
    # Bounding Box of Kalteng
    minx, miny, maxx, maxy = kalteng_union.bounds
    rect_box = Rectangle((minx, miny), maxx - minx, maxy - miny,
                         linewidth=1.4, edgecolor='#b91c1c', facecolor='none', linestyle='--', zorder=6)
    ax_a.add_patch(rect_box)
    
    ax_a.set_xlim(96.0, 125.0)
    ax_a.set_ylim(-10.5, 8.0)
    
    # Regional Labels
    ax_a.text(114.5, 1.8, "BORNEO", fontsize=9, fontweight='bold', color='#475569', ha='center', path_effects=halo)
    ax_a.text(102.0, -0.5, "Sumatra", fontsize=8, color='#64748b', ha='center', path_effects=halo)
    ax_a.text(110.0, -7.5, "Java", fontsize=8, color='#64748b', ha='center', path_effects=halo)
    ax_a.text(120.0, -2.0, "Sulawesi", fontsize=8, color='#64748b', ha='center', path_effects=halo)
    ax_a.text(101.5, 4.0, "Peninsular Malaysia", fontsize=7.5, color='#64748b', ha='center', path_effects=halo)
    ax_a.text(113.5, -4.5, "Central Kalimantan\n(Study Area)", fontsize=8, fontweight='bold', color='#b91c1c', ha='center', path_effects=halo)
    
    ax_a.set_title("(a) Regional Setting: Borneo & Southeast Asia", fontsize=11, fontweight='bold', loc='left', color='#0f172a', pad=8)
    ax_a.set_xlabel("Longitude (°E)", fontsize=8.5)
    ax_a.set_ylabel("Latitude (°N/S)", fontsize=8.5)
    ax_a.tick_params(labelsize=8)
    ax_a.grid(True, linestyle=':', alpha=0.5, color='#94a3b8')
    
    # -------------------------------------------------------------------------
    # PANEL (b): Central Kalimantan Province & Spatial Block CV Folds
    # -------------------------------------------------------------------------
    ax_b.set_facecolor('#f8fafc')
    
    # Plot regencies colored by fold
    for fold_name, color in fold_colors.items():
        subset = kab[kab['fold_name'] == fold_name]
        subset.plot(ax=ax_b, facecolor=color, edgecolor='#334155', linewidth=0.9, alpha=0.75, zorder=2)
    
    # Overlay 24 Peat Hydrological Units (KHG)
    gambut.plot(ax=ax_b, facecolor='#78350f', edgecolor='#451a03', linewidth=0.8, alpha=0.35, hatch='///', zorder=3)
    
    # Regency Labels with manual fine-tuned offsets for clarity
    label_offsets = {
        'Sukamara': (111.35, -2.70),
        'Kotawaringin Barat': (111.75, -2.35),
        'Kotawaringin Timur': (112.75, -2.05),
        'Seruyan': (112.20, -1.80),
        'Katingan': (113.25, -1.55),
        'Kota Palangka Raya': (113.85, -1.95),
        'Pulang Pisau': (114.20, -2.95),
        'Kapuas': (114.50, -1.65),
        'Gunung Mas': (113.60, -0.65),
        'Barito Selatan': (115.00, -1.60),
        'Barito Timur': (115.15, -2.05),
        'Barito Utara': (115.10, -0.80),
        'Murung Raya': (114.30, 0.20),
        'Lamandau': (111.30, -1.60)
    }
    
    for _, row in kab.iterrows():
        name_raw = row['shapeName']
        if name_raw in label_offsets:
            lx, ly = label_offsets[name_raw]
        else:
            pt = row.geometry.representative_point()
            lx, ly = pt.x, pt.y
        name_clean = name_raw.replace("Kota ", "")
        ax_b.text(lx, ly, name_clean, fontsize=7.5, fontweight='bold', color='#0f172a',
                  ha='center', va='center', path_effects=halo, zorder=4)
        
    # Extent rectangle for ex-PLG focal study area (Block A, B, C, D)
    plg_box_bounds = (112.75, -3.35, 114.95, -2.15) # lon min, lat min, lon max, lat max
    plg_rect = Rectangle((plg_box_bounds[0], plg_box_bounds[1]),
                         plg_box_bounds[2] - plg_box_bounds[0],
                         plg_box_bounds[3] - plg_box_bounds[1],
                         linewidth=2.0, edgecolor='#dc2626', facecolor='none', linestyle='--', zorder=6)
    ax_b.add_patch(plg_rect)
    ax_b.text(plg_box_bounds[0] + 0.08, plg_box_bounds[3] - 0.12, "Ex-PLG Landscape [Panel (c)]",
              fontsize=8.5, fontweight='bold', color='#dc2626', path_effects=halo, zorder=7)
    
    ax_b.set_xlim(110.5, 116.1)
    ax_b.set_ylim(-3.65, 0.95)
    
    # North Arrow & Scale Bar for Panel (b)
    add_north_arrow(ax_b, x=0.92, y=0.90, arrow_len=0.06)
    add_scale_bar(ax_b, lon_start=111.0, lat_start=-3.45, length_km=100, unit="km")
    
    ax_b.set_title("(b) Central Kalimantan: 5-Fold Spatial Block CV & Peat Hydrological Units (KHG)",
                   fontsize=11.5, fontweight='bold', loc='left', color='#0f172a', pad=8)
    ax_b.set_xlabel("Longitude (°E)", fontsize=9, fontweight='bold')
    ax_b.set_ylabel("Latitude (°N/S)", fontsize=9, fontweight='bold')
    ax_b.tick_params(labelsize=8.5)
    ax_b.grid(True, linestyle='--', alpha=0.4, color='#cbd5e1')
    
    # Legend for Panel (b)
    legend_elements_b = [
        Patch(facecolor=fold_colors['Fold 1 (Seruyan)'], edgecolor='#334155', label='Spatial Fold 1 (Seruyan)'),
        Patch(facecolor=fold_colors['Fold 2 (East & North Flank)'], edgecolor='#334155', label='Spatial Fold 2 (Pulang Pisau, Bartim, etc.)'),
        Patch(facecolor=fold_colors['Fold 3 (Central & Delta)'], edgecolor='#334155', label='Spatial Fold 3 (Kapuas, Barsel, Sukamara, Gumas)'),
        Patch(facecolor=fold_colors['Fold 4 (Sebangau Corridor)'], edgecolor='#334155', label='Spatial Fold 4 (Katingan, Palangka Raya)'),
        Patch(facecolor=fold_colors['Fold 5 (West Peat Basin)'], edgecolor='#334155', label='Spatial Fold 5 (Kobar, Kotim)'),
        Patch(facecolor='#78350f', edgecolor='#451a03', hatch='///', alpha=0.45, label='24 Peat Hydrological Units (KHG BBLSDLP)'),
        Line2D([0], [0], color='#dc2626', lw=2, linestyle='--', label='Ex-PLG Focal Landscape Boundary')
    ]
    ax_b.legend(handles=legend_elements_b, loc='upper left', fontsize=8.2, frameon=True, framealpha=0.95, facecolor='white', edgecolor='#cbd5e1')
    
    # -------------------------------------------------------------------------
    # PANEL (c): Detailed Zoom of the Ex-PLG Landscape & Canal Vectors
    # -------------------------------------------------------------------------
    ax_c.set_facecolor('#f8fafc')
    
    # Clip layers to ex-PLG focal box
    zoom_box = box(plg_box_bounds[0], plg_box_bounds[1], plg_box_bounds[2], plg_box_bounds[3])
    kab_zoom = kab.clip(zoom_box)
    gambut_zoom = gambut.clip(zoom_box)
    kanal_zoom = kanal.clip(zoom_box)
    
    # Plot regency background in zoom
    kab_zoom.plot(ax=ax_c, facecolor='#f1f5f9', edgecolor='#94a3b8', linewidth=1.2, zorder=1)
    
    # Plot Peat Domes in zoom
    gambut_zoom.plot(ax=ax_c, facecolor='#fed7aa', edgecolor='#d97706', linewidth=0.8, alpha=0.55, zorder=2)
    
    # Plot 13 Primary Canal Vectors
    kanal_zoom.plot(ax=ax_c, color='#0284c7', linewidth=2.0, zorder=4)
    
    # Annotate Ex-PLG Blocks and Key Features
    ax_c.text(114.60, -2.48, "BLOCK A\n(Dadahup)", fontsize=8.5, fontweight='bold', color='#0369a1', ha='center', path_effects=halo, zorder=5)
    ax_c.text(114.25, -2.68, "BLOCK B", fontsize=8.5, fontweight='bold', color='#0369a1', ha='center', path_effects=halo, zorder=5)
    ax_c.text(113.92, -2.52, "BLOCK C", fontsize=8.5, fontweight='bold', color='#0369a1', ha='center', path_effects=halo, zorder=5)
    ax_c.text(114.12, -3.05, "BLOCK D", fontsize=8.5, fontweight='bold', color='#0369a1', ha='center', path_effects=halo, zorder=5)
    
    # Sebangau National Park zone
    ax_c.text(113.45, -2.75, "Sebangau\nNational Park\n(Conservation Dome)", fontsize=8, fontweight='bold', color='#15803d', ha='center', path_effects=halo, zorder=5)
    
    # Rivers / Cities
    ax_c.text(113.92, -2.22, "Palangka Raya", fontsize=8, fontweight='bold', color='#0f172a', ha='center', path_effects=halo, zorder=5)
    ax_c.plot([113.92], [-2.21], marker='o', color='#0f172a', markersize=4, zorder=6)
    
    ax_c.set_xlim(plg_box_bounds[0], plg_box_bounds[2])
    ax_c.set_ylim(plg_box_bounds[1], plg_box_bounds[3])
    
    add_north_arrow(ax_c, x=0.92, y=0.86, arrow_len=0.08)
    add_scale_bar(ax_c, lon_start=112.95, lat_start=-3.25, length_km=30, unit="km")
    
    ax_c.set_title("(c) Focal Landscape: Ex-Mega Rice Project (PLG) & 13 Primary Canal Vectors",
                   fontsize=10.5, fontweight='bold', loc='left', color='#0f172a', pad=8)
    ax_c.set_xlabel("Longitude (°E)", fontsize=8.5)
    ax_c.set_ylabel("Latitude (°N/S)", fontsize=8.5)
    ax_c.tick_params(labelsize=8)
    ax_c.grid(True, linestyle='--', alpha=0.4, color='#cbd5e1')
    
    legend_elements_c = [
        Line2D([0], [0], color='#0284c7', lw=2.2, label='13 Primary Drainage Canals (POROS)'),
        Patch(facecolor='#fed7aa', edgecolor='#d97706', alpha=0.6, label='Deep Peat Domes (KHG Ecosystem)'),
        Patch(facecolor='#f1f5f9', edgecolor='#94a3b8', label='Regency Boundary Intersect')
    ]
    ax_c.legend(handles=legend_elements_c, loc='lower right', fontsize=7.8, frameon=True, framealpha=0.95, facecolor='white', edgecolor='#cbd5e1')
    
    # Save figure
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Successfully generated: {output_path} ({os.path.getsize(output_path):,} bytes)")

if __name__ == "__main__":
    generate_figure()
