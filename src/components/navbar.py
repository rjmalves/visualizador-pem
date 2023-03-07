from dash import html, dcc, callback, Input, Output, State, ctx
import os
from src.utils.settings import Settings
from src.utils.log import Log
from src.components.login import User, login_info, login_location, login_user
from src.components.loadscreenmodal import LoadScreenModal
from src.components.savescreenmodal import SaveScreenModal
from dash.exceptions import PreventUpdate

navbar = html.Header(
    [
        html.Div(
            [
                html.Img(src="assets/link.jpg", className="logo"),
                html.Nav(
                    html.Ul(
                        [
                            html.Li(
                                html.A(
                                    "CASOS",
                                    href=os.path.join(
                                        Settings.url_prefix, "casos"
                                    ),
                                    className="navbar-link",
                                    id="casos-navbar-link",
                                )
                            ),
                            html.Li(
                                html.A(
                                    "ENCADEADOR",
                                    href=os.path.join(
                                        Settings.url_prefix, "encadeador"
                                    ),
                                    className="navbar-link",
                                    id="encadeador-navbar-link",
                                )
                            ),
                            html.Li(
                                html.A(
                                    "PPQ",
                                    href=os.path.join(
                                        Settings.url_prefix, "ppquente"
                                    ),
                                    className="navbar-link",
                                    id="ppquente-navbar-link",
                                )
                            ),
                        ],
                        className="navbar-links",
                    ),
                ),
                html.Div(login_info),
                login_location,
                dcc.Location(id="url"),
            ],
            className="navbar",
        ),
    ],
)


@callback(
    Output("casos-navbar-link", "className"),
    Input("url", "pathname"),
)
def update_active_casos_link(pathname: str):
    relpath = pathname.split(Settings.url_prefix)
    if any(["casos" in p for p in relpath]) or relpath[-1] == "":
        return "navbar-link active"
    else:
        return "navbar-link"


@callback(
    Output("encadeador-navbar-link", "className"),
    Input("url", "pathname"),
)
def update_active_encadeador_link(pathname: str):
    relpath = pathname.split(Settings.url_prefix)
    if any(["encadeador" in p for p in relpath]):
        return "navbar-link active"
    else:
        return "navbar-link"


@callback(
    Output("ppquente-navbar-link", "className"),
    Input("url", "pathname"),
)
def update_active_ppquente_link(pathname: str):
    relpath = pathname.split(Settings.url_prefix)
    if any(["ppquente" in p for p in relpath]):
        return "navbar-link active"
    else:
        return "navbar-link"
