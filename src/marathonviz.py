from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from pages import race, training


# ------ Initialize dash app
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.DARKLY]
    )
server = app.server

intro = dcc.Markdown(
    '''
    ## About
    Marathonviz's goal is to give you an idea what is like to run marathon as
    well as practice for it.

    ## Sections
    This website includes following sections:
    - [Marathon run](/race)
    - [Marathon training](/training)
    '''
)

index_page = html.Div([
   intro 
])




# Navbar
navbar = dbc.NavbarSimple(
      children=[
          dbc.NavLink("Intro", href="/", active="exact", className="h-100"),
          dbc.NavLink("Race", href="/race", active="exact", className="h-100"),
          dbc.NavLink("Training", href="/training", active="exact", className="h-100"),
      ],
      brand="Marathonviz",
      color="#2a2b2b",
      dark=True,
      className='h-100'
)

# First row of graphs
header = dbc.Row(
    children=[
      dbc.Col(
            width=12,
            children=[navbar],
            className="h-100"
      )
    ],
    className="h-10"
)


row0 = dbc.Row(
    children=[
      dbc.Col(
            width=1,
            children=[dbc.NavLink("Intro", href="/", active="exact", className="h-100")],
            className="h-100"
      ),
      dbc.Col(
            width=1,
            children=[dbc.NavLink("training", href="/training", active="exact", className="h-100")],
            className="h-100"
      )
    ],
    className="h-5",
    justify="end"
)

row0 = dbc.Row(
    children=[
        dbc.Col(
            width=6,
            children=[dcc.Graph(id="hb1-overview", className="h-100")],
            className="h-100",
        ),
        dbc.Col(
            width=6,
            children=[dcc.Graph(id="map1", className="h-100")],
            className="h-100",
        ),
    ],
    className="h-25",
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
    className="h-40 py-2",
)

# Third row
row3 = dbc.Row(
    children=[
        dbc.Col(
            width=6,
            children=[dcc.Graph(id="hb3-overview", className="h-100")],
            className="h-100",
        ),
        dbc.Col(
            width=6,
            children=[dcc.Graph(id="map3", className="h-100")],
            className="h-100",
        ),
    ],
    className="h-50 py-2",
)

content = dbc.Container(id='page-content', className='h-90')













app.layout = dbc.Container([header, row2, row3], className="vh-100", fluid=False)









# ------- Main handler
@callback(Output('page-content', 'children'),
          Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/race':
        return race.layout
    elif pathname == '/training':
        return training.layout
    else:
        return index_page

if __name__ == '__main__':
    app.run_server(host='0.0.0.0')

