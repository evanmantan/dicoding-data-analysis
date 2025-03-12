import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np


def create_weekday_user(df):
    weekday_user_df = df.groupby("weekday")["cnt"].agg(["mean"]).reset_index()
    return weekday_user_df


def create_monthly_user(df):
    monthly_user_df = df.groupby("mnth")["cnt"].agg(["sum"]).reset_index()
    return monthly_user_df


def create_weather_user(df):
    weather_df = df.groupby("weathersit")["cnt"].agg(["mean"]).reset_index()
    weather_label = {
        1: "Cerah dan Sedikit Berawan",
        2: "Kabut dan Berawan",
        3: "Hujan/Salju Ringan dan Berawan",
        4: "Hujan Lebat, Badai, atau Salju",
    }
    weather_df["weathersit"] = weather_df["weathersit"].replace(weather_label)
    return weather_df


def create_hourly_user(df):
    hourly_user_df = df.groupby("hr")["cnt"].agg(["mean"]).reset_index()
    return hourly_user_df


day_df = pd.read_csv("clean_day.csv")
hour_df = pd.read_csv("clean_hour.csv")

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e0/SNice.svg")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )

selected_day_df = day_df[
    (day_df["dteday"] >= str(start_date)) & (day_df["dteday"] <= str(end_date))
]
selected_hour_df = hour_df[
    (hour_df["dteday"] >= str(start_date))
    & (hour_df["dteday"] <= str(end_date))
]

weekday_user_df = create_weekday_user(selected_day_df)
monthly_user_df = create_monthly_user(selected_day_df)
weather_user_df = create_weather_user(selected_hour_df)
hourly_user_df = create_hourly_user(selected_hour_df)

st.header("Evan's Dashboard :star:")

cols = st.columns(2)

with cols[0]:
    st.subheader("Pengguna Harian")
    fig, ax = plt.subplots(figsize=(12,5))
    sns.lineplot(x=weekday_user_df["weekday"], y=weekday_user_df["mean"], ax=ax)
    st.pyplot(fig)

with cols[1]:
    st.subheader("Pengguna Bulanan")
    fig, ax = plt.subplots(figsize=(12,5))
    sns.lineplot(x=monthly_user_df["mnth"], y=monthly_user_df["sum"], ax=ax)
    st.pyplot(fig)

st.subheader("Rata-Rata Pengguna per Jam berdasarkan Cuaca")
fig, ax = plt.subplots(figsize=(12,5))
sns.barplot(x=weather_user_df["weathersit"], y=weather_user_df["mean"], ax=ax)
ax.bar_label(ax.containers[0], label_type="edge")
ax.margins(y=0.1)
ax.set_ylabel("Rata-Rata Pengguna (orang/jam)")
ax.set_xlabel("Kategori Cuaca")
st.pyplot(fig)

st.subheader("Rata-Rata Pengguna per Jam")
fig, ax = plt.subplots(figsize=(12,5))
ax.set_xticks(np.arange(24))
ax.grid(True, axis="x")
ax.scatter(hourly_user_df["hr"], hourly_user_df["mean"])
ax.set_xlabel("Waktu (dalam satuan 24 jam)")
ax.set_ylabel("Rata-Rata Pengguna (orang/jam)")
st.pyplot(fig)
