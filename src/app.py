# notes
"""
This file is for housing the main dash application.
This is where we define the various css items to fetch as well as the layout of our application.
"""

# package imports
import dash
from dash import html
import dash_bootstrap_components as dbc
from waitress import serve
from flask_login import LoginManager

# local imports
from src.components import footer, navbar
from src.components.login import User

from src.utils.settings import Settings


def serve_layout():
    """Define the layout of the application"""
    return html.Div(
        [
            navbar.navbar,
            dbc.Container(dash.page_container),
            footer.footer,
        ]
    )


class App:
    def __init__(self) -> None:
        self.__app = dash.Dash(
            __name__,
            use_pages=True,
            # suppress_callback_exceptions=True,
            title="Visualizador",
            update_title="Carregando...",
            url_base_pathname=Settings.url_prefix,
        )
        self.__app.server.config.update(SECRET_KEY=Settings.secret_key)

        self.__login_manager = LoginManager()
        self.__login_manager.init_app(self.__app.server)

        @self.__login_manager.user_loader
        def load_user(username):
            """This function loads the user by user id. Typically this looks up the user from a user database.
            We won't be registering or looking up users in this example, since we'll just login using LDAP server.
            So we'll simply return a User object with the passed in username.
            """
            return User(username)

        self.__app.layout = serve_layout

    def serve(self):
        if Settings.mode == "DEV":
            self.__app.run(host="0.0.0.0", port=str(Settings.port), debug=True)
        elif Settings.mode == "PROD":
            serve(
                self.__app.server,
                host="0.0.0.0",
                port=str(Settings.port),
                threads=2,
            )
