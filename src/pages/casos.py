# package imports
import dash
from dash import html, dcc, callback, Input, Output, State, ctx
from dash.exceptions import PreventUpdate
from src.components.newstudymodal import NewStudyModal
from src.components.editstudymodal import EditStudyModal
from src.components.currentstudiestable import CurrentStudiesTable
from src.components.casos.operationgraph import OperationGraph

from src.components.casos.spatialviewgraph import SpatialViewGraph
from src.components.casos.scenariograph import ScenarioGraph
from src.components.casos.acumprobgraph import AcumProbGraph
from src.components.casos.timecostsgraph import TimeCostsGraph
from src.components.casos.convergencegraph import ConvergenceGraph
from src.components.casos.resourcesgraph import ResourcesGraph
from src.components.savescreenmodal import SaveScreenModal
from src.components.loadscreenmodal import LoadScreenModal
from flask_login import current_user
from src.utils.log import Log
from src.utils.settings import Settings
import src.utils.modals as modals
import src.utils.data as data
import src.utils.db as db


dash.register_page(
    __name__,
    path="/",
    redirect_from=["/casos"],
    title="Casos",
    path_template="/casos/<screen_id>",
)

casos_url = dcc.Location("casos-url")


def layout(screen_id=None):
    return html.Div(
        [
            NewStudyModal(aio_id="casos-modal"),
            EditStudyModal(aio_id="casos-edit-modal"),
            CurrentStudiesTable(aio_id="casos-current-studies"),
            OperationGraph(aio_id="casos-operation-graph"),
            AcumProbGraph(aio_id="casos-permanencia-graph"),
            SpatialViewGraph(aio_id="casos-espacial-graph"),
            ScenarioGraph(aio_id="casos-scenario-graph"),
            TimeCostsGraph(aio_id="casos-tempo-custos-graph"),
            ConvergenceGraph(aio_id="casos-convergence-graph"),
            ResourcesGraph(aio_id="casos-resources-graph"),
            SaveScreenModal(aio_id="casos-save-screen-modal"),
            LoadScreenModal(aio_id="casos-load-screen-modal"),
            dcc.Store("casos-screen", storage_type="memory", data=screen_id),
            dcc.Location("casos-url"),
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
    prevent_initial_call=True,
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
    prevent_initial_call=True,
)
def toggle_casos_modal(src1, src2, is_open, selected):
    if selected is None:
        raise PreventUpdate
    elif len(selected) == 0:
        raise PreventUpdate
    else:
        return modals.toggle_modal(src1, src2, is_open)


@callback(
    Output(SaveScreenModal.ids.modal("casos-save-screen-modal"), "is_open"),
    [
        Input(
            CurrentStudiesTable.ids.save_study_btn("casos-current-studies"),
            "n_clicks",
        ),
        Input(
            SaveScreenModal.ids.confirm_save_screen_btn(
                "casos-save-screen-modal"
            ),
            "n_clicks",
        ),
    ],
    [State(SaveScreenModal.ids.modal("casos-save-screen-modal"), "is_open")],
    prevent_initial_call=True,
)
def toggle_casos_modal(src1, src2, is_open):
    if current_user.is_authenticated:
        return modals.toggle_modal(src1, src2, is_open)
    else:
        return False


@callback(
    Output(LoadScreenModal.ids.modal("casos-load-screen-modal"), "is_open"),
    [
        Input(
            CurrentStudiesTable.ids.load_study_btn("casos-current-studies"),
            "n_clicks",
        ),
        Input(
            LoadScreenModal.ids.confirm_load_screen_btn(
                "casos-load-screen-modal"
            ),
            "n_clicks",
        ),
    ],
    [State(LoadScreenModal.ids.modal("casos-load-screen-modal"), "is_open")],
    prevent_initial_call=True,
)
def toggle_casos_modal(src1, src2, is_open):
    if current_user.is_authenticated:
        return modals.toggle_modal(src1, src2, is_open)
    else:
        return False


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
        "casos",
    )


@callback(
    Output(EditStudyModal.ids.edit_study_id("casos-edit-modal"), "data"),
    Input(
        CurrentStudiesTable.ids.selected("casos-current-studies"),
        "data",
    ),
    State(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
    prevent_initial_call=True,
)
def update_edit_study_modal_id(selected_study, current_studies):
    dados = data.extract_selected_study_data(
        selected_study,
        current_studies,
    )
    if dados is None:
        raise PreventUpdate
    else:
        return dados["table_id"]


@callback(
    Output(EditStudyModal.ids.edit_study_path("casos-edit-modal"), "value"),
    Input(
        CurrentStudiesTable.ids.selected("casos-current-studies"),
        "data",
    ),
    State(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
    prevent_initial_call=True,
)
def update_edit_study_modal_path(selected_study, current_studies):
    dados = data.extract_selected_study_data(
        selected_study,
        current_studies,
    )
    if dados is None:
        raise PreventUpdate
    else:
        return dados["path"]


@callback(
    Output(EditStudyModal.ids.edit_study_name("casos-edit-modal"), "value"),
    Input(
        CurrentStudiesTable.ids.selected("casos-current-studies"),
        "data",
    ),
    State(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
    prevent_initial_call=True,
)
def update_edit_study_modal_name(selected_study, current_studies):
    dados = data.extract_selected_study_data(
        selected_study,
        current_studies,
    )

    if dados is None:
        raise PreventUpdate
    else:
        return dados["name"]


@callback(
    Output(EditStudyModal.ids.edit_study_color("casos-edit-modal"), "value"),
    Input(
        CurrentStudiesTable.ids.selected("casos-current-studies"),
        "data",
    ),
    State(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
    prevent_initial_call=True,
)
def update_edit_study_modal_color(selected_study, current_studies):
    dados = data.extract_selected_study_data(
        selected_study,
        current_studies,
    )

    if dados is None:
        raise PreventUpdate
    else:
        return dados["color"]


@callback(
    Output(OperationGraph.ids.studies("casos-operation-graph"), "data"),
    Input(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
    prevent_initial_call=True,
)
def update_current_studies(studies_data):
    return studies_data


@callback(
    Output(AcumProbGraph.ids.studies("casos-permanencia-graph"), "data"),
    Input(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
    prevent_initial_call=True,
)
def update_current_studies(studies_data):
    return studies_data


@callback(
    Output(SpatialViewGraph.ids.studies("casos-espacial-graph"), "data"),
    Input(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
    prevent_initial_call=True,
)
def update_current_studies(studies_data):
    return studies_data


@callback(
    Output(TimeCostsGraph.ids.studies("casos-tempo-custos-graph"), "data"),
    Input(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
    prevent_initial_call=True,
)
def update_current_studies(studies_data):
    return studies_data


@callback(
    Output(ScenarioGraph.ids.studies("casos-scenario-graph"), "data"),
    Input(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
    prevent_initial_call=True,
)
def update_current_studies(studies_data):
    return studies_data


@callback(
    Output(ConvergenceGraph.ids.studies("casos-convergence-graph"), "data"),
    Input(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
    prevent_initial_call=True,
)
def update_current_studies(studies_data):
    return studies_data


@callback(
    Output(ResourcesGraph.ids.studies("casos-resources-graph"), "data"),
    Input(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
    prevent_initial_call=True,
)
def update_current_studies(studies_data):
    return studies_data


@callback(
    Output(
        SaveScreenModal.ids.current_studies("casos-save-screen-modal"), "data"
    ),
    Input(CurrentStudiesTable.ids.data("casos-current-studies"), "data"),
    prevent_initial_call=True,
)
def update_current_studies(studies_data):
    return studies_data


@callback(
    Output(
        LoadScreenModal.ids.load_screen_select("casos-load-screen-modal"),
        "options",
    ),
    Input(
        CurrentStudiesTable.ids.load_study_btn("casos-current-studies"),
        "n_clicks",
    ),
    State(
        LoadScreenModal.ids.screen_type_str("casos-load-screen-modal"), "data"
    ),
)
def update_screen_type_str(path, screen_type_str):
    return db.list_screens(screen_type_str)


@callback(
    Output("casos-url", "pathname"),
    Input(
        LoadScreenModal.ids.confirm_load_screen_btn("casos-load-screen-modal"),
        "n_clicks",
    ),
    Input(
        SaveScreenModal.ids.confirm_save_screen_btn("casos-save-screen-modal"),
        "n_clicks",
    ),
    State("_pages_location", "pathname"),
    State(
        LoadScreenModal.ids.load_screen_select("casos-load-screen-modal"),
        "value",
    ),
    State(
        SaveScreenModal.ids.new_screen_name("casos-save-screen-modal"),
        "value",
    ),
    prevent_initial_call=True,
)
def redirect_page(
    casos_load_screen_confirm_click,
    casos_save_screen_confirm_click,
    pathname,
    casos_load_screen_value,
    casos_save_screen_name,
):
    if ctx.triggered_id == LoadScreenModal.ids.confirm_load_screen_btn(
        "casos-load-screen-modal"
    ):
        if casos_load_screen_confirm_click is not None:
            if casos_load_screen_confirm_click > 0:
                Log.log().info(
                    f"Redirecionando TELA - {casos_load_screen_value}"
                )
                return Settings.url_prefix + f"casos/{casos_load_screen_value}"
    elif ctx.triggered_id == SaveScreenModal.ids.confirm_save_screen_btn(
        "casos-save-screen-modal"
    ):
        if casos_save_screen_confirm_click is not None:
            if casos_save_screen_confirm_click > 0:
                Log.log().info(
                    f"Redirecionando TELA - {casos_save_screen_name}"
                )
                return Settings.url_prefix + f"casos/{casos_save_screen_name}"
