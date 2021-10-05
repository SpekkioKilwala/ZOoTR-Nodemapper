"""
Author: Mohit Mayank

Idea: Plot Game of Thrones network using Visdcc in Dash.

PLUS: Comments, but NO modifications, by Spekkio to understand what the heck it does.
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

# Pandas has a function to read a CSV straight into a dataframe.
# Note it's only using the first csv; there's 5 in the given folder.
# The first row becomes column labels, and indexes (aka row labels?) are automatically supplied.
df = pd.read_csv("data/book1.csv")
# This is clearly a filter to only keep rows that have a weight > 10.
# From the first df... create a new little dataframe where each row is..
# ...only present if its 'weight' is greater than 10. And all the columns remain.
# Something like df['weight'] gives you back a Series, by the way. It's like a list with a label.
df = df.loc[df['weight']>10, :]
# We are getting a list. Every unique name in Sources, plus every unique name in Targets, added together.
# And then make that into a set and then back into a list just to filter out the duplicates.
# ...I'm sure that's not the most elegant wording.
# I think I would grab the Series' values, add THOSE, then filter for uniques, then convert to list.
node_list = list(set(df['Source'].unique().tolist() + df['Target'].unique().tolist()))
# And now we are creating a... list of nodes.
# Each element (each node) in the list is a DICT.
# Each dict (each node) gets created with certain key-value pairs.
# We enumerate() over node_list, doing list-comprehension on the iterable.
# So they get an 'id' (required), a 'label', a 'shape' (all of them dots) and a 'size' (all 7.)
nodes = [{'id': node_name, 'label': node_name, 'shape': 'dot', 'size': 7} for i, node_name in enumerate(node_list)]
# create edges from df
# Create empty list, and we'll add to that...
# You could also do this with a list comprehension.
# Even so.
# First step is to use df.to_dict.
# It gives you a LIST where each row has been converted to dict form.
# e.g. {'Source': 'Addam-Marbrand', 'Target': 'Jaime-Lannister', 'Type': 'Undirected', 'weight': 3, 'book': 1}
# And from this dict we are constructing a different, reformatted dict, with keys: id, from, to, and width.
# These lists-of-dicts are formatted in such a way that visdcc can make sense of it.
edges = []
for row in df.to_dict(orient='records'):
    source, target = row['Source'], row['Target']
    edges.append({
        'id': source + "__" + target,
        'from': source,
        'to': target,
        'width': 2,
    })

# define layout
app.layout = html.Div([
    # Create a network object! The 'data' parameter is a dict, specifying the node and edge lists we created above.
    visdcc.Network(id = 'net',
                    data = {'nodes': nodes, 'edges': edges},
                    options = dict(height= '600px', width= '100%')),
    # Create a radio-button that selects between three colours, on the id "color"
    dcc.RadioItems(id = 'color',
                    options=[{'label': 'Red'  , 'value': '#ff0000'},
                            {'label': 'Green', 'value': '#00ff00'},
                            {'label': 'Blue' , 'value': '#0000ff'} ],
                    value='Red'  )
])

# define callback
# For some reason, the inputs seem to have to be in a list.
# If I had multiple outputs, would they be in a list too?
# So the actual chain here is:
# It's attached to the 'value' member of the 'color' object (the radio-button.)
#   Which is going to be either '#ff0000', '00ff00', or '0000ff'
# Whenever that changes, the function runs.
# It creates dict-in-a-dict. It's right for setting the COLOUR of the NODES in a Network object.
# And that gets handed back to the options of net.
# Part of me wants to know if the options are "overwritten" or if it's more of an "added" situation.
# And I now think it's an arbitrary distinction.
@app.callback(
    Output('net', 'options'),
    [Input('color', 'value')])
def myfun(x):
    return {'nodes':{'color': x}}

# define main calling
if __name__ == '__main__':
    app.run_server(debug=True)
