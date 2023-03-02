# package imports
import dash
from dash import html, dcc, callback, Input, Output, State

from src.components.newstudymodal import NewStudyModal
from src.components.editstudymodal import EditStudyModal
from src.components.currentstudiestable import CurrentStudiesTable
from src.components.casos.operationgraph import OperationGraph
from src.components.casos.acumprobgraph import AcumProbGraph
from src.components.casos.timecostsgraph import TimeCostsGraph
from src.components.casos.convergencegraph import ConvergenceGraph
from src.components.casos.resourcesgraph import ResourcesGraph
from flask_login import current_user
import src.utils.modals as modals
import src.utils.data as data


dash.register_page(
    __name__,
    path="/",
    redirect_from=["/casos"],
    title="Casos",
    path_template="/casos/<screen_id>",
)


def layout(screen_id=None):
    return html.Div(
        [
            NewStudyModal(aio_id="casos-modal"),
            EditStudyModal(aio_id="casos-edit-modal"),
            CurrentStudiesTable(aio_id="casos-current-studies"),
            OperationGraph(aio_id="casos-operation-graph"),
            AcumProbGraph(aio_id="casos-permanencia-graph"),
            TimeCostsGraph(aio_id="casos-tempo-custos-graph"),
            ConvergenceGraph(aio_id="casos-convergence-graph"),
            ResourcesGraph(aio_id="casos-resources-graph"),
            dcc.Store("casos-screen", storage_type="memory", data=screen_id),
        ],
        className="casos-app-page",
    )


@callback(
    Output(NewStudyModal.ids.modal("casos-modal"), "is_open"),
    [
        Input(
            CurrentStudiesTable.ids.add_study_btn("casos-current-studies"),
            "n_clicks",
        ),
        Input(
            NewStudyModal.ids.confirm_study_btn("casos-modal"),
            "n_clicks",
        ),
    ],
    [State(NewStudyModal.ids.modal("casos-modal"), "is_open")],
)
def toggle_casos_modal(src1, src2, is_open):
    if current_user.is_authenticated:
        return modals.toggle_modal(src1, src2, is_open)
    else:
        return False


@callback(
    Output(EditStudyModal.ids.modal("casos-edit-modal"), "is_open"),
    [
        Input(
            CurrentStudiesTable.ids.edit_study_btn("casos-current-studies"),
            "n_clicks",
        ),
        Input(
            EditStudyModal.ids.confirm_study_btn("casos-edit-modal"),
            "n_clicks",
        ),
    ],
    State(EditStudyModal.ids.modal("casos-edit-modal"), "is_open"),
    State(
        CurrentStudiesTable.ids.selected("casos-current-studies"),
        "data",
    ),
)
def toggle_casos_modal(src1, src2, is_open, selected):
    if selected is None:
        return None
    elif len(selected) == 0:
        return None
    else:
        return modals.toggle_modal(src1, src2, is_open)


@callback(
    Output(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
    Input(NewStudyModal.ids.confirm_study_btn("casos-modal"), "n_clicks"),
    Input(
        EditStudyModal.ids.confirm_study_btn("casos-edit-modal"),
        "n_clicks",
    ),
    Input(
        CurrentStudiesTable.ids.remove_study_btn("casos-current-studies"),
        "n_clicks",
    ),
    State(NewStudyModal.ids.new_study_name("casos-modal"), "value"),
    State(NewStudyModal.ids.new_study_label("casos-modal"), "value"),
    State(NewStudyModal.ids.new_study_color("casos-modal"), "value"),
    State(EditStudyModal.ids.edit_study_id("casos-edit-modal"), "data"),
    State(EditStudyModal.ids.edit_study_path("casos-edit-modal"), "value"),
    State(EditStudyModal.ids.edit_study_name("casos-edit-modal"), "value"),
    State(EditStudyModal.ids.edit_study_color("casos-edit-modal"), "value"),
    State(
        CurrentStudiesTable.ids.selected("casos-current-studies"),
        "data",
    ),
    State(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
    State("casos-screen", "data"),
)
def edit_current_casos_study_data(
    add_study_button_clicks,
    edit_study_button_clicks,
    remove_study_button_clicks,
    new_study_id,
    new_study_label,
    new_study_color,
    edit_study_id,
    edit_study_path,
    edit_study_name,
    edit_study_color,
    selected_study,
    current_studies,
    screen,
):
    return data.edit_current_study_data(
        add_study_button_clicks,
        edit_study_button_clicks,
        remove_study_button_clicks,
        new_study_id,
        new_study_label,
        new_study_color,
        edit_study_id,
        edit_study_path,
        edit_study_name,
        edit_study_color,
        selected_study,
        current_studies,
        NewStudyModal.ids.confirm_study_btn("casos-modal"),
        EditStudyModal.ids.confirm_study_btn("casos-edit-modal"),
        CurrentStudiesTable.ids.remove_study_btn("casos-current-studies"),
        screen,
    )


@callback(
    Output(EditStudyModal.ids.edit_study_id("casos-edit-modal"), "data"),
    Input(
        CurrentStudiesTable.ids.selected("casos-current-studies"),
        "data",
    ),
    State(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
)
def update_edit_study_modal_id(selected_study, current_studies):
    dados = data.extract_selected_study_data(
        selected_study,
        current_studies,
    )
    if dados is None:
        return None
    else:
        return dados["id"]


@callback(
    Output(EditStudyModal.ids.edit_study_path("casos-edit-modal"), "value"),
    Input(
        CurrentStudiesTable.ids.selected("casos-current-studies"),
        "data",
    ),
    State(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
)
def update_edit_study_modal_path(selected_study, current_studies):
    dados = data.extract_selected_study_data(
        selected_study,
        current_studies,
    )
    if dados is None:
        return None
    else:
        return dados["CAMINHO"]


@callback(
    Output(EditStudyModal.ids.edit_study_name("casos-edit-modal"), "value"),
    Input(
        CurrentStudiesTable.ids.selected("casos-current-studies"),
        "data",
    ),
    State(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
)
def update_edit_study_modal_name(selected_study, current_studies):
    dados = data.extract_selected_study_data(
        selected_study,
        current_studies,
    )

    if dados is None:
        return None
    else:
        return dados["NOME"]


@callback(
    Output(EditStudyModal.ids.edit_study_color("casos-edit-modal"), "value"),
    Input(
        CurrentStudiesTable.ids.selected("casos-current-studies"),
        "data",
    ),
    State(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
)
def update_edit_study_modal_color(selected_study, current_studies):
    dados = data.extract_selected_study_data(
        selected_study,
        current_studies,
    )

    if dados is None:
        return None
    else:
        return dados["COR"]


@callback(
    Output(OperationGraph.ids.studies("casos-operation-graph"), "data"),
    Input(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
)
def update_current_studies(studies_data):
    return studies_data


@callback(
    Output(AcumProbGraph.ids.studies("casos-permanencia-graph"), "data"),
    Input(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
)
def update_current_studies(studies_data):
    return studies_data


@callback(
    Output(TimeCostsGraph.ids.studies("casos-tempo-custos-graph"), "data"),
    Input(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
)
def update_current_studies(studies_data):
    return studies_data


@callback(
    Output(ConvergenceGraph.ids.studies("casos-convergence-graph"), "data"),
    Input(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
)
def update_current_studies(studies_data):
    return studies_data


@callback(
    Output(ResourcesGraph.ids.studies("casos-resources-graph"), "data"),
    Input(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
)
def update_current_studies(studies_data):
    return studies_data
