import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import folium
from streamlit_folium import st_folium
from babel.numbers import format_currency

st.set_page_config(page_title="Beijing Air Quality Dashboard", layout='wide')
sns.set_theme(style='dark')
plt.rcParams["axes.spines.top"] = True
plt.rcParams["axes.spines.right"] = True

df_clean = pd.read_csv("data_clean.csv")
df_clean['datetime'] = pd.to_datetime(df_clean['datetime'])
Winter = [12,1,2]
Spring = [3,4,5]
Summer = [6,7,8]
Autumn = [9,10,11]
df_clean['season'] = df_clean['month'].apply(lambda m: 'Winter' if m in Winter 
                                 else ('Spring' if m in Spring 
                                 else ('Summer' if m in Summer 
                                 else 'Autumn')))
df_clean['waktu'] = df_clean['hour'].apply(lambda h: 'Rush Hour' if (7 <= h <= 9 or 17 <= h <= 19) 
                                   else ('Non Rush Hour'))

#Sidebar
with st.sidebar:
    st.image("image.png", width = 200)
    st.markdown("## Filter Data")
    min_date = df_clean["datetime"].min()
    max_date = df_clean['datetime'].max()
    dates = st.date_input(label='Rentang Waktu', 
                                         min_value = min_date,
                                         max_value = max_date,
                                         value =[min_date, max_date])
    
    years = st.multiselect("Tahun",
                           options=sorted(df_clean['year'].unique()),
                           default=sorted(df_clean['year'].unique()))
   
    hours = st.slider("Rentang Jam",
                      min_value=0,
                      max_value=23,
                      value=(0,23))
     
    seasons = st.multiselect("Musim:",
                             options=df_clean['season'].unique(),
                             default=[])
    
    stations = st.multiselect("Stasiun",
                              options=sorted(df_clean['station'].unique()),
                              default=[])

    polutan_list = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    polutan = st.multiselect('Polutan', 
                             options = polutan_list,
                             default = [])
    
#filter data
df = df_clean.copy()
if len(stations) > 0:
   df = df[df['station'].isin(stations)]
df = df[(df['datetime'].dt.date >= dates[0]) &
        (df['datetime'].dt.date <= dates[1]) &
        (df['hour'] >= hours[0]) &
        (df['hour'] <= hours[1])]
if len(seasons) > 0:
    df=df[df['season'].isin(seasons)]

if len(stations) > 0:
   monthly_mean_pm25 = df.groupby(['month', 'station'])['PM2.5'].mean().reset_index()
   filter_monthly_mean_pm25 = monthly_mean_pm25[monthly_mean_pm25['station'].isin(stations)]

st.markdown("""
# 🌬️Beijing Air Quality Dashboard)
### Visualisasi Analisis Kualitas Udara di Beijing (2013–2017)
""")
st.markdown("---")  

#Metrics
konsentrasi = {
    "PM2.5": [
        (0, 35, 0, 50),
        (35, 75, 51, 100),
        (75, 115, 101, 150),
        (115, 150, 151, 200),
        (150, 250, 201, 300),
        (250, 500, 301, 500)],
    
    "PM10": [
        (0, 50, 0, 50),
        (50, 150, 51, 100),
        (150, 250, 101, 150),
        (250, 350, 151, 200),
        (350, 420, 201, 300),
        (420, 600, 301, 500)],
    
    "SO2": [
        (0, 150, 0, 50),
        (150, 500, 51, 100),
        (500, 650, 101, 150),
        (650, 800, 151, 200),
        (800, 1600, 201, 300),
        (1600, 2100, 301, 500)],
    
    "NO2": [
        (0, 40, 0, 50),
        (40, 80, 51, 100),
        (80, 180, 101, 150),
        (180, 280, 151, 200),
        (280, 565, 201, 300),
        (565, 940, 301, 500)],
    
    "CO": [
        (0, 2000, 0, 50),
        (2000, 4000, 51, 100),
        (4000, 14000, 101, 150),
        (14000, 24000, 151, 200),
        (24000, 36000, 201, 300),
        (36000, 60000, 301, 500)],
    
    "O3": [
        (0, 100, 0, 50),
        (100, 160, 51, 100),
        (160, 215, 101, 150),
        (215, 265, 151, 200),
        (265, 800, 201, 300),
        (800, 1000, 301, 500)]}

def hitung_iaqi(conc, konsentrasi_list):
  for low, high, i_low, i_high in konsentrasi_list:
    if low <= conc <= high:
      return ((i_high - i_low)/(high - low)) * (conc-low) + i_low
  return None
  
for pol in konsentrasi.keys():
  df[f'IAQI_{pol}'] = df[pol].apply(lambda x: hitung_iaqi(x,konsentrasi[pol]))

aqi_col = [f'IAQI_{p}' for p in konsentrasi.keys()]
df['AQI'] = df[aqi_col].max(axis=1)
df['AQI_Dominant'] = df[aqi_col].idxmax(axis=1)

col1, col2, col3, col4 = st.columns(4)
with col1:
   total_stasiun = df['station'].nunique()
   st.metric("Jumlah Stasiun", f"{total_stasiun} Stasiun")
with col2:
   total_data = len(df)
   st.metric("Jumlah Observasi Data", f"{total_data} Data")
with col3:
   avg_aqi = round(df['AQI'].mean(), 1)
   st.metric("Rata-Rata AQI", f"{avg_aqi:.2f} µg/m³")
with col4:
   max_aqi = round(df['AQI'].max(), 1)
   st.metric("AQI Tertinggi", f"{max_aqi:.2f} µg/m³")

#Peta
st.markdown("""
---
## Peta AQI per Stasiun di Beijing
###### Note: Pilih stasiun yang ingin dilihat melalui filter di sidebar

##### Menampilkan peta sebaran kualitas udara (AQI) di 12 stasiun pemantauan Beijing menggunakan indikator warna berdasarkan standar AQI Beijing:
- 🟢Hijau : Baik (0 - 50)
- 🟡Kuning : Sedang (51 - 100)
- 🟠Oranye : Tidak Sehat bagi Kelompok Sensitif (101 - 150)
- 🔴Merah : Tidak Sehat (151 - 200)
- 🟣Ungu : Sangat Tidak Sehat (201 - 300)
- 🟤Maroon : Berbahaya (300+)""")

station_locations = pd.DataFrame({
    'station': ['Aotizhongxin', 'Changping', 'Dingling',
                'Dongsi', 'Guanyuan','Gucheng',
                'Huairou', 'Nongzhanguan', 'Shunyi',
                'Tiantan', 'Wanliu', 'Wanshouxigong'],
    'latitude': [39.9826, 40.2181, 40.2904,
                 39.9289, 39.9295, 39.9145,
                 40.3749, 39.9375, 40.1270,
                 39.8731, 39.9996, 39.8949],
    'longitude': [116.3970, 116.2317, 116.2302,
                  116.4177, 116.3393, 116.1853,
                  116.6371, 116.4708, 116.6545,
                  116.4123, 116.2785, 116.3466]})

df = df.merge(station_locations, on='station', how='left')

aqi_final = df.groupby('station', as_index=False).agg(
    AQI=('AQI', 'mean'),
    latitude=('latitude', 'first'),
    longitude=('longitude', 'first')
)

def kategori_warna(aqi):
  if aqi <= 50: return 'Baik', 'Green'
  elif aqi <= 100: return 'Sedang', 'Yellow'
  elif aqi <= 150: return 'Tidak Sehat bagi Kelompok Sensitif', 'Orange'
  elif aqi <= 200: return 'Tidak Sehat', 'Red'
  elif aqi <= 300: return 'Sangat Tidak Sehat', 'Purple'
  else: return 'Berbahaya', 'Maroon'

aqi_final['kategori'], aqi_final['warna']=zip(*aqi_final['AQI'].apply(kategori_warna))

map = folium.Map(location=[aqi_final.latitude.mean(), aqi_final.longitude.mean()], zoom_start=12, control_scale=True)

for index, station_info in aqi_final.iterrows():
    folium.CircleMarker(
        location=[station_info['latitude'], station_info['longitude']],
        radius=8,
        color=station_info['warna'],  
        fill=True,
        fill_color=station_info['warna'],
        fill_opacity=0.7,
        popup=f"{station_info['station']}\n {station_info['kategori']}\nAQI: {station_info['AQI']:.1f}"
    ).add_to(map)

st_folium(map, width=800, height=500)

# 1. Tren Bulanan
st.markdown("""
---
## Tren Bulanan Polutan PM2.5
###### Note: Pilih stasiun yang ingin dilihat melalui filter di sidebar""")
label_bulan = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
monthly_mean_pm25 = df.groupby(['month', 'station'])['PM2.5'].mean().reset_index()
filter_monthly_mean_pm25 = monthly_mean_pm25[monthly_mean_pm25['station'].isin(stations)]

for nama_stasiun in filter_monthly_mean_pm25['station'].unique():
    data_stasiun = filter_monthly_mean_pm25[filter_monthly_mean_pm25['station'] == nama_stasiun]

    plt.figure(figsize=(10,5))
    sns.lineplot(data=data_stasiun, x='month', y='PM2.5', marker='o', color='steelblue', linewidth=2)

    plt.title(f'Tren Bulanan Rata-rata PM2.5 di stasiun {nama_stasiun}', fontsize=14, weight='bold')
    plt.xlabel('Bulan', fontsize=12)
    plt.ylabel('PM2.5 (µg/m³)', fontsize=12)
    plt.xticks(ticks=range(1, 13), labels=label_bulan)

    max_pm25 = data_stasiun['PM2.5'].max()
    if not pd.isna(max_pm25):
        plt.ylim(0, max_pm25 * 1.1)

    for idx, row in data_stasiun.iterrows():
        if not pd.isna(row['PM2.5']):
            plt.text(row['month'], row['PM2.5'] + (max_pm25 * 0.03),
                     f"{row['PM2.5']:.1f}", ha='center', va='bottom', fontsize=9, color='black')
            
    sns.despine(trim=True)
    plt.grid(visible=True, which='major', axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()

    st.pyplot(plt.gcf(), use_container_width=False)

# 2. Rush Hour
st.markdown("""
---
## Rush Hour tiap Polutan
###### Note: Pilih polutan yang ingin dilihat melalui filter di sidebar""")

for p in polutan:
   plt.figure(figsize=(5,5))
   
   sns.boxplot(
        data=df,
        x='waktu', y=p,
        hue='waktu',
        palette=['#4A90E2', '#4A90E2'],
        legend=False
    )
   plt.title(f'{p}: Rush Hour vs Non Rush Hour', fontsize=12, weight='bold')
   plt.xlabel('Periode Waktu', fontsize=10)
   plt.ylabel('{polutan} (µg/m³)', fontsize=10)
   plt.grid(axis='y', linestyle='--', alpha=0.7)
   plt.ylim(0, df[p].max() + 10)
   
   st.pyplot(plt.gcf(), use_container_width=False)

# 3. Korelasi
st.markdown("""
---
## Korelasi Faktor Cuaca dengan Polutan""")
polutan = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
cuaca = ['TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
correlation = df[polutan + cuaca].corr()

plt.figure(figsize=(10, 5))
sns.heatmap(correlation,
               annot=True,
               cmap='coolwarm',
               fmt=".2f",
               vmin=-1,
               vmax=1)
st.pyplot(plt.gcf())

#===Footer===
st.markdown("---")
st.caption("Data: Kualitas Udara Beijing (2013-2017)")



