# package imports
import dash
import pandas as pd
from dash import html, callback, Input, Output, State, ctx

from src.components.newstudymodalaio import NewStudyModalAIO
from src.components.currentstudiestableaio import CurrentStudiesTableAIO
from src.components.operationgraphaio import OperationGraphAIO

import src.utils.modals as modals
import src.utils.dropdowns as dropdowns
import src.utils.data as data
import src.utils.plots as plots


dash.register_page(
    __name__, path="/", redirect_from=["/encadeador"], title="Encadeador"
)

layout = html.Div(
    [
        NewStudyModalAIO(aio_id="encadeador-modal"),
        CurrentStudiesTableAIO(aio_id="encadeador-current-studies"),
        OperationGraphAIO(aio_id="encadeador-operation-graph"),
    ],
    className="encadeador-app-page",
)


@callback(
    Output(NewStudyModalAIO.ids.modal("encadeador-modal"), "is_open"),
    [
        Input(
            CurrentStudiesTableAIO.ids.add_study_btn(
                "encadeador-current-studies"
            ),
            "n_clicks",
        ),
        Input(
            NewStudyModalAIO.ids.confirm_study_btn("encadeador-modal"),
            "n_clicks",
        ),
    ],
    [State(NewStudyModalAIO.ids.modal("encadeador-modal"), "is_open")],
)
def toggle_encadeador_modal(src1, src2, is_open):
    return modals.toggle_modal(src1, src2, is_open)


@callback(
    Output(
        CurrentStudiesTableAIO.ids.data("encadeador-current-studies"), "data"
    ),
    Input(
        NewStudyModalAIO.ids.confirm_study_btn("encadeador-modal"), "n_clicks"
    ),
    Input(
        CurrentStudiesTableAIO.ids.remove_study_btn(
            "encadeador-current-studies"
        ),
        "n_clicks",
    ),
    State(NewStudyModalAIO.ids.new_study_name("encadeador-modal"), "value"),
    State(
        CurrentStudiesTableAIO.ids.selected("encadeador-current-studies"),
        "data",
    ),
    State(
        CurrentStudiesTableAIO.ids.data("encadeador-current-studies"), "data"
    ),
)
def edit_current_encadeador_study_data(
    add_study_button_clicks,
    remove_study_button_clicks,
    new_study_id,
    selected_study,
    current_studies,
):
    return data.edit_current_study_data(
        add_study_button_clicks,
        remove_study_button_clicks,
        new_study_id,
        selected_study,
        current_studies,
        NewStudyModalAIO.ids.confirm_study_btn("encadeador-modal"),
        CurrentStudiesTableAIO.ids.remove_study_btn(
            "encadeador-current-studies"
        ),
    )


@callback(
    Output(
        OperationGraphAIO.ids.variable_dropdown("encadeador-operation-graph"),
        "options",
    ),
    Input(
        OperationGraphAIO.ids.updater("encadeador-operation-graph"),
        "n_intervals",
    ),
    Input(
        CurrentStudiesTableAIO.ids.data("encadeador-current-studies"), "data"
    ),
)
def update_variables_dropdown_options(interval, studies_data):
    return dropdowns.update_operation_variables_dropdown_options_encadeador(
        interval, studies_data
    )


@callback(
    Output(
        OperationGraphAIO.ids.options("encadeador-operation-graph"), "data"
    ),
    Input(
        OperationGraphAIO.ids.updater("encadeador-operation-graph"),
        "n_intervals",
    ),
    Input(
        CurrentStudiesTableAIO.ids.data("encadeador-current-studies"), "data"
    ),
    Input(
        OperationGraphAIO.ids.variable_dropdown("encadeador-operation-graph"),
        "value",
    ),
)
def update_options(interval, studies, variable: str):
    return dropdowns.update_operation_options_encadeador(
        interval, studies, variable
    )


@callback(
    Output(OperationGraphAIO.ids.data("encadeador-operation-graph"), "data"),
    Input(
        OperationGraphAIO.ids.updater("encadeador-operation-graph"),
        "n_intervals",
    ),
    Input(
        CurrentStudiesTableAIO.ids.data("encadeador-current-studies"), "data"
    ),
    Input(OperationGraphAIO.ids.filters("encadeador-operation-graph"), "data"),
    Input(
        OperationGraphAIO.ids.variable_dropdown("encadeador-operation-graph"),
        "value",
    ),
)
def update_data(interval, studies, filters: dict, variable: str):
    return data.update_operation_data_encadeador(
        interval, studies, filters, variable
    )


@callback(
    Output(
        OperationGraphAIO.ids.graph("encadeador-operation-graph"), "figure"
    ),
    Input(OperationGraphAIO.ids.data("encadeador-operation-graph"), "data"),
    State(
        OperationGraphAIO.ids.variable_dropdown("encadeador-operation-graph"),
        "value",
    ),
)
def generate_operation_graph(operation_data, variable):
    return plots.generate_operation_graph_encadeador(operation_data, variable)
