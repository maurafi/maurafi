import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


all_df = pd.read_csv("all_monthly_trends.csv")
all_df['Year-Month'] = pd.to_datetime(all_df['Year-Month'])


datetime_columns = ['Year-Month']
all_df.sort_values(by='Year-Month', inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
  all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df['Year-Month'].min()
max_date = all_df['Year-Month'].max()
# Sidebar untuk input
with st.sidebar:
    st.image("AQ-img.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date.date(),
        max_value=max_date.date(),
        value=[min_date.date(), max_date.date()]
    )

# Konversi start_date dan end_date ke datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Fungsi filter
def filter_by_date(all_df, start_date, end_date):
    return all_df[(all_df['Year-Month'] >= start_date) & (all_df['Year-Month'] <= end_date)]

# Filter data berdasarkan input tanggal
filtered_data = filter_by_date(all_df, start_date, end_date)

# Statistik Deskriptif
st.header('Air Quality Indeks (AQI):bar_chart:')
col1, col2 = st.columns(2)
with col1:
    avg_pm25 = filtered_data['PM2.5'].mean()
    st.metric(label="Rata-rata PM2.5", value=f"{avg_pm25:.2f}")
    
with col2:
    avg_rain = filtered_data['RAIN'].mean()
    st.metric(label="Rata-rata Curah Hujan (mm)", value=f"{avg_rain:.2f}")

combined_data = filtered_data.groupby('Year-Month', as_index=False)['PM_Avg'].mean()

# Visualisasi rata-rata bulanan PM2.5 gabungan semua stasiun
st.subheader("Tren Rata-rata AQI Bulanan (Akumulasi Semua Stasiun)")
fig, ax = plt.subplots(figsize=(15, 8))
sns.lineplot(
    data=combined_data,
    x="Year-Month",
    y="PM_Avg",
    marker='o',
    color='blue',
    ax=ax
)

# Menambahkan keterangan pada grafik
ax.set_title("Tren Rata-rata PM Bulanan (Gabungan Semua Stasiun)", fontsize=16)
ax.set_xlabel("Waktu", fontsize=12)
ax.set_ylabel("Rata-rata PM", fontsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
st.pyplot(fig)

# Mengurutkan data berdasarkan waktu
filtered_data['Month'] = filtered_data['Year-Month'].dt.month

all_stations_data = filtered_data.sort_values('Year-Month')

# Visualisasi rata-rata bulanan PM2.5 untuk setiap stasiun
st.subheader("Tren PM2.5 Bulanan untuk Semua Stasiun")
fig, ax = plt.subplots(figsize=(15, 8))
sns.lineplot(
    data=all_stations_data,
    x="Year-Month",
    y="PM2.5",
    hue="station",
    marker='o',
    ax=ax
)

# Menambahkan keterangan pada grafik
ax.set_title("Tren PM2.5 Bulanan untuk Semua Stasiun", fontsize=16)
ax.set_xlabel("Waktu", fontsize=12)
ax.set_ylabel("Rata-rata PM2.5", fontsize=12)
ax.legend(title="Stasiun", bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
st.pyplot(fig)

# Visualisasi rata-rata bulanan PM2.5 untuk setiap stasiun
st.subheader("Tren PM10 Bulanan untuk Semua Stasiun")
fig, ax = plt.subplots(figsize=(15, 8))
sns.lineplot(
    data=all_stations_data,
    x="Year-Month",
    y="PM10",
    hue="station",
    marker='o',
    ax=ax
)

# Menambahkan keterangan pada grafik
ax.set_title("Tren PM10 Bulanan untuk Semua Stasiun", fontsize=16)
ax.set_xlabel("Waktu", fontsize=12)
ax.set_ylabel("Rata-rata PM10", fontsize=12)
ax.legend(title="Stasiun", bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
st.pyplot(fig)

# Menghitung rata-rata bulanan untuk setiap stasiun PM2.5
filtered_data['Month'] = filtered_data['Year-Month'].dt.month
monthly_avg_data = filtered_data.groupby(['station', 'Month'])[['PM2.5']].mean().reset_index()

# Visualisasi tren rata-rata bulanan PM2.5
st.subheader("Rata-rata Bulanan PM2.5 untuk Setiap Stasiun")
fig, ax = plt.subplots(figsize=(15, 8))
sns.lineplot(
    data=monthly_avg_data,
    x="Month",
    y="PM2.5",
    hue="station",
    marker='o',
    ax=ax
)

# Menambahkan keterangan pada grafik PM2.5
ax.set_title("Rata-rata Bulanan PM2.5 untuk Setiap Stasiun", fontsize=16)
ax.set_xlabel("Bulan", fontsize=12)
ax.set_ylabel("Rata-rata PM2.5", fontsize=12)
ax.set_xticks(range(1, 13))
ax.set_xticklabels([
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
])
ax.legend(title="Stasiun", bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
st.pyplot(fig)

# Menghitung rata-rata bulanan untuk setiap stasiun PM10
filtered_data['Month'] = filtered_data['Year-Month'].dt.month
monthly_avg_data = filtered_data.groupby(['station', 'Month'])[['PM10']].mean().reset_index()

# Visualisasi tren rata-rata bulanan PM10
st.subheader("Rata-rata Bulanan PM10 untuk Setiap Stasiun")
fig, ax = plt.subplots(figsize=(15, 8))
sns.lineplot(
    data=monthly_avg_data,
    x="Month",
    y="PM10",
    hue="station",
    marker='o',
    ax=ax
)

# Menambahkan keterangan pada grafik PM10
ax.set_title("Rata-rata Bulanan PM10 untuk Setiap Stasiun", fontsize=16)
ax.set_xlabel("Bulan", fontsize=12)
ax.set_ylabel("Rata-rata PM10", fontsize=12)
ax.set_xticks(range(1, 13))
ax.set_xticklabels([
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
])
ax.legend(title="Stasiun", bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
st.pyplot(fig)


# Ranking Stasiun
st.subheader("Stasiun dengan Air Quality Terburuk (PM2.5)")
if not filtered_data.empty:
    station_ranking = (
        filtered_data.groupby('station')['PM2.5']
        .mean()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={'PM2.5': 'Average PM2.5'})
    )
    station_ranking['Rank'] = station_ranking['Average PM2.5'].rank(ascending=False).astype(int)
    #st.dataframe(station_ranking)

    # Visualisasi Ranking
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(
        x='Average PM2.5',
        y='station',
        data=station_ranking,
        palette='viridis',
        ax=ax
    )
    ax.set_title("Ranking Stasiun Berdasarkan Rata-rata PM2.5")
    st.pyplot(fig)
else:
    st.write("Data tidak tersedia untuk rentang tanggal yang dipilih.")

# Analisis Korelasi
st.subheader("Korelasi Curah Hujan dengan Air Quality")
if 'RAIN' in filtered_data.columns:
    correlation = filtered_data[['PM2.5', 'RAIN']].corr()
    st.write("Matriks Korelasi:")
    #st.write(correlation)
    st.dataframe(correlation.style.format("{:.2f}"), use_container_width=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(
        data=filtered_data,  # Menggunakan data yang sudah difilter
        x='RAIN',
        y='PM2.5',
        scatter_kws={'alpha': 0.6, 'edgecolor': 'k'},
        line_kws={'color': 'red'},
        ax=ax
    )

    # Menambahkan keterangan pada grafik
    ax.set_title("Korelasi antara RAIN dan PM2.5", fontsize=14)
    ax.set_xlabel("Curah Hujan (RAIN)", fontsize=12)
    ax.set_ylabel("PM2.5", fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    # Heatmap Korelasi
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)
else:
    st.write("Tidak ada data parameter tambahan untuk korelasi.")
