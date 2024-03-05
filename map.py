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

# folium.GeoJson(
#     df,
#     style_function=lambda x: {
#         "fillColor": colormap(x["properties"]["change"])
#         if x["properties"]["change"] is not None
#         else "transparent",
#         "color": "black",
#         "fillOpacity": 0.4,
#     },
#     tooltip=tooltip,
#     popup=popup,
# ).add_to(m)

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

# left, right = st.columns(2)
# with left:
#     st.write("## Tooltip")
#     st.write(output["last_object_clicked_tooltip"])
# with right:
#     st.write("## Popup")
#     st.write(output["last_object_clicked_popup"])

# st.divider()

#############################################
# st.markdown("""## `GeoPandas`
# GeoPandas and streamlit do not interact perfectly for polygons and lines. 
# However, we can extract X / Y point data from GeoDataFrames and plot simply. To do so, creat a `lat` and `long` column. To do so, I will read a shapefile from lecture 13 and assign two new columns:
# ```python
# df = gpd.read_file("zip://./geopandas-tutorial/data/ne_110m_populated_places.zip", engine="pyogrio")

# df['lon'] = df.geometry.x  # extract longitude from geometry
# df['lat'] = df.geometry.y  # extract latitude from geometry
# df = df[['lon','lat']]     # only keep longitude and latitude
# st.write(df.head())        # show on table for testing only
# st.map(df) 
# ```
# """)

# df = gpd.read_file("zip://./geopandas-tutorial/data/ne_110m_populated_places.zip", engine="pyogrio")

# df['lon'] = df.geometry.x 
# df['lat'] = df.geometry.y 
# df = df[['lon','lat']]     
# st.write(df.head())  
# st.map(df) 