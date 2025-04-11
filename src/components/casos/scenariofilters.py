from dash import html, dcc, callback, Input, State, Output, MATCH
from dash.exceptions import PreventUpdate
import uuid
import pandas as pd
from io import StringIO
import src.utils.dropdowns as dropdowns
import src.utils.data as data

NOMES_SUBMERCADOS = {
    "SUDESTE": "'SUDESTE'|'SE'",
    "SUL": "'SUL'|'S'",
    "NORDESTE": "'NORDESTE'|'NE'",
    "NORTE": "'NORTE'|'N'",
    "FC": "'FC'",
}

GRUPOS_SUBMERCADOS = {
    "SUDESTE": "SUDESTE",
    "SE": "SUDESTE",
    "SUL": "SUL",
    "S": "SUL",
    "NORDESTE": "NORDESTE",
    "NE": "NORDESTE",
    "NORTE": "NORTE",
    "N": "NORTE",
}


class ScenarioFilters(html.Div):
    class ids:
        studies = lambda aio_id: {
            "component": "ScenarioFilters",
            "subcomponent": "studies",
            "aio_id": aio_id,
        }
        data = lambda aio_id: {
            "component": "ScenarioFilters",
            "subcomponent": "data",
            "aio_id": aio_id,
        }
        options = lambda aio_id: {
            "component": "ScenarioFilters",
            "subcomponent": "options",
            "aio_id": aio_id,
        }
        filters = lambda aio_id: {
            "component": "ScenarioFilters",
            "subcomponent": "filters",
            "aio_id": aio_id,
        }
        usina_dropdown = lambda aio_id: {
            "component": "ScenarioFilters",
            "subcomponent": "usina_dropdown",
            "aio_id": aio_id,
        }
        usina_dropdown_container = lambda aio_id: {
            "component": "ScenarioFilters",
            "subcomponent": "usina_dropdown_container",
            "aio_id": aio_id,
        }
        ree_dropdown = lambda aio_id: {
            "component": "ScenarioFilters",
            "subcomponent": "ree_dropdown",
            "aio_id": aio_id,
        }
        ree_dropdown_container = lambda aio_id: {
            "component": "ScenarioFilters",
            "subcomponent": "ree_dropdown_container",
            "aio_id": aio_id,
        }
        iteracao_dropdown = lambda aio_id: {
            "component": "ScenarioFilters",
            "subcomponent": "iteracao_dropdown",
            "aio_id": aio_id,
        }
        iteracao_dropdown_container = lambda aio_id: {
            "component": "ScenarioFilters",
            "subcomponent": "iteracao_dropdown_container",
            "aio_id": aio_id,
        }
        etapa_dropdown = lambda aio_id: {
            "component": "ScenarioFilters",
            "subcomponent": "etapa_dropdown",
            "aio_id": aio_id,
        }
        etapa_dropdown_container = lambda aio_id: {
            "component": "ScenarioFilters",
            "subcomponent": "etapa_dropdown_container",
            "aio_id": aio_id,
        }
        resolution_dropdown = lambda aio_id: {
            "component": "ScenarioFilters",
            "subcomponent": "resolution_dropdown",
            "aio_id": aio_id,
        }
        resolution_dropdown_container = lambda aio_id: {
            "component": "ScenarioFilters",
            "subcomponent": "resolution_dropdown_container",
            "aio_id": aio_id,
        }
        variable_dropdown = lambda aio_id: {
            "component": "ScenarioFilters",
            "subcomponent": "variable_dropdown",
            "aio_id": aio_id,
        }
        download = lambda aio_id: {
            "component": "ScenarioFilters",
            "subcomponent": "download",
            "aio_id": aio_id,
        }
        download_btn = lambda aio_id: {
            "component": "ScenarioFilters",
            "subcomponent": "download_btn",
            "aio_id": aio_id,
        }
        updater = lambda aio_id: {
            "component": "ScenarioFilters",
            "subcomponent": "updater",
            "aio_id": aio_id,
        }

    ids = ids

    def __init__(
        self,
        aio_id=None,
        usina_dropdown_props=None,
        ree_dropdown_props=None,
        iteracao_dropdown_props=None,
        etapa_dropdown_props=None,
        resolution_dropdown_props=None,
        variable_dropdown_props=None,
    ):
        if aio_id is None:
            aio_id = str(uuid.uuid4())
        pass

        usina_dropdown_props = (
            usina_dropdown_props.copy() if usina_dropdown_props else {}
        )
        ree_dropdown_props = (
            ree_dropdown_props.copy() if ree_dropdown_props else {}
        )
        iteracao_dropdown_props = (
            iteracao_dropdown_props.copy() if iteracao_dropdown_props else {}
        )
        etapa_dropdown_props = (
            etapa_dropdown_props.copy() if etapa_dropdown_props else {}
        )
        resolution_dropdown_props = (
            resolution_dropdown_props.copy()
            if resolution_dropdown_props
            else {}
        )
        variable_dropdown_props = (
            variable_dropdown_props.copy() if variable_dropdown_props else {}
        )

        if "style" not in usina_dropdown_props:
            usina_dropdown_props["style"] = {"display": "none"}
        if "style" not in ree_dropdown_props:
            ree_dropdown_props["style"] = {"display": "none"}
        if "style" not in iteracao_dropdown_props:
            iteracao_dropdown_props["style"] = {"display": "none"}
        if "style" not in etapa_dropdown_props:
            etapa_dropdown_props["style"] = {"display": "none"}
        if "style" not in resolution_dropdown_props:
            resolution_dropdown_props["style"] = {"display": "none"}
        # if "style" not in variable_dropdown_props:
        #     variable_dropdown_props["style"] = {"display": "none"}

        if "className" not in usina_dropdown_props:
            usina_dropdown_props["className"] = "dropdown-container"
        if "className" not in ree_dropdown_props:
            ree_dropdown_props["className"] = "dropdown-container"
        if "className" not in iteracao_dropdown_props:
            iteracao_dropdown_props["className"] = "dropdown-container"
        if "className" not in etapa_dropdown_props:
            etapa_dropdown_props["className"] = "dropdown-container"
        if "className" not in resolution_dropdown_props:
            resolution_dropdown_props["className"] = "dropdown-container"
        if "className" not in variable_dropdown_props:
            variable_dropdown_props["className"] = "dropdown-container"

        if "children" not in usina_dropdown_props:
            usina_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.usina_dropdown(aio_id),
                options=[],
                value=None,
                placeholder="Usina",
                className="variable-dropdown",
            )
        if "children" not in ree_dropdown_props:
            ree_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.ree_dropdown(aio_id),
                options=[],
                style={
                    "width": "150px",
                },
                value=None,
                placeholder="REE",
                className="variable-dropdown",
            )
        if "children" not in iteracao_dropdown_props:
            iteracao_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.iteracao_dropdown(aio_id),
                options=[],
                style={
                    "width": "100px",
                },
                value=None,
                placeholder="Iteração",
                className="variable-dropdown",
            )
        if "children" not in etapa_dropdown_props:
            etapa_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.etapa_dropdown(aio_id),
                options=[],
                value=None,
                placeholder="Etapa",
                className="variable-dropdown",
            )
        if "children" not in resolution_dropdown_props:
            resolution_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.resolution_dropdown(aio_id),
                options=[],
                value=None,
                placeholder="Agregação",
                className="variable-dropdown",
            )
        if "children" not in variable_dropdown_props:
            variable_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.variable_dropdown(aio_id),
                options=[],
                style={
                    "width": "250px",
                },
                value=None,
                placeholder="Variavel",
                className="variable-dropdown",
            )

        super().__init__(
            children=[
                html.Div(
                    id=self.ids.usina_dropdown_container(aio_id),
                    **usina_dropdown_props,
                ),
                html.Div(
                    id=self.ids.ree_dropdown_container(aio_id),
                    **ree_dropdown_props,
                ),
                html.Div(
                    id=self.ids.iteracao_dropdown_container(aio_id),
                    **iteracao_dropdown_props,
                ),
                html.Div(
                    id=self.ids.etapa_dropdown_container(aio_id),
                    **etapa_dropdown_props,
                ),
                html.Div(
                    id=self.ids.resolution_dropdown_container(aio_id),
                    **resolution_dropdown_props,
                ),
                html.Div(
                    **variable_dropdown_props,
                ),
                dcc.Store(
                    id=self.ids.studies(aio_id),
                    storage_type="memory",
                ),
                dcc.Store(
                    id=self.ids.data(aio_id),
                    storage_type="memory",
                ),
                dcc.Store(
                    id=self.ids.options(aio_id),
                    storage_type="memory",
                ),
                dcc.Store(
                    id=self.ids.filters(aio_id),
                    storage_type="memory",
                ),
                dcc.Download(id=self.ids.download(aio_id)),
                html.Button(
                    "CSV",
                    id=self.ids.download_btn(aio_id),
                ),
            ],
            className="card-menu-row",
        )

    @callback(
        Output(ids.usina_dropdown_container(MATCH), "style"),
        Input(ids.resolution_dropdown(MATCH), "value"),
    )
    def update_display_usina_dropdown(resolution: str):
        return (
            {"display": "flex"}
            if resolution == "Usina Hidroelétrica"
            else {"display": "none"}
        )

    @callback(
        Output(ids.ree_dropdown_container(MATCH), "style"),
        Input(ids.resolution_dropdown(MATCH), "value"),
    )
    def update_display_ree_dropdown(resolution: str):
        return (
            {"display": "flex"}
            if resolution == "Reservatório Equivalente"
            else {"display": "none"}
        )

    @callback(
        Output(ids.iteracao_dropdown_container(MATCH), "style"),
        Input(ids.etapa_dropdown(MATCH), "value"),
    )
    def update_display_iteracao_dropdown(etapa: str):
        return (
            {"display": "flex"}
            if etapa in ["Forward", "Backward"]
            else {"display": "none"}
        )

    @callback(
        Output(ids.etapa_dropdown_container(MATCH), "style"),
        Input(ids.studies(MATCH), "data"),
        Input(ids.resolution_dropdown(MATCH), "value"),
        Input(ids.variable_dropdown(MATCH), "value"),
    )
    def update_display_etapa_dropdown(studies_data, resolution, variable: str):
        return (
            {"display": "flex"}
            if variable is not None and resolution is not None
            else {"display": "none"}
        )

    @callback(
        Output(ids.resolution_dropdown_container(MATCH), "style"),
        Input(ids.studies(MATCH), "data"),
        Input(ids.variable_dropdown(MATCH), "value"),
    )
    def update_display_resolution_dropdown(studies_data, variable: str):
        return (
            {"display": "flex"}
            if variable is not None
            else {"display": "none"}
        )

    @callback(
        Output(ids.usina_dropdown(MATCH), "options"),
        Input(ids.studies(MATCH), "data"),
        prevent_initial_call=True,
    )
    def update_usina_options(studies_data):
        return dropdowns.update_operation_dropdown_system_entity_options_casos(
            studies_data, "UHE"
        )

    @callback(
        Output(ids.ree_dropdown(MATCH), "options"),
        Input(ids.studies(MATCH), "data"),
        prevent_initial_call=True,
    )
    def update_ree_options(studies_data):
        return dropdowns.update_operation_dropdown_system_entity_options_casos(
            studies_data, "REE"
        )

    @callback(
        Output(ids.etapa_dropdown(MATCH), "options"),
        Input(ids.studies(MATCH), "data"),
        Input(ids.variable_dropdown(MATCH), "value"),
        Input(ids.resolution_dropdown(MATCH), "value"),
        prevent_initial_call=True,
    )
    def update_etapa_options(studies_data, variable, resolution):
        return dropdowns.update_scenarios_etapa_dropdown_options_casos(
            studies_data, variable, resolution
        )

    @callback(
        Output(ids.resolution_dropdown(MATCH), "options"),
        Input(ids.studies(MATCH), "data"),
        Input(ids.variable_dropdown(MATCH), "value"),
        prevent_initial_call=True,
    )
    def update_resolution_options(studies_data, variable):
        return dropdowns.update_scenarios_resolution_dropdown_options_casos(
            studies_data, variable
        )

    @callback(
        Output(ids.iteracao_dropdown(MATCH), "options"),
        Input(ids.studies(MATCH), "data"),
        prevent_initial_call=True,
    )
    def update_iteracao_options(options):
        return list(range(1, 101))

    @callback(
        Output(ids.filters(MATCH), "data"),
        Input(ids.usina_dropdown(MATCH), "value"),
        Input(ids.ree_dropdown(MATCH), "value"),
        Input(ids.iteracao_dropdown(MATCH), "value"),
        Input(ids.etapa_dropdown(MATCH), "value"),
        Input(ids.resolution_dropdown(MATCH), "value"),
    )
    def update_filters(
        uhe: str,
        ree: str,
        iteracao: str,
        etapa: str,
        agregacao: str,
    ):
        filtros = {}
        if uhe:
            filtros["codigo_uhe"] = uhe
        if ree:
            filtros["codigo_ree"] = ree
        if iteracao:
            filtros["iteracao"] = iteracao
        if etapa:
            filtros["etapa"] = etapa
        if agregacao:
            filtros["agregacao"] = agregacao
        return filtros

    @callback(
        Output(ids.variable_dropdown(MATCH), "options"),
        Input(ids.studies(MATCH), "data"),
    )
    def update_variables_dropdown_options(studies_data):
        return dropdowns.update_scenario_variables_dropdown_options_casos(
            studies_data
        )

    @callback(
        Output(ids.data(MATCH), "data"),
        Input(ids.studies(MATCH), "data"),
        Input(ids.filters(MATCH), "data"),
        Input(ids.variable_dropdown(MATCH), "value"),
    )
    def update_data(studies, filters: dict, variable: str):
        return data.update_scenario_data_casos(
            studies, filters, variable, kind="SCENARIOS"
        )

    @callback(
        Output(ids.download(MATCH), "data"),
        Input(ids.download_btn(MATCH), "n_clicks"),
        State(ids.data(MATCH), "data"),
        State(ids.variable_dropdown(MATCH), "value"),
    )
    def generate_csv(n_clicks, operation_data, variable):
        if n_clicks is None:
            raise PreventUpdate
        if operation_data is not None:
            dados = pd.read_json(StringIO(operation_data), orient="split")
            dados["data_inicio"] = pd.to_datetime(
                dados["data_inicio"], unit="ms"
            )
            dados["data_fim"] = pd.to_datetime(dados["data_fim"], unit="ms")
            return dcc.send_data_frame(dados.to_csv, f"{variable}.csv")
