"""
Test file, firstly for seeing how different edges work.
Then for many different things, in no particular order:
    An interface for actually looking at the data of nodes and edges
    User interfaces for connecting/disconnecting edges
    How to label edges good
    Path finding?
    Saving and reloading
    Changing how a given edge is displayed according to user inputs (gaining items,  adult/child filters)
    Encoding rules from the csv, to the dataframe, to the dict.
        (that will need json. If I'm going to use json, maybe I should skip the csv?)
"""
# imports
import dash
import visdcc
import pandas as pd
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

# create app
app = dash.Dash()

# This test will not do the csv-dataframe import thing.
nodes_initial = [ {'id': 'A', 'label': 'A', 'shape': 'circle', 'size': '50', 'color': '#CC0000'},
                  {'id': 'B', 'label': 'B', 'shape': 'circle', 'size': '50', 'color': '#CCCC00'},
                  {'id': 'C', 'label': 'C', 'shape': 'circle', 'size': '50', 'color': '#00CC00'},
                  {'id': 'D', 'label': 'D', 'shape': 'circle', 'size': '50', 'color': '#0000CC'},
                  {'id': 'CL1', 'label': 'loose end C', 'shape': 'text', 'size': '5', 'color': '#555555'},
                  {'id': 'DL1', 'label': 'loose end D', 'shape': 'text', 'size': '5', 'color': '#555555'} ]

edges_initial = [ {'from': 'A', 'to': 'B', 'weight': 10, 'arrows': 'to', 'color': {'color': '#00FF00'}},
                  {'from': 'B', 'to': 'A', 'weight': 10, 'arrows': 'to,from', 'color': {'color': '#00FFFF'}},
                  {'from': 'C', 'to': 'CL1', 'weight': 5, 'color': '#000000', 'label': 'Zora Waterfall'},
                  {'from': 'D', 'to': 'DL1', 'weight': 5, 'color': '#000000', 'label': "Darunia's Statue"} ]

# define layout
app.layout = html.Div([
    # Create a network object! The 'data' parameter is a dict, specifying the node and edge lists we created above.
    visdcc.Network(id='net',
                   data={'nodes': nodes_initial, 'edges': edges_initial},
                   options=dict(height='700px', width='100%', physics={'solver': 'forceAtlas2Based'})),
    # Create a radio-button that selects between three colours, on the id "color"
    html.Div(id='edge_toggle_title', children='Extra Edge Mode:'),
    dcc.RadioItems(id='edge_radio',
                   options=[{'label': 'Edge Off', 'value': 'off'},  # these values HAVE to be strings or numbers
                            {'label': 'Edge On', 'value': 'on'}],
                   value='off'),
    html.Div(id='active_nodes_readout'),
    html.Div(id='active_edges_readout'),
    html.Div(id='edge_detail_readout')
])

# Very important question:
# Let's say that I have page inputs, and then a great deal of behind-the-scenes work, and then outputs.
# Do I actually need one mega-function that oversees the entire process from start to end?
# I know, it can still be abstracted away, but being able break apart the start, middle, and end would be nice.


@app.callback(
    Output('net', 'data'),
    [Input('edge_radio', 'value')])
def edge_switcher(toggle):
    """
    Turns the edge between two loose ends on and off, according to a radio button toggle.
    """
    extra_edges = [{'from': 'CL1', 'to': 'DL1', 'weight': 2, 'arrows': 'middle', 'color': '#000000'}]
    if toggle == 'on':
        edges_out = edges_initial + extra_edges
    else:
        edges_out = edges_initial
    return {'nodes': nodes_initial, 'edges': edges_out}

@app.callback(
    Output('active_nodes_readout', 'children'),
    Output('active_edges_readout', 'children'),
    Input('net', 'selection'))
def display_selected(selected):
    """Display which nodes and edges are currently selected to some screen-text."""
    nodes_prefix = "Selected nodes: "
    edges_prefix = "Selected edges: "
    if selected is None:
        return nodes_prefix, edges_prefix
    else:
        nodes_payload = '; '.join([str(x) for x in selected['nodes']])
        edges_payload = '; '.join([str(x) for x in selected['edges']])
        return nodes_prefix + nodes_payload, edges_prefix + edges_payload

def show_detailed_data():
    """Display everything knowable about a certain node or edge"""
    

# define main calling
if __name__ == '__main__':
    app.run_server(debug=True)