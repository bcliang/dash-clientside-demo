from collections import Counter
from textwrap import dedent

import dash_core_components as dcc
import dash_html_components as html

from ..app import app


def get_layout(**kwargs):
    initial_text = kwargs.get("text", "Type some text into me!")

    # Note that if you need to access multiple values of an argument, you can
    # use args.getlist("param")
    return html.Div([
        dcc.Markdown(
            dedent(
                """
                # `dash-clientside-demo`

                ## Introduction

                This demo implements a real-time bitcoin price (BTC-USD) tracker using Dash with clientside callbacks.

                ## Background

                Dash introduced clientside callbacks in version [0.41.0](https://github.com/plotly/dash/). This feature allows for faster interaction with the user, as callbacks no longer need to be communicated between client and server and can be handled entirely in javascript within the client browser. Some good candidates for this: registering UI actions, simple data processing tasks (e.g. moving average), and even large file downloads directly from the figure.

                I have found this to be particularly useful for real-time data applications. A typical consideration in design of data applications is separation of business logic (e.g. algorithms) from the application layer (interactions, display, etc). Clientside callbacks allow for sensitive business logic to stay on the server side (python callbacks), while everything else can potentially be implemented in the browser. This approach also will (typically) have secondary benefits of improved responsiveness (and significantly reduced overhead).

                ## Credits

                - Dash app boilerplate generated using [`slapdash`](https://github.com/ned2/slapdash).
                - Graphs use the [`dash-extendable-graph`](https://github.com/bcliang/dash-extendable-graph) component in place of `dcc.Graph`
                - Clientside data download implemented using `FileSaverJS`.
                - Clientside filter implemented using `KalmanJS`.

                ## eof

            """)
        ),
    ]
    )
