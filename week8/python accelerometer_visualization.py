import requests
import time
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objs as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

client_id = 'sVZxD1HXodmnW1hxOlH5do7BuLAxgTza'
client_secret = 'q84umsgq7B2bAqGhmXn9vC0H12VOqblPpWB8wy1QzVkOyipFSG07e0rCdf5AT5n6'
thing_id = '2f2ff316-eb9a-41fd-b377-7b157b0bcdf0'
token_url = "https://api2.arduino.cc/iot/v1/clients/token"

def get_access_token():
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'audience': 'https://api2.arduino.cc/iot'
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        access_token = response.json()['access_token']
        print(f"Access Token: {access_token}")
        return access_token
    else:
        raise Exception(f"Failed to get access token: {response.text}")

def read_variable(access_token, variable_id):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    url = f"https://api2.arduino.cc/iot/v2/things/{thing_id}/properties/{variable_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['last_value']
    else:
        raise Exception(f"Failed to get variable: {response.text}")

def collect_data_and_visualize():
    access_token = get_access_token()
    x_data = []
    y_data = []
    z_data = []

    app = Dash(__name__)

    app.layout = html.Div([
        html.H1("Real-time Accelerometer Data Visualization"),
        dcc.Graph(id='live-graph'),
        dcc.Interval(
            id='graph-update',
            interval=2000,
            n_intervals=0
        )
    ])

    @app.callback(Output('live-graph', 'figure'), [Input('graph-update', 'n_intervals')])
    def update_graph_live(n):
        x_variable_id = '7c699472-185e-4443-937f-4e95421f2213'
        y_variable_id = '9347588a-9da5-43ff-8e30-e6d4f990c35e'
        z_variable_id = 'b81b3ea8-d9e4-4ebf-9368-eece53d8fdd1'

        try:
            Accelerometer_X = read_variable(access_token, x_variable_id)
            Accelerometer_Y = read_variable(access_token, y_variable_id)
            Accelerometer_Z = read_variable(access_token, z_variable_id)

            print(f"X: {Accelerometer_X}, Y: {Accelerometer_Y}, Z: {Accelerometer_Z}")

        except Exception as e:
            print(f"Error reading variables: {e}")
            return go.Figure()

        x_data.append(Accelerometer_X)
        y_data.append(Accelerometer_Y)
        z_data.append(Accelerometer_Z)

        data = {'x': x_data, 'y': y_data, 'z': z_data}
        df = pd.DataFrame(data)

        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=('X', 'Y', 'Z'))

        fig.add_trace(go.Scatter(y=df['x'], mode='lines', name='X-Axis'), row=1, col=1)
        fig.add_trace(go.Scatter(y=df['y'], mode='lines', name='Y-Axis'), row=2, col=1)
        fig.add_trace(go.Scatter(y=df['z'], mode='lines', name='Z-Axis'), row=3, col=1)

        fig.update_yaxes(range=[-1, 1], row=1, col=1)
        fig.update_yaxes(range=[-1, 1], row=2, col=1)
        fig.update_yaxes(range=[-1, 1], row=3, col=1)

        fig.update_layout(title='Accelerometer Data', height=800)
        return fig

    app.run_server(debug=True)

if __name__ == '__main__':
    collect_data_and_visualize()
