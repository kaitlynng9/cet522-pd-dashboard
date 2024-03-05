import branca
import folium
import geopandas as gpd
import pandas as pd
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

demographic_var = "PctBlack"

colormap = branca.colormap.LinearColormap(
    vmin=census_gdf[demographic_var].quantile(0.0),
    vmax=census_gdf[demographic_var].quantile(1),
    colors=["white", "red"],
    caption=demographic_var
)

m = folium.Map(location=[47.751, -120.740], zoom_start=10)

popup = GeoJsonPopup(
    fields=["TractID", demographic_var],
    aliases=["Tract", demographic_var],
    localize=True,
    labels=True,
    style="background-color: yellow;",
)

tooltip = GeoJsonTooltip(
    fields=["TractID", demographic_var],
    aliases=["Tract", demographic_var],
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

folium.GeoJson(
    census_gdf,
    style_function=lambda x: {
        "fillColor": colormap(x["properties"][demographic_var])
        if x["properties"][demographic_var] is not None
        else "transparent",
        "color": "black",
        "fillOpacity": 0.4,
    },
    # tooltip=tooltip,
    popup=popup,
).add_to(m)

tooltip_stop = GeoJsonTooltip(
    fields=['subject_age', 'subject_race', 'subject_sex', 'citation_issued', 'warning_issued', 'outcome', 'contraband_found', 'frisk_performed', 'search_conducted'],
    aliases=['Subject Age', 'Subject Race', 'Subject Sex', 'Citation Issued', 'Warning Issued','Outcome', 'Contraband Found', 'Frisk Performed', 'Search Conducted'],
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
    columns=["TractID",demographic_var],
    tooltip=tooltip_stop).add_to(m)



colormap.add_to(m)

output = st_folium(m, width=700, height=500)