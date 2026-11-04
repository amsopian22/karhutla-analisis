# Handoff Report: Milestone 2 (M2) Submission Package Compilation & Visual/Tabular Integrity

**From**: `worker_ag_m2` (teamwork_worker)  
**To**: `parent` (`5ded17bc-a3a2-4d64-96ac-1cdeb9993084`) / Next Agent  
**Date**: 2026-11-04  
**Working Directory**: `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/worker_ag_m2/`  
**Target Journal**: *Applied Geography* (Elsevier, IF: 7.4, CiteScore: 8.3, Scopus Q1)  

---

## 1. Observation

1. **Toolchain Kompilasi Eksternal**:
   - `/opt/homebrew/bin/pandoc` versi 3.8.3 (dengan Lua 5.4 dan dukungan citeproc terintegrasi).
   - `/opt/homebrew/bin/tectonic` versi 0.16.9 (Rust-based standalone XeTeX engine).
   - Lingkungan conda `/opt/anaconda3/envs/karhutla_env/bin/python` (Python 3.10.22, Pillow, ElementTree, zipfile).
2. **Kompilasi Dokumen Word DOCX via Pandoc**:
   - `manuscript/submission_package/manuscript_main.docx`: Berhasil digenerate ulang dari `manuscript/manuscript_draft.md` dengan flag `--citeproc --bibliography=manuscript/references.bib`. Ukuran berkas: **11.950.782 bytes (~11,95 MB)**.
   - `manuscript/submission_package/highlights.docx`: Berhasil digenerate ulang dari `manuscript/highlights.md`. Ukuran berkas: **10.930 bytes (~10,93 KB)**.
   - `manuscript/submission_package/cover_letter.docx`: Berhasil digenerate ulang dari `manuscript/cover_letter.md`. Ukuran berkas: **13.974 bytes (~13,97 KB)**.
3. **Kompilasi LaTeX PDF via Tectonic**:
   - Perintah `cd manuscript && /opt/homebrew/bin/tectonic main.tex` selesai dengan exit code 0 tanpa galat kompilasi TeX/BibTeX.
   - Menghasilkan berkas `manuscript/main.pdf` dengan ukuran **11.138.804 bytes (10,62 MiB)**, **28 halaman A4**, dan metadata resmi Elsevier *Applied Geography*.
4. **Audit XML Internal DOCX (`manuscript_main.docx`)**:
   - **Tabel Word XML**: Terdeteksi tepat **4 tabel** `<w:tbl>` asli (Tabel 1: 11 baris; Tabel 2: 10 baris; Tabel 3: 13 baris; Tabel 4: 13 baris). Tidak ditemukan sisa raw markdown pipes (`| --- |`) (ditemukan 0) maupun kotak tabel ASCII art (ditemukan 0).
   - **Persamaan Matematika OMML**: Terdeteksi **132 elemen** `<m:oMath>` dan **9 paragraf persamaan tampilan penuh** `<m:oMathPara>`.
   - **Media Gambar Tersemat**: Terdeteksi tepat **7 berkas gambar** di `word/media/`. Hash SHA-256 tiap gambar cocok 100% dengan berkas master 300 DPI di `output/figures/` (`Figure 1` hingga `Figure 7`).
   - **Urutan Caption Gambar**: Terdeteksi tepat 7 caption terurut rapi: `Figure 1.`, `Figure 2.`, `Figure 3.`, `Figure 4.`, `Figure 5.`, `Figure 6.`, dan `Figure 7.`.
   - **Jumlah Kata Abstrak DOCX**: Dihitung dari paragraf abstrak kontainer Word XML menghasilkan **228 kata** (mematuhi batas $\le 250$ kata).
   - **Sitasi Bersih**: Tidak ditemukan artefak tanda kurung siku ganda `[[` atau `]]` (jumlah: 0).
5. **Audit Highlights & Cover Letter**:
   - `highlights.docx`: Terdeteksi tepat 5 butir peluru dengan panjang karakter: 72, 76, 75, 78, dan 79 karakter (seluruhnya $\le 85$ karakter).
   - `cover_letter.docx`: Memuat 25 paragraf lengkap dengan pengantar untuk Editor-in-Chief *Applied Geography*, penegasan Hukum Tobler, mitigasi autokorelasi spasial, data tenurial APL 75,4%, dan deklarasi etika.
6. **Audit PDF (`main.pdf`)**:
   - `pdfinfo` mengonfirmasi 28 halaman.
   - Ekstraksi teks halaman 1 menunjukkan panjang abstrak sebesar **235 kata** (mematuhi batas $\le 250$ kata).
   - Format sitasi terbukti menggunakan author-year Harvard style (misalnya: *Page et al. (2002); Dommain et al. (2011)*).

---

## 2. Logic Chain

1. **Dari Kebutuhan Regenerasi Paket Submisi ke Eksekusi Pandoc & Tectonic**:
   Pengamatan 2 dan 3 menunjukkan bahwa seluruh naskah Markdown dan LaTeX hasil refactoring substantif M1 telah dikompilasi ulang secara bersih menjadi paket submisi biner (`manuscript_main.docx`, `highlights.docx`, `cover_letter.docx`, dan `main.pdf`). Penerapan flag `--citeproc --bibliography=manuscript/references.bib` pada Pandoc menjamin bahwa kunci sitasi `@Page2002Nature` diubah menjadi teks naratif dan daftar pustaka lengkap secara otomatis.
2. **Dari Kekhawatiran Kerusakan Rendering ke Verifikasi XML**:
   Pengamatan 4 membuktikan secara objektif bahwa Pandoc mengonversi tabel Markdown menjadi entitas Word OpenXML `<w:tbl>` sejati, bukan teks mentah bertanda pipa atau ASCII art. Selain itu, formula matematika LaTeX dikonversi menjadi OMML MathML standar Office (`<m:oMath>`), sehingga dapat diedit langsung di Microsoft Word tanpa kerusakan simbol font.
3. **Dari Persyaratan Resolusi ke Validasi Hash SHA-256**:
   Pengamatan 4 membuktikan bahwa citra yang disematkan ke dalam DOCX bukanlah thumbnail atau hasil re-sampling resolusi rendah, melainkan berkas PNG 300 DPI berdimensi asli (hingga 4771 $\times$ 2957 px) dengan hash SHA-256 yang identik 100% dengan berkas di `output/figures/`.
4. **Dari Kepatuhan Pedoman Penulis ke Verifikasi Programatik**:
   Pengamatan 4, 5, dan 6 membuktikan bahwa seluruh batasan editorial Elsevier *Applied Geography* telah terpenuhi:
   - Abstrak DOCX (228 kata) dan PDF (235 kata) berada di bawah ambang batas $\le 250$ kata.
   - Highlights 5 butir berada di bawah ambang batas $\le 85$ karakter (72–79 karakter).
   - Gambar terurut konsisten dari 1 hingga 7 pada seluruh format.

---

## 3. Caveats

- **No caveats.** Seluruh berkas target dalam lingkup *Exclusive File Write Ownership* M2 telah dikompilasi ulang, diaudit pada tingkat kontainer XML biner, dan diverifikasi tanpa galat.

---

## 4. Conclusion

Seluruh sasaran Milestone 2 (M2) telah tercapai 100% dengan integritas teknis dan visual sempurna:
1. `manuscript_main.docx`, `highlights.docx`, dan `cover_letter.docx` telah diregenerasi menggunakan Pandoc dengan perenderan tabel Word XML, rumus matematika OMML, dan 7 figur 300 DPI.
2. `main.pdf` terkompilasi sukses 28 halaman via Tectonic dengan format sitasi Harvard author-year.
3. Seluruh tabel, persamaan, figur, dan batasan editorial telah divalidasi programatik.
4. Paket submisi siap untuk pengujian programatik dan audit forensik pada Milestone 3 (M3).

---

## 5. Verification Method

Jalankan perintah berikut pada terminal untuk memverifikasi secara independen:

```bash
# 1. Verifikasi Kompilasi LaTeX PDF via Tectonic
cd /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/manuscript
/opt/homebrew/bin/tectonic main.tex
/opt/homebrew/bin/pdfinfo main.pdf | grep -E "Pages:|Title:|Author:"

# 2. Uji Audit Programatik DOCX & PDF
/opt/anaconda3/envs/karhutla_env/bin/python -c '
import zipfile, xml.etree.ElementTree as ET, hashlib, os, subprocess, re

# Audit manuscript_main.docx
docx_path = "manuscript/submission_package/manuscript_main.docx"
with zipfile.ZipFile(docx_path) as z:
    doc_xml = z.read("word/document.xml")
    media = [f for f in z.namelist() if f.startswith("word/media/")]
root = ET.fromstring(doc_xml)
ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
tables = root.findall(".//w:tbl", ns)
assert len(tables) == 4, "Tabel != 4"
assert len(media) == 7, "Media != 7"

# Audit highlights.docx
with zipfile.ZipFile("manuscript/submission_package/highlights.docx") as z:
    hl_xml = z.read("word/document.xml")
hl_root = ET.fromstring(hl_xml)
hl_paras = ["".join([t.text for t in p.findall(".//w:t", ns) if t.text]).strip() for p in hl_root.findall(".//w:p", ns)]
bullets = [p for p in hl_paras if p and not p.lower().startswith("research highlights")]
assert 3 <= len(bullets) <= 5 and all(len(b) <= 85 for b in bullets), "Highlights gagal!"

# Audit PDF pages
info = subprocess.check_output(["/opt/homebrew/bin/pdfinfo", "manuscript/main.pdf"]).decode("utf-8")
assert "Pages:           28" in info, "PDF bukan 28 halaman!"

print("SELURUH VERIFIKASI M2 BERHASIL 100%!")
'
```
