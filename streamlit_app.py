import streamlit as st
import plotly.express as px

import d4f_emissions.app

CONFIG_FILE = "config.json"
OWID_LINK = "https://ourworldindata.org/co2-and-other-greenhouse-gas-emissions"
app = d4f_emissions.app.App.create_from_config(CONFIG_FILE)

CHART_TYPE_TO_PLOT = {
    "Sunburst": app.plot_cumulative_sunburst,
    "Treemap": app.plot_cumulative_treemap,
}

# PAGE START
st.title("Cumulative carbon dioxide emissions")
st.markdown(
    f"""
    Interactive graphics of data regarding worldwide cumulative CO$_2$ emission. 
    Data from [Our World in Data]({OWID_LINK}).
    """
)

# USER INPUT
# Chart Type
chart_type = st.radio("Choose chart type", ["Sunburst", "Treemap"], index=0)

# Year
year = st.select_slider(
    "Select year",
    options=list(
        range(
            app.df_emissions_cum.year.min(), app.df_emissions_cum.year.max() + 1
        )
    ),
    value=2018,
)

# PLOTS
st.plotly_chart(CHART_TYPE_TO_PLOT[chart_type](year=year))
