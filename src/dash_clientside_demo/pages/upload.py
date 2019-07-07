import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_extendable_graph as fig
from dash.dependencies import ClientsideFunction, Input, State, Output
import pandas as pd
import base64
import io

from ..app import app


def get_layout(**kwargs):
    initial_text = kwargs.get("text", "Type some text into me!")
    return html.Div([
        dbc.Container([
            dbc.Row([
                dcc.Markdown(
                    """
                # Upload File to Figure

                Upload a data file (single-row header), and then download the data out of the figure. This demo supports CSV and XLS file formats.

                You can find an example file in [`/examples/example_data.csv`](https://github.com/bcliang/dash-clientside-demo/blob/master/examples/example_upload_data.csv)

                This page is meant to demonstrate the ability of the clientside-based File download to exceeed browser size limitations.
                """)
            ], className="graph-header-row"),
            dbc.Row([
                dcc.Upload([dbc.Button("Upload CSV File")], id='upload-data')
            ], className="graph-header-row"),
            dbc.Row([
                dbc.Col(
                    fig.ExtendableGraph(
                        id='upload-signal',
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
                                showlegend=True,
                                uirevision='upload-signal-layout',
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
                dbc.Col([
                    dbc.Button('Download CSV', id='button-upload-download'),
                    html.Div(id='button-upload-target', style=dict(display='none'))
                ], style={'text-align': 'left'}),
            ], className="graph-options-row")
        ]),
    ])


"""
" Load CSV data into figure
"""

# file upload function


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            df = None
    except Exception as e:
        print(e)
        return None

    return df


@app.callback(Output('upload-signal', 'figure'),
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename')],
              [State('upload-signal', 'figure')])
def update_output(contents, filename, fig):
    if contents is not None:
        df = parse_contents(contents, filename)

        if df is not None:
            if 'timestamp' in df.columns:
                df.set_index('timestamp', inplace=True)

            data = []
            for col in df.columns:
                data.append(
                    dict(x=df.index.values,
                         y=df[col].values,
                         name=col)
                )
            fig['data'] = data
            fig['layout']['title'] = filename
            return fig
        else:
            return dash.no_update
    else:
        return dash.no_update


"""
" Download Figure Data
"""
# FileSaverJS supports 500MB downloads from the browser!
app.clientside_callback(
    ClientsideFunction('download', 'csvDownload'),
    Output('button-upload-target', 'children'),
    [Input('button-upload-download', 'n_clicks')],
    [State('upload-signal', 'figure')]
)
