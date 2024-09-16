import requests
import time
import pandas as pd
import plotly.graph_objs as go
from dash import dcc, html, dash
from dash.dependencies import Input, Output

# New Client ID and Secret from PDF
client_id = 'ZcBTV3tDI7o7spWpttS1aqCC3bXGf2V8'
client_secret = 'r8JorkGA1YJXAT08jm4pet6S081cMV6zUPxD4NHqI1Tzw2KhpDLPy04VVLNhTwgR'
thing_id = '91b555d9-f122-4f47-86ff-07544220d279'
token_url = 'https://api2.arduino.cc/iot/v1/clients/token'
api_url = f'https://api2.arduino.cc/iot/v2/things/{thing_id}/properties'

# Function to get access token
def get_access_token():
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'audience': 'https://api2.arduino.cc/iot'
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        token = response.json()['access_token']
        return token
    else:
        print(f"Failed to get token: {response.status_code}")
        return None

# Function to get accelerometer data
def get_accelerometer_data():
    token = get_access_token()
    if not token:
        return None, None, None
    
    headers = {
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("Full JSON response:", data)

        # Filter the data to only capture Accelerometer X, Y, and Z
        accelerometer_data = {prop['name']: prop['last_value'] for prop in data if prop['name'] in ['Accelerometer_X', 'Accelerometer_Y', 'Accelerometer_Z']}
        
        accelerationX = accelerometer_data.get('Accelerometer_X')
        accelerationY = accelerometer_data.get('Accelerometer_Y')
        accelerationZ = accelerometer_data.get('Accelerometer_Z')

        return accelerationX, accelerationY, accelerationZ
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None, None, None

app = dash.Dash(__name__)

df = pd.DataFrame({'time': [], 'x': [], 'y': [], 'z': []})

app.layout = html.Div([
    html.H1("Live Accelerometer Data"),
    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(
        id='interval-component',
        interval=1000,  # Update interval every second
        n_intervals=0
    )
])

@app.callback(Output('live-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    global df
    x, y, z = get_accelerometer_data()

    if x is not None and y is not None and z is not None:
        new_data = {'time': [time.time()], 'x': [x], 'y': [y], 'z': [z]}
        df = pd.concat([df, pd.DataFrame(new_data)])
        df = df.iloc[-1000:]  # Keep only the last 1000 rows to avoid memory overflow

    figure = go.Figure()
    figure.add_trace(go.Scatter(x=df['time'], y=df['x'], mode='lines', name='X'))
    figure.add_trace(go.Scatter(x=df['time'], y=df['y'], mode='lines', name='Y'))
    figure.add_trace(go.Scatter(x=df['time'], y=df['z'], mode='lines', name='Z'))

    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
