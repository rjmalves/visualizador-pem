# package imports
import dash
from dash import html, callback, Input, Output, State

from src.components.newstudymodal import NewStudyModal
from src.components.currentstudiestable import CurrentStudiesTable
from src.components.encadeador.operationgraphencadeador import (
    OperationGraphEncadeador,
)
from src.components.encadeador.timecostsgraphencadeador import (
    TimeCostsGraphEncadeador,
)
from src.components.encadeador.violationgraphencadeador import (
    ViolationGraph,
)

import src.utils.modals as modals
import src.utils.data as data


dash.register_page(__name__, title="Encadeador")

layout = html.Div(
    [
        NewStudyModal(aio_id="encadeador-modal"),
        CurrentStudiesTable(aio_id="encadeador-current-studies"),
        OperationGraphEncadeador(aio_id="encadeador-operation-graph"),
        TimeCostsGraphEncadeador(aio_id="encadeador-tempo-custos-graph"),
        ViolationGraph(aio_id="encadeador-inviabs-graph"),
    ],
    className="encadeador-app-page",
)


@callback(
    Output(NewStudyModal.ids.modal("encadeador-modal"), "is_open"),
    [
        Input(
            CurrentStudiesTable.ids.add_study_btn(
                "encadeador-current-studies"
            ),
            "n_clicks",
        ),
        Input(
            NewStudyModal.ids.confirm_study_btn("encadeador-modal"),
            "n_clicks",
        ),
    ],
    [State(NewStudyModal.ids.modal("encadeador-modal"), "is_open")],
)
def toggle_encadeador_modal(src1, src2, is_open):
    return modals.toggle_modal(src1, src2, is_open)


@callback(
    Output(CurrentStudiesTable.ids.data("encadeador-current-studies"), "data"),
    Input(NewStudyModal.ids.confirm_study_btn("encadeador-modal"), "n_clicks"),
    Input(
        CurrentStudiesTable.ids.remove_study_btn("encadeador-current-studies"),
        "n_clicks",
    ),
    State(NewStudyModal.ids.new_study_name("encadeador-modal"), "value"),
    State(NewStudyModal.ids.new_study_label("encadeador-modal"), "value"),
    State(
        CurrentStudiesTable.ids.selected("encadeador-current-studies"),
        "data",
    ),
    State(CurrentStudiesTable.ids.data("encadeador-current-studies"), "data"),
)
def edit_current_encadeador_study_data(
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
        NewStudyModal.ids.confirm_study_btn("encadeador-modal"),
        CurrentStudiesTable.ids.remove_study_btn("encadeador-current-studies"),
    )


@callback(
    Output(
        OperationGraphEncadeador.ids.studies("encadeador-operation-graph"),
        "data",
    ),
    Input(CurrentStudiesTable.ids.data("encadeador-current-studies"), "data"),
)
def update_current_studies(studies_data):
    return studies_data


@callback(
    Output(
        TimeCostsGraphEncadeador.ids.studies("encadeador-tempo-custos-graph"),
        "data",
    ),
    Input(CurrentStudiesTable.ids.data("encadeador-current-studies"), "data"),
)
def update_current_studies(studies_data):
    return studies_data


@callback(
    Output(
        ViolationGraph.ids.studies("encadeador-inviabs-graph"),
        "data",
    ),
    Input(CurrentStudiesTable.ids.data("encadeador-current-studies"), "data"),
)
def update_current_studies(studies_data):
    return studies_data
