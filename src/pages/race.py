from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from plotly import express as px
import plotly.graph_objects as go
from utils.config import MAPBOX_TOKEN
px.set_mapbox_access_token(MAPBOX_TOKEN)  
import pandas as pd

# -------- Load data
df = pd.read_csv('data/processed/df.csv')
reduced_df = pd.read_csv('data/processed/reduced_df.csv')
merged = pd.read_csv('data/processed/merged.csv')


# --------- Define initial figures
# Pace
pace = go.Scatter(
    x = merged['Exact Distance'],
    y = (merged['elapsed_time']/60).round(2),
    mode='lines+markers'
)

# Heartbeat
hb = go.Scatter(
    x = merged['Exact Distance'],
    y = merged['average_heartrate'],
    mode='lines+markers'
)

# Map
track = go.Scattermapbox(
      mode = 'lines',
      lon = df['Lon'].tolist(),
      lat = df['Lat'].tolist(),
      hoverinfo='none',
      showlegend=False
)


# --------- Page layout

# Instructions
instructions = dbc.Row(
    [
    dbc.Col(
      html.Div("Use the slider below to navigate through the whole marathon experience."),
      width=12, className='h-100 text-light', style={'text-align': 'center'})
    ],
    className='h-10 pb-2',
    justify='center'
)

# Slider control
marks = {i: {'label': f'{i} km'} for i in range(0, 43, 6)}
marks[42] = {'label': '42 km', 'style': {'text-indent':'-3.02em'}}
marks[0] = {'label': '0 km', 'style': {'text-indent':'1.95em'}}
slider = dbc.Row(
    [
    dbc.Col(
      [
        dcc.Slider(
          0,
          42,
          step=6,
          value=0,
          marks=marks,
          tooltip=None,
          id='km-slider',
          className='h-100'
          )
      ],
      className='h-100',
      width=12
    )
    ],
    justify='center',
    className='h-25'
)

# First row of graphs
row1 = dbc.Row(
    children=[
        dbc.Col(
            width=6,
            children=[instructions, slider],
            className="h-100",
        ),
        dbc.Col(
            width=6,
            children=[dcc.Graph(id="pace-overview", className="h-100")],
            className="h-100",
        ),
    ],
    className="h-50 py-2",
)


# Second row of graphs
row2 = dbc.Row(
    children=[
        dbc.Col(
            width=6,
            children=[dcc.Graph(id="hb-overview", className="h-100")],
            className="h-100",
        ),
        dbc.Col(
            width=6,
            children=[dcc.Graph(id="map", className="h-100")],
            className="h-100",
        ),
    ],
    className="h-50 pt-2 pb-4",
)


layout = dbc.Container([row1, row2], className="h-100")

# -------- Callbacks
@callback([
    Output('hb-overview', 'figure'),
    Output('pace-overview', 'figure'),
    Output('map', 'figure')],
    Input('km-slider', 'value'))
def update_visuals(selected_km):

  # Global vars
  section_bg = 'rgba(22,22,23,1)'
  
  # Map
  # Overall progress
  filtered_df = df[df['distance [m]'] <= selected_km*1000]
  overall_progress = go.Scattermapbox(
      mode = "lines",
      lon = filtered_df['Lon'].tolist(),
      lat = filtered_df['Lat'].tolist(), 
      showlegend=False,
      hoverinfo='none',
      line=dict(color="#f54142")
  )
  
  # Particular position
  filtered_df = reduced_df[reduced_df['Exact Distance'] == selected_km]
  runner_position = go.Scattermapbox(
      mode = "markers",
      lon = filtered_df['Lon'].tolist(),
      lat = filtered_df['Lat'].tolist(),
      text = filtered_df['Exact Distance'].tolist(),
      marker=dict(
              color='rgb(245, 66, 66)',
              size=12,
              opacity=.8
          ),
      showlegend=False,
      hovertemplate = '%{text} [km]<extra></extra>'
  )

  map_fig = go.Figure()
  map_fig.update_layout(
    mapbox = {
        'accesstoken': MAPBOX_TOKEN,
        'style': "dark", 'zoom': 11.5,
        'center': {'lon': 12.57, 'lat': 55.685}
    },
    paper_bgcolor=section_bg,
    plot_bgcolor=section_bg,
    margin=dict(l=0.05, r=0.05, t=0.05, b=0.05),
    
  ) 
  map_fig.add_trace(track)
  map_fig.add_trace(runner_position)
  map_fig.add_trace(overall_progress)

  # Pace
  pace_fig = go.Figure()
  pace_fig.update_layout(
    yaxis=dict(autorange='reversed', color='white', title='Pace per km (min)', automargin=True),
    xaxis=dict(color='white', title='# of km', automargin=True),
    paper_bgcolor=section_bg,
    plot_bgcolor=section_bg,
    margin=dict(l=0.05, r=0.05, t=0.05, b=0.05),
    template='plotly_dark' 
  )
  pace_fig.add_vrect(x0=0, x1=selected_km, annotation_text='',
                fillcolor="#f54142", opacity=0.25, line_width=0)
  pace_fig.add_trace(pace)

  # Heartbeat
  hb_fig = go.Figure()
  hb_fig.update_layout(
    yaxis=dict(color='white', title='Average heartbeat per kilometer', automargin=True),
    xaxis=dict(color='white', title='# of km', automargin=True),
    paper_bgcolor=section_bg,
    plot_bgcolor=section_bg,
    margin=dict(l=0.15, r=0.05, t=0.05, b=0.05),
    template='plotly_dark',
    
  )
  hb_fig.add_vrect(x0=0, x1=selected_km, annotation_text='',
                fillcolor="#f54142", opacity=0.25, line_width=0,
                )
  hb_fig.add_trace(hb)

  return hb_fig, pace_fig, map_fig

