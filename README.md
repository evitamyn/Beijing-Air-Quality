# Beijing Air Quality Analysis

Proyek ini berfokus pada analisis kualitas udara di Beijing untuk mengidentifikasi tren bulanan, pola polutan berdasarkan jam, dan faktor cuaca yang memengaruhinya. Dibangun menggunakan Python dan Streamlit, proyek ini berisi notebook analisis data dan dashboard interaktif yang menyajikan eksplorasi insight secara visual dan sistematis.

---
## 📌 Tujuan Proyek
- Menganalisis tren bulanan kosentrasi polutan PM2.5 di tiap stasiun pemantauan untuk memahami perubahan kualitas udara antar lokasi dari waktu ke waktu
- Mengidentifikasi rush hour masing-masing polutan dengan menganalisis pola konsentrasi polutan berdasarkan jam
- Menganalisis faktor cuaca yang paling berpengaruh terhadap konsentrasi polutan untuk memahami hubungan antara kondisi lingkungan dan tingkat polusi udara

---
## 📊 Dataset 
- **Ukuran** : 420.768 baris × 18 kolom
- **Deskripsi** : Dataset ini menyajikan gambaran mendalam mengenai data kualitas udara di Beijing selama periode 2013 - 2017, sehingga sangat ideal untuk eskplorasi pola dan tren kualitas udara. Data mencakup informasi waktu, konsentrasi polutan, dan variabel cuaca yang memungkinkan analisis untuk memahami dinamika kualitas udara secara lebih komprehensif.
- **Fitur:**
  - `No` : Nomor urut data pengamatan
  - `year` : Tahun pengamatan data
  - `month` : Bulan pengamatan data
  - `day` : Hari pengamatan data
  - `hour` : Jam pengamatan data dalam satu hari
  - `PM2.5` : Konsentrasi partikel halus dengan diameter maksimum 2,5 mikrometer
  - `PM10` : Konsentrasi partikel dengan diameter maksimum 10 mikrometer
  - `SO2` : Konsentrasi sulfur dioksida di udara
  - `NO2` : Konsentrasi nitrogen dioksida di udara
  - `CO` : Konsentrasi karbon monoksida di udara
  - `O3` : Konsentrasi ozon di tanah
  - `TEMP` : Suhu udara pada waktu pengukuran (°C)
  - `PRES` : Tekanan udara atmosfer yang dapat memengaruhi penyebaran polutan
  - `DEWP` : Titik embun, menunjukkan tingkat kelembapan udara dan kejenuhan uap air
  - `RAIN` : Curah hujan pada waktu pengukuran 
  - `wd` : Arah angin yang menunjukkan dari mana angin bertiup
  - `WSPM` : Kecepatan angin pada waktu pengukuran (m/s)
  - `station` : Nama stasiun pemantauan kualitas udara di Beijing
    
---
## 🛠️ Library
- **Programming** : Python
- **Data Analysis** : Pandas, Numpy
- **Visualization** : Matplotlib, Seaborn, Folium
- **Dashboard** : Streamlit
- **IDE** : Jupyter Notebook

---
## 🔎 Cara Menjalankan dengan Anaconda:
### 1. Clone Repository
```
git clone https://github.com/evitamyn/Air-Quality.git
```
### 2. Buat Environment
```
conda create --name main-ds python = 3.13.9 
conda activate main-ds
```

## 3. Install Packages
```
pip install -r requirements.txt
```

### 3. Jalankan Streamlit
```
streamlit run proyek_data_analis.py
```

---
## 🔗 Link Dashboard
https://beijing-airquality.streamlit.app/

---
## 👩‍💻 About Me
**Evita Meilinda Yudhit Nabena**   
[LinkedIn](https://www.linkedin.com/in/evitameilinda) | [GitHub](https://github.com/evitamyn)
