# notes
"""
This file is for housing the main dash application.
This is where we define the various css items to fetch as well as the layout of our application.
"""

# package imports
import dash
from dash import html
import dash_bootstrap_components as dbc
from flask import Flask

# local imports
from src.components import footer, navbar
from src.utils.log import Log
from src.utils.settings import Settings


def serve_layout():
    """Define the layout of the application"""
    return html.Div(
        [
            navbar.navbar,
            dbc.Container(dash.page_container, class_name="my-2"),
            footer.footer,
        ]
    )


class App:
    def __init__(self) -> None:
        self.__server = Flask(__name__)
        self.__app = dash.Dash(
            __name__,
            server=self.__server,
            use_pages=True,  # turn on Dash pages
            meta_tags=[
                {  # check if device is a mobile device. This is a must if you do any mobile styling
                    "name": "viewport",
                    "content": "width=device-width, initial-scale=1",
                }
            ],
            # suppress_callback_exceptions=True,
            title="Encadeador",
            update_title="Carregando...",
            url_base_pathname=Settings.url_prefix,
        )
        self.__app.layout = (
            serve_layout  # set the layout to the serve_layout function
        )
        self.__server = (
            self.__app.server
        )  # the server is needed to deploy the application

    def serve(self):
        if Settings.mode == "DEV":
            self.__app.run(host="0.0.0.0", port=str(Settings.port), debug=True)
        elif Settings.mode == "PROD":
            self.__app.run(host="0.0.0.0", port=str(Settings.port))
