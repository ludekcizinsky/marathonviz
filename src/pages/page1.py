from dash import dcc, html, Input, Output, callback
from plotly import express as px
import plotly.graph_objects as go
from utils.config import MAPBOX_TOKEN
px.set_mapbox_access_token(MAPBOX_TOKEN)  
import pandas as pd

# -------- Load data
df = pd.read_csv('data/processed/df.csv')
reduced_df = pd.read_csv('data/processed/reduced_df.csv')

# --------- Define core figures
track = go.Scattermapbox(
      mode = 'lines',
      lon = df['Lon'].tolist(),
      lat = df['Lat'].tolist(),
      hoverinfo='none',
      showlegend=False
)


# --------- Define layout
marathon_intro = dcc.Markdown(
    '''
    ## About
    This section visualizes my marathon run
    '''
)

layout = html.Div([
    marathon_intro,
    html.Br(),
    dcc.Graph(id='map'),
    html.Br(),
    dcc.Slider(
        reduced_df['Exact Distance'].min(),
        reduced_df['Exact Distance'].max(),
        step=1,
        value=reduced_df['Exact Distance'].min(),
        marks={str(km): str(km) for km in reduced_df['Exact Distance'].unique()},
        id='km-slider'
    )
], style={'width': '90vh', 'height': '90vh'})


@callback(
    Output('map', 'figure'),
    Input('km-slider', 'value'))
def update_map(selected_km):

  filtered_df = reduced_df[reduced_df['Exact Distance'] == selected_km]
  runner_position = go.Scattermapbox(
      mode = "markers",
      lon = filtered_df['Lon'].tolist(),
      lat = filtered_df['Lat'].tolist(),
      text = filtered_df['Exact Distance'].tolist(),
      marker=dict(
              color='rgb(245, 66, 66)',
              size=8,
              opacity=1
          ),
      showlegend=False,
      hovertemplate = '%{text} [km]<extra></extra>'
  )
  
  fig = go.Figure()
  fig.update_layout(
    mapbox = {
        'accesstoken': MAPBOX_TOKEN,
        'style': "dark", 'zoom': 11.5,
        'center': {'lon': 12.57, 'lat': 55.685}
    },
    margin=dict(l=0, r=0, t=0, b=0),
  ) 
  fig.add_trace(track)
  fig.add_trace(runner_position) 
  fig.update_layout(transition_duration=500)

  return fig

