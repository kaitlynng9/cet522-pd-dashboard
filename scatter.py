import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from math import ceil
import plotly_express as px
import plotly.graph_objects as go

@st.cache_resource
def get_data():
    df = pd.read_csv('merged_data/census_stops_merged_tract_grouped.csv')
    return df

def stats(dataframe):
    st.header('Data Statistics')
    st.write(dataframe.describe())

def data_header(dataframe):
    st.header('Data Header')
    st.write(dataframe.head())

def interactive_race_plot(dataframe):
    x_options = ['TractPctWhite', 'TractPctBlack', 'TractPctHispanic', 'TractPctAAPI', 'TractPctOther', 'TractPctBIPOC']
    y_options = ['StopsPctWhite', 'StopsPctBlack', 'StopsPctHispanic', 'StopsPctAAPI', 'StopsPctOther', 'StopsPctBIPOC']
    x_axis_val = st.selectbox('Select Tract % Race (x-axis)', options=x_options)
    y_axis_val = st.selectbox('Select Traffic Stops % Race (y-axis)', options=y_options)
    col = st.color_picker('Select a color for the plot', '#039A3E')

    plot = px.scatter(dataframe, x=x_axis_val, y=y_axis_val, trendline='ols',
                      trendline_color_override='white',
                      custom_data=dataframe)
    
    plot.update_traces(
        hovertemplate='<b>Point Data:</b><br>' +
                                x_axis_val + ': %{x:.3f}<br>' + y_axis_val + ': %{y:.3f}<br>' +
                               '----------------------------<br>' +
                               '<b>Census Tract Data:</b><br>' +
                               'Tract ID: %{customdata[0]}<br>' + 
                               'County: %{customdata[19]}<br>' +
                               'Population: %{customdata[20]}<br>' +
                               'Median Age: %{customdata[21]}<br>' +
                               'Median Income: $%{customdata[22]:,}/yr<br>' +
                               '<br>'
                               '% Below Poverty Line: %{customdata[23]:.3f}<br>' +
                               '% Bachelors Degree: %{customdata[24]:.3f}<br>' +
                               '% Male: %{customdata[18]:.3f}<br>' +
                               '<br>' +
                               '% White: %{customdata[12]:.3f}<br>' + 
                               '% Black: %{customdata[13]:.3f}<br>' + 
                               '% Hispanic: %{customdata[14]:.3f}<br>' + 
                               '% Asian: %{customdata[15]:.3f}<br>' + 
                               '% Other: %{customdata[16]:.3f}<br>' +
                               '% BIPOC: %{customdata[17]:.3f}<br><extra></extra>'
    )
    
    plot.update_traces(marker=dict(color=col))
    results = px.get_trendline_results(plot)
    
    # show the plot
    st.plotly_chart(plot)
    
    # show the trendline equation
    gradient = results.px_fit_results.iloc[0].params[1]
    intercept = results.px_fit_results.iloc[0].params[0]
    st.write('The equation of the trendline is:')
    st.latex(f'y = {gradient:.3f}x + {intercept:.3f}')

    if gradient <= 1.0:
        st.write('''The expected gradient for equality is 1. Since the gradient is less than 1, this suggests that the percentage of traffic stops for the selected race
                  is less than expected percentage, given the percentage of population for the selected race.''')
    else:
        st.write('''The expected gradient for equality is 1. Since the gradient is greater than 1, this suggests that the percentage of traffic stops for the selected race
                    is greater than expected percentage, given the percentage of population for the selected race.''')

def interactive_stops_plot(dataframe):
    x_options = ['TractPctWhite', 'TractPctBlack', 'TractPctHispanic', 'TractPctAAPI', 'TractPctOther', 'TractPctBIPOC']
    y_options = ['StopsPctSearched', 'StopsPctFrisked', 'StopsPctContrabandFound', 'StopsPctCitation', 'StopsPctWarning']
    x_axis_val = st.selectbox('Select Tract % Race (x-axis)', options=x_options)
    y_axis_val = st.selectbox('Select Traffic Stops % Race (y-axis)', options=y_options)
    col = st.color_picker('Select a color for the plot', '#1AA5E0')

    plot = px.scatter(dataframe, x=x_axis_val, y=y_axis_val, trendline='ols',
                      trendline_color_override='white',
                      custom_data=dataframe)
    
    plot.update_traces(
        hovertemplate='<b>Point Data:</b><br>' +
                                x_axis_val + ': %{x:.3f}<br>' + y_axis_val + ': %{y:.3f}<br>' +
                               '----------------------------<br>' +
                               '<b>Census Tract Data:</b><br>' +
                               'Tract ID: %{customdata[0]}<br>' + 
                               'County: %{customdata[19]}<br>' +
                               'Population: %{customdata[20]}<br>' +
                               'Median Age: %{customdata[21]}<br>' +
                               'Median Income: $%{customdata[22]:,}/yr<br>' +
                               '<br>'
                               '% Below Poverty Line: %{customdata[23]:.3f}<br>' +
                               '% Bachelors Degree: %{customdata[24]:.3f}<br>' +
                               '% Male: %{customdata[18]:.3f}<br>' +
                               '<br>' +
                               '% White: %{customdata[12]:.3f}<br>' + 
                               '% Black: %{customdata[13]:.3f}<br>' + 
                               '% Hispanic: %{customdata[14]:.3f}<br>' + 
                               '% Asian: %{customdata[15]:.3f}<br>' + 
                               '% Other: %{customdata[16]:.3f}<br>' +
                               '% BIPOC: %{customdata[17]:.3f}<br><extra></extra>'
    )
    
    plot.update_traces(marker=dict(color=col))
    results = px.get_trendline_results(plot)
    
    # show the plot
    st.plotly_chart(plot)
    
    # show the trendline equation
    gradient = results.px_fit_results.iloc[0].params[1]
    intercept = results.px_fit_results.iloc[0].params[0]

    st.write(f'The equation of the trendline is:')
    st.latex(f'y = {gradient:.5f}x + {intercept:.5f}')

    if gradient < 0.0:
        st.write('''The expected gradient for equality is 0. Since the gradient is negative, this suggests that the percentage of stop activity
                  reduced with the percentage of population for the selected race.''')
    elif gradient > 0.0:
        st.write('''The expected gradient for equality is 0. Since the gradient is positive, this suggests that the percentage of stop activity
                increased with the percentage of population for the selected race.''')
    else:
        st.write('The gradient is zero, which suggests that there is no relationship between the percentage of traffic stops and the percentage of population for the selected race.')

def interactive_all_plot(dataframe):
    options_list = list(dataframe.columns.values)
    options_list.remove('TractID')
    options_list.remove('geometry')
    options_list.remove('County')
    
    x_options = options_list
    y_options = options_list
    x_axis_val = st.selectbox('Select X-Axis Variable', options=x_options)
    y_axis_val = st.selectbox('Select Y-Axis Variable', options=y_options)
    col = st.color_picker('Select a color for the plot', '#E4C41C')

    plot = px.scatter(dataframe, x=x_axis_val, y=y_axis_val, trendline='ols',
                      trendline_color_override='white',
                      custom_data=dataframe)

    plot.update_traces(
         hovertemplate='<b>Point Data:</b><br>' +
                                 x_axis_val + ': %{x:.3f}<br>' + y_axis_val + ': %{y:.3f}<br>' +
                                '----------------------------<br>' +
                                '<b>Census Tract Data:</b><br>' +
                                'Tract ID: %{customdata[0]}<br>' + 
                                'County: %{customdata[19]}<br>' +
                                'Population: %{customdata[20]}<br>' +
                                'Median Age: %{customdata[21]}<br>' +
                                'Median Income: $%{customdata[22]:,}/yr<br>' +
                                '<br>'
                                '% Below Poverty Line: %{customdata[23]:.3f}<br>' +
                                '% Bachelors Degree: %{customdata[24]:.3f}<br>' +
                                '% Male: %{customdata[18]:.3f}<br>' +
                                '<br>' +
                                '% White: %{customdata[12]:.3f}<br>' + 
                                '% Black: %{customdata[13]:.3f}<br>' + 
                                '% Hispanic: %{customdata[14]:.3f}<br>' + 
                                '% Asian: %{customdata[15]:.3f}<br>' + 
                                '% Other: %{customdata[16]:.3f}<br>' +
                                '% BIPOC: %{customdata[17]:.3f}<br><extra></extra>'
    )
    
    plot.update_traces(marker=dict(color=col))
    results = px.get_trendline_results(plot)
    
    # show the plot
    st.plotly_chart(plot)
    
    # show the trendline equation
    gradient = results.px_fit_results.iloc[0].params[1]
    intercept = results.px_fit_results.iloc[0].params[0]

    st.write(f'The equation of the trendline is:')
    st.latex(f'y = {gradient:.5f}x + {intercept:.5f}')

# Page begins here
        
df = get_data()

st.title('Washington State Patrol - Traffic Stop Data')
st.text('''This page shows the traffic stop data from the Washington State Patrol. The data is
from 2015 to 2020. The data is from the Washington State Patrol and is available 
from the Stanford Open Policing Project website.''')

st.sidebar.title('Navigation')

options = st.sidebar.radio('Page Options', options=[
'Home', 
'Data Statistics', 
'Data Header', 
'Interactive Plot (by Race)',
'Interactive Plot (by Stop Activity)',
'Interactive Plot (All)'
])

if options == 'Data Statistics':
    stats(df)
elif options == 'Data Header':
    data_header(df)
elif options == 'Interactive Plot (by Race)':
    interactive_race_plot(df)
elif options == 'Interactive Plot (by Stop Activity)':
    interactive_stops_plot(df)
elif options == 'Interactive Plot (All)':
    interactive_all_plot(df)