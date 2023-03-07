from flask_login import UserMixin, current_user, logout_user, login_user


from dash import (
    Output,
    Input,
    State,
    html,
    dcc,
    callback,
    ctx,
    no_update,
)
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from src.utils.settings import Settings
from src.utils.log import Log
from src.components.loadscreenmodal import LoadScreenModal
from src.components.savescreenmodal import SaveScreenModal
from dash.exceptions import PreventUpdate


class User(UserMixin):
    def __init__(self, username):
        self.id = username


login_button = dbc.Button(
    "Login",
    id="login-button",
    className="login-button",
)
login_card = html.Div(
    dbc.Form(
        html.Div(
            [
                html.Div(
                    [
                        html.H4(
                            "LOGIN",
                            className="card-title",
                        ),
                        html.Div(
                            [login_button],
                            className="card-menu",
                        ),
                    ],
                    className="card-header",
                ),
                html.Div(
                    [
                        dbc.Label(
                            "Usuário",
                            className="login-form-comment",
                        ),
                        dbc.Input(
                            placeholder="",
                            id="login-username",
                            className="login-input-field",
                            type="text",
                        ),
                        dbc.Label(
                            "Senha",
                            className="login-form-comment",
                        ),
                        dbc.Input(
                            type="password",
                            id="login-password",
                            className="login-input-field",
                        ),
                    ],
                    className="card-content",
                ),
            ],
            className="card",
        ),
    )
)

login_location = dcc.Location(id="page-location")
login_info = html.Div(id="user-status-header")
logged_in_info = html.Div(
    [
        html.A(
            html.Button("Logout"),
            href=Settings.url_prefix + "logout",
            className="logout",
        ),
    ]
)
logged_out_info = (
    html.A(
        html.Button("Login"),
        href=Settings.url_prefix + "login",
        className="login",
    ),
)

logout_card = (
    html.Div(
        html.H2(
            "Você foi desconectado. Por favor, faça login novamente",
            className="logout-message",
        ),
        className="logout-body",
    ),
)


@callback(
    Output("user-status-header", "children"),
    Input("page-location", "pathname"),
)
def update_authentication_status(path):
    logged_in = current_user.is_authenticated
    Log.log().info(f"AUTH: {logged_in} - {path}")
    if path == (Settings.url_prefix + "logout") and logged_in:
        Log.log().info("LOGOUT: Sucesso")
        logout_user()
        child = logged_out_info
    elif logged_in:
        child = logged_in_info
    else:
        child = logged_out_info
    return child


@callback(
    Output("page-location", "pathname"),
    Input("login-button", "n_clicks"),
    State("login-username", "value"),
    State("login-password", "value"),
    State("_pages_location", "pathname"),
    prevent_initial_call=True,
)
def redirect_page(
    login_n_clicks,
    username,
    password,
    pathname,
):
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
