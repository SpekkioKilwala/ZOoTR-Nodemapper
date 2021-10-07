"""
For playing with cytoscape's features progressively and getting a handle on them.
I want to work through this list approximately in order.

    Done: hard-coded VERY SMALL dumb network
    Done: turning an edge on and off
    Done: migrate ZOOTR map across so that I have something better to play with
    Done: Physics-based layout
    Done: How to label edges good

    Background colour and layout of elements on the page. Sidebars! Night mode!
    Toggle-box for equipment, toggle for child/adult/either.
    Animation
    An interface for actually looking at the data of nodes and edges
    User interfaces for connecting/disconnecting edges
    Proof of concept of making two
    Path finding?
    Saving and reloading
    Changing how a given edge is displayed according to user inputs (gaining items,  adult/child filters)
    Encoding rules from the csv, to the dataframe, to the dict.
        (that will need json. If I'm going to use json, maybe I should skip the csv?)
        This has got to be something that should be easy to research.
"""

import dash
import dash_cytoscape as cyto
from dash import html
from dash import dcc
import pandas as pd

from dash.dependencies import Input, Output, State

df_nodes_default = pd.read_csv("data/zootr_nodes_simple.csv")
df_edges_default = pd.read_csv("data/zootr_edges_simple.csv")

default_nodes = [{
    'group': 'nodes',
    'data': {
        'id': row['Name']  # eventually, Parent information goes here too.
        },
    'classes': row['Classes']} for row in df_nodes_default.to_dict(orient='records')]

default_edges = [{
    'group': 'edges',
    'data': {
        'id': str(row['Index']) + ' ' + row['Source'] + ' ' + row['Target'],
        'source': row['Source'],
        'target': row['Target'],
        'width': row['Weight'],  # No impact without stylesheet?
        'sl': row['FromLabel'],  # Note, these aren't drawn without a stylesheet
        'tl': row['ToLabel']},  # Also note you can put in WHATEVER data you like. Which is... handy.
    'classes': row['Type']} for row in df_edges_default.to_dict(orient='records')]

world_map = default_nodes + default_edges

app = dash.Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-two-nodes',
        layout={'name': 'cose'},
        style={'width': '100%', 'height': '800px'},
        elements=world_map,
        stylesheet=[
            # all nodes; the label is the LABEL, and it goes in the MIDDLE. Plus an outline.
            {'selector': 'node', 'style': {
                'text-valign': 'center',
                'label': 'data(id)',
                'text-outline-color': '#FFFFFF',
                'text-outline-width': 0.5}},

            # Doesn't work. Where can I set the background colour? Is it part of this at all?
            # {'selector': 'core', 'style': {'color': '#333333'}},

            # Node label size and node size by the flag size
            {'selector': '.small', 'style': {'width': 7, 'height': 7, 'font-size': 5}},
            {'selector': '.medium', 'style': {'width': 10, 'height': 10, 'font-size': 7}},
            {'selector': '.large', 'style': {'width': 14, 'height': 14, 'font-size': 7}},
            {'selector': '.huge', 'style': {'width': 20, 'height': 20, 'font-size': 10}},

            # Node shape and colour by the general/town/dungeon/warp flags
            {'selector': '.regular', 'style': {'background-color': '#005500'}},  # regular is green
            {'selector': '.town', 'style': {'background-color': '#3333BB'}},  # town is blue
            {'selector': '.song', 'style': {'background-color': '#DDBB00'}},  # warps are yellow
            {'selector': '.spawn', 'style': {'background-color': '#DDBB00'}},  # so are spawns
            {'selector': '.dungeon', 'style': {'background-color': '#880000', 'shape': 'rectangle'}},  # red square

            # all edges get two labels, in white, pretty small, and are bezier.
            {'selector': 'edge', 'style': {
                'source-label': 'data(sl)',
                'source-text-offset': 15,
                'target-text-offset': 15,
                'target-label': 'data(tl)',
                'color': '#666666',
                'font-size': 5,
                'width': 'data(width)',
                'curve-style': 'bezier',
                'control-point-step-size': 20}},

            # edge colour and arrow-ness by each type
            {'selector': '.free', 'style': {'line-color': '#336633'}},
            {'selector': '.oneway', 'style': {'line-color': '#336633', 'mid-target-arrow-color': '#114411', 'mid-target-arrow-shape': 'vee'}},
            {'selector': '.owl', 'style': {'line-color': '#AC5B16', 'mid-target-arrow-color': '#8A3904', 'mid-target-arrow-shape': 'vee'}},
            {'selector': '.warp', 'style': {'line-color': '#DDBB00', 'mid-target-arrow-color': '#BB9900', 'mid-target-arrow-shape': 'vee'}}
        ]
        # responsive=True
    ),
    html.Div(id='label', children='Button is disconnected'),
    dcc.RadioItems(id='edge_radio',
                   options=[{'label': 'Edge Off', 'value': 'off'},  # these values HAVE to be strings or numbers
                            {'label': 'Edge On', 'value': 'on'}],
                   value='off'),
    html.Div(id='radio_readout'),

    # Wanted a textbox example for reference
    dcc.Input(id='my-input', value='initial value', type='text')
])


# @app.callback(
#     Output('cytoscape-two-nodes', 'elements'),
#     Input('edge_radio', 'value'))
# def basic_radio(toggle):
#     if toggle == 'off':
#         return initial_nodes + initial_edges
#     else:
#         return initial_nodes + initial_edges + extra_edge


if __name__ == '__main__':
    app.run_server(debug=True)