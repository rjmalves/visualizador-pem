# package imports
import dash
from dash import html, dcc, callback, Input, Output, State

from src.components.newstudymodal import NewStudyModal
from src.components.editstudymodal import EditStudyModal
from src.components.currentstudiestable import CurrentStudiesTable
from src.components.ppquente.distributionsgraphppq import DistributionsGraphPPQ
from src.components.ppquente.operationgraphppq import OperationGraphPPQ
from flask_login import current_user
import src.utils.modals as modals
import src.utils.data as data


dash.register_page(
    __name__,
    path="/ppquente",
    title="PPQ",
    path_template="/ppquente/<screen_id>",
)


def layout(screen_id=None):
    return html.Div(
        [
            NewStudyModal(aio_id="ppq-modal"),
            EditStudyModal(aio_id="ppq-edit-modal"),
            CurrentStudiesTable(aio_id="ppq-current-studies"),
            OperationGraphPPQ(aio_id="ppq-operation-graph"),
            DistributionsGraphPPQ(aio_id="ppq-distribution-graph"),
            dcc.Store("ppq-screen", storage_type="memory", data=screen_id),
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
def toggle_ppq_modal(src1, src2, is_open):
    if current_user.is_authenticated:
        return modals.toggle_modal(src1, src2, is_open)
    else:
        return False


@callback(
    Output(EditStudyModal.ids.modal("ppq-edit-modal"), "is_open"),
    [
        Input(
            CurrentStudiesTable.ids.edit_study_btn("ppq-current-studies"),
            "n_clicks",
        ),
        Input(
            EditStudyModal.ids.confirm_study_btn("ppq-edit-modal"),
            "n_clicks",
        ),
    ],
    State(EditStudyModal.ids.modal("ppq-edit-modal"), "is_open"),
    State(
        CurrentStudiesTable.ids.selected("ppq-current-studies"),
        "data",
    ),
)
def toggle_ppq_modal(src1, src2, is_open, selected):
    if selected is None:
        return None
    elif len(selected) == 0:
        return None
    else:
        return modals.toggle_modal(src1, src2, is_open)


@callback(
    Output(CurrentStudiesTable.ids.data("ppq-current-studies"), "data"),
    Input(NewStudyModal.ids.confirm_study_btn("ppq-modal"), "n_clicks"),
    Input(
        EditStudyModal.ids.confirm_study_btn("ppq-edit-modal"),
        "n_clicks",
    ),
    Input(
        CurrentStudiesTable.ids.remove_study_btn("ppq-current-studies"),
        "n_clicks",
    ),
    State(NewStudyModal.ids.new_study_name("ppq-modal"), "value"),
    State(NewStudyModal.ids.new_study_label("ppq-modal"), "value"),
    State(NewStudyModal.ids.new_study_color("ppq-modal"), "value"),
    State(EditStudyModal.ids.edit_study_id("ppq-edit-modal"), "data"),
    State(EditStudyModal.ids.edit_study_path("ppq-edit-modal"), "value"),
    State(EditStudyModal.ids.edit_study_name("ppq-edit-modal"), "value"),
    State(EditStudyModal.ids.edit_study_color("ppq-edit-modal"), "value"),
    State(
        CurrentStudiesTable.ids.selected("ppq-current-studies"),
        "data",
    ),
    State(CurrentStudiesTable.ids.data("ppq-current-studies"), "data"),
    State("ppq-screen", "data"),
)
def edit_current_ppq_study_data(
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
        NewStudyModal.ids.confirm_study_btn("ppq-modal"),
        EditStudyModal.ids.confirm_study_btn("ppq-edit-modal"),
        CurrentStudiesTable.ids.remove_study_btn("ppq-current-studies"),
        screen,
    )


@callback(
    Output(EditStudyModal.ids.edit_study_id("ppq-edit-modal"), "data"),
    Input(
        CurrentStudiesTable.ids.selected("ppq-current-studies"),
        "data",
    ),
    State(CurrentStudiesTable.ids.data("ppq-current-studies"), "data"),
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
    Output(EditStudyModal.ids.edit_study_path("ppq-edit-modal"), "value"),
    Input(
        CurrentStudiesTable.ids.selected("ppq-current-studies"),
        "data",
    ),
    State(CurrentStudiesTable.ids.data("ppq-current-studies"), "data"),
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
    Output(EditStudyModal.ids.edit_study_color("ppq-edit-modal"), "value"),
    Input(
        CurrentStudiesTable.ids.selected("ppq-current-studies"),
        "data",
    ),
    State(CurrentStudiesTable.ids.data("ppq-current-studies"), "data"),
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
    Output(EditStudyModal.ids.edit_study_name("ppq-edit-modal"), "value"),
    Input(
        CurrentStudiesTable.ids.selected("ppq-current-studies"),
        "data",
    ),
    State(CurrentStudiesTable.ids.data("ppq-current-studies"), "data"),
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
    Output(
        DistributionsGraphPPQ.ids.studies("ppq-distribution-graph"), "data"
    ),
    Input(CurrentStudiesTable.ids.data("ppq-current-studies"), "data"),
)
def update_current_studies(studies_data):
    return studies_data


@callback(
    Output(OperationGraphPPQ.ids.studies("ppq-operation-graph"), "data"),
    Input(CurrentStudiesTable.ids.data("ppq-current-studies"), "data"),
)
def update_current_studies(studies_data):
    return studies_data
