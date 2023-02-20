import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Power Plants", layout="wide")

# st.balloons()

st.title("Power Plants in Europe")


@st.cache_data
def load_powerplants():
    url = "https://raw.githubusercontent.com/PyPSA/powerplantmatching/master/powerplants.csv"
    return pd.read_csv(url, index_col=0)

ppl = load_powerplants()

with st.sidebar:
    st.title("Data Science for Energy System Modelling")

    st.markdown(":+1: This notebook introduces you to the `streamlit` library.")

    tech = st.selectbox(
        "Select a technology",
        ppl.Fueltype.unique(),
    )

    start, end = st.slider(
        "Range of commissioning years", 1900, 2022, (1900, 2022), step=1, help="Pick years!"
    )

st.warning(":building_construction: Sorry, this page is still under construction")

hover_data = ['Name', 'Fueltype', 'Technology', "Capacity", 'Efficiency', 'DateIn']

df = ppl.query("Fueltype == @tech and DateIn >= @start and DateIn <= @end")

if not df.empty:
    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        mapbox_style="carto-positron",
        color="DateIn",
        size="Capacity",
        zoom=2,
        height=700,
        hover_data=hover_data,
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("Sorry, no power plants to display!")
