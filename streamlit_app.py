import streamlit as st
import plotly.express as px

from d4f_emissions.data import df_co2_cumulative_with_continents

fig = px.sunburst(
    df_co2_cumulative_with_continents.dropna(),
    path=["continent", "country_german"],
    values="cumulative_emissions",
)

st.plotly_chart(fig)