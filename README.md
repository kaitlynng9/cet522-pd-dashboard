# cet522-pd-dashboard

Cleaned data:
- `data/census_data_wa_2018.geojson`: has census tract shapefile polygon geometries, along with deomgraphic data for each tract
- `wa_stp_stops_tracts_2018.geojson`: has WA State Polic stop point geometries (lat/lon) along with stop data 
- Note: The two datasets can be joined on `TractID`
- Note: only 2018 WA data was processed due to large file sizes (for all years, all PDs)


To read in data:

`census_gdf = gpd.read_file("data/census_data_wa_2018.geojson")`  

`stops_gdf = gpd.read_file("data/wa_stp_stops_tracts_2018.geojson")`

  
