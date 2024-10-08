import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Air Quality Data Analysis")
st.write("This app provides an analysis of air quality data from different stations with filtering options for pollutants and stations.")

changping_df = pd.read_csv("data/Changping.csv")
shunyi_df = pd.read_csv("data/Shunyi.csv")

pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
station = st.selectbox("Select Station", ["Changping", "Shunyi"])

if station == "Changping":
    df = changping_df
else:
    df = shunyi_df

selected_pollutants = st.multiselect("Select Pollutants", pollutants, default=pollutants)

if selected_pollutants:

    st.write(f"Showing data for {station} station:")
    st.dataframe(df[selected_pollutants].head())

    st.write("## Pollutant Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    df[selected_pollutants].hist(ax=ax, bins=20, figsize=(15, 10))
    plt.suptitle(f'{station} - Pollutant Distribution')
    st.pyplot(fig)

    st.write("## Correlation Between Pollutants")
    corr = df[selected_pollutants].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
    ax.set_title(f'{station} - Correlation Between Pollutants')
    st.pyplot(fig)

    st.write("## Seasonal Variations in Air Pollutant Concentrations")
    seasonal_pollutants = df.groupby('month')[selected_pollutants].mean()
    fig, ax = plt.subplots(figsize=(15, 7))
    seasonal_pollutants.plot(kind='bar', ax=ax)
    ax.set_xlabel('Month')
    ax.set_ylabel('Mean Concentration (µg/m³)')
    ax.set_title(f'{station} - Seasonal Variations in Air Pollutant Concentrations')
    plt.xticks(rotation=0)
    st.pyplot(fig)

    if station == "Changping":
        mean_pollutants_changping = changping_df[selected_pollutants].mean()
        mean_pollutants_shunyi = shunyi_df[selected_pollutants].mean()

        st.write("## Comparison of Mean Pollutant Levels Between Changping and Shunyi")
        comparison_df = pd.DataFrame({
            'Changping': mean_pollutants_changping,
            'Shunyi': mean_pollutants_shunyi
        })
        fig, ax = plt.subplots(figsize=(15, 7))
        comparison_df.plot(kind='bar', ax=ax)
        ax.set_title('Comparison of Mean Air Pollutant Levels Between Changping and Shunyi')
        ax.set_ylabel('Mean Concentration (µg/m³)')
        plt.xticks(rotation=45)
        st.pyplot(fig)
else:
    st.write("Please select at least one pollutant to visualize the data.")
