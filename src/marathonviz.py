from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from pages import race, training, intro

# Header
navbar = dbc.NavbarSimple(
      children=[
          dbc.NavLink("Intro", href="/", active="exact", className="h-100"),
          dbc.NavLink("Race", href="/race", active="exact", className="h-100"),
          dbc.NavLink("Training", href="/training", active="exact", className="h-100"),
      ],
      brand="🏃 Marathonviz",
      brand_style={'color': '#c9c9c9', 'font-weight': 'bold', 'font-family': "Poppins"},
      className='h-100 navbar-dark',
      color="#191a1a"
)

header = dbc.Row(
    children=[
      dbc.Col(
            width=12,
            children=[navbar],
            className="h-66"
      ),
      dcc.Location(id='url', refresh=False),
      html.Hr(style={'color': '#575655', 'height': '2px'})
    ],
    className="h-10"
)

# Content
content = dbc.Container(id='page-content', className='h-90')

# Dash App
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.icons.FONT_AWESOME]
    )
server = app.server
app.layout = dbc.Container([header, content], className="vh-100", fluid=True)


# Redirect to correct pages
@callback(Output('page-content', 'children'),
          Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/race':
        return race.layout
    elif pathname == '/training':
        return training.layout
    else:
        return intro.layout

if __name__ == '__main__':
    app.run_server(debug=True)

