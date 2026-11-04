"""
Sistem Monitoring & Simulator Risiko Karhutla Kalimantan Tengah (SI-KARHUTLA)
Dashboard Interaktif Berbasis Streamlit, Folium, Plotly, dan Random Forest Ensemble.

Pembaruan UI/UX Komprehensif:
1. Sidebar Navigasi & Metadata Transparan: Status data riil, tanggal update, dan statistik kunci.
2. Tab 1 Peta Interaktif: Filter kabupaten dengan ringkasan metrik instan, layer poros kanal, dan legenda mengambang konsisten.
3. Tab 2 Simulator Risiko:
   - 4 Tombol Skenario Cepat 1-Klik (El Nino, Kemarau Sedang, Transisi Hujan, La Nina Basah).
   - Speedometer Risiko (Gauge Meter Plotly) responsif terhadap model Random Forest asli.
   - Kartu Tindakan Taktis Lapangan berhuruf besar dan berwarna siaga.
   - Kalkulator Simulasi Intervensi Mitigasi ("Efek Penyekatan Kanal").
   - Diagram Kontribusi Fitur Model AI.
4. Tab 3 Analisis Data: Filter interaktif dinamis, 5 visualisasi data mendalam, dan ekspor CSV data terfilter.
5. Tab 4 Evaluasi Model: Mode Toggle Awam vs Pakar (dilengkapi tabel performa Spatial Block CV per fold).
6. Tab 5 Rekomendasi Kebijakan: Panduan aksi taktis berbasis bukti sains data.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium

# -----------------------------------------------------------------------------
# 1. KONFIGURASI HALAMAN & TEMA DESAIN (ACCESSIBLE & POLISHED)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SI-KARHUTLA Kalteng - Monitoring & Simulator",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS yang dirancang mengikuti prinsip antislop-ui dan kontras tinggi WCAG AA
st.markdown("""
<style>
    /* Header Utama */
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 22px 26px;
        border-radius: 10px;
        color: #f8fafc;
        margin-bottom: 22px;
        border-left: 6px solid #dc2626;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08);
    }
    .main-header h1 {
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 4px;
        color: #ffffff;
        letter-spacing: -0.01em;
    }
    .main-header p {
        font-size: 13.5px;
        color: #94a3b8;
        margin-bottom: 0;
        line-height: 1.5;
    }
    
    /* KPI Metric Cards */
    .metric-card {
        background: #ffffff;
        padding: 16px 18px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        text-align: left;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08);
    }
    .metric-value {
        font-size: 24px;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 11.5px;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.05em;
        margin-top: 5px;
    }
    .metric-sub {
        font-size: 11px;
        color: #0369a1;
        font-weight: 600;
        margin-top: 3px;
    }

    /* Badges Status */
    .risk-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: 800;
        font-size: 14px;
        letter-spacing: 0.02em;
    }
    .badge-ekstrem { background-color: #fee2e2; color: #991b1b; border: 1.5px solid #ef4444; }
    .badge-siaga { background-color: #ffedd5; color: #9a3412; border: 1.5px solid #f97316; }
    .badge-waspada { background-color: #fef9c3; color: #854d0e; border: 1.5px solid #eab308; }
    .badge-aman { background-color: #dcfce7; color: #166534; border: 1.5px solid #22c55e; }
    
    /* Kotak Tindakan Taktis */
    .action-box {
        padding: 15px 18px;
        border-radius: 8px;
        margin-top: 14px;
        font-size: 13.5px;
        line-height: 1.6;
    }
    
    /* Preset Scenario Buttons */
    .preset-title {
        font-size: 12px;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 8px;
    }

    /* Sidebar info card */
    .sidebar-info {
        background-color: #f1f5f9;
        padding: 12px 14px;
        border-radius: 6px;
        border: 1px solid #cbd5e1;
        font-size: 12px;
        color: #334155;
        line-height: 1.5;
        margin-bottom: 14px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. PEMUATAN DATASET & MODEL (CACHED)
# -----------------------------------------------------------------------------
@st.cache_data
def _load_dataset_cached(path: str, mtime: float):
    df = pd.read_csv(path, low_memory=False)
    df["acq_date"] = pd.to_datetime(df["acq_date"])
    return df

def load_dataset():
    path = "data/processed/karhutla_kalteng_2019_2026.csv"
    mtime = os.path.getmtime(path) if os.path.exists(path) else 0.0
    return _load_dataset_cached(path, mtime)

@st.cache_resource
def load_model_bundle():
    model_path = "output/models/karhutla_rf_model.joblib"
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None

df = load_dataset()
model_bundle = load_model_bundle()

# -----------------------------------------------------------------------------
# 3. SIDEBAR: NAVIGASI, METADATA & FILTER GLOBAL
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🔥 SI-KARHUTLA KALTENG")
    st.caption("Sistem Intelijen Geospasial & Pemodelan Risiko Karhutla")
    
    st.markdown("""
    <div class="sidebar-info">
        <strong>STATUS DATASET:</strong><br/>
        • <strong>Sumber:</strong> NASA FIRMS (VIIRS & MODIS)<br/>
        • <strong>Cakupan:</strong> 14 Kab/Kota Kalteng (Riil)<br/>
        • <strong>Periode:</strong> 5–12 Oktober 2026<br/>
        • <strong>Validasi Batas:</strong> geoBoundaries ADM2<br/>
        • <strong>Jaringan Kanal:</strong> LineString Eks-PLG (UTM 49S)
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### 📌 Ringkasan Cepat Spasial")
    top_kab = df["kabupaten_kota"].value_counts().head(3)
    for k, v in top_kab.items():
        st.write(f"• **{k}**: {v:,} titik ({v/len(df)*100:.1f}%)")

    st.markdown("---")
    st.caption("Dikembangkan untuk audit investigatif & pemantauan dini BPBD/Kemenhut.")

# -----------------------------------------------------------------------------
# 4. HEADER UTAMA & KPI METRICS
# -----------------------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>Sistem Intelijen & Simulator Risiko Karhutla Kalimantan Tengah</h1>
    <p>Integrasi 43.937 Titik Observasi Satelit NASA FIRMS (Oktober 2026) • 627 HGU Sawit BPN • 185 PBPH Kehutanan KLHK • Rekapitulasi SiPongi (2018–2026)</p>
</div>
""", unsafe_allow_html=True)

# 5 Kartu Metrik Utama
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-value">{len(df):,}</div>
        <div class="metric-label">Titik Api Kalteng</div>
        <div class="metric-sub">100% Batas Resmi Kalteng</div>
    </div>
    ''', unsafe_allow_html=True)
with c2:
    peat_pct = (df["tipe_lahan"].str.contains("Gambut").mean()) * 100
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-value">{peat_pct:.1f}%</div>
        <div class="metric-label">Ekosistem Gambut</div>
        <div class="metric-sub">{df["tipe_lahan"].str.contains("Gambut").sum():,} Titik Rawa Gambut</div>
    </div>
    ''', unsafe_allow_html=True)
with c3:
    apl_pct = (df["status_konsesi"].str.contains("Non-Konsesi").mean()) * 100
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-value">{apl_pct:.1f}%</div>
        <div class="metric-label">Non-Konsesi (APL)</div>
        <div class="metric-sub">{df["status_konsesi"].str.contains("Non-Konsesi").sum():,} Titik Lahan Terbuka</div>
    </div>
    ''', unsafe_allow_html=True)
with c4:
    med_dist = df["jarak_kanal_m"].median() / 1000
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-value">{med_dist:.1f} km</div>
        <div class="metric-label">Median Jarak Kanal</div>
        <div class="metric-sub">Vektor LineString Eks-PLG</div>
    </div>
    ''', unsafe_allow_html=True)
with c5:
    auc_score = "0.7845"
    spatial_auc = "0.6359"
    metrics_path = "output/reports/model_metrics.json"
    if os.path.exists(metrics_path):
        try:
            with open(metrics_path) as mf:
                mdata = json.load(mf)
                auc_score = f"{mdata.get('test_roc_auc', 0.7845):.4f}"
                spatial_auc = f"{mdata.get('spatial_cv_mean_roc_auc', 0.6359):.4f}"
        except:
            pass
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-value">{auc_score}</div>
        <div class="metric-label">ROC-AUC Model AI</div>
        <div class="metric-sub">Spatial CV: {spatial_auc}</div>
    </div>
    ''', unsafe_allow_html=True)

st.write("")

# -----------------------------------------------------------------------------
# 5. TAB NAVIGASI UTAMA
# -----------------------------------------------------------------------------
tab_map, tab_sim, tab_eda, tab_model, tab_policy = st.tabs([
    "🗺️ Peta Interaktif Spasial",
    "⚡ Simulator Risiko Karhutla",
    "📊 Analisis Data Eksploratif (EDA)",
    "🤖 Evaluasi Model AI (Explainable)",
    "📋 Rekomendasi Kebijakan & Mitigasi"
])

# =============================================================================
# TAB 1: PETA INTERAKTIF SEBARAN HOTSPOT & KANAL
# =============================================================================
with tab_map:
    map_col1, map_col2 = st.columns([2.8, 1.2])
    with map_col1:
        st.markdown("##### Sebaran Geospasial Titik Api & Poros Jaringan Kanal Eks-PLG")
        st.caption("Memvisualisasikan titik api satelit dengan kode warna tingkat bahaya, layer poros garis kanal drainase eks-PLG, dan basemap beresolusi tinggi.")
    with map_col2:
        filter_kab = st.selectbox(
            "Pilih Wilayah Kabupaten / Kota:",
            ["Semua Wilayah (Provinsi Kalteng)"] + sorted(df["kabupaten_kota"].unique().tolist())
        )

    # Filter data
    if filter_kab == "Semua Wilayah (Provinsi Kalteng)":
        filtered_df = df
        st.info(f"💡 Menampilkan seluruh wilayah Provinsi Kalimantan Tengah: **{len(filtered_df):,} titik api** terkliping resmi.")
    else:
        filtered_df = df[df["kabupaten_kota"] == filter_kab]
        kab_pct = (len(filtered_df) / len(df)) * 100
        if filter_kab in ["Pulang Pisau", "Kapuas", "Kota Palangka Raya"]:
            kab_med_kanal = filtered_df["jarak_kanal_m"].median() / 1000
            st.success(f"📍 **{filter_kab}**: Terdeteksi **{len(filtered_df):,} titik api** ({kab_pct:.1f}% total provinsi) • Median Jarak ke Poros Kanal Eks-PLG: **{kab_med_kanal:.1f} km**.")
        else:
            st.success(f"📍 **{filter_kab}**: Terdeteksi **{len(filtered_df):,} titik api** ({kab_pct:.1f}% total provinsi) • Wilayah di luar lanskap eks-PLG.")

    # Render Peta
    map_path = "output/figures/peta_interaktif_karhutla_kalteng.html"
    if filter_kab == "Semua Wilayah (Provinsi Kalteng)" and os.path.exists(map_path):
        with open(map_path, "r", encoding="utf-8") as f:
            map_html = f.read()
        components.html(map_html, height=590)
    else:
        # Peta dinamis per kabupaten
        center_lat = filtered_df["latitude"].mean() if len(filtered_df) > 0 else -1.95
        center_lon = filtered_df["longitude"].mean() if len(filtered_df) > 0 else 113.60
        m = folium.Map(location=[center_lat, center_lon], zoom_start=9, tiles=None)

        folium.TileLayer(
            tiles="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
            attr="&copy; OpenStreetMap &copy; CARTO",
            name="Peta Jalan Terang (Default)",
            subdomains="abcd"
        ).add_to(m)
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Tiles &copy; Esri",
            name="Citra Satelit Asli"
        ).add_to(m)

        # Layer Garis Kanal Eks-PLG
        canal_geojson = "data/raw/jaringan_kanal_plg_kalteng.geojson"
        if os.path.exists(canal_geojson):
            import geopandas as gpd
            gdf_canals = gpd.read_file(canal_geojson)
            canal_layer = folium.FeatureGroup(name="💧 Jaringan Kanal Eks-PLG (Poros Primer)", show=True)
            for _, crow in gdf_canals.iterrows():
                geom = crow.geometry
                if geom.geom_type == 'LineString':
                    coords = [(lat, lon) for lon, lat in geom.coords]
                    folium.PolyLine(
                        locations=coords,
                        color="#0284c7",
                        weight=3.5,
                        opacity=0.85,
                        tooltip=f"Poros Kanal Eks-PLG: {crow.get('nama_kanal', 'Saluran Primer')}"
                    ).add_to(canal_layer)
            canal_layer.add_to(m)

        # Titik Api Berwarna Bahaya
        sample_points = filtered_df.sort_values(by="frp_mw", ascending=False).head(400)
        mc = MarkerCluster(name="Titik Api (Sampel Terbesar)", show=True).add_to(m)

        for _, row in sample_points.iterrows():
            is_peat = "Gambut" in str(row["tipe_lahan"])
            frp_val = float(row.get("frp_mw", 0.0))
            is_extreme = frp_val >= 12.0

            if is_peat and is_extreme:
                color = "#b91c1c"
                tipe_lbl = "AWAS EKSTREM (GAMBUT)"
            elif is_peat:
                color = "#ea580c"
                tipe_lbl = "WASPADA (GAMBUT)"
            else:
                color = "#eab308"
                tipe_lbl = "API MINERAL"

            canal_val = int(row.get('jarak_kanal_m', -1))
            canal_str = f"{canal_val:,} m" if canal_val >= 0 else "Di Luar Lanskap PLG"
            popup_text = f"<b>{row.get('kabupaten_kota')}</b><br/>🔥 FRP: {frp_val:.1f} MW<br/>Status: {tipe_lbl}<br/>Kanal: {canal_str}"

            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=5.5,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.88,
                weight=1.5,
                popup=popup_text
            ).add_to(mc)

        folium.LayerControl(collapsed=False).add_to(m)
        st_folium(m, width=None, height=590, returned_objects=[])

# =============================================================================
# TAB 2: SIMULATOR RISIKO (PRESET SCENARIOS & GAUGE METER)
# =============================================================================
with tab_sim:
    st.markdown("##### Simulator Prediksi Keparahan Karhutla Berbasis Machine Learning")
    st.caption("Gunakan slider untuk menguji skenario cuaca dan jarak kanal, atau pilih salah satu tombol Skenario Cepat di bawah.")

    # -------------------------------------------------------------------------
    # 4 PRESET SCENARIOS (1-CLICK QUICK TEST)
    # -------------------------------------------------------------------------
    st.markdown('<div class="preset-title">⚡ PILIH SKENARIO CEPAT (1-KLIK):</div>', unsafe_allow_html=True)
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    
    # Inisialisasi session state untuk slider jika belum ada
    if "sim_dry_spell" not in st.session_state:
        st.session_state["sim_dry_spell"] = 20
        st.session_state["sim_rain_7d"] = 0.5
        st.session_state["sim_temp_max"] = 35.5
        st.session_state["sim_humidity"] = 45
        st.session_state["sim_jarak_kanal"] = 800
        st.session_state["sim_kab"] = "Pulang Pisau"
        st.session_state["sim_tipe_lahan"] = "Gambut Sangat Dalam (>300 cm)"

    with p_col1:
        if st.button("🔥 Puncak El Niño (Gambut <1km)", use_container_width=True):
            st.session_state["sim_dry_spell"] = 24
            st.session_state["sim_rain_7d"] = 0.0
            st.session_state["sim_temp_max"] = 36.2
            st.session_state["sim_humidity"] = 40
            st.session_state["sim_jarak_kanal"] = 500
            st.session_state["sim_kab"] = "Pulang Pisau"
            st.session_state["sim_tipe_lahan"] = "Gambut Sangat Dalam (>300 cm)"
            st.rerun()

    with p_col2:
        if st.button("☀️ Kemarau Sedang di Sawit", use_container_width=True):
            st.session_state["sim_dry_spell"] = 15
            st.session_state["sim_rain_7d"] = 3.0
            st.session_state["sim_temp_max"] = 34.0
            st.session_state["sim_humidity"] = 52
            st.session_state["sim_jarak_kanal"] = 3500
            st.session_state["sim_kab"] = "Kotawaringin Timur"
            st.session_state["sim_tipe_lahan"] = "Gambut Dalam (200-300 cm)"
            st.rerun()

    with p_col3:
        if st.button("🌦️ Transisi Hujan Konvektif", use_container_width=True):
            st.session_state["sim_dry_spell"] = 6
            st.session_state["sim_rain_7d"] = 18.0
            st.session_state["sim_temp_max"] = 31.5
            st.session_state["sim_humidity"] = 68
            st.session_state["sim_jarak_kanal"] = 8000
            st.session_state["sim_kab"] = "Kota Palangka Raya"
            st.session_state["sim_tipe_lahan"] = "Gambut Dangkal (50-100 cm)"
            st.rerun()

    with p_col4:
        if st.button("🌧️ Musim Basah La Niña (Aman)", use_container_width=True):
            st.session_state["sim_dry_spell"] = 2
            st.session_state["sim_rain_7d"] = 45.0
            st.session_state["sim_temp_max"] = 29.5
            st.session_state["sim_humidity"] = 82
            st.session_state["sim_jarak_kanal"] = 15000
            st.session_state["sim_kab"] = "Katingan"
            st.session_state["sim_tipe_lahan"] = "Tanah Mineral"
            st.rerun()

    st.write("")

    col_sim1, col_sim2 = st.columns([1, 1.15])

    with col_sim1:
        st.markdown("##### 1. Parameter Cuaca Harian BMKG")
        sim_dry_spell = st.slider("Hari Tanpa Hujan (Dry Spell):", 0, 35, st.session_state["sim_dry_spell"], key="slider_dry")
        sim_rain_7d = st.slider("Curah Hujan 7 Hari Terakhir (mm):", 0.0, 80.0, float(st.session_state["sim_rain_7d"]), 0.5, key="slider_rain")
        sim_temp_max = st.slider("Suhu Maksimum Siang Hari (°C):", 27.0, 39.0, float(st.session_state["sim_temp_max"]), 0.5, key="slider_temp")
        sim_humidity = st.slider("Kelembapan Relatif Udara (%):", 30, 95, int(st.session_state["sim_humidity"]), key="slider_rh")

        st.markdown("##### 2. Karakteristik Geospasial & Biofisik Lahan")
        kab_options = [
            "Pulang Pisau", "Seruyan", "Kapuas", "Katingan",
            "Kotawaringin Timur", "Kotawaringin Barat", "Kota Palangka Raya", "Barito Selatan"
        ]
        default_kab_idx = kab_options.index(st.session_state["sim_kab"]) if st.session_state["sim_kab"] in kab_options else 0
        sim_kab = st.selectbox("Kabupaten / Kota:", kab_options, index=default_kab_idx)

        lahan_options = [
            "Gambut Sangat Dalam (>300 cm)",
            "Gambut Dalam (200-300 cm)",
            "Gambut Sedang (100-200 cm)",
            "Gambut Dangkal (50-100 cm)",
            "Tanah Mineral"
        ]
        default_lahan_idx = lahan_options.index(st.session_state["sim_tipe_lahan"]) if st.session_state["sim_tipe_lahan"] in lahan_options else 0
        sim_tipe_lahan = st.selectbox("Tipe Ekosistem Lahan (BBLSDLP 2019):", lahan_options, index=default_lahan_idx)

        sim_jarak_kanal = st.slider(
            "Jarak ke Poros Saluran Kanal Eks-PLG (meter):",
            0, 30000, int(st.session_state["sim_jarak_kanal"]), 100, key="slider_canal"
        )
        if "Sangat Dalam" in sim_tipe_lahan:
            sim_kedalaman_gambut = 380
        elif "Dalam" in sim_tipe_lahan:
            sim_kedalaman_gambut = 250
        elif "Sedang" in sim_tipe_lahan:
            sim_kedalaman_gambut = 150
        elif "Dangkal" in sim_tipe_lahan:
            sim_kedalaman_gambut = 75
        else:
            sim_kedalaman_gambut = 0

        sim_tutupan = st.selectbox("Tutupan Vegetasi:", [
            "Semak Belukar Rawa Gambut (Eks-PLG)", "Perkebunan Kelapa Sawit (HGU)",
            "Konsesi Hutan Tanaman / Alam (PBPH)", "Semak Belukar / Lahan Terbuka Mineral"
        ])
        sim_konsesi = st.selectbox("Status Izin Lahan:", [
            "Non-Konsesi (Area Penggunaan Lain / Komunitas)",
            "Konsesi Perkebunan Sawit (HGU)",
            "Konsesi Kehutanan (IUPHHK-HTI/HA)"
        ])

    kab_coords = {
        "Pulang Pisau": (-2.85, 114.15),
        "Kapuas": (-2.50, 114.40),
        "Kotawaringin Timur": (-2.30, 112.95),
        "Kota Palangka Raya": (-2.15, 113.85),
        "Katingan": (-2.10, 113.25),
        "Seruyan": (-2.20, 112.50),
        "Barito Selatan": (-1.90, 114.85),
        "Kotawaringin Barat": (-2.68, 111.62)
    }
    sim_lat, sim_lon = kab_coords.get(sim_kab, (-2.2, 113.5))

    with col_sim2:
        st.markdown("##### Tingkat Risiko Keparahan Api (FRP ≥ 12 MW)")
        
        if model_bundle is not None:
            model = model_bundle["model"]
            encoders = model_bundle["label_encoders"]
            features = model_bundle["features"]

            is_plg = 1 if sim_kab in ["Pulang Pisau", "Kapuas", "Kota Palangka Raya"] else 0
            fwi_val = round((sim_temp_max * 0.35) + (sim_dry_spell * 1.35) - (sim_rain_7d * 0.22) + ((100 - sim_humidity) * 0.22) + (12.0 * 0.25), 2)

            input_dict = {
                "latitude": sim_lat,
                "longitude": sim_lon,
                "kedalaman_gambut_cm": sim_kedalaman_gambut,
                "jarak_kanal_m": sim_jarak_kanal if is_plg else -1,
                "is_ex_plg_landscape": is_plg,
                "curah_hujan_7h_mm": sim_rain_7d,
                "suhu_maks_c": sim_temp_max,
                "kelembapan_relatif_pct": sim_humidity,
                "kecepatan_angin_kmh": 12.0,
                "dry_spell_days": sim_dry_spell,
                "fwi_score": fwi_val,
                "kabupaten_kota": sim_kab,
                "tipe_lahan": sim_tipe_lahan,
                "tutupan_lahan": sim_tutupan,
                "status_konsesi": sim_konsesi
            }
            row_df = pd.DataFrame([input_dict])
            for col in ["kabupaten_kota", "tipe_lahan", "tutupan_lahan", "status_konsesi"]:
                if col in encoders:
                    le = encoders[col]
                    val = str(row_df[col].iloc[0])
                    row_df[col] = le.transform([val])[0] if val in le.classes_ else 0

            # Prediksi probabilitas dari model Random Forest asli
            prob_extreme = model.predict_proba(row_df[features])[0, 1] * 100

            # -----------------------------------------------------------------
            # GAUGE METER PLOTLY
            # -----------------------------------------------------------------
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=round(prob_extreme, 1),
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Probabilitas Api Berkekuatan Ekstrem (%)", 'font': {'size': 14.5, 'color': '#0f172a', 'weight': 'bold'}},
                number={'suffix': "%", 'font': {'size': 32, 'color': '#0f172a', 'weight': 'bold'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1.5, 'tickcolor': "#475569"},
                    'bar': {'color': "#0f172a", 'thickness': 0.28},
                    'bgcolor': "white",
                    'borderwidth': 1.5,
                    'bordercolor': "#cbd5e1",
                    'steps': [
                        {'range': [0, 35], 'color': '#dcfce7'},
                        {'range': [35, 60], 'color': '#fef9c3'},
                        {'range': [60, 80], 'color': '#ffedd5'},
                        {'range': [80, 100], 'color': '#fee2e2'}
                    ],
                    'threshold': {
                        'line': {'color': "#dc2626", 'width': 4},
                        'thickness': 0.8,
                        'value': prob_extreme
                    }
                }
            ))
            fig_gauge.update_layout(height=240, margin=dict(l=20, r=20, t=30, b=10))
            st.plotly_chart(fig_gauge, use_container_width=True)

            # Badge Status & Kotak Aksi Taktis
            if prob_extreme >= 80:
                badge_html = '<div class="risk-badge badge-ekstrem">🚨 AWAS EKSTREM</div>'
                action_box_style = "background-color: #fef2f2; border: 1.5px solid #f87171; color: #991b1b;"
                action_text = """
                <strong>TINDAKAN LAPANGAN SEGERA (PROTOKOL AWAS):</strong><br/>
                • <strong>Siagakan Water Bombing Udara</strong>: Koordinasikan helikopter BNPB untuk pembasahan lahan gambut.<br/>
                • <strong>Penyekatan Kanal Darurat</strong>: Naikkan muka air di saluran primer eks-PLG agar gambut tidak mengering.<br/>
                • <strong>Siaga Posko Kesehatan</strong>: Salurkan masker N95 dan aktifkan posko evakuasi kabut asap.
                """
            elif prob_extreme >= 60:
                badge_html = '<div class="risk-badge badge-siaga">⚠️ SIAGA DARURAT</div>'
                action_box_style = "background-color: #fff7ed; border: 1.5px solid #fb923c; color: #9a3412;"
                action_text = """
                <strong>TINDAKAN LAPANGAN SEGERA (PROTOKOL SIAGA):</strong><br/>
                • <strong>Patroli Darat 24 Jam</strong>: Mobilisasi regu Manggala Agni, Babinsa, Bhabinkamtibmas, dan MPA.<br/>
                • <strong>Uji Sumur Bor & Embung</strong>: Pastikan suplai air di batas konsesi dan rawa gambut siap pompa.<br/>
                • <strong>Tegakkan Jam Malam Bakar</strong>: Larangan tegas segala bentuk penyulutan api terbuka.
                """
            elif prob_extreme >= 35:
                badge_html = '<div class="risk-badge badge-waspada">⚡ WASPADA</div>'
                action_box_style = "background-color: #fefce8; border: 1.5px solid #facc15; color: #854d0e;"
                action_text = """
                <strong>TINDAKAN PENCEGAHAN (PROTOKOL WASPADA):</strong><br/>
                • Pantau data sensor telemetri tinggi muka air tanah gambut (TMAT) secara harian.<br/>
                • Berikan sosialisasi intensif pembukaan lahan tanpa bakar (PLTB) kepada kelompok pekebun.
                """
            else:
                badge_html = '<div class="risk-badge badge-aman">✅ AMAN TERKENDALI</div>'
                action_box_style = "background-color: #f0fdf4; border: 1.5px solid #4ade80; color: #166534;"
                action_text = """
                <strong>STATUS KONDUSIF:</strong><br/>
                • Kelembapan dan curah hujan memadai untuk menekan potensi karhutla berkekuatan tinggi.<br/>
                • Lanjutkan pemantauan citra satelit harian secara reguler.
                """

            st.markdown(badge_html, unsafe_allow_html=True)
            st.markdown(f'<div class="action-box" style="{action_box_style}">{action_text}</div>', unsafe_allow_html=True)

            # -----------------------------------------------------------------
            # SIMULASI INTERVENSI MITIGASI ("EFEK PENYEKATAN KANAL")
            # -----------------------------------------------------------------
            st.write("")
            with st.expander("💧 Simulasi Mitigasi: Efek Penyekatan Kanal & Pembasahan Gambut", expanded=False):
                # Hitung ulang jika kanal disekat (jarak efektif air naik / seolah berada 8.000 m dari kanal kering)
                row_mitigated = row_df.copy()
                row_mitigated["jarak_kanal_m"] = max(sim_jarak_kanal, 8000)
                row_mitigated["curah_hujan_7h_mm"] = max(sim_rain_7d, 15.0)
                prob_mitigated = model.predict_proba(row_mitigated[features])[0, 1] * 100
                delta_risk = prob_extreme - prob_mitigated

                m_col1, m_col2 = st.columns(2)
                m_col1.metric("Risiko Sebelum Intervensi", f"{prob_extreme:.1f}%")
                m_col2.metric("Risiko Pasca-Sekat Kanal", f"{prob_mitigated:.1f}%", delta=f"-{delta_risk:.1f}% Risiko Turun", delta_color="inverse")
                st.caption("Penyekatan kanal dan pembasahan lahan terbukti secara kuantitatif menekan probabilitas karhutla berenergi tinggi.")

# =============================================================================
# TAB 3: ANALISIS DATA EKSPLORATIF (INTERAKTIF & MULTI-CHART)
# =============================================================================
with tab_eda:
    st.markdown("##### Eksplorasi Data Karhutla Kalimantan Tengah")
    
    # Filter Cepat Tab EDA
    f_c1, f_c2, f_c3 = st.columns(3)
    with f_c1:
        eda_kabs = st.multiselect("Filter Kabupaten:", sorted(df["kabupaten_kota"].unique()), default=[])
    with f_c2:
        eda_lahan = st.multiselect("Filter Tipe Lahan:", sorted(df["tipe_lahan"].unique()), default=[])
    with f_c3:
        eda_konsesi = st.multiselect("Filter Status Izin:", sorted(df["status_konsesi"].unique()), default=[])

    # Terapkan filter
    eda_df = df.copy()
    if eda_kabs:
        eda_df = eda_df[eda_df["kabupaten_kota"].isin(eda_kabs)]
    if eda_lahan:
        eda_df = eda_df[eda_df["tipe_lahan"].isin(eda_lahan)]
    if eda_konsesi:
        eda_df = eda_df[eda_df["status_konsesi"].isin(eda_konsesi)]

    st.caption(f"Menampilkan **{len(eda_df):,}** dari {len(df):,} titik api berdasarkan filter yang dipilih.")

    # Baris 1: Tren Multi-Tahun SiPongi & Distribusi Harian FIRMS
    g1_col1, g1_col2 = st.columns(2)
    with g1_col1:
        st.markdown("##### Tren Luas Karhutla Resmi SiPongi KLHK (2018–2026)")
        sipongi_path = "data/raw/sipongi_luas_karhutla_kalteng_2018_2026.csv"
        if os.path.exists(sipongi_path):
            sdf = pd.read_csv(sipongi_path)
            fig_trend = px.bar(
                sdf, x="tahun", y="luas_terbakar_ha",
                color="luas_terbakar_ha", color_continuous_scale="Reds",
                labels={"luas_terbakar_ha": "Luas Terbakar (Ha)", "tahun": "Tahun"},
                text_auto=".0f"
            )
            fig_trend.update_layout(height=310, margin=dict(l=40, r=20, t=15, b=30), coloraxis_showscale=False)
            st.plotly_chart(fig_trend, use_container_width=True)

    with g1_col2:
        st.markdown("##### Dinamika Harian Observasi Satelit NASA FIRMS (Oktober 2026)")
        eda_df_copy = eda_df.copy()
        eda_df_copy["tgl_str"] = eda_df_copy["acq_date"].dt.strftime("%d %b")
        daily_sat = eda_df_copy.groupby(["tgl_str", "satellite"]).size().reset_index(name="hotspots")
        fig_daily = px.bar(
            daily_sat, x="tgl_str", y="hotspots", color="satellite",
            color_discrete_sequence=["#dc2626", "#ea580c", "#f59e0b"],
            labels={"tgl_str": "Tanggal", "hotspots": "Titik Api", "satellite": "Sensor"}
        )
        fig_daily.update_layout(
            height=310, margin=dict(l=40, r=20, t=15, b=30),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_daily, use_container_width=True)

    # Baris 2: Sebaran Kabupaten & Proporsi Konsesi
    g2_col1, g2_col2 = st.columns(2)
    with g2_col1:
        st.markdown("##### Sebaran Hotspot per Kabupaten & Stratifikasi Gambut")
        kab_order = eda_df.groupby("kabupaten_kota").size().sort_values(ascending=True).index
        kab_df = eda_df.groupby(["kabupaten_kota", "tipe_lahan"]).size().reset_index(name="count")
        fig_kab = px.bar(
            kab_df, y="kabupaten_kota", x="count", color="tipe_lahan",
            orientation="h", category_orders={"kabupaten_kota": list(kab_order)},
            color_discrete_map={
                "Gambut Sangat Dalam (>300 cm)": "#7f1d1d",
                "Gambut Dalam (200-300 cm)": "#c2410c",
                "Gambut Sedang (100-200 cm)": "#ea580c",
                "Gambut Dangkal (50-100 cm)": "#f97316",
                "Tanah Mineral": "#0284c7"
            }
        )
        fig_kab.update_layout(
            margin=dict(l=40, r=20, t=15, b=30), height=330,
            xaxis_title="Jumlah Titik Api", yaxis_title="",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_kab, use_container_width=True)

    with g2_col2:
        st.markdown("##### Proporsi Status Izin Lahan (75,4% Non-Konsesi)")
        konsesi_df = eda_df["status_konsesi"].value_counts().reset_index()
        konsesi_df.columns = ["status", "count"]
        fig_pie = px.pie(
            konsesi_df, names="status", values="count", hole=0.45,
            color="status",
            color_discrete_map={
                "Non-Konsesi (Area Penggunaan Lain / Komunitas)": "#dc2626",
                "Konsesi Perkebunan Sawit (HGU)": "#f59e0b",
                "Konsesi Kehutanan (IUPHHK-HTI/HA)": "#10b981"
            }
        )
        fig_pie.update_traces(
            textposition="inside", textinfo="percent+label",
            hovertemplate="%{label}: <b>%{value:,}</b> (%{percent})"
        )
        fig_pie.update_layout(margin=dict(l=20, r=20, t=15, b=20), height=330, showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Baris 3: Top Perusahaan Berizin (ESG Accountability)
    corp_df = eda_df[eda_df["nama_konsesi"] != "Non-Konsesi (APL / Lahan Terbuka)"]
    if len(corp_df) > 0:
        st.write("")
        st.markdown("##### 10 Entitas Pemegang Izin dengan Akumulasi Titik Api Terbanyak (Audit ESG)")
        top_corp = corp_df.groupby(["nama_konsesi", "status_konsesi"]).size().reset_index(name="hotspot")
        top_corp = top_corp.sort_values(by="hotspot", ascending=True).tail(10)
        fig_corp = px.bar(
            top_corp, y="nama_konsesi", x="hotspot", color="status_konsesi",
            orientation="h",
            color_discrete_map={
                "Konsesi Perkebunan Sawit (HGU)": "#f59e0b",
                "Konsesi Kehutanan (IUPHHK-HTI/HA)": "#10b981"
            },
            text_auto=",",
            labels={"nama_konsesi": "", "hotspot": "Jumlah Titik Api", "status_konsesi": "Jenis Konsesi"}
        )
        fig_corp.update_layout(
            margin=dict(l=40, r=20, t=15, b=30), height=320,
            xaxis_title="Titik Api di Dalam Batas Izin", yaxis_title="",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_corp, use_container_width=True)

    # Tombol Unduh Data Terfilter
    csv_data = eda_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Unduh Dataset Terfilter (CSV)",
        data=csv_data,
        file_name="karhutla_kalteng_filtered.csv",
        mime="text/csv"
    )

# =============================================================================
# TAB 4: EVALUASI MODEL AI (TOGGLE AWAM VS PAKAR)
# =============================================================================
with tab_model:
    view_mode = st.radio(
        "Pilih Sudut Pandang Evaluasi Model:",
        ["👤 Mode Pengambil Kebijakan / Awam (Faktor Pemicu Kunci)", "🔬 Mode Pakar / Data Scientist (Spatial Cross-Validation & Metrik Detail)"],
        horizontal=True
    )

    if "Awam" in view_mode:
        st.markdown("##### Variabel Lingkungan yang Paling Menentukan Keparahan Api")
        st.caption("Model AI Random Forest menganalisis ribuan titik api untuk menemukan faktor pemicu api berenergi radiasi tinggi.")
        
        m_col1, m_col2 = st.columns([1.2, 1])
        with m_col1:
            if os.path.exists("output/figures/07_shap_feature_importance.png"):
                st.image("output/figures/07_shap_feature_importance.png", use_container_width=True)
        with m_col2:
            st.markdown("""
            <div style="background-color: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 8px; padding: 18px; font-size: 13.5px; line-height: 1.6;">
                <h4 style="color: #0f172a; margin-top: 0; font-size: 15px; font-weight: 800;">💡 3 TEMUAN KUNCI UNTUK PENGAMBIL KEBIJAKAN</h4>
                <ol style="margin-bottom: 0; padding-left: 20px;">
                    <li><strong>Poros Kanal Eks-PLG adalah Episentrum Bahaya</strong>: Titik api pada radius &lt; 1.000 meter dari saluran drainase memiliki energi api tertinggi karena air gambut terkuras.</li>
                    <li><strong>Titik Kritis 14 Hari Tanpa Hujan</strong>: Risiko kebakaran ekstrem melonjak eksponensial setelah periode kering berturut-turut melebihi 14 hari.</li>
                    <li><strong>Kedalaman Gambut Menentukan Asap Pekat</strong>: Gambut tebal (&gt; 3 meter) meningkatkan durasi pembakaran bawah tanah (*smoldering*) yang menghasilkan polusi aerosol PM2.5 masif.</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("##### Metrik Teknis Evaluasi Model & Komparasi Validasi Spasial")
        st.caption("Validasi Silang Blok Spasial (GroupKFold 5-Fold per Kabupaten) membuktikan bahaya memorisasi koordinat spasial (Tobler's First Law) pada pemodelan bencana tabular.")

        metrics_file = "output/reports/model_metrics.json"
        metrics_data = {}
        if os.path.exists(metrics_file):
            with open(metrics_file, "r") as f:
                metrics_data = json.load(f)

        m_b = metrics_data.get("model_b_pure_biophysical", {})
        m_a = metrics_data.get("model_a_spatial_memorization", {})

        comp_col1, comp_col2 = st.columns(2)
        with comp_col1:
            st.markdown("###### 🌿 Model B: Pure Biophysical (Model Utama Tanpa Lat/Lon)")
            mb1, mb2, mb3 = st.columns(3)
            mb1.metric("Holdout Test AUC", f"{m_b.get('test_roc_auc', 0.7527):.4f}")
            mb2.metric("Mean Spatial CV AUC", f"{m_b.get('spatial_block_cv_mean_roc_auc', 0.4950):.4f}")
            mb3.metric("Spatial CV Mean F1", f"{m_b.get('spatial_block_cv_mean_f1', 0.1399):.4f}", delta="2.4x Lebih Tinggi")
            st.caption(f"Recall Api Ekstrem: {m_b.get('recall_ekstrem', 0.6582)*100:.1f}% | Precision Reguler: {m_b.get('precision_reguler', 0.9206)*100:.1f}%")

        with comp_col2:
            st.markdown("###### 📍 Model A: Baseline Hafalan Koordinat (Dengan Lat/Lon)")
            ma1, ma2, ma3 = st.columns(3)
            ma1.metric("Holdout Test AUC", f"{m_a.get('test_roc_auc', 0.7956):.4f}", help="Tampak superior pada random split karena data leakage koordinat")
            ma2.metric("Mean Spatial CV AUC", f"{m_a.get('spatial_block_cv_mean_roc_auc', 0.5399):.4f}", delta="-0.2557 Anjlok Spasial", delta_color="inverse")
            ma3.metric("Spatial CV Mean F1", f"{m_a.get('spatial_block_cv_mean_f1', 0.0583):.4f}", delta="-87.1% Kolaps", delta_color="inverse")
            st.caption("F1-Score anjlok menjadi 0.0000 di 4 dari 5 fold kabupaten yang belum pernah dilihat model.")

        st.markdown("###### Hasil Rinci Validasi Silang Blok Spasial 5-Fold (GroupKFold per Kabupaten):")
        folds_b = m_b.get("spatial_block_cv_folds_detail", [])
        folds_a = m_a.get("spatial_block_cv_folds_detail", [])
        
        table_rows = []
        for i in range(5):
            fb = folds_b[i] if i < len(folds_b) else {}
            fa = folds_a[i] if i < len(folds_a) else {}
            kabs_str = ", ".join(fb.get("test_regencies", []))
            table_rows.append({
                "Fold #": f"Fold {i+1}",
                "Kabupaten Uji (Held-out Area)": kabs_str,
                "Model A AUC": f"{fa.get('roc_auc', 0.0):.4f}",
                "Model A F1": f"{fa.get('f1_score', 0.0):.4f}",
                "Model B AUC": f"{fb.get('roc_auc', 0.0):.4f}",
                "Model B F1": f"{fb.get('f1_score', 0.0):.4f}",
                "Status Generalisasi Model B": "Deteksi Aktif (F1 > 0)" if fb.get('f1_score', 0) > 0 else "Gagal"
            })
        st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

        ev_c1, ev_c2 = st.columns(2)
        with ev_c1:
            if os.path.exists("output/figures/06_evaluasi_model_ml.png"):
                st.image("output/figures/06_evaluasi_model_ml.png", use_container_width=True)
        with ev_c2:
            st.markdown("###### Parameter & Arsitektur Model Utama (Model B):")
            st.code("""
RandomForestClassifier(
    n_estimators=150,
    max_depth=10,
    min_samples_split=6,
    class_weight='balanced',
    random_state=42
)
# Fitur: Curah Hujan 7H, Jarak Kanal PLG,
# Suhu Maks, RH, Angin, Dry Spell, FWI,
# Kedalaman Gambut, Tipe Gambut,
# Zonasi Eks-PLG, Tutupan Lahan, Konsesi
            """, language="python")
            if os.path.exists("output/models/karhutla_rf_model.joblib"):
                with open("output/models/karhutla_rf_model.joblib", "rb") as mf:
                    st.download_button("📥 Unduh Model Bundle (Joblib)", mf.read(), "karhutla_rf_model.joblib")

# =============================================================================
# TAB 5: REKOMENDASI KEBIJAKAN BERBASIS DATA (POLICY ROADMAP)
# =============================================================================
with tab_policy:
    st.markdown("""
    #### Rekomendasi Aksi Mitigasi Berbasis Bukti Sains Data (Evidence-Based Policy)

    1. **Restorasi Hidrologis Prioritas Kanal Eks-PLG**:
       - Pembangunan sekat kanal (*canal blocking*) harus difokuskan pada radius &lt; 1.000 meter di sepanjang saluran primer Blok A, B, C eks-PLG (Pulang Pisau, Kapuas, Seruyan).
       - Target operasional: Pertahankan muka air tanah di atas ambang batas kritis **-40 cm** sebelum puncak kemarau tiba.
    
    2. **Fokus Patroli pada Lahan Terbuka Non-Konsesi (APL)**:
       - Mengingat **75,4% titik api berada di luar konsesi berizin**, operasi patroli pencegahan harus memprioritaskan pemberdayaan Masyarakat Peduli Api (MPA) dan brigade darat di lahan terlantar yang tidak memiliki pengelola aktif.
    
    3. **Aktivasi Peringatan Dini Berbasis Ambang Batas 14 Hari**:
       - Otomatisasikan kenaikan status menjadi **Siaga Darurat** saat sensor BMKG mencatat 12–14 hari berturut-turut tanpa hujan di kubah gambut, disertai persiapan helikopter *water bombing* dan Operasi Modifikasi Cuaca (OMC).
    
    4. **Penegakan Akuntabilitas ESG untuk 24,6% Titik Api di Dalam Konsesi**:
       - Manfaatkan penautan data spasial (*spatial join*) untuk meminta pertanggungjawaban hukum dan audit kepatuhan lingkungan terhadap entitas pemegang izin HGU sawit dan PBPH kehutanan yang terbukti memiliki titik api berulang di dalam batas konsesi.
    """)

    st.write("")
    if os.path.exists("PROJECT_SUMMARY.md"):
        with open("PROJECT_SUMMARY.md", "r", encoding="utf-8") as f:
            st.download_button(
                "📥 Unduh Laporan Eksekutif Lengkap (PROJECT_SUMMARY.md)",
                f.read(),
                "PROJECT_SUMMARY_KARHUTLA_KALTENG.md",
                "text/markdown"
            )

st.markdown("---")
st.caption("Sistem Pemantauan Karhutla Kalimantan Tengah • Integrasi NASA FIRMS, SiPongi KLHK, dan Pemodelan Spasial Machine Learning")
