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


footer = html.Footer(
    [
      html.Div(
        [
          html.Span(
            [
              "Created by Ludek Cizinsky."
            ],
            className='text-muted'
          )
        ],
      className="container"
      ) 
    ],
    className="footer"
)


app.layout = html.Div(
    [
        dcc.Location(id="url"),
        dbc.NavbarSimple(
            children=[
                dbc.NavLink("Intro", href="/", active="exact"),
                dbc.NavLink("Race", href="/race", active="exact"),
                dbc.NavLink("Training", href="/training", active="exact"),
            ],
            brand="Marathonviz",
            color="#2a2b2b",
            dark=True,
            className='py-1'
        ),
        dbc.Container(id="page-content")
    ],
    style={"height": "100vh"}
)


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

