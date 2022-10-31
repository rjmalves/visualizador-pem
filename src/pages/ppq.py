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


dash.register_page(__name__, path="/ppquente", title="Casos")

layout = html.Div(
    [
        NewStudyModalAIO(aio_id="ppq-modal"),
        CurrentStudiesTableAIO(aio_id="ppq-current-studies"),
        OperationGraphAIO(aio_id="ppq-operation-graph"),
    ],
    className="ppq-app-page",
)


@callback(
    Output(NewStudyModalAIO.ids.modal("ppq-modal"), "is_open"),
    [
        Input(
            CurrentStudiesTableAIO.ids.add_study_btn("ppq-current-studies"),
            "n_clicks",
        ),
        Input(
            NewStudyModalAIO.ids.confirm_study_btn("ppq-modal"),
            "n_clicks",
        ),
    ],
    [State(NewStudyModalAIO.ids.modal("ppq-modal"), "is_open")],
)
def toggle_casos_modal(src1, src2, is_open):
    return modals.toggle_modal(src1, src2, is_open)


@callback(
    Output(CurrentStudiesTableAIO.ids.data("ppq-current-studies"), "data"),
    Input(NewStudyModalAIO.ids.confirm_study_btn("ppq-modal"), "n_clicks"),
    Input(
        CurrentStudiesTableAIO.ids.remove_study_btn("ppq-current-studies"),
        "n_clicks",
    ),
    State(NewStudyModalAIO.ids.new_study_name("ppq-modal"), "value"),
    State(
        CurrentStudiesTableAIO.ids.selected("ppq-current-studies"),
        "data",
    ),
    State(CurrentStudiesTableAIO.ids.data("ppq-current-studies"), "data"),
)
def edit_current_casos_study_data(
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
        NewStudyModalAIO.ids.confirm_study_btn("ppq-modal"),
        CurrentStudiesTableAIO.ids.remove_study_btn("ppq-current-studies"),
    )


@callback(
    Output(
        OperationGraphAIO.ids.variable_dropdown("ppq-operation-graph"),
        "options",
    ),
    Input(
        OperationGraphAIO.ids.updater("ppq-operation-graph"),
        "n_intervals",
    ),
    Input(CurrentStudiesTableAIO.ids.data("ppq-current-studies"), "data"),
)
def update_variables_dropdown_options(interval, studies_data):
    return dropdowns.update_operation_variables_dropdown_options_casos(
        interval, studies_data
    )


@callback(
    Output(OperationGraphAIO.ids.options("ppq-operation-graph"), "data"),
    Input(
        OperationGraphAIO.ids.updater("ppq-operation-graph"),
        "n_intervals",
    ),
    Input(CurrentStudiesTableAIO.ids.data("ppq-current-studies"), "data"),
    Input(
        OperationGraphAIO.ids.variable_dropdown("ppq-operation-graph"),
        "value",
    ),
)
def update_options(interval, studies, variable: str):
    return dropdowns.update_operation_options_casos(
        interval, studies, variable
    )


@callback(
    Output(OperationGraphAIO.ids.data("ppq-operation-graph"), "data"),
    Input(
        OperationGraphAIO.ids.updater("ppq-operation-graph"),
        "n_intervals",
    ),
    Input(CurrentStudiesTableAIO.ids.data("ppq-current-studies"), "data"),
    Input(OperationGraphAIO.ids.filters("ppq-operation-graph"), "data"),
    Input(
        OperationGraphAIO.ids.variable_dropdown("ppq-operation-graph"),
        "value",
    ),
)
def update_data(interval, studies, filters: dict, variable: str):
    return data.update_operation_data_ppq(interval, studies, filters, variable)


@callback(
    Output(OperationGraphAIO.ids.graph("ppq-operation-graph"), "figure"),
    Input(OperationGraphAIO.ids.data("ppq-operation-graph"), "data"),
    State(
        OperationGraphAIO.ids.variable_dropdown("ppq-operation-graph"),
        "value",
    ),
    State(OperationGraphAIO.ids.filters("ppq-operation-graph"), "data"),
)
def generate_operation_graph(operation_data, variable, filters):
    return plots.generate_operation_graph_ppq(
        operation_data, variable, filters
    )


@callback(
    Output(
        OperationGraphAIO.ids.estagio_dropdown_container(
            "ppq-operation-graph"
        ),
        "style",
    ),
    Input(OperationGraphAIO.ids.data("ppq-operation-graph"), "data"),
)
def show_estagio_dropdown(variable):
    return {"display": "flex"}
