import streamlit as st
import pandas as pd
import geopandas as gpd
import holoviews as hv
import hvplot.pandas

st.set_page_config(page_title="Power Plants", layout="wide")

# st.balloons()

st.title("Power Plants in Europe")


@st.cache
def load_powerplants():
    url = "https://raw.githubusercontent.com/PyPSA/powerplantmatching/master/powerplants.csv"
    ppl = pd.read_csv(url, index_col=0)
    geometry = gpd.points_from_xy(ppl["lon"], ppl["lat"])
    return gpd.GeoDataFrame(ppl, geometry=geometry, crs=4326)


ppl = load_powerplants()

with st.sidebar:
    st.title("Data Science for Energy System Modelling")

    st.markdown(":+1: This notebook introduces you to the `streamlit` library.")

    tech = st.selectbox(
        "Select a technology",
        ppl.Fueltype.unique(),
    )

    start, end = st.slider(
        "Range of commissioning years", 1900, 2022, (1900, 2022), step=1, help=""
    )

st.warning(":building_construction: Sorry, this page is still under construction")

df = ppl.query("Fueltype == @tech and DateIn >= @start and DateIn <= @end")

if not df.empty:
    plot = df.hvplot(
        geo=True,
        tiles="CartoLight",
        frame_height=720,
        c="DateIn",
        s=df["Capacity"] / 10,
        alpha=0.6,
        hover_cols=["Name", "Capacity", "DateIn", "DateOut"],
    ).opts(xaxis=None, yaxis=None, active_tools=["pan", "wheel_zoom"])

    st.bokeh_chart(hv.render(plot, backend="bokeh"), use_container_width=True)

else:
    st.error("Sorry, no power plants to display!")
