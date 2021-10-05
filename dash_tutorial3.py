import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H6("Change the value in the text box to see callbacks in action!"),
    html.Div([
        "Input: ",
        # Placing a Dash Core Component textbox-input here.
        # It has a unique ID and an initial input set.

        dcc.Input(id='my-input', value='initial value', type='text')
    ]),
    html.Br(),
    # And this is just some html text with another unique ID.
    # It doesn't even supply an initial value here.
    html.Div(id='my-output'),

    html.Div(id='test-output', children="This is test data")

])

# And here's where the magic happens.
# The first part to understand is the function below.
# It's simple. It takes an input and put it inside a string.
# The new part is the callback decorator!
# This defines that the input of this function is the ID = "my-input" textbox.
# And it defines that the output is "my-output"... children?
# Ok I can see how that works.
# You should probably have as many inputs as your function requires.
@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)

# So the spine of this all is...
# You declare the existence of the app object.
# You import data, make a dataframe, display that in a figure.
# You declare the layout of the page, including where the figure is.
# You can write whatever functions you like.
# Functions for relations between data behind-the-scenes, and the decorator to link it to page elements.

# There's two different things here called Input, don't confuse them.
# dcc.Input is an element on the page.
# the Input from Dash Dependencies is just used inside the decorator.

# There's a new, critical takeaway from all this.
# Notice that everything is defined in terms of ID and Component Property.
# That function returns one thing, and it's aimed at a particular property of a particular component.
# Therefore, your functions can change ANY property of ANYTHING on the page.

# (OK, what if I want a general function?)
# Like one that will change the property of a lot of different things the same way.
#   If I have an unchanging list of outputs, then I can just write all of them.
# Do I have a valid case where I'd want a list of outputs to grow or shrink?

# Surely I can give the decorator a string EXPRESSION, rather than a string in itself?
# But, do I want to? Do I need to?

if __name__ == '__main__':
    app.run_server(debug=True)