from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

# Intro
t = dcc.Markdown('''## Welcome to Marathonviz!
This page was created with the goal of sharing how
it is like to run a marathon. Whether you are an experienced runner, a beginner
or just interested what this page is up to, I hope this visualization gives you some interesting insights as
well as motivation for running. Enjoy the marathon race! 
'''
)

button = dbc.Button(html.Span("Get started", className="responsive-text"), href='/race')

text = dbc.Col(
    html.Div(
      [
        t,
        button
      ],
      style={'text-align': 'center'}
    ),
    className='h-100',
    width=12
) 

intro = dbc.Row([text], className='h-25 text-light responsive-text mb-4')


# Photo
img_style={"max-height": "50vh", "max-width": 'auto'}

photo = dbc.Col(html.Img(src="/assets/images/3.jpeg", className='h-100 rounded mx-auto d-block',
                style=img_style),
        className='h-100', width=12)
photo_row = dbc.Row([photo], className='h-75', align="center")

layout = dbc.Container([intro, photo_row], className="h-90")

