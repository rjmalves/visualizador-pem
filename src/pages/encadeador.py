# package imports
import dash
from dash import html, dcc, callback, Input, Output, State

from src.components.newstudymodal import NewStudyModal
from src.components.editstudymodal import EditStudyModal
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
from src.components.encadeador.statustableencadeador import (
    StatusTable,
)
from src.components.login import login_location
from flask_login import current_user
import src.utils.modals as modals
import src.utils.data as data


dash.register_page(
    __name__,
    path="/encadeador",
    title="Encadeador",
    path_template="/encadeador/<screen_id>",
)


def layout(screen_id=None):
    return html.Div(
        [
            NewStudyModal(aio_id="encadeador-modal"),
            EditStudyModal(aio_id="encadeador-edit-modal"),
            CurrentStudiesTable(aio_id="encadeador-current-studies"),
            StatusTable(aio_id="encadeador-status-table"),
            OperationGraphEncadeador(aio_id="encadeador-operation-graph"),
            TimeCostsGraphEncadeador(aio_id="encadeador-tempo-custos-graph"),
            ViolationGraph(aio_id="encadeador-inviabs-graph"),
            dcc.Store(
                "encadeador-screen", storage_type="memory", data=screen_id
            ),
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
    if current_user.is_authenticated:
        return modals.toggle_modal(src1, src2, is_open)
    else:
        return False


@callback(
    Output(EditStudyModal.ids.modal("encadeador-edit-modal"), "is_open"),
    [
        Input(
            CurrentStudiesTable.ids.edit_study_btn(
                "encadeador-current-studies"
            ),
            "n_clicks",
        ),
        Input(
            EditStudyModal.ids.confirm_study_btn("encadeador-edit-modal"),
            "n_clicks",
        ),
    ],
    State(EditStudyModal.ids.modal("encadeador-edit-modal"), "is_open"),
    State(
        CurrentStudiesTable.ids.selected("encadeador-current-studies"),
        "data",
    ),
)
def toggle_encadeador_modal(src1, src2, is_open, selected):
    if selected is None:
        return None
    elif len(selected) == 0:
        return None
    else:
        return modals.toggle_modal(src1, src2, is_open)


@callback(
    Output(CurrentStudiesTable.ids.data("encadeador-current-studies"), "data"),
    Input(NewStudyModal.ids.confirm_study_btn("encadeador-modal"), "n_clicks"),
    Input(
        EditStudyModal.ids.confirm_study_btn("encadeador-edit-modal"),
        "n_clicks",
    ),
    Input(
        CurrentStudiesTable.ids.remove_study_btn("encadeador-current-studies"),
        "n_clicks",
    ),
    State(NewStudyModal.ids.new_study_name("encadeador-modal"), "value"),
    State(NewStudyModal.ids.new_study_label("encadeador-modal"), "value"),
    State(NewStudyModal.ids.new_study_color("encadeador-modal"), "value"),
    State(EditStudyModal.ids.edit_study_id("encadeador-edit-modal"), "data"),
    State(
        EditStudyModal.ids.edit_study_path("encadeador-edit-modal"), "value"
    ),
    State(
        EditStudyModal.ids.edit_study_name("encadeador-edit-modal"), "value"
    ),
    State(
        EditStudyModal.ids.edit_study_color("encadeador-edit-modal"), "value"
    ),
    State(
        CurrentStudiesTable.ids.selected("encadeador-current-studies"),
        "data",
    ),
    State(CurrentStudiesTable.ids.data("encadeador-current-studies"), "data"),
    State("encadeador-screen", "data"),
)
def edit_current_encadeador_study_data(
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
        NewStudyModal.ids.confirm_study_btn("encadeador-modal"),
        EditStudyModal.ids.confirm_study_btn("encadeador-edit-modal"),
        CurrentStudiesTable.ids.remove_study_btn("encadeador-current-studies"),
        screen,
    )


@callback(
    Output(EditStudyModal.ids.edit_study_id("encadeador-edit-modal"), "data"),
    Input(
        CurrentStudiesTable.ids.selected("encadeador-current-studies"),
        "data",
    ),
    State(CurrentStudiesTable.ids.data("encadeador-current-studies"), "data"),
)
def update_edit_study_modal_id(selected_study, current_studies):
    dados = data.extract_selected_study_data(
        selected_study,
        current_studies,
    )
    if dados is None:
        return None
    else:
        return dados["table_id"]


@callback(
    Output(
        EditStudyModal.ids.edit_study_path("encadeador-edit-modal"), "value"
    ),
    Input(
        CurrentStudiesTable.ids.selected("encadeador-current-studies"),
        "data",
    ),
    State(CurrentStudiesTable.ids.data("encadeador-current-studies"), "data"),
)
def update_edit_study_modal_path(selected_study, current_studies):
    dados = data.extract_selected_study_data(
        selected_study,
        current_studies,
    )
    if dados is None:
        return None
    else:
        return dados["path"]


@callback(
    Output(
        EditStudyModal.ids.edit_study_name("encadeador-edit-modal"), "value"
    ),
    Input(
        CurrentStudiesTable.ids.selected("encadeador-current-studies"),
        "data",
    ),
    State(CurrentStudiesTable.ids.data("encadeador-current-studies"), "data"),
)
def update_edit_study_modal_name(selected_study, current_studies):
    dados = data.extract_selected_study_data(
        selected_study,
        current_studies,
    )

    if dados is None:
        return None
    else:
        return dados["name"]


@callback(
    Output(
        EditStudyModal.ids.edit_study_color("encadeador-edit-modal"), "value"
    ),
    Input(
        CurrentStudiesTable.ids.selected("encadeador-current-studies"),
        "data",
    ),
    State(CurrentStudiesTable.ids.data("encadeador-current-studies"), "data"),
)
def update_edit_study_modal_color(selected_study, current_studies):
    dados = data.extract_selected_study_data(
        selected_study,
        current_studies,
    )

    if dados is None:
        return None
    else:
        return dados["color"]


@callback(
    Output(
        StatusTable.ids.studies("encadeador-status-table"),
        "data",
    ),
    Input(CurrentStudiesTable.ids.data("encadeador-current-studies"), "data"),
)
def update_current_studies_status_table(studies_data):
    return studies_data


@callback(
    Output(
        OperationGraphEncadeador.ids.studies("encadeador-operation-graph"),
        "data",
    ),
    Input(CurrentStudiesTable.ids.data("encadeador-current-studies"), "data"),
)
def update_current_studies_operation_graph(studies_data):
    return studies_data


@callback(
    Output(
        TimeCostsGraphEncadeador.ids.studies("encadeador-tempo-custos-graph"),
        "data",
    ),
    Input(CurrentStudiesTable.ids.data("encadeador-current-studies"), "data"),
)
def update_current_studies_timecosts_graph(studies_data):
    return studies_data


@callback(
    Output(
        ViolationGraph.ids.studies("encadeador-inviabs-graph"),
        "data",
    ),
    Input(CurrentStudiesTable.ids.data("encadeador-current-studies"), "data"),
)
def update_current_studies_violation_graph(studies_data):
    return studies_data
