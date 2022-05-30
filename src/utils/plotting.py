from .config import MAPBOX_TOKEN
import plotly.graph_objects as go
import pandas as pd
import json


def get_race_plot():

  """
  The code inspired from:
  https://plotly.com/python/animations/
  """
  
  # Load the data
  df = pd.read_csv('data/processed/df.csv')
  reduced_df = pd.read_csv('data/processed/reduced_df.csv')
  with open('data/processed/minutes_distance.csv') as f:
    minutes_distance = [float(d) for d in f.read().strip().split(',')]
  with open('data/processed/dm_to_loc.json') as f:
    dm_to_loc = json.load(f)


  # ---------- Initial figure layout setup section
  # Define figure 
  fig_dict = {
      "data": [],
      "layout": {},
      "frames": []
  }

  # Buttons setup
  fig_dict["layout"]["updatemenus"] = [
      {
          "buttons": [
              {
                  "args": [None, {"frame": {"duration": 250, "redraw": True},
                                  "fromcurrent": True, "transition": {"duration": 250,
                                                                      "easing": "quadratic-in-out"}}],
                  "label": "Play",
                  "method": "animate"
              },
              {
                  "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}}],
                  "label": "Pause",
                  "method": "animate"
              }
          ],
          "direction": "left",
          "pad": {"r": 10, "t": 87},
          "showactive": False,
          "type": "buttons",
          "x": 0.1,
          "xanchor": "right",
          "y": 0,
          "yanchor": "top"
      }
  ]

  # Map setup
  fig_dict["layout"]["hovermode"] = "closest"
  fig_dict["layout"]["title_text"] = 'CPH Marathon 2022'
  fig_dict["layout"]["mapbox"] = {'center': {'lon': 12.57, 'lat': 55.685}, 'style': "dark", 'zoom': 11.5}
  fig_dict["layout"]["mapbox_accesstoken"] = MAPBOX_TOKEN

  # Slider
  sliders_dict = {
      "active": 0,
      "yanchor": "top",
      "xanchor": "left",
      "currentvalue": {
          "font": {"size": 20},
          "prefix": "Minute: ",
          "visible": True,
          "xanchor": "right"
      },
      "transition": {"duration": 300, "easing": "cubic-in-out"},
      "pad": {"b": 10, "t": 50},
      "len": 0.9,
      "x": 0.1,
      "y": 0,
      "steps": []
  }

  # ---------- Data section
  # --- Create initial view
  track = go.Scattermapbox(
      mode = 'lines',
      lon = df['Lon'].tolist(),
      lat = df['Lat'].tolist(),
      hoverinfo='none',
      showlegend=False
  )

  km_markers = go.Scattermapbox(
      mode = "markers",
      lon = reduced_df['Lon'].tolist(),
      lat = reduced_df['Lat'].tolist(),
      text=reduced_df['Exact Distance'],
      marker=dict(
              color='rgb(158, 67, 232)',
              size=8,
              opacity=1
          ),
      showlegend=False,
      hovertemplate = '%{text} km<extra></extra>'
  )

  runner_position = go.Scattermapbox(
      mode = "markers",
      lon = [12.57587],
      lat = [55.66598],
      text = [round(0, 2)],
      marker=dict(
              color='rgb(245, 66, 66)',
              size=8,
              opacity=1
          ),
      showlegend=False,
      hovertemplate = '%{text} m<extra></extra>'
  )

  fig_dict["data"] = [track, km_markers, runner_position]

  # --- Make frames
  for i, dm  in enumerate(minutes_distance):

      # Account for zero based indexing
      m = i + 1

      # Get locatin
      lat, lon = dm_to_loc[dm]

      # Create a dot on the map 
      runner_position = go.Scattermapbox(
          mode = "markers",
          lon = [lon],
          lat = [lat],
          text = [round(dm, 2)],
          marker=dict(
                  color='rgb(245, 66, 66)',
                  size=8,
                  opacity=1
              ),
          showlegend=False,
          hovertemplate = '%{text} m<extra></extra>'
      )

      # Annotation
      a1 = dict(font=dict(color="black",size=12),
                            x=0.0,
                            y=1.05,
                            showarrow=False,
                            text=f'Distance: <b>{round(dm/1000, 2)} [km]</b>',
                            textangle=0,
                            xref="paper",
                            yref="paper"
      )
      layout = go.Layout(annotations= [a1])

      frame = go.Frame(
          data=[track, km_markers, runner_position], 
          name=str(m),
          layout = layout
      )

      fig_dict["frames"].append(frame)

      # Slider step
      slider_step = {"args": [
          [m],
          {"frame": {"duration": 300, "redraw": True},
           "mode": "immediate",
           "transition": {"duration": 300}}
      ],
          "label": m,
          "method": "animate"}
      sliders_dict["steps"].append(slider_step)


  fig_dict["layout"]["sliders"] = [sliders_dict]

  # ---------- Figure evaluation section
  fig = go.Figure(fig_dict)
  
  return fig

