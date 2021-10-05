import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import visdcc

# Whatever you do, don't delete this file, working out how to set the options is important

app = dash.Dash()
app.layout = html.Div([
    visdcc.Network(id = 'net',
                   options=dict(height='600px', width='100%', physics={'solver':'forceAtlas2Based'}),
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
    dcc.RadioItems(id='toggle_edge',
                   options=[{'label': 'Off'  , 'value': False},
                            {'label': 'On'   , 'value': True}],
                   value='Off'  ),
    html.Div(id = 'nodes'),
    html.Div(id = 'edges')
])

node_list = [{"id": 1, "label": 'Node 1'},
             {"id": 2, "label": 'Node 2'},
             {"id": 3, "label": 'Node 3'},
             {"id": 4, "label": 'Node 4'},
             {"id": 5, "label": 'Node 5'} ]

edge_list_default = [{"from": 1, "to": 3},
                     {"from": 1, "to": 2},
                     {"from": 2, "to": 4}]

edge_extra = [{"from": 2, "to": 5}]

# Embrace functional programming principles
# ARE these callbacks ONLY to interface with the page?
# Where do I need them? Can I do without?

# So I want a function that....
# Has an input: the on/off radio button.
# And an output: the data object that actually gets given to the net gizmo on the page.
# It might have to call other things, but that's the mouth and ass of the thing.

# These lists can just be added together, but is that a good way to do it?
# I don't know. We'll find out.
# What happens when the edges get replaced with one that is suddenly missing a member?
# I don't know! We'll find out!

@app.callback(
    Output('net', 'data'),
    [Input('label', 'value')])
def myfun(x):
    data ={"nodes":node_list,
        "edges" : edge_list_default}
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
