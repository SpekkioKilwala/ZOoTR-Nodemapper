"""
Author: Jonathan Walsh
With thanks to Mohit Mayank for their visdcc examples, even if Jaal didn't seem like what I needed.

Purpose: To assist the user in mapping a randomised OoT-zelda world.
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

# I'm going to have a dataframe of nodes and a dataframe of edges.
# The nodes actually have got features that are independent of their attached edges.
df_nodes_default = pd.read_csv("data/zootr_nodes_simple.csv")
df_edges_default = pd.read_csv("data/zootr_edges_simple.csv")

# Keeping an example line of selecting only some rows of a dataframe
# df = df.loc[df['weight']>10, :]
# You can ALSO select only some COLUMNS. That would go after the comma, replacing the colon.
# Note: I think I read that in pandas, it INCLUDES the end, unlike normal python syntax.

# First step is to use df.to_dict.
# It gives you a LIST where each row has been converted to dict form.
# e.g. {'Source': 'Addam-Marbrand', 'Target': 'Jaime-Lannister', 'Type': 'Undirected', 'weight': 3, 'book': 1}

# We're just going to immediately turn that into a list of dicts that is usable by visdcc in one line.
nodes = [{
            'id': row['Name'],
            'label': row['Name'],
            'shape': row['Shape'],
            'size': row['Size'],
            'color': row['Colour']
        } for row in df_nodes_default.to_dict(orient='records')]

# Turn the edges dataframe into a list of dicts that we can use
edges = [{
            # Apparently, IDs are optional, and are automatically assigned if not provided.
            # 'id': str(row['Index']) + ': ' + row['From'] + ' -> ' + row['To'],
            'from': row['From'],
            'to': row['To'],
            'weight': row['Weight']
        } for row in df_edges_default.to_dict(orient='records')]

# I don't know about this. I think I should be beginning with CSS.
theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

# define layout
app.layout = html.Div([
    # Create a network object! The 'data' parameter is a dict, specifying the node and edge lists we created above.
    visdcc.Network(id = 'net',
                   data = {'nodes': nodes, 'edges': edges},
                   options = dict(height= '700px', width= '100%', physics={'solver': 'forceAtlas2Based'})),
    # Create a radio-button that selects between three colours, on the id "color"
    dcc.RadioItems(id = 'background_radio',
                   options=[{'label': 'Light Mode', 'value': '#ffffff'},
                            {'label': 'Dark Mode', 'value': '#333333'}],
                   value='Default value!'),
    html.Div(id='test_text_title', children="Radio button output below:"),
    html.Div(id='radio_display'),
    html.Div(id='second_radio_display'),
    dcc.RadioItems(id = 'edge_radio',
                   options=[{'label': 'Edge Off', 'value': 'off'}, # because these values HAVE to be strings or numbers
                            {'label': 'Edge On', 'value': 'on'}],
                   value='off'),
])

# define callback

# A callback to go from the radio buttons, to raw text.
# The VALUE (e.g. #ffffff) of the radio buttons comes into the function.
# It goes straight back out, to the 'children' property of radio_display.
# Which, helpfully, immediately displays the thingy.
@app.callback(
    Output('radio_display', 'children'),
    Output('second_radio_display', 'children'),
    [Input('background_radio', 'value')])
def myfun(x):
    return x, x

# I want:
# The user hits a radio button
# A certain edge (between two certain nodes) becomes active, or inactive.
@app.callback(
    Output('net', 'data'),
    [Input('edge_radio', 'value')])
def edge_switcher(toggle):
    extra_edge = {'id': 'Extra', 'from': 'Temple of Time', 'to': 'Castle', 'weight': 4}
    if toggle == 'on':
        edges_out = edges + [extra_edge]
    else:
        edges_out = edges
    return {'nodes': nodes, 'edges': edges_out}

# @app.callback(
#     Output('net', 'options'),
#     [Input('background', 'value')])
# def myfun(x):
#     return {'nodes':{'color': x}}

# define main calling
if __name__ == '__main__':
    app.run_server(debug=True)