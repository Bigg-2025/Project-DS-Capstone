# ♻️ Dashboard Pengelolaan Sampah Nasional

Dashboard interaktif berbasis **Streamlit** untuk menganalisis data timbulan dan pengelolaan sampah seluruh Indonesia, dengan tema warna hijau dan dukungan peta choropleth.

---

## 📁 Struktur Proyek

```
dashboard_app/
├── app.py            # Entry point utama — layout & orkestrasi halaman
├── theme.py          # Warna, konstanta, dan CSS responsif
├── data_loader.py    # Load Excel & GeoJSON, cleaning, filter, agregasi
├── sidebar.py        # Komponen filter sidebar (provinsi, jenis TPA, timbulan)
├── kpi.py            # 5 metric card KPI (CSS grid, responsif mobile)
├── charts.py         # Semua fungsi chart Plotly (10 chart + 3 peta choropleth)
├── requirements.txt  # Dependency Python
└── README.md         # Dokumentasi ini
```

---

##  File Data yang Dibutuhkan

Letakkan kedua file berikut **di folder yang sama** dengan `app.py`:

| File | Keterangan |
|---|---|
| `data_sampah_clean.xlsx` | Data utama timbulan & pengelolaan sampah |
| `gadm41_IDN_1.json` | GeoJSON batas provinsi Indonesia (GADM level 1) |

> Jika `gadm41_IDN_1.json` tidak ada, dashboard tetap berjalan tanpa fitur peta.

---

## 🚀 Cara Menjalankan

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan dashboard
```bash
streamlit run app.py
```

### 3. Buka di browser
```
http://localhost:8501
```

---

## 📊 Fitur Dashboard

### 🔢 KPI Cards (5 metrik)
| Metrik | Keterangan |
|---|---|
| Total Timbulan | Jumlah total timbulan sampah (ton/hari) |
| Rata-rata Terkelola | Rata-rata % sampah terkelola (skala 0–1) |
| Rata-rata Belum Terkelola | Rata-rata % sampah belum terkelola |
| Jumlah Kota/Kab | Jumlah wilayah kota/kabupaten |
| Jumlah Provinsi | Jumlah provinsi dalam data |

### 📈 Visualisasi Chart
| Section | Chart | Keterangan |
|---|---|---|
| Persebaran Timbulan | Bar horizontal | Top 10 kota/kab timbulan terbesar |
| Persebaran Timbulan | Donut chart | Distribusi jenis TPA |
| Analisis Pengelolaan | Bar vertikal (hijau) | % Terkelola per provinsi |
| Analisis Pengelolaan | Bar vertikal (merah) | % Belum Terkelola per provinsi |
| Analisis Pengelolaan | Scatter plot | Timbulan vs % Belum Terkelola |
| Distribusi Timbulan | Bar vertikal | Total timbulan per provinsi |
| Distribusi Timbulan | Box plot | Distribusi timbulan per jenis TPA |

### 🗺️ Peta Choropleth (3 tab)
| Tab | Warna | Keterangan |
|---|---|---|
| Total Timbulan | Hijau muda → Kuning → Hijau tua | Semakin gelap = timbulan makin besar |
| % Terkelola | Merah → Kuning → Hijau | Merah = buruk, Hijau = baik |
| % Belum Terkelola | Hijau → Kuning → Merah | Hijau = baik, Merah = buruk |

> Warna peta menggunakan **range data aktual** (bukan 0–100) agar perbedaan antar provinsi terlihat jelas.

### 🔽 Filter Sidebar
- **Provinsi** — multi-select semua provinsi
- **Jenis TPA** — multi-select jenis TPA (Controlled Landfill, Open Dumping, dll.)
- **Rentang Timbulan** — slider min–max (tpd)

### 📋 Tabel Data
- Tabel lengkap data terfilter dengan tombol **Download CSV**

---

## 🎨 Kustomisasi Warna

### Warna Tema (`theme.py`)
```python
HIJAU_TUA   = "#1B5E20"   # Header, judul
HIJAU_MED   = "#388E3C"   # Elemen sekunder
HIJAU_MUDA  = "#4CAF50"   # Bar chart, aksen
HIJAU_CERAH = "#81C784"   # Palette pie/box
HIJAU_PALE  = "#C8E6C9"   # Background ringan
KUNING      = "#FDD835"   # Midpoint peta
MERAH       = "#C62828"   # Bar belum terkelola
```

### Warna Peta Choropleth (`charts.py`)
```python
# Peta Timbulan: hijau muda → kuning → hijau tua
_SCALE_TIM = [[0, HIJAU_PALE], [0.5, KUNING], [1, HIJAU_TUA]]

# Peta % Terkelola: merah → kuning → hijau
_SCALE_RYG = [[0, MERAH], [0.5, KUNING], [1, HIJAU_MED]]

# Peta % Belum Terkelola: hijau → kuning → merah
_SCALE_GYR = [[0, HIJAU_MED], [0.5, KUNING], [1, MERAH]]
```

Bisa diganti dengan nama skala bawaan Plotly:
```python
color_scale = "Greens"   # Blues, Reds, YlOrRd, RdYlGn, Viridis, dll.
```

---

## ⚠️ Catatan Data

| Kolom | Skala | Keterangan |
|---|---|---|
| `% S. Terkelola` | 0 – 1 (desimal) | Nilai `0.44` = 44% |
| `% S. Belum Terkelola` | 0 – 100 (persen) | Nilai `99.77` = 99.77% |
| `Timbulan` | ton/hari (tpd) | Bisa ada suffix `tpd` di data asli |

> Kedua kolom persentase **bukan komplemen** satu sama lain — didefinisikan secara independen dalam data sumber.

---

## 🛠️ Dependencies

```
streamlit>=1.35.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.20.0
openpyxl>=3.1.0
```

---

## 📱 Responsif Mobile

- Sidebar default **collapsed** di mobile
- KPI grid otomatis 2 kolom di layar ≤ 768px
- Font menggunakan `clamp()` untuk menyesuaikan ukuran layar
- Chart Plotly scrollable horizontal jika terlalu lebar
