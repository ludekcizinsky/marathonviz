from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc


img_style={"max-height": "250px", 'width': '100px'}

text = dbc.Col(dcc.Markdown(
    '''
    ## Welcome
    Welcome to Marathonviz! This page was created with the goal of sharing how
    it is like to run a marathon. Whether you are an experienced runner or just
    beginner, I hope this visualization gives you some interesting insights as
    well as motivates you in your running efforts. Enjoy the [Marathon
    race](/race)!

    ## Photos
    To be added.
    '''
), className='h-100', width=12)

carousel = dbc.Col(dbc.Carousel(
    items=[
        {"key": "1", "src": "/assets/images/1.jpg", "img_style": img_style},
        {"key": "2", "src": "/assets/images/2.jpg", "img_style": img_style}
    ],
    controls=True,
    indicators=True,
    className='h-100'
), className='h-100', width=12)

intro = dbc.Row(text, className='h-25 text-light')
photos = dbc.Row([carousel], className='h-75', justify="center")

layout = dbc.Container([intro], className="h-100")

