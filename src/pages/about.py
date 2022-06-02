from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

# Intro
text = dbc.Col(dcc.Markdown(
    '''
    ## Welcome
    Welcome to Marathonviz! This page was created with the goal of sharing how
    it is like to run a marathon. Whether you are an experienced runner or just
    beginner, I hope this visualization gives you some interesting insights as
    well as motivates you in your running efforts. Enjoy the [Marathon
    race!](/race)
    '''
), className='h-100', width=12)
intro = dbc.Row(text, className='h-20 text-light mb-2 text-wrap responsive-text')

# Photo
img_style={"max-height": "250px", "max-width": 'auto'}

photo = dbc.Col(html.Img(src="/assets/images/3.jpeg", className='h-100 rounded mx-auto d-block img-fluid'),
        className='h-100', width=12)
photo_row = dbc.Row([photo], className='h-60', align="center")

layout = dbc.Container([intro, photo_row], className="h-100")

