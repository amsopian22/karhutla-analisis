"""
Membuat Peta Interaktif Sebaran Hotspot Karhutla Kalimantan Tengah menggunakan Folium.
Pembaruan Visual Ramah Pengguna:
1. Menampilkan layer vektor garis jaringan kanal drainase eks-PLG (Biru Tegas).
2. Kode warna bahaya titik api yang komunikatif:
   - Merah Pekat: Bahaya Ekstrem di Gambut (FRP >= 12 MW)
   - Oranye Terang: Kebakaran Gambut Reguler
   - Kuning Keemasan: Kebakaran Tanah Mineral
3. Legenda visual interaktif mengambang (Floating Legend) yang menerangkan arti warna.
4. Multi-basemap CartoDB & Esri Satellite bebas blokir kebijakan OSM.
"""

import os
import json
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap, MarkerCluster

def generate_interactive_map(csv_path="data/processed/karhutla_kalteng_2019_2026.csv",
                             canal_geojson="data/raw/jaringan_kanal_plg_kalteng.geojson",
                             output_html="output/figures/peta_interaktif_karhutla_kalteng.html"):
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset {csv_path} tidak ditemukan.")
        
    print(f"Membaca data untuk visualisasi peta: {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Ambil sampel representatif berbobot energi FRP tertinggi (2.500 titik) untuk fluiditas browser
    high_impact_df = df.sort_values(by="frp_mw", ascending=False).head(2500)
    
    # Koordinat pusat Kalimantan Tengah (Palangka Raya)
    center_lat, center_lon = -1.95, 113.60
    
    # Inisialisasi peta
    m = folium.Map(location=[center_lat, center_lon], zoom_start=8, tiles=None)
    
    # -------------------------------------------------------------------------
    # MULTI-BASEMAP TERPERCAYA
    # -------------------------------------------------------------------------
    # 1. CartoDB Voyager (Default)
    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
        attr="&copy; OpenStreetMap &copy; CARTO",
        name="Peta Jalan Terang (CartoDB Voyager - Default)",
        subdomains="abcd",
        max_zoom=19,
        control=True
    ).add_to(m)

    # 2. Esri World Imagery (Citra Satelit Asli)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Tiles &copy; Esri",
        name="Citra Satelit Asli (Esri Satellite)",
        max_zoom=18,
        control=True
    ).add_to(m)

    # 3. CartoDB Dark Matter (Mode Gelap)
    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        attr="&copy; OpenStreetMap &copy; CARTO",
        name="Mode Gelap Kontras (Dark Matter)",
        subdomains="abcd",
        max_zoom=19,
        control=True
    ).add_to(m)
    
    # -------------------------------------------------------------------------
    # LAYER 1: JARINGAN KANAL EKS-PLG (VEKTOR LINESTRING)
    # -------------------------------------------------------------------------
    if os.path.exists(canal_geojson):
        print("Menambahkan layer vektor garis poros kanal eks-PLG...")
        gdf_canals = gpd.read_file(canal_geojson)
        canal_layer = folium.FeatureGroup(name="💧 Jaringan Poros Kanal Eks-PLG (Blok A, B, C, D)", show=True)
        
        for _, row in gdf_canals.iterrows():
            geom = row.geometry
            if geom.geom_type == 'LineString':
                coords = [(lat, lon) for lon, lat in geom.coords]
                folium.PolyLine(
                    locations=coords,
                    color="#0284c7",
                    weight=3.5,
                    opacity=0.85,
                    tooltip=f"Poros Kanal Drainase Eks-PLG: {row.get('nama_kanal', 'Saluran Primer')}"
                ).add_to(canal_layer)
        canal_layer.add_to(m)

    # -------------------------------------------------------------------------
    # LAYER 2: HEATMAP DENSITAS ENERGI PEMBAKARAN (FRP)
    # -------------------------------------------------------------------------
    heat_data = [[row["latitude"], row["longitude"], float(row["frp_mw"])] for _, row in high_impact_df.iterrows()]
    HeatMap(
        heat_data,
        radius=14,
        blur=16,
        max_zoom=10,
        name="🔥 Heatmap Intensitas Energi Api (FRP)",
        show=False
    ).add_to(m)
    
    # -------------------------------------------------------------------------
    # LAYER 3: TITIK OBSERVASI DENGAN KODE WARNA TINGKAT BAHAYA
    # -------------------------------------------------------------------------
    marker_cluster = MarkerCluster(
        name="📍 Titik Api Berdasarkan Tingkat Bahaya (Top 450)",
        show=True
    ).add_to(m)
    
    for _, row in high_impact_df.head(450).iterrows():
        is_peat = "Gambut" in str(row["tipe_lahan"])
        frp_val = float(row.get("frp_mw", 0.0))
        is_extreme = frp_val >= 12.0
        
        if is_peat and is_extreme:
            point_color = "#b91c1c" # Merah Pekat: Ekstrem Gambut
            badge_title = "AWAS EKSTREM (GAMBUT)"
            header_bg = "#991b1b"
        elif is_peat:
            point_color = "#ea580c" # Oranye: Gambut Reguler
            badge_title = "WASPADA (GAMBUT)"
            header_bg = "#c2410c"
        else:
            point_color = "#eab308" # Kuning: Tanah Mineral
            badge_title = "API MINERAL"
            header_bg = "#0369a1"
            
        kab_name = str(row.get("kabupaten_kota", "-"))
        canal_dist = int(row.get("jarak_kanal_m", 0))
        canal_dist_str = f"{canal_dist:,} m" if canal_dist >= 0 else "Di luar lanskap PLG"
        date_str = str(row.get("acq_date", "-"))[:10]
        time_str = str(row.get("acq_time", "-"))
        lahan_name = str(row.get("tipe_lahan", "-"))
        tutupan_name = str(row.get("tutupan_lahan", "-"))
        status_k = str(row.get("status_konsesi", "-"))
        nama_k = str(row.get("nama_konsesi", "-"))
        no_sk = str(row.get("no_izin_sk", "-")) if pd.notnull(row.get("no_izin_sk")) else "-"

        konsesi_badge_color = "#dc2626" if "Non-Konsesi" in status_k else ("#f59e0b" if "Sawit" in status_k else "#10b981")
        
        popup_html = f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; font-size: 12px; width: 260px; line-height: 1.45; color: #0f172a;">
            <div style="background: {header_bg}; color: white; padding: 7px 10px; border-radius: 6px 6px 0 0; margin: -10px -10px 8px -10px;">
                <div style="font-weight: 700; font-size: 13px;">📍 {kab_name}</div>
                <div style="font-size: 11px; opacity: 0.95;">📅 {date_str} ({time_str} WIB) • {badge_title}</div>
            </div>
            <div style="padding: 2px 2px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="color: #64748b;">Intensitas Radiasi:</span>
                    <span style="font-weight: 700; color: #dc2626;">🔥 {frp_val:.1f} MW</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="color: #64748b;">Tipe Ekosistem:</span>
                    <span style="font-weight: 600; text-align: right; max-width: 150px;">{lahan_name}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="color: #64748b;">Status Izin:</span>
                    <span style="font-weight: 600; color: {konsesi_badge_color}; text-align: right; max-width: 150px;">{status_k}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="color: #64748b;">Nama Entitas:</span>
                    <span style="font-weight: 700; text-align: right; max-width: 150px; color: #1e293b;">{nama_k}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="color: #64748b;">Jarak Kanal PLG:</span>
                    <span style="font-weight: 600;">{canal_dist_str}</span>
                </div>
                {f'<div style="font-size: 10px; color: #64748b; border-top: 1px dashed #cbd5e1; padding-top: 3px; margin-top: 4px;">SK: {no_sk}</div>' if no_sk != "-" else ""}
            </div>
        </div>
        """
        
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=5.5,
            color=point_color,
            fill=True,
            fill_color=point_color,
            fill_opacity=0.88,
            weight=1.5,
            popup=folium.Popup(popup_html, max_width=290)
        ).add_to(marker_cluster)

    # -------------------------------------------------------------------------
    # FLOATING INTERACTIVE LEGEND (LEGENDA MENGAMBANG RAMAH PENGGUNA)
    # -------------------------------------------------------------------------
    legend_html = """
    <div style="
        position: fixed; 
        bottom: 25px; left: 25px; width: 230px; 
        background-color: white; 
        border: 2px solid #cbd5e1; 
        border-radius: 8px; 
        z-index: 9999; 
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 12px; 
        padding: 10px 14px; 
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1);
        line-height: 1.5;
    ">
        <div style="font-weight: 700; font-size: 13px; color: #0f172a; margin-bottom: 6px; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px;">
            LEGENDA TINGKAT BAHAYA
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 4px;">
            <span style="height: 11px; width: 11px; background-color: #b91c1c; border-radius: 50%; display: inline-block; margin-right: 8px;"></span>
            <span style="color: #334155; font-weight: 600;">Bahaya Ekstrem Gambut (FRP ≥12 MW)</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 4px;">
            <span style="height: 11px; width: 11px; background-color: #ea580c; border-radius: 50%; display: inline-block; margin-right: 8px;"></span>
            <span style="color: #334155;">Gambut Reguler (FRP &lt;12 MW)</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 6px;">
            <span style="height: 11px; width: 11px; background-color: #eab308; border-radius: 50%; display: inline-block; margin-right: 8px;"></span>
            <span style="color: #334155;">Kebakaran Tanah Mineral</span>
        </div>
        <div style="display: flex; align-items: center; border-top: 1px solid #f1f5f9; padding-top: 4px;">
            <span style="height: 4px; width: 18px; background-color: #0284c7; display: inline-block; margin-right: 8px; border-radius: 2px;"></span>
            <span style="color: #0369a1; font-weight: 600;">Poros Kanal Eks-PLG</span>
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    folium.LayerControl(collapsed=False).add_to(m)
    
    os.makedirs(os.path.dirname(output_html), exist_ok=True)
    m.save(output_html)
    print(f"[SUKSES] Peta interaktif ramah pengguna berhasil disimpan: {output_html}")

if __name__ == "__main__":
    generate_interactive_map()
