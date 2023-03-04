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


@callback(
    Output("page-location", "pathname"),
    Input("login-button", "n_clicks"),
    Input(
        LoadScreenModal.ids.confirm_load_screen_btn("casos-load-screen-modal"),
        "n_clicks",
    ),
    Input(
        SaveScreenModal.ids.confirm_save_screen_btn("casos-save-screen-modal"),
        "n_clicks",
    ),
    Input(
        LoadScreenModal.ids.confirm_load_screen_btn(
            "encadeador-load-screen-modal"
        ),
        "n_clicks",
    ),
    Input(
        SaveScreenModal.ids.confirm_save_screen_btn(
            "encadeador-save-screen-modal"
        ),
        "n_clicks",
    ),
    Input(
        LoadScreenModal.ids.confirm_load_screen_btn("ppq-load-screen-modal"),
        "n_clicks",
    ),
    Input(
        SaveScreenModal.ids.confirm_save_screen_btn("ppq-save-screen-modal"),
        "n_clicks",
    ),
    State("login-username", "value"),
    State("login-password", "value"),
    State("_pages_location", "pathname"),
    State(
        LoadScreenModal.ids.load_screen_select("casos-load-screen-modal"),
        "value",
    ),
    State(
        SaveScreenModal.ids.new_screen_name("casos-save-screen-modal"),
        "value",
    ),
    State(
        LoadScreenModal.ids.load_screen_select("encadeador-load-screen-modal"),
        "value",
    ),
    State(
        SaveScreenModal.ids.new_screen_name("encadeador-save-screen-modal"),
        "value",
    ),
    State(
        LoadScreenModal.ids.load_screen_select("ppq-load-screen-modal"),
        "value",
    ),
    State(
        SaveScreenModal.ids.new_screen_name("ppq-save-screen-modal"),
        "value",
    ),
    prevent_initial_call=True,
)
def redirect_page(
    login_n_clicks,
    casos_load_screen_confirm_click,
    casos_save_screen_confirm_click,
    encadeador_load_screen_confirm_click,
    encadeador_save_screen_confirm_click,
    ppq_load_screen_confirm_click,
    ppq_save_screen_confirm_click,
    username,
    password,
    pathname,
    casos_load_screen_value,
    casos_save_screen_name,
    encadeador_load_screen_value,
    encadeador_save_screen_name,
    ppq_load_screen_value,
    ppq_save_screen_name,
):
    if ctx.triggered_id == "login-button":
        if login_n_clicks is not None:
            if login_n_clicks > 0:
                if username == Settings.user and password == Settings.password:
                    login_user(User(username))
                    Log.log().info(
                        f"LOGIN: Sucesso. Usuario: {username} - {pathname}"
                    )
                    return Settings.url_prefix
                return pathname
        raise PreventUpdate
    elif ctx.triggered_id == LoadScreenModal.ids.confirm_load_screen_btn(
        "casos-load-screen-modal"
    ):
        if casos_load_screen_confirm_click is not None:
            if casos_load_screen_confirm_click > 0:
                pass
    elif ctx.triggered_id == SaveScreenModal.ids.confirm_save_screen_btn(
        "casos-save-screen-modal"
    ):
        if casos_save_screen_confirm_click is not None:
            if casos_save_screen_confirm_click > 0:
                pass
