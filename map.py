import branca
import folium
import geopandas as gpd
import pandas as pd
import requests
import streamlit as st
from folium.features import GeoJsonPopup, GeoJsonTooltip

from streamlit_folium import st_folium

@st.cache_resource
def get_data():
    census_data =  gpd.read_file("/Users/kaitlynng/Desktop/UW/cet522/final_proj/cet522-pd-dashboard/data/census_data_wa_2018.geojson")
    stop_data = gpd.read_file("/Users/kaitlynng/Desktop/UW/cet522/final_proj/cet522-pd-dashboard/data/wa_stp_stops_tracts_2018.geojson")
    stop_data['date_time'] = stop_data['date_time'].astype(str)
    return census_data, stop_data

census_gdf, stop_gdf = get_data()

# colormap = branca.colormap.LinearColormap(
#     vmin=df["change"].quantile(0.0),
#     vmax=df["change"].quantile(1),
#     colors=["red", "orange", "lightblue", "green", "darkgreen"],
#     caption="State Level Median County Household Income (%)",
# )

m = folium.Map(location=[47.751, -120.740], zoom_start=10)

popup = GeoJsonPopup(
    fields=["TractID", "PctBlack"],
    aliases=["Tract", "% Black"],
    localize=True,
    labels=True,
    style="background-color: yellow;",
)

tooltip = GeoJsonTooltip(
    fields=["TractID", "PctBlack"],
    aliases=["Tract", "% Black"],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
    max_width=800,
)

folium.Choropleth(
    geo_data=census_gdf,
    name="Census Data",
    data=census_gdf,
    columns=["TractID", "PctBlack"],
    key_on="feature.properties.TractID",
    tooltip=tooltip,
    popup=popup
).add_to(m)

tooltip_stop = GeoJsonTooltip(
    fields=["subject_race"],
    aliases=["subject_race"],
    localize=True,
    sticky=False,
    labels=True,
    style="""
    background-color: #F0EFEF;
    border: 2px solid black;
    border-radius: 3px;
    box-shadow: 3px;
    """,
)

folium.GeoJson(
    stop_gdf.head(100),
    columns=["TractID","subject_race"],
    tooltip=tooltip_stop).add_to(m)



# colormap.add_to(m)

output = st_folium(m, width=700, height=500)