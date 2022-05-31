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
layout = dbc.Container([
  
  # Row section 2
  dbc.Row([

    # Col 1
    dbc.Col([
      
      # Slider control
      dbc.Row(
        [
          dcc.Markdown(
            """
            Use the slider below to navigate through the whole
            marathon experience.
            """
          ),
          dcc.Slider(
            0,
            42,
            step=6,
            value=0,
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
            id='km-slider'
          )
        ]
      ),

      # Marathon description
      dbc.Row([
        dcc.Markdown(
        """
        The race was packed, but first three kilometers go very fast
        """,
        id='race-description'
        )
      ])

    ]),

    # Col 2
    dbc.Col([
        dcc.Graph(id='pace-overview', style={"height": "100%"})
    ],
    style={"height": "100%"}
    ),

  ],
  align="start",
  className='py-2 my-2 h-70'
  ),
   
 
  # Row section 2
  dbc.Row(
    [
    
      # Col 1
      dbc.Col([
        dcc.Graph(id='hb-overview', style={"height": "80%"})
      ],
      style={"height": "100%"}
      ),
      
      # Col 2
      dbc.Col([
        dcc.Graph(id='map', style={"height": "80%"})
      ],
      style={"height": "100%"}
      )

    ],
    className='py-2 my-2 h-20'
  )

],
style={"height": "100%"}
) # Container end


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
    yaxis=dict(autorange='reversed', color='white', title='Pace per km (min)'),
    xaxis=dict(color='white', title='# of km'),
    paper_bgcolor=section_bg,
    plot_bgcolor=section_bg,
    margin=dict(l=0.05, r=0.05, t=0.05, b=0.05),
    template='plotly_dark',
    
  )
  pace_fig.add_vrect(x0=selected_km-6, x1=selected_km, annotation_text='',
                fillcolor="#f54142", opacity=0.25, line_width=0)
  pace_fig.add_trace(pace)

  # Heartbeat
  hb_fig = go.Figure()
  hb_fig.update_layout(
    yaxis=dict(color='white', title='Average heartbeat per kilometer'),
    xaxis=dict(color='white', title='# of km'),
    paper_bgcolor=section_bg,
    plot_bgcolor=section_bg,
    margin=dict(l=0.05, r=0.05, t=0.05, b=0.05),
    template='plotly_dark',
    
  )
  hb_fig.add_vrect(x0=selected_km-6, x1=selected_km, annotation_text='',
                fillcolor="#f54142", opacity=0.25, line_width=0,
                )
  hb_fig.add_trace(hb)

  return hb_fig, pace_fig, map_fig

