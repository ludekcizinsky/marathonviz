from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from pages import about, race

# Header
navbar = dbc.NavbarSimple(
      children=[
          dbc.NavLink("About", href="/", active="exact", className="h-100"),
          dbc.NavLink("Race", href="/race", active="exact", className="h-100")
      ],
      brand="🏃 Marathonviz",
      brand_href='/',
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
    className="h-10",
    align='center'
)

# Content
content = dbc.Container(id='page-content', className='h-90')

# Dash App
font_url = 'https://fonts.googleapis.com/css2?family=Poppins&display=swap'
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.icons.FONT_AWESOME, font_url]
    )
server = app.server
app.css.config.serve_locally = True
app.layout = dbc.Container([header, content], className="vh-100", fluid=True)



# Redirect to correct pages
@callback(Output('page-content', 'children'),
          Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/race':
        return race.layout
    else:
        return about.layout

if __name__ == '__main__':
    app.run_server(debug=True)

