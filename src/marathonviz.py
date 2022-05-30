from dash import Dash, dcc, html, Input, Output
from utils import fetch_marathon_data, get_map_data, get_race_plot


# ------ Fetch marathon data (should be done only once after reboot)
#print('Fetching marathon data')
#fetch_marathon_data()

# ------ Load figures
print('Preparing data for the figure')
df, reduced_df, minutes_distance, dm_to_loc = get_map_data()
print('Creating figure')
marathon_track_fig = get_race_plot(df, reduced_df, minutes_distance, dm_to_loc)

# ------ Initialize dash app
app = Dash(__name__)
server = app.server

# ------ App layout
app.layout = html.Div([
    dcc.Graph(id='marathon-fig', figure=marathon_track_fig, style={'width': '90vh', 'height': '90vh'})
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0')

