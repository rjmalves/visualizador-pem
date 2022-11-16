# package imports
import dash
from dash import html, callback, Input, Output, State

from src.components.newstudymodalaio import NewStudyModalAIO
from src.components.currentstudiestableaio import CurrentStudiesTableAIO
from src.components.casos.operationgraph import OperationGraph
from src.components.casos.acumprobgraph import AcumProbGraph

import src.utils.modals as modals
import src.utils.data as data


dash.register_page(__name__, path="/", redirect_from=["/casos"], title="Casos")

layout = html.Div(
    [
        NewStudyModalAIO(aio_id="casos-modal"),
        CurrentStudiesTableAIO(aio_id="casos-current-studies"),
        OperationGraph(aio_id="casos-operation-graph"),
        AcumProbGraph(aio_id="casos-permanencia-graph"),
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
    Output(OperationGraph.ids.studies("casos-operation-graph"), "data"),
    Input(CurrentStudiesTableAIO.ids.data("casos-current-studies"), "data"),
)
def update_current_studies(studies_data):
    return studies_data


@callback(
    Output(AcumProbGraph.ids.studies("casos-permanencia-graph"), "data"),
    Input(CurrentStudiesTableAIO.ids.data("casos-current-studies"), "data"),
)
def update_current_studies(studies_data):
    return studies_data
