# package imports
import dash
from dash import html, callback, Input, Output, State

from src.components.newstudymodalaio import NewStudyModalAIO
from src.components.currentstudiestableaio import CurrentStudiesTableAIO
from src.components.encadeador.operationgraphencadeador import (
    OperationGraphEncadeador,
)
from src.components.encadeador.timecostsgraphencadeador import (
    TimeCostsGraphEncadeador,
)

import src.utils.modals as modals
import src.utils.data as data


dash.register_page(__name__, title="Encadeador")

layout = html.Div(
    [
        NewStudyModalAIO(aio_id="encadeador-modal"),
        CurrentStudiesTableAIO(aio_id="encadeador-current-studies"),
        OperationGraphEncadeador(aio_id="encadeador-operation-graph"),
        TimeCostsGraphEncadeador(aio_id="encadeador-tempo-custos-graph"),
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
        OperationGraphEncadeador.ids.studies("encadeador-operation-graph"),
        "data",
    ),
    Input(
        CurrentStudiesTableAIO.ids.data("encadeador-current-studies"), "data"
    ),
)
def update_current_studies(studies_data):
    return studies_data


@callback(
    Output(
        TimeCostsGraphEncadeador.ids.studies("encadeador-tempo-custos-graph"),
        "data",
    ),
    Input(
        CurrentStudiesTableAIO.ids.data("encadeador-current-studies"), "data"
    ),
)
def update_current_studies(studies_data):
    return studies_data
