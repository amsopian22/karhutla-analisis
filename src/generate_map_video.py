"""
Membuat Video Demonstrasi & Animasi GIF Peta Interaktif Karhutla Kalimantan Tengah.
Menghasilkan video MP4 (H.264) dan animasi GIF untuk disematkan pada artikel Medium & GitHub.
"""

import os
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

def generate_map_video(csv_path="data/processed/karhutla_kalteng_2019_2026.csv",
                       output_mp4="output/figures/video_peta_interaktif_karhutla.mp4",
                       output_gif="output/figures/animasi_peta_interaktif_karhutla.gif"):
    
    print("Memuat dataset untuk perenderan video peta interaktif...")
    df = pd.read_csv(csv_path)
    
    # Ambil sampel 3.000 titik api untuk visualisasi cepat dan jernih
    sample_df = df.sample(min(3000, len(df)), random_state=42)
    
    temp_dir = "output/figures/temp_frames"
    os.makedirs(temp_dir, exist_ok=True)
    
    total_frames = 120
    fps = 12
    print(f"Merender {total_frames} frame animasi peta interaktif...")
    
    # Koordinat Kalimantan Tengah
    center_lat, center_lon = -1.80, 113.50
    
    for f in range(total_frames):
        fig, ax = plt.subplots(figsize=(12, 7), dpi=100)
        
        # Timeline aksi video:
        # Frame 0 - 30: Overview Kalteng (Peta Jalan)
        # Frame 31 - 60: Heatmap layer diaktifkan
        # Frame 61 - 90: Zoom in ke Pulang Pisau & Kapuas (Eks-PLG)
        # Frame 91 - 120: Popup detail hotspot aktif & switch ke citra satelit
        
        if f < 60:
            # Tampilan luas Kalimantan Tengah
            ax.set_xlim(110.8, 115.8)
            ax.set_ylim(-3.5, 0.2)
            bg_color = "#1e293b" if f >= 90 else "#f8fafc"
        else:
            # Zoom in ke Pulang Pisau & Kapuas
            progress = (f - 60) / 30.0
            progress = min(1.0, progress)
            lon_min = 110.8 + progress * (113.4 - 110.8)
            lon_max = 115.8 - progress * (115.8 - 114.8)
            lat_min = -3.5 + progress * (-3.2 - -3.5)
            lat_max = 0.2 - progress * (0.2 - -2.3)
            ax.set_xlim(lon_min, lon_max)
            ax.set_ylim(lat_min, lat_max)
            bg_color = "#1a252f" if f >= 90 else "#f1f5f9"
            
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        
        # Gambar grid garis lat/lon halus
        ax.grid(True, color="#cbd5e1" if bg_color != "#1a252f" and bg_color != "#1e293b" else "#334155", linestyle="--", alpha=0.5)
        
        # Plot titik api
        is_peat = sample_df["tipe_lahan"].str.contains("Gambut")
        
        if f >= 30:
            # Heatmap glow effect
            ax.scatter(sample_df.loc[is_peat, "longitude"], sample_df.loc[is_peat, "latitude"],
                       s=180, color="#ef4444", alpha=0.15, edgecolors="none")
            ax.scatter(sample_df.loc[~is_peat, "longitude"], sample_df.loc[~is_peat, "latitude"],
                       s=120, color="#f97316", alpha=0.15, edgecolors="none")
                       
        # Titik api inti
        ax.scatter(sample_df.loc[is_peat, "longitude"], sample_df.loc[is_peat, "latitude"],
                   s=28, color="#dc2626", alpha=0.85, edgecolors="white", linewidths=0.3, label="Lahan Gambut (>73%)")
        ax.scatter(sample_df.loc[~is_peat, "longitude"], sample_df.loc[~is_peat, "latitude"],
                   s=22, color="#ea580c", alpha=0.8, edgecolors="white", linewidths=0.3, label="Tanah Mineral")
                   
        # Label Kota / Kabupaten Utama
        cities = {
            "Palangka Raya": (-2.20, 113.92),
            "Pulang Pisau (Eks-PLG)": (-2.85, 114.25),
            "Kapuas": (-2.60, 114.40),
            "Sampit (Kotim)": (-2.40, 112.95),
            "Pangkalan Bun": (-2.68, 111.62)
        }
        for name, (c_lat, c_lon) in cities.items():
            if ax.get_xlim()[0] <= c_lon <= ax.get_xlim()[1] and ax.get_ylim()[0] <= c_lat <= ax.get_ylim()[1]:
                ax.plot(c_lon, c_lat, marker="s", markersize=6, color="#0f172a" if bg_color=="#f8fafc" or bg_color=="#f1f5f9" else "#f8fafc")
                ax.text(c_lon + 0.05, c_lat + 0.04, name, fontsize=9, fontweight="bold",
                        color="#0f172a" if bg_color=="#f8fafc" or bg_color=="#f1f5f9" else "#f8fafc",
                        bbox=dict(boxstyle="round,pad=0.2", facecolor="white" if bg_color=="#f8fafc" or bg_color=="#f1f5f9" else "#334155", alpha=0.8, edgecolor="none"))
                        
        # Simulasi Jendela Popup Interaktif (Frame 75 ke atas)
        if f >= 75:
            target_lon, target_lat = 114.22, -2.78
            # Kursor klik
            ax.plot(target_lon, target_lat, marker="o", markersize=14, color="#e11d48", fillstyle="none", mew=2.5)
            ax.plot(target_lon, target_lat, marker="o", markersize=6, color="#e11d48")
            
            # Card Popup Folium
            popup_box = patches.FancyBboxPatch(
                (target_lon + 0.06, target_lat - 0.28), 0.70, 0.46,
                boxstyle="round,pad=0.03", facecolor="white", edgecolor="#e11d48", linewidth=2.0, alpha=0.98, zorder=10
            )
            ax.add_patch(popup_box)
            
            popup_text = (
                "🔥 HOTSPOT ID: ID-KT-2023-014882\n"
                "• Lokasi: Pulang Pisau (Eks-PLG Blok A)\n"
                "• Intensitas FRP: 185.4 MW (Sangat Tinggi)\n"
                "• Ekosistem: Lahan Gambut (> 3.5 meter)\n"
                "• Jarak ke Kanal: 320 meter\n"
                "• FWI Risk Index: EKSTREM (48.2)\n"
                "• Karakteristik: Subsurface Smoldering"
            )
            ax.text(target_lon + 0.09, target_lat - 0.25, popup_text, fontsize=8.5, color="#0f172a",
                    fontweight="semibold", va="bottom", linespacing=1.4, zorder=11)
                    
        # Header / Status Bar Simulasi
        layer_mode = "Citra Satelit Esri (High-Res)" if f >= 90 else ("Peta Jalan + Heatmap FRP" if f >= 30 else "Peta Jalan CartoDB Voyager")
        title_box = dict(boxstyle="round,pad=0.4", facecolor="#0f172a", alpha=0.9, edgecolor="none")
        ax.text(0.02, 0.96, f"🛰️ DEMO PETA INTERAKTIF KARHUTLA KALTENG\nLayer Aktif: [{layer_mode}] | Resolusi Observasi 2019-2026",
                transform=ax.transAxes, fontsize=10.5, color="white", fontweight="bold", va="top", bbox=title_box, zorder=15)
                
        # Kontrol Navigasi & Legenda Folium Mockup di Pojok Kanan Atas
        ax.text(0.98, 0.96, "☑ Heatmap Layer\n☑ Marker Cluster (400)\n☑ Basemap Switcher",
                transform=ax.transAxes, fontsize=8.5, color="#1e293b" if bg_color=="#f8fafc" or bg_color=="#f1f5f9" else "#f8fafc",
                ha="right", va="top", bbox=dict(boxstyle="round,pad=0.4", facecolor="white" if bg_color=="#f8fafc" or bg_color=="#f1f5f9" else "#1e293b", alpha=0.9, edgecolor="#cbd5e1"), zorder=15)
                
        ax.set_xlabel("Garis Bujur (Longitude)", fontsize=9)
        ax.set_ylabel("Garis Lintang (Latitude)", fontsize=9)
        
        plt.tight_layout()
        frame_file = os.path.join(temp_dir, f"frame_{f:04d}.png")
        plt.savefig(frame_file)
        plt.close()
        
    print("Mengonversi frame menjadi Video MP4 (H.264) menggunakan FFmpeg...")
    ffmpeg_cmd = f"/opt/homebrew/bin/ffmpeg -y -framerate {fps} -i {temp_dir}/frame_%04d.png -c:v libx264 -pix_fmt yuv420p {output_mp4}"
    os.system(ffmpeg_cmd)
    
    print("Mengonversi frame menjadi Animasi GIF untuk artikel Medium...")
    # Ambil setiap frame ganjil untuk menjaga ukuran GIF tetap ringan (< 5MB)
    images = []
    for f in range(0, total_frames, 2):
        frame_file = os.path.join(temp_dir, f"frame_{f:04d}.png")
        if os.path.exists(frame_file):
            img = Image.open(frame_file).resize((720, 420), Image.Resampling.LANCZOS)
            images.append(img)
            
    if images:
        images[0].save(output_gif, save_all=True, append_images=images[1:], duration=150, loop=0, optimize=True)
        print(f"Animasi GIF berhasil disimpan di: {output_gif}")
        
    # Bersihkan frame temporer
    shutil.rmtree(temp_dir, ignore_errors=True)
    print(f"Video MP4 berhasil disimpan di: {output_mp4}")

if __name__ == "__main__":
    generate_map_video()
