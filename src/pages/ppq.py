# package imports
import dash
from dash import html, dcc, callback, Input, Output, State, ctx

from src.components.newstudymodal import NewStudyModal
from src.components.editstudymodal import EditStudyModal
from src.components.currentstudiestable import CurrentStudiesTable
from src.components.ppquente.distributionsgraphppq import DistributionsGraphPPQ
from src.components.ppquente.operationgraphppq import OperationGraphPPQ
from src.components.savescreenmodal import SaveScreenModal
from src.components.loadscreenmodal import LoadScreenModal
from flask_login import current_user
import src.utils.db as db
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
            SaveScreenModal(aio_id="encadeador-save-screen-modal"),
            LoadScreenModal(aio_id="encadeador-load-screen-modal"),
            dcc.Store("ppq-screen", storage_type="memory", data=screen_id),
            dcc.Location(id="ppq-url"),
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
    Output(
        SaveScreenModal.ids.modal("encadeador-save-screen-modal"), "is_open"
    ),
    [
        Input(
            CurrentStudiesTable.ids.save_study_btn(
                "encadeador-current-studies"
            ),
            "n_clicks",
        ),
        Input(
            SaveScreenModal.ids.confirm_save_screen_btn(
                "encadeador-save-screen-modal"
            ),
            "n_clicks",
        ),
    ],
    [
        State(
            SaveScreenModal.ids.modal("encadeador-save-screen-modal"),
            "is_open",
        )
    ],
)
def toggle_encadeador_modal(src1, src2, is_open):
    if current_user.is_authenticated:
        return modals.toggle_modal(src1, src2, is_open)
    else:
        return False


@callback(
    Output(
        LoadScreenModal.ids.modal("encadeador-load-screen-modal"), "is_open"
    ),
    [
        Input(
            CurrentStudiesTable.ids.load_study_btn(
                "encadeador-current-studies"
            ),
            "n_clicks",
        ),
        Input(
            LoadScreenModal.ids.confirm_load_screen_btn(
                "encadeador-load-screen-modal"
            ),
            "n_clicks",
        ),
    ],
    [
        State(
            LoadScreenModal.ids.modal("encadeador-load-screen-modal"),
            "is_open",
        )
    ],
)
def toggle_encadeador_modal(src1, src2, is_open):
    if current_user.is_authenticated:
        return modals.toggle_modal(src1, src2, is_open)
    else:
        return False


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
        "ppquente",
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
        return dados["table_id"]


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
        return dados["path"]


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
        return dados["color"]


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
        return dados["name"]


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


@callback(
    Output(
        SaveScreenModal.ids.current_studies("encadeador-save-screen-modal"),
        "data",
    ),
    Input(CurrentStudiesTable.ids.data("encadeador-current-studies"), "data"),
)
def update_current_studies(studies_data):
    return studies_data


@callback(
    Output(
        LoadScreenModal.ids.load_screen_select("encadeador-load-screen-modal"),
        "options",
    ),
    Input(
        CurrentStudiesTable.ids.load_study_btn("encadeador-current-studies"),
        "n_clicks",
    ),
    State(
        LoadScreenModal.ids.screen_type_str("encadeador-load-screen-modal"),
        "data",
    ),
)
def update_screen_type_str(path, screen_type_str):
    return db.list_screens(screen_type_str)


@callback(
    Output("ppq-url", "pathname"),
    Input(
        LoadScreenModal.ids.confirm_load_screen_btn("ppq-load-screen-modal"),
        "n_clicks",
    ),
    Input(
        SaveScreenModal.ids.confirm_save_screen_btn("ppq-save-screen-modal"),
        "n_clicks",
    ),
    State("_pages_location", "pathname"),
    State(
        LoadScreenModal.ids.load_screen_select("ppq-load-screen-modal"),
        "value",
    ),
    State(
        SaveScreenModal.ids.new_screen_name("ppq-save-screen-modal"),
        "value",
    ),
    prevent_initial_call=True,
)
def redirect_page(
    ppq_load_screen_confirm_click,
    ppq_save_screen_confirm_click,
    pathname,
    ppq_load_screen_value,
    ppq_save_screen_name,
):
    if ctx.triggered_id == LoadScreenModal.ids.confirm_load_screen_btn(
        "ppq-load-screen-modal"
    ):
        if ppq_load_screen_confirm_click is not None:
            if ppq_load_screen_confirm_click > 0:
                pass
    elif ctx.triggered_id == SaveScreenModal.ids.confirm_save_screen_btn(
        "ppq-save-screen-modal"
    ):
        if ppq_load_screen_confirm_click is not None:
            if ppq_load_screen_confirm_click > 0:
                pass
