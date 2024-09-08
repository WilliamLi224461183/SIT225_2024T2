import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

data = pd.read_csv(r'C:\Users\ausle\Documents\Data\week6\sensor_data.csv')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Temperature and Humidity Data Visualization"),

    html.Label("Select Graph Type"),
    dcc.Dropdown(
        id='graph-type',
        options=[
            {'label': 'Scatter Plot', 'value': 'scatter'},
            {'label': 'Line Chart', 'value': 'line'},
            {'label': 'Distribution Plot', 'value': 'distribution'}
        ],
        value='scatter'
    ),

    html.Label("Select Variable (Temperature, Humidity)"),
    dcc.Dropdown(
        id='variable-select',
        options=[
            {'label': 'Temperature', 'value': 'Temperature'},
            {'label': 'Humidity', 'value': 'Humidity'},
            {'label': 'Both', 'value': 'both'}
        ],
        value='both',
        multi=False
    ),

    html.Label("Enter Number of Samples"),
    dcc.Input(id='sample-size', type='number', value=100),

    html.Button('Previous', id='prev-button', n_clicks=0),
    html.Button('Next', id='next-button', n_clicks=0),

    dcc.Graph(id='data-graph'),

    html.Div(id='summary-table')
])


@app.callback(
    [Output('data-graph', 'figure'),
     Output('summary-table', 'children')],
    [Input('graph-type', 'value'),
     Input('variable-select', 'value'),
     Input('sample-size', 'value'),
     Input('prev-button', 'n_clicks'),
     Input('next-button', 'n_clicks')]
)
def update_graph(graph_type, variable, sample_size, prev_clicks, next_clicks):
    start_index = max(0, prev_clicks - next_clicks) * sample_size
    end_index = start_index + sample_size

    filtered_data = data.iloc[start_index:end_index]

    fig = go.Figure()

    if variable == 'Temperature' or variable == 'both':
        if graph_type == 'scatter':
            fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data['Temperature'], mode='markers', name='Temperature'))
        elif graph_type == 'line':
            fig.add_trace(go.Line(x=filtered_data.index, y=filtered_data['Temperature'], name='Temperature'))
        elif graph_type == 'distribution':
            fig = px.histogram(filtered_data, x='Temperature', nbins=30)

    if variable == 'Humidity' or variable == 'both':
        if graph_type == 'scatter':
            fig.add_trace(go.Scatter(x=filtered_data.index, y=filtered_data['Humidity'], mode='markers', name='Humidity'))
        elif graph_type == 'line':
            fig.add_trace(go.Line(x=filtered_data.index, y=filtered_data['Humidity'], name='Humidity'))
        elif graph_type == 'distribution':
            fig = px.histogram(filtered_data, x='Humidity', nbins=30)

    fig.update_layout(title="Temperature and Humidity Data", xaxis_title="Samples", yaxis_title="Value")

    summary_table = html.Table([
        html.Tr([html.Th(col) for col in ['Temperature', 'Humidity']]),
        html.Tr([html.Td(filtered_data['Temperature'].describe().to_dict()), html.Td(filtered_data['Humidity'].describe().to_dict())])
    ])

    return fig, summary_table


if __name__ == '__main__':
    app.run_server(debug=True)
