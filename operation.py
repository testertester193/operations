# Sample Python File for Project Ganesha
# Sample Python File for Project Ganesha
import dash
from dash import dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import flask
import os

# Initialize Dash app
server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], server=server, suppress_callback_exceptions=True)

# Fake user credentials
VALID_USERNAME = "Kevin"
VALID_PASSWORD = "password"

# Header with logo and user dropdown
header = dbc.Navbar([
    dbc.Row([
        dbc.Col(html.Img(src="/assets/logo.png", height="50px")),
        dbc.Col(html.H2("Company Name", className="ml-2"))
    ], align="center", className="g-0"),
    dbc.NavbarToggler(id="navbar-toggler"),
    dbc.DropdownMenu([
        dbc.DropdownMenuItem("Logout", id="logout", n_clicks=0)
    ], nav=True, in_navbar=True, label="Admin")
], color="dark", dark=True, className="mb-4")

# Footer
footer = html.Footer(
    "© 2025 Company Name. All rights reserved.",
    style={"textAlign": "center", "padding": "10px", "backgroundColor": "#f8f9fa", "marginTop": "20px"}
)

# Layout for Login Page
login_layout = dbc.Container([
    dbc.Row(dbc.Col(html.H2("Login", className="text-center"), width=12)),
    dbc.Row([
        dbc.Col([
            dbc.Input(id="username", placeholder="Enter Username", type="text", className="mb-2"),
            dbc.Input(id="password", placeholder="Enter Password", type="password", className="mb-2"),
            dbc.Button("Login", id="login-button", color="primary", className="mb-2", n_clicks=0),
            html.Div(id="login-output", className="text-danger"),
            # Hidden dummy logout button to prevent missing ID error
            html.Button(id="logout", style={"display": "none"})
        ], width=6)
    ], justify="center")
])

# Driver Dashboard with Charts
def driver_dashboard():
    battery_chart = go.Figure()
    battery_chart.add_trace(go.Bar(x=['Best', 'Normal', 'Worst'], y=[50, 60, 40], marker_color=['green', 'yellow', 'red']))
    battery_chart.update_layout(title='Battery Usage Over Last 30 Days', xaxis_title='Usage Category', yaxis_title='Cost ($)')

    return html.Div([
        html.H2("Driver Dashboard", className="text-center"),
        dbc.Row([
            dbc.Col(dbc.Card(html.Div("Battery Usage: 80%", className="p-3 text-white bg-primary text-center"), className="m-2")),
            dbc.Col(dbc.Card(html.Div("Remaining Balance: $25", className="p-3 text-white bg-primary text-center"), className="m-2")),
            dbc.Col(dbc.Card(html.Div("Total Cost Last 30 Days: $150", className="p-3 text-white bg-primary text-center"), className="m-2"))
        ]),
        dcc.Graph(figure=battery_chart)
    ])

# Fleet Manager Dashboard with Charts
def fleet_manager_dashboard():
    transaction_chart = go.Figure()
    transaction_chart.add_trace(go.Bar(x=['2025-02-01', '2025-02-02', '2025-02-03'], y=[5, 7, 10], marker_color='blue'))
    transaction_chart.update_layout(title='Transaction Costs Over Last 3 Days', xaxis_title='Date', yaxis_title='Cost ($)')
    
    return html.Div([
        html.H2("Fleet Manager Dashboard", className="text-center"),
        dbc.Input(id="driverId", placeholder="Enter Driver ID", type="text", className="mb-2"),
        dbc.Button("Search", id="fetch-driver", color="primary", className="mb-2", n_clicks=0),
        html.Div(id="driver-info"),
        html.H3("Transaction History"),
        dbc.Table(bordered=True, hover=True, id="transaction-history"),
        dcc.Graph(figure=transaction_chart)
    ])

# Convert Operations Team UI to Dash Components
def operations_team_dashboard():
    return html.Div([
        html.H2("Battery Monitoring Dashboard", className="text-center"),
        dbc.Input(id="search-bar", placeholder="Search battery...", type="text", className="mb-2"),
        html.Div(id="battery-container"),
        dbc.Row([
            dbc.Col(html.Div("Best: 0 hrs", id="best-hours", className="p-3 bg-light text-center")),
            dbc.Col(html.Div("Normal: 0 hrs", id="normal-hours", className="p-3 bg-light text-center")),
            dbc.Col(html.Div("Worst: 0 hrs", id="worst-hours", className="p-3 bg-light text-center"))
        ])
    ])

# Layout for Main Dashboard
main_layout = dbc.Container([
    header,
    dcc.Tabs(id="tabs", value="driver", children=[
        dcc.Tab(label="Driver Dashboard", value="driver"),
        dcc.Tab(label="Fleet Manager", value="fleet"),
        dcc.Tab(label="Operations Team", value="operations")
    ]),
    html.Div(id="content"),
    footer
], fluid=True)

# App layout
app.layout = html.Div(id="page-content", children=[login_layout])

# Single Callback for Login and Logout
@app.callback(
    Output("page-content", "children"),
    [Input("login-button", "n_clicks"), Input("logout", "n_clicks")],
    [State("username", "value"), State("password", "value")],
    prevent_initial_call=True
)
def login_logout_handler(login_clicks, logout_clicks, username, password):
    trigger = ctx.triggered_id
    
    if trigger == "login-button":
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            return main_layout
        return login_layout
    
    if trigger == "logout":
        return login_layout
    
    return login_layout

@app.callback(
    Output("content", "children"),
    Input("tabs", "value")
)
def render_tab(tab_name):
    if tab_name == "driver":
        return driver_dashboard()
    elif tab_name == "fleet":
        return fleet_manager_dashboard()
    elif tab_name == "operations":
        return operations_team_dashboard()
    return "Select a tab to display content."

# Run server
if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)
