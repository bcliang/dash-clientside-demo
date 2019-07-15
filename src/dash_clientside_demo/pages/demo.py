import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_extendable_graph as fig
from dash.dependencies import ClientsideFunction, Input, Output, State

from ..app import app
from ..utils import get_url
from ..components import make_dropdown
from datetime import datetime
import json
import requests


def get_layout(**kwargs):
    initial_text = kwargs.get("text", "Type some text into me!")

    # Note that if you need to access multiple values of an argument, you can
    # use args.getlist("param")
    return html.Div([
        dbc.Container([
            dbc.Row([
                dcc.Markdown(
                    """
                    # BTC-USD Chart

                    This page shows a live-streaming graph. The dropdowns and buttons use clientside callbacks for improved responsiveness.

                    *Note* The "Import Price History" button fetches a file from the application's web-accessible "assets" folder.
                    """
                ),
                dcc.Interval(id='btc-signal-interval',
                             interval=5000,  # 1 min
                             max_intervals=-1
                             )
            ], className="graph-header-row"),
            dbc.Row([
                dbc.Col(
                    fig.ExtendableGraph(
                        id='btc-signal',
                        config=dict(
                            showAxisDragHandles=True,
                            showAxisRangeEntryBoxes=True,
                            modeBarButtonsToRemove=[
                                'sendDataToCloud',
                                'lasso2d',
                                'autoScale2d',
                                'hoverClosestCartesian',
                                'hoverCompareCartesian',
                                'toggleSpikelines'
                            ],
                            displaylogo=False,
                        ),
                        figure=dict(
                            data=[],
                            layout=dict(
                                title='BTC-USD Spot Price (Coinbase)',
                                showlegend=True,
                                uirevision='btc-signal-layout',
                                legend={
                                    'orientation': 'h',
                                    'xanchor': 'right',
                                    'yanchor': 'top',
                                    'x': 0.98,
                                    'y': 1.05,
                                },
                            )
                        )
                    ),
                ),
            ], className="graph-content-row"),
            dbc.Row([
                dbc.Col('namespace: ui', style={'text-align': 'right'}),
                dbc.Col(
                    make_dropdown('btc-dropdown-zoom',
                                  'Zoom Mode',
                                  ['Scale', '5 min', '30 min', '1 hour', '3 hours', '12 hours', '1 day', '7 days'],
                                  [0, 5 / 60 / 24, 30 / 60 / 24, 1 / 24, 3 / 24, .5, 1, 7]),
                ),
                dbc.Col(
                    make_dropdown('btc-dropdown-title',
                                  'Chart Title',
                                  ['BTC-USD', '+ latest timestamp', '+ latest value'],
                                  [0, 1, 2]),
                ),
                dbc.Col(
                    make_dropdown('btc-dropdown-refresh',
                                  'Refresh Rate',
                                  ['1 sec', '2 sec', '5 sec (default)', '60 sec'],
                                  [1000, 2000, 5000, 60000],
                                  5000),
                ),
                html.Div(id='ui-relayout-target', style=dict(display='none')),
            ], className='ui-row'),
            dbc.Row([
                dbc.Col('namespace: download', style={'text-align': 'right'}),
                dbc.Col([
                    dbc.Button('Download CSV', id='button-csv-download'),
                    html.Div(id='button-csv-target', style=dict(display='none'))
                ], style={'text-align': 'left'}),
                dbc.Col([
                    dbc.Button('Download JSON', id='button-json-download'),
                    html.Div(id='button-json-target', style=dict(display='none'))
                ], style={'text-align': 'left'}),
                dbc.Col([
                    dbc.Button('Import Price History', id='button-history-download'),
                    html.Div(id='button-history-target', style=dict(display='none'))
                ], style={'text-align': 'left'})
            ], className='ui-row'),
        ]),
    ])

    """
        dbc.Row([
            dbc.Col('namespace: signal', style={'text-align': 'right'}),
            dbc.Col(
                make_dropdown('btc-dropdown-filter',
                              'Filter',
                              ['mavg(10)', 'kalman'],
                              [0, 1])
            ),
            html.Div(id='filter-target', style=dict(display='none')),
        ]),
        """


"""
" Python Callbacks contain business logic.
"""


def check_coinbase_price(request_time=None):
    if request_time is None:
        request_time = datetime.utcnow().isoformat(' ')[:22]

    response = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot')
    if not response:
        return {}
    response = response.json()
    output = dict(x=[request_time], y=[float(response['data']['amount'])])
    return output


@app.callback(
    Output('btc-signal', 'extendData'),
    [Input('btc-signal-interval', 'n_intervals')],
    [State('btc-signal', 'figure')]
)
def request_current_price(n_clicks, fig):
    "we should execute our top-secret business logic here"
    # check the coindesk bpi api
    # response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    output = check_coinbase_price()

    # you might normally do-something with the price signal here

    if len(fig['data']) == 0:
        output['name'] = 'BPI'
        output['type'] = 'scattergl',
        output['mode'] = 'lines+markers'
    return [output]


"""
" Clientside callbacks are exposed to the browser. Use them for UI actions and other generic functionality
"""

""" UI Actions """
app.clientside_callback(
    ClientsideFunction('ui', 'disable'),
    Output('button-history-download', 'disabled'),
    [Input('button-history-download', 'n_clicks')]
)

app.clientside_callback(
    ClientsideFunction('ui', 'value'),
    Output('btc-signal-interval', 'interval'),
    [Input('btc-dropdown-refresh', 'value')]
)

app.clientside_callback(
    ClientsideFunction('ui', 'relayout'),
    Output('ui-relayout-target', 'children'),
    [Input('btc-signal', 'extendData'),
     Input('btc-dropdown-zoom', 'value'),
     Input('btc-dropdown-title', 'value')],
    [State('btc-signal', 'figure')]
)

""" Download Actions """
# FileSaverJS supports >500MB downloads from the browser!
# csvDownload runs figDataToStr(), converting a figure's timeseries data into a table (x,y1,y2,y...)
# note: assumes all traces are scatter format (x,y) and that all traces share the same x-values.
app.clientside_callback(
    ClientsideFunction('download', 'csvDownload'),
    Output('button-csv-target', 'children'),
    [Input('button-csv-download', 'n_clicks')],
    [State('btc-signal', 'figure')]
)

# json stringify the figure object; works for any type of Graph trace(s)
app.clientside_callback(
    ClientsideFunction('download', 'jsonDownload'),
    Output('button-json-target', 'children'),
    [Input('button-json-download', 'n_clicks')],
    [State('btc-signal', 'figure')]
)

# Use JS to fetch files
app.clientside_callback(
    ClientsideFunction('download', 'loadHistorical'),
    Output('button-history-target', 'children'),
    [Input('button-history-download', 'n_clicks')],
    [State('btc-signal', 'extendData')]
)

""" Simple Operations (basic signal processing) """
# TODO
