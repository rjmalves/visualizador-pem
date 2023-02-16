# package imports
import dash
from dash import html

from src.components.login import logout_card

dash.register_page(__name__, path="/logout", title="Logout")

layout = html.Div(
    logout_card,
    className="logout-app-page",
)
