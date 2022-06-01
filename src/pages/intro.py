from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

text = dcc.Markdown(
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

intro = dbc.Row(text, className='h-100')

layout = dbc.Container([intro], className="h-100")

