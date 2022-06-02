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
target = pd.read_csv('data/processed/run_plan.csv')


# -------  Config for all charts
config={'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'toImage',
                                  'zoom2d', 'select2d','autoScale2d']}

# Colors for statuses
easy = '#48e090'
middle = '#fce26c'
hard = '#f67c7c'

# Main colors
primary = '#636efa'


# --------- Define initial figures
merged['time [s]'] = pd.to_timedelta(merged['elapsed_time'], unit='s')
merged['time [s]'] = merged['time [s]'] + pd.to_datetime('1970/01/01')

target['time [s]'] = pd.to_timedelta(target['time [s]'], unit='s')
target['time [s]'] = target['time [s]'] + pd.to_datetime('1970/01/01')

# Pace
pace = go.Scatter(
    x = merged['Exact Distance'],
    y = merged['time [s]'],
    mode='lines+markers',
    showlegend=False,
    name='Actual pace'
)

# Target pace
target_pace = go.Scatter(
  x = target['km'],
  y = target['time [s]'],
  mode='lines',
  showlegend=False,
  line=dict(color='#5c5b5b'),
  name='Planned pace'
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
      width=12, className='h-100 text-light slider-desc', style={'text-align': 'center'})
    ],
    className='h-10 mb-2',
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
    className='h-10 mt-2 mb-3',
    align='center'
)

# Color explanation
badges = html.Div(html.Span(
    [
        html.Span("Feeling good", className="badge responsive-badges me-2 text-muted", style={'background-color': easy}),
        html.Span("Can barely talk", className="badge responsive-badges me-2 text-muted", style={'background-color': middle}),
        html.Span("Hard", className="badge responsive-badges me-2 text-muted", style={'background-color': hard})
    ]
  ),
  className='text-center'
)

color_info = dbc.Row(
    [
      dbc.Col(
      [badges],
      className='h-100',
      width = 12
      ) 

    ],
    className='h-10 my-2',
    align='center',
    justify='center'
)

# Description of the phase
description = dbc.Row(
    [
    dbc.Col(id='description-content', width=12, className='h-100 text-light')
    ],
    className='h-60',
    justify='center'
)


# First row of graphs
row1 = dbc.Row(
    children=[
        dbc.Col(
            width=6,
            children=[instructions, slider, color_info, description],
            className="h-100",
        ),
        dbc.Col(
            width=6,
            children=[dcc.Graph(id="pace-overview", className="h-100",
                      config=config)],
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
            children=[dcc.Graph(id="hb-overview", className="h-100",
                      config=config)],
            className="h-100",
        ),
        dbc.Col(
            width=6,
            children=[dcc.Graph(id="map", className="h-100",
                      config=config)],
            className="h-100",
        ),
    ],
    className="h-50 pt-2",
)


layout = dbc.Container([row1, row2], className="h-90")

# -------- Callbacks
@callback([
    Output('description-content', 'children'),
    Output('hb-overview', 'figure'),
    Output('pace-overview', 'figure'),
    Output('map', 'figure')],
    Input('km-slider', 'value'))
def update_visuals(selected_km):

  # Global vars
  section_bg = 'rgba(22,22,23,1)'
  
  # Overall progress
  final_color = None

  if selected_km <= 24:

    filtered_df = df[df['distance [m]'] <= selected_km*1000]
    t1 = go.Scattermapbox(
      mode = "lines",
      lon = filtered_df['Lon'].tolist(),
      lat = filtered_df['Lat'].tolist(), 
      showlegend=False,
      hoverinfo='none',
      line=dict(color=easy, width=2)
    )

    final_color = easy
    traces = [t1]

  elif selected_km <= 36:

    filtered_df = df[df['distance [m]'] <= 24*1000]
    t1 = go.Scattermapbox(
      mode = "lines",
      lon = filtered_df['Lon'].tolist(),
      lat = filtered_df['Lat'].tolist(), 
      showlegend=False,
      hoverinfo='none',
      line=dict(color=easy, width=2)
    )

    filtered_df = df[(df['distance [m]'] > 24*1000) & (df['distance [m]'] <= selected_km*1000)]
    t2 = go.Scattermapbox(
      mode = "lines",
      lon = filtered_df['Lon'].tolist(),
      lat = filtered_df['Lat'].tolist(), 
      showlegend=False,
      hoverinfo='none',
      line=dict(color=middle, width=2)
    )

    final_color = middle
    traces = [t1, t2]

  else:

    filtered_df = df[df['distance [m]'] <= 24*1000]
    t1 = go.Scattermapbox(
      mode = "lines",
      lon = filtered_df['Lon'].tolist(),
      lat = filtered_df['Lat'].tolist(), 
      showlegend=False,
      hoverinfo='none',
      line=dict(color=easy, width=2)
    )

    filtered_df = df[(df['distance [m]'] > 24*1000) & (df['distance [m]'] <= 36*1000)]
    t2 = go.Scattermapbox(
      mode = "lines",
      lon = filtered_df['Lon'].tolist(),
      lat = filtered_df['Lat'].tolist(), 
      showlegend=False,
      hoverinfo='none',
      line=dict(color=middle, width=2)
    )

    filtered_df = df[(df['distance [m]'] > 36*1000)]
    t3 = go.Scattermapbox(
      mode = "lines",
      lon = filtered_df['Lon'].tolist(),
      lat = filtered_df['Lat'].tolist(), 
      showlegend=False,
      hoverinfo='none',
      line=dict(color=hard, width=2)
    )

    final_color = hard
    traces = [t1, t2, t3]
 
  # Particular position
  runner_position = go.Scattermapbox(
      mode = "markers",
      lon = [filtered_df['Lon'].tolist()[-1]],
      lat = [filtered_df['Lat'].tolist()[-1]],
      text = [selected_km],
      marker=dict(
              color=final_color,
              size=14,
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
    uirevision=1
  ) 
  map_fig.add_trace(track)
  map_fig.add_trace(runner_position)
  for t in traces:
    map_fig.add_trace(t)

  # Pace
  pace_fig = go.Figure()
  pace_fig.update_layout(
      yaxis=dict(autorange='reversed', color='white', title='Pace per km (min:sec)',
               automargin=True, minor=dict(ticks="inside", showgrid=True), showgrid=True),
    xaxis=dict(color='white', title='# of km', automargin=True,
               tickmode= 'linear', tick0 = 0, dtick = 6, range=[0, 42]),
    paper_bgcolor=section_bg,
    plot_bgcolor=section_bg,
    margin=dict(l=0.05, r=0.05, t=0.05, b=0.05),
    template='plotly_dark',
    yaxis_tickformat = '%M:%S'
  )
  pace_fig.add_vrect(x0=0, x1=selected_km, annotation_text='',
                fillcolor="#636efa", opacity=0.25, line_width=0)
  pace_fig.add_vrect(x0=selected_km-6, x1=selected_km, annotation_text='',
                fillcolor="#636efa", opacity=0.25, line_width=0)
  pace_fig.add_trace(pace)
  pace_fig.add_trace(target_pace)
  pace_fig.add_annotation(x=20, y=target['time [s]'].iloc[17],
            text="Planned pace",
            showarrow=False,
            yshift=-12,
            font=dict(color='#737373')
            )

  # Heartbeat
  hb_fig = go.Figure()
  hb_fig.update_layout(
    yaxis=dict(color='white', title='Average heartbeat per kilometer',
               automargin=True, minor=dict(ticks="inside", showgrid=True), showgrid=True),
    xaxis=dict(color='white', title='# of km', automargin=True,
               tickmode= 'linear', tick0 = 0, dtick = 6, range=[0, 42]),
    paper_bgcolor=section_bg,
    plot_bgcolor=section_bg,
    margin=dict(l=0.15, r=0.05, t=0.05, b=0.05),
    template='plotly_dark',
    
  )
  hb_fig.add_vrect(x0=0, x1=selected_km, annotation_text='',
                fillcolor="#636efa", opacity=0.25, line_width=0,
                )
  hb_fig.add_vrect(x0=selected_km-6, x1=selected_km, annotation_text='',
                fillcolor="#636efa", opacity=0.25, line_width=0,
                )
  hb_fig.add_trace(hb)

  # Description
  detail_style = 'fw-normal responsive-text'
  title_style = 'fw-bold responsive-title pb-2'
  if selected_km == 0: 

    # Title
    title_status = html.Span(
        "Feeling good",
        className="badge responsive-badges2 me-2 text-muted",
        style={'background-color': easy}
    )
    title = html.Div([f'Status after {selected_km} km: ', title_status],
            style={'text-align': 'center'}, className=title_style)
    
    # Detail
    text = """
    I woke up at 7 fully excited while a bit nervous. For breakfast,
    I ate oat-meal which is recommended since it is easy to process for the
    body. I arrive at the Islands Brygge at around 8.30 - one hour before the
    race starts. Fast forward 45 minutes, I am warmed up, stretched and ready
    to tackle the race. My initial plan is to start at a pace around five
    minutes and 30s per kilometer.
    """
    detail = html.Div(text, style={'text-align': 'justify'}, className=detail_style)
    desc = html.Div([title, detail])

  elif selected_km == 6:

    # Title
    title_status = html.Span(
        "Feeling good",
        className="badge responsive-badges2 me-2 text-muted",
        style={'background-color': easy}
    )
    title = html.Div([f'Status after {selected_km} km: ', title_status],
            style={'text-align': 'center'}, className=title_style)
    
    # Detail
    text1 = """
    The race was packed which has its pros and cons. The
    biggest pro is the motivation that you get from running
    next to other runners.In addition, I also ran faster than I initially planned.
    I planned to run around 5.30 min/km but I sped up to
    """
    text2 = html.Span('5.10 min/km', style={'color': '#636efa', 'font-weight': 'bold'})
    
    text3 = """
    Yet, my heartrate was about
    """
    text4 = html.Span('150 BPM', style={'color': '#636efa', 'font-weight': 'bold'})
    text5 = """
    which means I could have a comfortable conversation.
    """
    detail = html.Div([text1, text2, text3, text4, text5],
                      style={'text-align': 'justify'},
                      className=detail_style)
    desc = html.Div([title, detail])

  elif selected_km == 12:

    # Title
    title_status = html.Span(
        "Feeling good",
        className="badge responsive-badges2 me-2 text-muted",
        style={'background-color': easy}
    )
    title = html.Div([f'Status after {selected_km} km: ', title_status],
            style={'text-align': 'center'}, className=title_style)
    
    # Detail
    text1 = """
    At this point, I stabilized my pace about 
    """
    text2 = html.Span('5 min/km', style={'color': primary, 'font-weight': 'bold'})
    text3 = """
    . I started debated myself whether I should not have stuck to the initial
    plan since now I am running 30 seconds faster per kilometer. I finally
    concluded that either I am right and it was a right bet or I will suffer 
    towards the end.
    """

    detail = html.Div([text1, text2, text3], style={'text-align': 'justify'},
        className=detail_style)
    desc = html.Div([title, detail])

  elif selected_km == 18:

    # Title
    title_status = html.Span(
        "Feeling good",
        className="badge responsive-badges2 me-2 text-muted",
        style={'background-color': easy}
    )
    title = html.Div([f'Status after {selected_km} km: ', title_status],
            style={'text-align': 'center'}, className=title_style)
    
    # Detail
    text1 = """
    Things are going well since I managed to find pace makers for  
    """
    text2 = html.Span('4.59 min/km', style={'color': primary, 'font-weight': 'bold'})
    text3 = """
    . These runners are like your guides through the run, you can simply follow
    them and will reach the needed time. Apart from keeping track of my pace,
    I also had to make sure that I stay hydrated and refill needed nutritions.
    The latter part was ensured by my girlfriend who had to travel on bike
    throughout the Copenhagen and give me my gels. Looking back, this
    was a bad idea and I should have just carried the gels with me.
    """

    detail = html.Div([text1, text2, text3], style={'text-align': 'justify'},
        className=detail_style)
    desc = html.Div([title, detail])

  elif selected_km == 24:

    # Title
    title_status = html.Span(
        "Feeling good",
        className="badge responsive-badges2 me-2 text-muted",
        style={'background-color': easy}
    )
    title = html.Div([f'Status after {selected_km} km: ', title_status],
            style={'text-align': 'center'}, className=title_style)
    
    # Detail
    text1 = """
    I finally hit the half-marathon mark which felt awesome, almost like I am
    very close to the end. This led me to unconsciously speed up. At the highest
    I hit 
    """
    text2 = html.Span('4.34 min/km', style={'color': primary, 'font-weight': 'bold'})
    text3 = """
    which is a pace where I start to feel little uncomfortable. This can also be
    seen from my heart beat which climbed up to 
    """
    text4 = html.Span('170 BMP', style={'color': primary, 'font-weight': 'bold'})
    text5 = """
    . Although I knew all of this I kept going at this pace.
    """

    detail = html.Div([text1, text2, text3, text4, text5], style={'text-align':
      'justify'}, className=detail_style)
    desc = html.Div([title, detail])

  elif selected_km == 30:
    # Title
    title_status = html.Span(
        "Can barely talk",
        className="badge responsive-badges2 me-2 text-muted",
        style={'background-color': middle}
    )
    title = html.Div([f'Status after {selected_km} km: ', title_status],
            style={'text-align': 'center'}, className=title_style)
    
    # Detail
    text1 = """
    After the half marathon mark, I started to think quite a lot about how many
    kilometers are left, in fact, this is a good way how one can think of
    something else than the pain. I was quite nervous around 27th km mark as
    this was the furthest distance I ran during my training. As can be seen
    nicely from the figures, from this moment on, I only ran slower. Learning
    point: next time run at least 33 km as part of the training.
    """
    
    detail = html.Div([text1], style={'text-align': 'justify'},
        className=detail_style)
    desc = html.Div([title, detail])

  elif selected_km == 36:

    # Title
    title_status = html.Span(
        "Can barely talk",
        className="badge responsive-badges2 me-2 text-muted",
        style={'background-color': middle}
    )
    title = html.Div([f'Status after {selected_km} km: ', title_status],
            style={'text-align': 'center'}, className=title_style)

    # Detail
    text1 = """
    Many runners will tell you that 33rd km is the most critical. For me at this
    point started a mental battle. It is very important that one stays mentally
    strong and keeps running. If you stop, it is very hard to start running
    again. I also realized that my initial bet probably was not the best and
    I will start suffering more and more towards the end.
    """

    detail = html.Div([text1], style={'text-align': 'justify'},
        className=detail_style)
    desc = html.Div([title, detail])

  elif selected_km == 42:

    # Title
    title_status = html.Span(
        "Hurting",
        className="badge responsive-badges2 me-2 text-muted",
        style={'background-color': hard}
    )
    title = html.Div([f'Status after {selected_km} km: ', title_status],
            style={'text-align': 'center'}, className=title_style)
    
    # Detail
    text1 = """
    I knew that it is going to be over soon, but each kilometer left seemed
    very painful. Even stopping at refreshing station did not help. At 41st
    km I hit the wall. This is a moment where one's body simply rejects to run.
    I walked for 50 m until I started running again. What helped me the most
    mentally was the fact of knowing the exact path I have to run to get to
    finish. I finished in 3 hours, 34 minutes and 48 seconds.
    """

    detail = html.Div([text1], style={'text-align': 'justify'},
        className=detail_style)
    desc = html.Div([title, detail])

  
  return desc, hb_fig, pace_fig, map_fig

