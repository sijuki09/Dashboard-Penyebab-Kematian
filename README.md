# Dashboard Visualisasi Penyebab Kematian di Indonesia

> Dashboard interaktif yang memvisualisasikan data tren dan penyebab kematian di Indonesia berdasarkan data resmi Profil Kesehatan Kementerian Kesehatan RI tahun 2000–2021.

## Isi Dashboard
- **Chart 1: Tren Kematian Tahunan (Line Chart)** - Menampilkan pergerakan total kematian dari tahun ke tahun secara keseluruhan maupun terbagi berdasarkan kategori (Penyakit & Bencana Non-Alam, Bencana Alam, dan Bencana Sosial).
- **Chart 2: Proporsi Kategori Kematian (Doughnut Chart)** - Menampilkan persentase perbandingan antara kategori penyebab kematian di Indonesia.
- **Chart 3: 10 Penyebab Kematian Terbesar (Horizontal Bar Chart)** - Peringkat 10 penyebab kematian spesifik dengan korban terbanyak berdasarkan filter yang sedang aktif.
- **Fitur Interaktif**: 
  - *Filter Dropdown Tipe*: Memilih kategori tertentu (Penyakit, Bencana Alam, Bencana Sosial) untuk memperbarui semua chart secara instan.
  - *Pencarian Tekstual*: Menyaring data penyebab kematian berdasarkan ketikan pengguna.
  - *Slider Rentang Tahun*: Membatasi visualisasi hingga tahun tertentu secara dinamis.
  - *Legend Toggle*: Klik legend pada Line Chart untuk menyembunyikan/menampilkan grafik per tipe.
  - *Interactive Tooltips*: Menampilkan angka detail riil saat hover di atas grafik Chart.js.
  - *Tabel Rincian Paginated*: Menampilkan tabel baris data riil dengan pagination responsif.
- **Animasi**:
  - *Entrance Chart.js Animation*: Chart dimuat dengan animasi transisi bawaan.
  - *Count-up Number*: Angka KPI (Total Kematian) berhitung naik dari 0 ke nilai akhir saat halaman dibuka atau saat filter berubah.
  - *CSS Fade-in*: Seluruh dashboard dimuat secara estetik menggunakan animasi fade-in `@keyframes`.

## Sumber Data
- **Nama dataset**: Causes of Death in Indonesia (2000 - 2021) oleh Hendratno.
- **URL sumber**: [Kaggle - Causes of Death in Indonesia](https://www.kaggle.com/datasets/hendratno/cause-of-death-in-indonesia) yang dikompilasi dari Laporan Buku Profil Kesehatan Indonesia (Kemenkes RI).

## Cara Jalankan di Lokal

### Jalur A (Static - Paling Cepat):
1. Buka file [index.html](file:/index.html) langsung di web browser pilihan Anda (Google Chrome, Firefox, Safari, Edge).
2. Atau klik kanan pada `index.html` dan pilih **Open with Live Server** di VS Code untuk reload otomatis.

### Jalur B (Server - Menggunakan Static Server):
Jika ingin menjalankan dalam mode server lokal sederhana:
```bash
npm install -g serve
serve .
```
Buka `http://localhost:3000` di browser Anda.

## Teknologi
- **Chart.js** (Visualisasi data interaktif via CDN)
- **HTML5 & CSS3** (Tata letak grid responsif, variabel CSS, dan glassmorphic UI)
- **Vanilla JavaScript** (State filter, pengolahan agregasi data, dan animasi count-up)