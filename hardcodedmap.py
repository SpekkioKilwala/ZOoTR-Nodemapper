import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import visdcc

# Whatever you do, don't delete this file, working out how to set the options is important

app = dash.Dash()
app.layout = html.Div([
    visdcc.Network(id = 'net',
                   options=dict(height='800px', width='100%',
                                physics={'solver':'forceAtlas2Based'},
                                shape='circle',
                                color={'background':'#333333', 'border':'#AAAAAA'}),
                   selection = {'nodes':[], 'edges':[]},),
    dcc.Input(id = 'label',
              placeholder = 'Enter a label ...',
              type = 'text',
              value = ''  ),
    html.Br(),html.Br(),
    dcc.RadioItems(id = 'color',
                   options=[{'label': 'Red'  , 'value': '#ff0000'},
                            {'label': 'Green', 'value': '#00ff00'},
                            {'label': 'Blue' , 'value': '#0000ff'} ],
                   value='Red'  ),
    html.Div(id = 'nodes'),
    html.Div(id = 'edges')
])


@app.callback(
    Output('net', 'data'),
    [Input('label', 'value')])
def myfun(x):
    data ={"nodes":[{'id': 'dmc', "label": 'Death Mountain Crater'},
                    {'id': 'dmt', "label": 'Death Mountain Trail'},
                    {'id': 'col', "label": 'Desert Colossus'},
                    {'id': 'gef', "label": 'Gerudo Fortress'},
                    {'id': 'gev', "label": 'Gerudo Valley'},
                    {'id': 'goc', "label": 'Goron City'},
                    {'id': 'gra', "label": 'Graveyard'},
                    {'id': 'haw', "label": 'Haunted Wasteland'},
                    {'id': 'hyf', "label": 'Hyrule Field'},
                    {'id': 'kak', "label": 'Kakariko Village'},
                    {'id': 'kok', "label": 'Kokiri Forest'},
                    {'id': 'lak', "label": 'Lake Hylia'},
                    {'id': 'low', "label": 'Lost Woods'},
                    {'id': 'lwb', "label": 'Lost Woods Bridge'},
                    {'id': 'mar', "label": 'Market'},
                    {'id': 'mke', "label": 'Market Entrance'},
                    {'id': 'sfm', "label": 'Sacred Forest Meadow'},
                    {'id': 'csp', "label": 'Child Spawn'},
                    {'id': 'asp', "label": 'Adult Spawn'},
                    {'id': 'tte', "label": 'Temple of Time Entrance'},
                    {'id': 'tot', "label": 'Temple of Time'},
                    {'id': 'zof', "label": 'Zora Fountain'},
                    {'id': 'zor', "label": 'Zora River'},
                    {'id': 'zod', "label": "Zora's Domain"}],
           "edges" :[{"from": 'dmc', "to": 'hyf'},
                     {"from": 'dmc', "to": 'hyf'},
                     {"from": 'dmt', "to": 'gef'},
                     {"from": 'dmt', "to": 'hyf'},
                     {"from": 'dmt', "to": 'mke'},
                     {"from": 'dmt', "to": 'mar'},
                     {"from": 'col', "to": 'kok'},
                     {"from": 'gef', "to": 'goc'},
                     {"from": 'gev', "to": 'tte'},
                     {"from": 'gev', "to": 'mar'},
                     {"from": 'gev', "to": 'lak'},
                     {"from": 'goc', "to": 'kak'},
                     {"from": 'goc', "to": 'zof'},
                     {"from": 'gra', "to": 'zod'},
                     {"from": 'haw', "to": 'kok'},
                     {"from": 'haw', "to": 'mar'},
                     {"from": 'hyf', "to": 'mar'},
                     {"from": 'hyf', "to": 'zor'},
                     {"from": 'hyf', "to": 'lwb'},
                     {"from": 'hyf', "to": 'sfm'},
                     {"from": 'kak', "to": 'mke'},
                     {"from": 'kak', "to": 'low'},
                     {"from": 'kok', "to": 'tot'},
                     {"from": 'lak', "to": 'low'},
                     {"from": 'lak', "to": 'gef'},
                     {"from": 'low', "to": 'zor'},
                     {"from": 'low', "to": 'zor'},
                     {"from": 'low', "to": 'lwb'},
                     {"from": 'lwb', "to": 'zod'},
                     {"from": 'csp', "to": 'lak'},
                     {"from": 'asp', "to": 'mar'},]}
    return data

@app.callback(
    Output('net', 'options'),
    [Input('color', 'value')])
def myfun(x):
    return {'nodes':{'color': x}}

@app.callback(
    Output('nodes', 'children'),
    [Input('net', 'selection')])
def myfun(x):
    s = 'Selected nodes : '
    if len(x['nodes']) > 0 : s += str(x['nodes'][0])
    return s

@app.callback(
    Output('edges', 'children'),
    [Input('net', 'selection')])
def myfun(x):
    s = 'Selected edges : '
    if len(x['edges']) > 0 : s = [s] + [html.Div(i) for i in x['edges']]
    return s

if __name__ == '__main__':
    app.run_server()