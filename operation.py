import dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta

# Generate last 30 days from today - 1
last_30_days = [f"Day {i+1}" for i in range(30)]

# Sample battery data
batteries = [
    {"id": "Battery A", "status": "healthy", "best": 50, "normal": 30, "worst": 10,
     "last30Days": [2, 18, 16, 0, 12, 6, 4, 3, 2, 6, 7, 8, 9, 10, 11, 18, 17, 16, 12, 14, 15, 10, 9, 6, 7, 8, 2, 1, 4, 10]},
    {"id": "Battery B", "status": "problem", "best": 30, "normal": 40, "worst": 20,
     "last30Days": [1, 2, 3, 4, 5, 6, 10, 12, 14, 15, 16, 18, 17, 10, 8, 7, 6, 5, 10, 14, 18, 20, 16, 15, 14, 13, 6, 5, 8, 12]}
]

# Dash App
external_stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server
app.layout = html.Div(style={'backgroundColor': '#2E2E2E', 'minHeight': '100vh', 'padding': '20px'}, children=[
    # Header Section with Logo
    html.Div([
        html.Nav([
            html.Div([
                html.Div([
                    html.Img(src="/assets/logo.png", style={"height": "50px"})
                ], style={"flex": "1", "textAlign": "left"}),
                html.Div([
                    html.Ul([
                        html.Li(html.A("Logout", id="logout-button", className="waves-effect waves-light btn red darken-3"))
                    ], className="right")
                ], style={"flex": "1", "textAlign": "right"})
            ], style={"display": "flex", "alignItems": "center", "width": "100%"})
        ], className="nav-wrapper blue darken-3")
    ], className="container"),
    
    # Login Section
    html.Div(id='login-screen', children=[
        html.Div([
            html.H4("Login", className="center-align white-text"),
            html.Div([
                dcc.Input(id='username', type='text', placeholder='Enter username', className="input-field col s12"),
                dcc.Input(id='password', type='password', placeholder='Enter password', className="input-field col s12"),
                html.Button("Login", id='login-button', n_clicks=0, className="waves-effect waves-light btn green darken-3 col s12"),
                html.Div(id='login-output', className='red-text center-align mt-2')
            ], className="row")
        ], className="card-panel grey darken-3 white-text", style={"maxWidth": "400px", "margin": "auto", "padding": "20px"})
    ], className='container center-align', style={'marginTop': '100px'}),
    
    html.Div(id='dashboard', style={'display': 'none'}, children=[
        html.Div(className="container", children=[
            html.H1("Battery Monitoring Dashboard", className="center-align white-text"),
            
            # Search Bar
            html.Div(className="input-field", children=[
                dcc.Input(id='search-bar', type='text', placeholder='Search battery...', className="validate", debounce=True)
            ]),
            
             # Battery Selection
            html.Div(id='battery-container', className="row center-align", children=[
                html.Button("Battery A", id='battery-a', n_clicks=0, className="btn waves-effect waves-light green" if batteries[0]['status'] == 'healthy' else "btn waves-effect waves-light red"),
                html.Button("Battery B", id='battery-b', n_clicks=0, className="btn waves-effect waves-light green" if batteries[1]['status'] == 'healthy' else "btn waves-effect waves-light red")
            ]),
            
            # Stats Boxes
            html.Div(className="row", children=[
                html.Div("Best: 0 hrs", id='best-hours', className="col s4 card-panel", style={'background': '#90EE90', 'color': 'black'}),
                html.Div("Normal: 0 hrs", id='normal-hours', className="col s4 card-panel", style={'background': '#FFD580', 'color': 'black'}),
                html.Div("Worst: 0 hrs", id='worst-hours', className="col s4 card-panel", style={'background': '#FF9999', 'color': 'black'})
            ]),
            
            # Chart
            html.Div(className="card-panel", style={'backgroundColor': '#4E4E4E'}, children=[
                html.H2("Last 30 Days Usage in Hours", className="center-align white-text"),
                dcc.Graph(id='usageChart')
            ])
        ])
    ])
])

@app.callback(
    [Output('dashboard', 'style'), Output('login-screen', 'style')],
    [Input('login-button', 'n_clicks'), Input('logout-button', 'n_clicks')],
    [State('username', 'value'), State('password', 'value')]
)
def login_logout(n_clicks, logout_clicks, username, password):
    if ctx.triggered_id == 'login-button' and username == "admin" and password == "password":
        return {'display': 'block'}, {'display': 'none'}
    elif ctx.triggered_id == 'logout-button':
        return {'display': 'none'}, {'display': 'block'}
    return {'display': 'none'}, {'display': 'block'}

@app.callback(
    [Output('best-hours', 'children'), Output('normal-hours', 'children'), Output('worst-hours', 'children'),
     Output('usageChart', 'figure')],
    [Input('battery-a', 'n_clicks'), Input('battery-b', 'n_clicks')]
)
def update_dashboard(a_clicks, b_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        selected_battery = batteries[0]
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        selected_battery = batteries[0] if button_id == 'battery-a' else batteries[1]
    
    figure = {
        'data': [
            go.Bar(x=last_30_days, y=selected_battery['last30Days'],
                   marker_color=['#FF9999' if v > 15 else '#FFD580' if v > 7 else '#90EE90' for v in selected_battery['last30Days']],
                   name='Usage in Hours')
        ],
        'layout': go.Layout(title='Usage in Hours Over Last 30 Days', xaxis_title='Day', yaxis_title='Usage Hours',
                            plot_bgcolor='#4E4E4E', paper_bgcolor='#4E4E4E', font=dict(color='white'))
    }
    return f"Best: {selected_battery['best']} hrs", f"Normal: {selected_battery['normal']} hrs", f"Worst: {selected_battery['worst']} hrs", figure

if __name__ == '__main__':
    app.run_server(debug=True)
