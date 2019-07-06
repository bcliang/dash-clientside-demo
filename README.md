# Dash Clientside Download

Demo Dash application implementing clientside downloads


## Installation

After cloning/downloading the repository, simply install this app as a package
into your target virtual environment:

    $ pip install .

During development you will likely want to perform an editable install so that
changes to the source code take immediate effect on the installed package.

    $ pip install -e .


## Running Your App

This project comes with two convenience scripts for running your project in
development and production environments, or you can use your own WSGI server to
run the app.


### run-app-dev

Installing this package into your virtualenv will result into the `run-app-dev`
executable being installed into the same virtualenv. This command invokes your
Dash app's `run_server` method, which in turn uses the Flask development server
to run your app.

    $ run-app-dev

The script takes a couple of arguments optional parameters, which you can
discover with the `--help`. You may need to set the port using the `--port`
parameter. If you need to expose your app outside your local machine, you will
want to set `--host 0.0.0.0`.


### run-app-prod

While convenient, the development webserver should *not* be used in
production. Installing this package will also result in the bash script
`run-app-prod` being installed in your virtualenv.

This is a wrapper around the `mod_wsgi-express` command, which
streamlines use of the [mod_wsgi Apache
module](https://pypi.org/project/mod_wsgi/) to run your your app. In addition to
installing the `mod_wsgi` Python package, you will need to have installed
Apache. See installation instructions in the [mod_wsgi
documentation](https://pypi.org/project/mod_wsgi/). Like its development
counterpart, `run-app-prod` takes a range of command line arguments, which
can be discovered with the `--help` flag.

    $ run-app-prod

`run-app-prod` will also apply settings found in the
module `dash_clientside_demo.prod_settings` (or a custom Python file
supplied with the `--settings` flag) and which take precedence over the same
settings found in `dash_clientside_demo.settings`.

A notable advantage of using `mod_wsgi` over other WSGI servers is that we do
not need to configure and run a web server separate to the WSGI server. When
using other WSGI servers (such as Gunicorn or uWSGI), you do not want to expose
them directly to web requests from the outside world for two reasons: 1)
incoming requests will not be buffered, exposing you to potential denial of
service attacks, and 2) you will be serving your static assets via Dash's Flask
instance, which is slow. `run-app-prod` uses `mod_wsgi-express` to spin up an
Apache process (separate to any process already running and listening on port
80) that will buffer requests, passing them off to the worker processes running
your app, and will also set up the Apache instance to serve your static assets
much faster than would be the case through the Python worker processes.

_Note:_ You will need to reinstall this package in order for changes to the
`run-app-prod` script to take effect even if you installed its an editable
install with (ie `pip install -e`).


### Running with a different WSGI Server

You can easily run your app using a WSGI server of your choice (such as Gunicorn
for example) with the `dash_clientside_app.wsgi` entry point
(defined in `wsgi.py`) like so:

    $ gunicorn dash_clientside_download.wsgi

_Note:_ if you want to enable Dash's debug mode while running with a WSGI server,
you'll need to export the `DASH_DEBUG` environment variable to `true`. See the
[Dev Tools](https://dash.plot.ly/devtools) section of the Dash Docs for more
details.
