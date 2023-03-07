# package imports
import dash
from dash import html
from src.components.login import login_card


dash.register_page(__name__, path="/login", title="Login")

layout = html.Div(
    [login_card],
    className="login-app-page",
)
