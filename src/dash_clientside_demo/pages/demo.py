import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_extendable_graph as fig
from dash.dependencies import ClientsideFunction, Input, Output, State

from ..app import app


layout = html.Div("Page 2")

app.clientside_callback(
    ClientsideFunction('download', 'download'),
    Output('button-target', 'children'),
    [Input('button-download', 'n_clicks')],
    [State('sensor-signal', 'figure'),
     State('experiment-chart-label', 'children'),
     ]
)
