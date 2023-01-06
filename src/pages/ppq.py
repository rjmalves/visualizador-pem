# package imports
import dash
import pandas as pd
from dash import html, callback, Input, Output, State

from src.components.newstudymodal import NewStudyModal
from src.components.currentstudiestable import CurrentStudiesTable
from src.components.ppquente.operationgraphppq import OperationGraphPPQ

import src.utils.modals as modals
import src.utils.data as data


dash.register_page(__name__, path="/ppquente", title="Casos")

layout = html.Div(
    [
        NewStudyModal(aio_id="ppq-modal"),
        CurrentStudiesTable(aio_id="ppq-current-studies"),
        OperationGraphPPQ(aio_id="ppq-operation-graph"),
    ],
    className="ppq-app-page",
)


@callback(
    Output(NewStudyModal.ids.modal("ppq-modal"), "is_open"),
    [
        Input(
            CurrentStudiesTable.ids.add_study_btn("ppq-current-studies"),
            "n_clicks",
        ),
        Input(
            NewStudyModal.ids.confirm_study_btn("ppq-modal"),
            "n_clicks",
        ),
    ],
    [State(NewStudyModal.ids.modal("ppq-modal"), "is_open")],
)
def toggle_casos_modal(src1, src2, is_open):
    return modals.toggle_modal(src1, src2, is_open)


@callback(
    Output(CurrentStudiesTable.ids.data("ppq-current-studies"), "data"),
    Input(NewStudyModal.ids.confirm_study_btn("ppq-modal"), "n_clicks"),
    Input(
        CurrentStudiesTable.ids.remove_study_btn("ppq-current-studies"),
        "n_clicks",
    ),
    State(NewStudyModal.ids.new_study_name("ppq-modal"), "value"),
    State(NewStudyModal.ids.new_study_label("ppq-modal"), "value"),
    State(
        CurrentStudiesTable.ids.selected("ppq-current-studies"),
        "data",
    ),
    State(CurrentStudiesTable.ids.data("ppq-current-studies"), "data"),
)
def edit_current_casos_study_data(
    add_study_button_clicks,
    remove_study_button_clicks,
    new_study_id,
    new_study_label,
    selected_study,
    current_studies,
):
    return data.edit_current_study_data(
        add_study_button_clicks,
        remove_study_button_clicks,
        new_study_id,
        new_study_label,
        selected_study,
        current_studies,
        NewStudyModal.ids.confirm_study_btn("ppq-modal"),
        CurrentStudiesTable.ids.remove_study_btn("ppq-current-studies"),
    )


@callback(
    Output(OperationGraphPPQ.ids.studies("ppq-operation-graph"), "data"),
    Input(CurrentStudiesTable.ids.data("ppq-current-studies"), "data"),
)
def update_current_studies(studies_data):
    return studies_data
