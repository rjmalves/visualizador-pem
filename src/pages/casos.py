# package imports
import dash
from dash import html

from src.components.currentstudiestable import (
    current_studies,
    selected_study,
    table,
)
from src.components.newstudymodal import modal
from src.components.operationgraphcasos import (
    graph_updater,
    operation_variables_options,
    operation_variables_data,
    operation_variables_filter,
    operation_data_download,
    graph,
)

dash.register_page(__name__, path="/", redirect_from=["/casos"], title="Casos")

layout = html.Div(
    [
        modal,
        current_studies,
        selected_study,
        table,
        graph,
        operation_variables_options,
        operation_variables_filter,
        operation_variables_data,
        operation_data_download,
        graph_updater,
    ],
    className="casos-app-page",
)
