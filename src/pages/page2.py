from dash import dcc, html, Input, Output, callback


layout = html.Div([
  dcc.Markdown(
    """
    ## About
    This page is about my marathon training.
    """
  )
])

