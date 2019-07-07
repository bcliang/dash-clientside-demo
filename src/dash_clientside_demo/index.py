import dash_html_components as html

from .app import app
from .utils import DashRouter, DashNavBar
from .pages import intro, demo, upload
from .components import fa


# Ordered iterable of routes: tuples of (route, layout), where 'route' is a
# string corresponding to path of the route (will be prefixed with Dash's
# 'routes_pathname_prefix' and 'layout' is a Dash Component.
urls = (
    ("", intro.get_layout),
    ("intro", intro.get_layout),
    ("demo", demo.get_layout),
    ("upload", upload.get_layout),
)

# Ordered iterable of navbar items: tuples of `(route, display)`, where `route`
# is a string corresponding to path of the route (will be prefixed with
# 'routes_pathname_prefix') and 'display' is a valid value for the `children`
# keyword argument for a Dash component (ie a Dash Component or a string).
nav_items = (
    ("intro", html.Div([fa("fas fa-keyboard"), "Introduction"])),
    ("demo", html.Div([fa("fas fa-chart-area"), "Real-time"])),
    ("upload", html.Div([fa("fas fa-chart-line"), "Upload"])),
)

router = DashRouter(app, urls)
navbar = DashNavBar(app, nav_items)
