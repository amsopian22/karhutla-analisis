# Handoff Report: Milestone 1 (M1) Text Refactoring & Scope Alignment

**From**: `worker_ag_m1` (teamwork_worker)  
**To**: `parent` (`5ded17bc-a3a2-4d64-96ac-1cdeb9993084`) / Next Agent  
**Date**: 2026-11-04  
**Working Directory**: `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/worker_ag_m1/`  
**Target Journal**: *Applied Geography* (Elsevier, IF: 7.4, CiteScore: 8.3, Scopus Q1)

---

## 1. Observation

1. **Abstract Word Count**:
   - `manuscript/sections/00_abstract.tex`: Sebelumnya 363 kata (+113 kata di atas batas 250 kata). Kini terkalibrasi menjadi **240 kata** (whitespace split) / **241 kata** (regex word tokens).
   - `manuscript/manuscript_draft.md`: Sebelumnya 369 kata. Kini terkalibrasi menjadi **241 kata** (whitespace split) / **241 kata** (regex word tokens).
   - Seluruh metrik kuantitatif esensial dipertahankan secara utuh: 43.937 titik api FIRMS, keruntuhan spasial Model A (ROC-AUC 0.7956 $\rightarrow$ 0.5399, $F_1 = 0.0000$ pada 4 lipatan), generalisasi biofisik Model B (ROC-AUC 0.7527, recall api ekstrem 65,8%, retensi $F_1$ rata-rata 0.1399 [2,4x Model A]), ambang batas TreeSHAP (defisit hujan 7-hari $< 5.0$\,mm, jarak kanal $< 3.0$\,km, hari tanpa hujan berturut-turut $> 14$\,hari), serta temuan tenurial APL 75,4% vs konsesi korporasi 24,6%.
2. **Keywords Count**:
   - `00_abstract.tex` dan `manuscript_draft.md`: Sebelumnya memuat 9–10 kata kunci. Kini tepat memuat **7 kata kunci**:
     *Applied spatial geography; Tropical peatlands; Spatial autocorrelation; Spatial block cross-validation; Land tenure governance; Wildfire intensity modeling; Mega Rice Project*
3. **Research Highlights**:
   - `manuscript/highlights.md`: Tepat 5 butir peluru. Panjang karakter per butir:
     - Butir 1: 72 karakter
     - Butir 2: 76 karakter
     - Butir 3: 75 karakter
     - Butir 4: 78 karakter
     - Butir 5: 79 karakter
     Semua berada di bawah ambang batas maksimum pedoman Elsevier ($\le 85$ karakter termasuk spasi).
4. **Reframing Tematik Applied Geography & GIScience**:
   - `sections/01_introduction.tex`: Memasukkan landasan Hukum Pertama Tobler, jebakan memorisasi spasial pada algoritma *decision trees*, kebocoran data autokorelasi spasial, serta dikotomi geografi politik tenurial Kawasan Hutan vs Area Penggunaan Lain (APL). Hipotesis $H_1$ dan $H_2$ dirumuskan secara eksplisit.
   - `sections/04_discussion.tex`: Ditambahkan Sub-bab 4.4 mengenai perencanaan spasial terapan (RTRWP/RPPEG), zonasi prioritas sekat kanal koridor 3.000 m (SPI Blok A & B), resolusi ruang hampa tata kelola APL melalui Perhutanan Sosial (HKm/Hutan Desa) / KPH, pertanggungjawaban mutlak (*strict liability* Pasal 88 UU 32/2009), dan permodelan dispersi aerosol $\text{PM}_{2.5}$ lintas batas di bawah angin Monsun Barat Daya ke Kuching ($197.3\,\mu\text{g}/\text{m}^3$), Singapura ($165.3\,\mu\text{g}/\text{m}^3$), dan Kuala Lumpur ($191.7\,\mu\text{g}/\text{m}^3$).
   - `sections/05_conclusions.tex`: Merangkum implikasi geografi terapan dan sains informasi geografis, 4 pilar rekomendasi kebijakan spasial, dan arah riset regional ke depan.
5. **Sinkronisasi Markdown `manuscript_draft.md`**:
   - Target journal header baris 10: `**Target Journal:** *Applied Geography* (Elsevier)`.
   - Jumlah titik api ekstrem: $n = 6.648$ (15,13%) terverifikasi konsisten di seluruh teks.
   - Penomoran sub-bab Hasil (Section 3), tabel (Tabel 1–4), dan gambar (Gambar 1–7) kini selaras 1:1 dengan versi LaTeX tanpa ada gambar/tabel yang kehilangan pemanggilan teks (*uncalled / orphaned assets*).
6. **Gaya Sitasi LaTeX**:
   - `main.tex`: Menggunakan `\usepackage[authoryear,round]{natbib}` dan `\bibliographystyle{elsarticle-harv}`.
   - Kompilasi via `/opt/homebrew/bin/tectonic main.tex` berhasil sempurna (Exit code: 0), menghasilkan `main.pdf` 28 halaman (10,62 MB) dengan sitasi format `(Penulis, Tahun)` dan daftar pustaka Harvard alfabetis.
7. **Cover Letter**:
   - `manuscript/cover_letter.md`: Memaparkan keselarasan naskah dengan Aims & Scope *Applied Geography*, menjelaskan konteks penolakan sebelumnya dari *Ecological Modelling* (murni karena ketidakcocokan skop di mana jurnal tersebut mengkhususkan diri pada simulasi metabolik/biologis murni), dan menguraikan kontribusi geografi spasial terapan secara lugas.

---

## 2. Logic Chain

1. **Dari Masalah Editorial ke Solusi Abstrak & Keywords**:
   Pedoman resmi *Applied Geography Guide for Authors* menetapkan batas mutlak $\le 250$ kata untuk abstrak dan 1–7 kata kunci. Teks abstrak lama (363–369 kata) berisiko memicu penolakan teknis (*technical screening failure*) oleh sistem editorial Elsevier. Dengan memadatkan struktur kalimat tanpa membuang angka statistik empiris, tercapai panjang 240–241 kata dan 7 kata kunci yang merepresentasikan pilar spasial naskah.
2. **Dari Evaluasi Skop ke Reframing Narasi**:
   Penolakan awal dari *Ecological Modelling* terjadi karena naskah dinilai berada di luar cakupan simulasi biologis. Oleh karena itu, penguatan narasi pada Hukum Pertama Tobler, mitigasi autokorelasi spasial melalui Spatial Block CV (`GroupKFold` per kabupaten), forensik jarak kanal metrik UTM 49S, analisis tenurial APL 75,4%, dan dispersi asap monsun regional menempatkan naskah tepat di jantung fokus *Applied Geography* ("putting problems in a geographical perspective").
3. **Dari Inkonsistensi Draf ke Keselarasan 1:1**:
   Pada draf markdown sebelumnya, Sub-bab 3.1 mengangkat tren temporal sehingga Gambar 5 menjadi Figure 2 di markdown, yang mengacaukan penomoran gambar berikutnya dan merusak kalimat pemanggil (*in-text callouts*). Dengan menyelaraskan urutan sub-bab Markdown persis mengikuti arsitektur modular LaTeX `03_results.tex`, seluruh gambar 1–7 dan tabel 1–4 kini terhubung secara deterministik dan bebas galat.
4. **Dari Sitasi Numerik ke Author-Year**:
   *Applied Geography* menggunakan format author-year (Harvard / APA 7th). Pengubahan opsi natbib dan penerapan `elsarticle-harv.bst` menjamin bahwa naskah cetak LaTeX mematuhi konvensi jurnal tanpa merusak makro sitasi yang sudah ada.

---

## 3. Caveats

1. **Regenerasi Dokumen Word DOCX (Tugas Milestone 2)**:
   Perubahan teks substantif pada `manuscript_draft.md`, `highlights.md`, dan `cover_letter.md` telah selesai. Regenerasi berkas biner DOCX (`manuscript_main.docx`, `highlights.docx`, `cover_letter.docx`) menggunakan Pandoc `--citeproc` dan CSL APA dijadwalkan secara terpisah pada Milestone 2 (M2) oleh agen pelaksana berikutnya sesuai pembagian kerja pada `SCOPE.md`.
2. **Ketersediaan Toolchain Pandoc**:
   Pandoc 3.8.3 terpasang di sistem (`/opt/homebrew/bin/pandoc`) dan siap digunakan pada fase M2 untuk regenerasi DOCX.

---

## 4. Conclusion

Seluruh sasaran Milestone 1 (M1) telah tercapai 100% dengan kepatuhan penuh terhadap pedoman *Applied Geography* dan kriteria integritas:
- Abstrak $\le 250$ kata (240–241 kata) dan tepat 7 kata kunci.
- Highlights 5 butir $\le 85$ karakter (72–79 karakter).
- Reframing tematik geografi spasial terapan kokoh di seluruh bagian teks.
- Angka titik api ekstrem sinkron pada $n = 6.648$ (15,13%).
- Keterhubungan gambar dan tabel 100% konsisten antara Markdown dan LaTeX.
- Kompilasi LaTeX `main.tex` via Tectonic menghasilkan PDF 28 halaman bebas galat dengan gaya sitasi author-year `elsarticle-harv`.
- Naskah siap dilanjutkan ke Milestone 2 (Kompilasi & Perenderan Paket Submisi DOCX).

---

## 5. Verification Method

Untuk memverifikasi secara independen hasil pekerjaan ini, jalankan perintah-perintah berikut:

1. **Uji Verifikasi Kuantitatif Programatik (Python)**:
   ```bash
   /opt/anaconda3/envs/karhutla_env/bin/python -c '
   import re

   # 1. Cek Kata Abstrak LaTeX & Markdown
   with open("manuscript/sections/00_abstract.tex") as f:
       tex = f.read()
   m_tex = re.search(r"\\begin\{abstract\}(.*?)(?:\\vspace|\\noindent\\textbf\{Keywords:\}|\\end\{abstract\})", tex, re.DOTALL)
   clean_tex = re.sub(r"\\[a-zA-Z]+|[{}\$~%]", " ", m_tex.group(1))
   assert len(clean_tex.split()) <= 250, "Abstrak LaTeX > 250 kata!"

   with open("manuscript/manuscript_draft.md") as f:
       md = f.read()
   m_md = re.search(r"## Abstract\s+(.*?)\s+\*\*Keywords:\*\*", md, re.DOTALL)
   clean_md = re.sub(r"[{}\$~%*`]", " ", m_md.group(1))
   assert len(clean_md.split()) <= 250, "Abstrak MD > 250 kata!"

   # 2. Cek Keywords == 7
   kw_tex = [k.strip() for k in re.search(r"\\textbf\{Keywords:\}.*?\\textit\{(.*?)\}", tex, re.DOTALL).group(1).split(";") if k.strip()]
   assert len(kw_tex) == 7, "Keywords LaTeX != 7"

   # 3. Cek Highlights <= 85 karakter
   with open("manuscript/highlights.md") as f:
       hl = [line.strip().lstrip("*-").strip() for line in f if line.strip().startswith(("*", "-"))]
   assert 3 <= len(hl) <= 5 and all(len(b) <= 85 for b in hl), "Highlights tidak patuh!"

   print("VERIFIKASI SUKSES: Semua batasan editorial terpenuhi 100%!")
   '
   ```

2. **Kompilasi Ulang LaTeX PDF**:
   ```bash
   cd /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/manuscript
   /opt/homebrew/bin/tectonic main.tex
   # Konfirmasi: exit code 0, menghasilkan main.pdf (~10.6 MB, 28 halaman)
   ```
