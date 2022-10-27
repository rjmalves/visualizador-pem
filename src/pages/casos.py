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


dash.register_page(__name__, path="/casos", title="Casos")

layout = html.Div(
    [
        NewStudyModalAIO(aio_id="casos-modal"),
        CurrentStudiesTableAIO(aio_id="casos-current-studies"),
        OperationGraphAIO(aio_id="casos-operation-graph"),
    ],
    className="casos-app-page",
)


@callback(
    Output(NewStudyModalAIO.ids.modal("casos-modal"), "is_open"),
    [
        Input(
            CurrentStudiesTableAIO.ids.add_study_btn("casos-current-studies"),
            "n_clicks",
        ),
        Input(
            NewStudyModalAIO.ids.confirm_study_btn("casos-modal"),
            "n_clicks",
        ),
    ],
    [State(NewStudyModalAIO.ids.modal("casos-modal"), "is_open")],
)
def toggle_casos_modal(src1, src2, is_open):
    return modals.toggle_modal(src1, src2, is_open)


@callback(
    Output(CurrentStudiesTableAIO.ids.data("casos-current-studies"), "data"),
    Input(NewStudyModalAIO.ids.confirm_study_btn("casos-modal"), "n_clicks"),
    Input(
        CurrentStudiesTableAIO.ids.remove_study_btn("casos-current-studies"),
        "n_clicks",
    ),
    State(NewStudyModalAIO.ids.new_study_name("casos-modal"), "value"),
    State(
        CurrentStudiesTableAIO.ids.selected("casos-current-studies"),
        "data",
    ),
    State(CurrentStudiesTableAIO.ids.data("casos-current-studies"), "data"),
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
        NewStudyModalAIO.ids.confirm_study_btn("casos-modal"),
        CurrentStudiesTableAIO.ids.remove_study_btn("casos-current-studies"),
    )


@callback(
    Output(
        OperationGraphAIO.ids.variable_dropdown("casos-operation-graph"),
        "options",
    ),
    Input(
        OperationGraphAIO.ids.updater("casos-operation-graph"),
        "n_intervals",
    ),
    Input(CurrentStudiesTableAIO.ids.data("casos-current-studies"), "data"),
)
def update_variables_dropdown_options(interval, studies_data):
    return dropdowns.update_operation_variables_dropdown_options_casos(
        interval, studies_data
    )


@callback(
    Output(OperationGraphAIO.ids.options("casos-operation-graph"), "data"),
    Input(
        OperationGraphAIO.ids.updater("casos-operation-graph"),
        "n_intervals",
    ),
    Input(CurrentStudiesTableAIO.ids.data("casos-current-studies"), "data"),
    Input(
        OperationGraphAIO.ids.variable_dropdown("casos-operation-graph"),
        "value",
    ),
)
def update_options(interval, studies, variable: str):
    return dropdowns.update_operation_options_casos(
        interval, studies, variable
    )


@callback(
    Output(OperationGraphAIO.ids.data("casos-operation-graph"), "data"),
    Input(
        OperationGraphAIO.ids.updater("casos-operation-graph"),
        "n_intervals",
    ),
    Input(CurrentStudiesTableAIO.ids.data("casos-current-studies"), "data"),
    Input(OperationGraphAIO.ids.filters("casos-operation-graph"), "data"),
    Input(
        OperationGraphAIO.ids.variable_dropdown("casos-operation-graph"),
        "value",
    ),
)
def update_data(interval, studies, filters: dict, variable: str):
    return data.update_operation_data_casos(
        interval, studies, filters, variable
    )


@callback(
    Output(OperationGraphAIO.ids.graph("casos-operation-graph"), "figure"),
    Input(OperationGraphAIO.ids.data("casos-operation-graph"), "data"),
    State(
        OperationGraphAIO.ids.variable_dropdown("casos-operation-graph"),
        "value",
    ),
    State(OperationGraphAIO.ids.filters("casos-operation-graph"), "data"),
)
def generate_operation_graph(operation_data, variable, filters):
    return plots.generate_operation_graph_casos(
        operation_data, variable, filters
    )
