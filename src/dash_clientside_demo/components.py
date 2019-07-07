import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask import current_app as server

from .utils import get_url, component


def fa(className):
    """A convenience component for adding Font Awesome icons"""
    return html.I(className=className)


@component
def make_dropdown(component_id, label, optionlabels, optionvals, default=None, msg_help=None):
    def convert_options(optionlabels, optionvals):
        return [dict(label=x, value=y) for x, y in zip(optionlabels, optionvals)]

    if not default:
        default = optionvals[0]

    elts = [
        dbc.Label(label, html_for=component_id),
        dcc.Dropdown(
            id=component_id,
            options=convert_options(optionlabels, optionvals),
            value=default,
            searchable=False,
            clearable=False
        ),
    ]
    if msg_help:
        elts.append(dbc.FormText(msg_help, color="secondary"))

    return dbc.FormGroup(elts)


@component
def make_brand(**kwargs):
    return html.Header(
        className="brand",
        children=dcc.Link(
            href=get_url(""),
            children=html.H3([fa("far fa-chart-bar"), server.config["TITLE"]]),
        ),
        **kwargs,
    )


@component
def make_header(**kwargs):
    return dbc.Navbar(
        id="header",
        className="sticky-top",
        color="dark",
        dark=True,
        children=[
            make_brand(),
            html.Ul(
                id=server.config["NAVBAR_CONTAINER_ID"], className="navbar-nav ml-auto"
            ),
        ],
        **kwargs,
    )


@component
def make_sidebar(**kwargs):
    return html.Nav(
        id=f"sidebar",
        className="nav navbar-dark bg-dark flex-column align-items-start",
        children=[make_brand(), html.Div(id=server.config["NAVBAR_CONTAINER_ID"])],
        **kwargs,
    )
