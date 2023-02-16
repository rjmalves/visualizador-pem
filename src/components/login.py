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


class User(UserMixin):
    def __init__(self, username):
        self.id = username


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
                            [
                                dbc.Button(
                                    "Login",
                                    id="login-button",
                                    className="login-button",
                                )
                            ],
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

login_location = dcc.Location(id="url-login")
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


@callback(
    Output("user-status-header", "children"), Input("url-login", "pathname")
)
def update_authentication_status(path):
    logged_in = current_user.is_authenticated
    if path == Settings.url_prefix + "logout" and logged_in:
        logout_user()
        child = logged_out_info
    elif logged_in:
        child = logged_in_info
    else:
        child = logged_out_info
    return child


@callback(
    Output("url-login", "pathname"),
    Input("login-button", "n_clicks"),
    State("login-username", "value"),
    State("login-password", "value"),
    State("_pages_location", "pathname"),
    prevent_initial_call=True,
)
def login_button_click(n_clicks, username, password, pathname):
    if n_clicks is None:
        raise PreventUpdate
    if n_clicks > 0:
        if username == Settings.user and password == Settings.password:
            login_user(User(username))
            return Settings.url_prefix
        return pathname
