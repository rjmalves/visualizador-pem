import uuid
from io import StringIO

import pandas as pd
from dash import MATCH, Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate

import src.utils.data as data
import src.utils.dropdowns as dropdowns
from src.utils.constants import END_DATE_COLUMN, START_DATE_COLUMN

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


class OperationFiltersEncadeador(html.Div):
    class ids:
        studies = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "studies",
            "aio_id": aio_id,
        }
        data = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "data",
            "aio_id": aio_id,
        }
        options = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "options",
            "aio_id": aio_id,
        }
        filters = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "filters",
            "aio_id": aio_id,
        }
        uhe_dropdown = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "uhe_dropdown",
            "aio_id": aio_id,
        }
        uhe_dropdown_container = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "uhe_dropdown_container",
            "aio_id": aio_id,
        }
        ute_dropdown = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "ute_dropdown",
            "aio_id": aio_id,
        }
        ute_dropdown_container = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "ute_dropdown_container",
            "aio_id": aio_id,
        }
        ree_dropdown = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "ree_dropdown",
            "aio_id": aio_id,
        }
        ree_dropdown_container = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "ree_dropdown_container",
            "aio_id": aio_id,
        }
        submercado_dropdown = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "submercado_dropdown",
            "aio_id": aio_id,
        }
        submercado_dropdown_container = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "submercado_dropdown_container",
            "aio_id": aio_id,
        }
        submercado_de_dropdown = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "submercado_de_dropdown",
            "aio_id": aio_id,
        }
        submercado_de_dropdown_container = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "submercado_de_dropdown_container",
            "aio_id": aio_id,
        }
        submercado_para_dropdown = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "submercado_para_dropdown",
            "aio_id": aio_id,
        }
        submercado_para_dropdown_container = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "submercado_para_dropdown_container",
            "aio_id": aio_id,
        }
        # patamar_dropdown = lambda aio_id: {
        #     "component": "OperationFiltersEncadeador",
        #     "subcomponent": "patamar_dropdown",
        #     "aio_id": aio_id,
        # }
        # patamar_dropdown_container = lambda aio_id: {
        #     "component": "OperationFiltersEncadeador",
        #     "subcomponent": "patamar_dropdown_container",
        #     "aio_id": aio_id,
        # }
        estagio_dropdown = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "estagio_dropdown",
            "aio_id": aio_id,
        }
        estagio_dropdown_container = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "estagio_dropdown_container",
            "aio_id": aio_id,
        }
        resolution_dropdown = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "resolution_dropdown",
            "aio_id": aio_id,
        }
        resolution_dropdown_container = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "resolution_dropdown_container",
            "aio_id": aio_id,
        }
        variable_dropdown = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "variable_dropdown",
            "aio_id": aio_id,
        }
        download = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "download",
            "aio_id": aio_id,
        }
        download_btn = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "download_btn",
            "aio_id": aio_id,
        }
        updater = lambda aio_id: {
            "component": "OperationFiltersEncadeador",
            "subcomponent": "updater",
            "aio_id": aio_id,
        }

    ids = ids

    def __init__(
        self,
        aio_id=None,
        uhe_dropdown_props=None,
        ute_dropdown_props=None,
        ree_dropdown_props=None,
        submercado_dropdown_props=None,
        submercado_de_dropdown_props=None,
        submercado_para_dropdown_props=None,
        # patamar_dropdown_props=None,
        estagio_dropdown_props=None,
        resolution_dropdown_props=None,
        variable_dropdown_props=None,
    ):
        if aio_id is None:
            aio_id = str(uuid.uuid4())
        pass

        uhe_dropdown_props = (
            uhe_dropdown_props.copy() if uhe_dropdown_props else {}
        )
        ute_dropdown_props = (
            ute_dropdown_props.copy() if ute_dropdown_props else {}
        )
        ree_dropdown_props = (
            ree_dropdown_props.copy() if ree_dropdown_props else {}
        )
        submercado_dropdown_props = (
            submercado_dropdown_props.copy()
            if submercado_dropdown_props
            else {}
        )
        submercado_de_dropdown_props = (
            submercado_de_dropdown_props.copy()
            if submercado_de_dropdown_props
            else {}
        )
        submercado_para_dropdown_props = (
            submercado_para_dropdown_props.copy()
            if submercado_para_dropdown_props
            else {}
        )
        # patamar_dropdown_props = (
        #     patamar_dropdown_props.copy() if patamar_dropdown_props else {}
        # )
        estagio_dropdown_props = (
            estagio_dropdown_props.copy() if estagio_dropdown_props else {}
        )
        resolution_dropdown_props = (
            resolution_dropdown_props.copy()
            if resolution_dropdown_props
            else {}
        )
        variable_dropdown_props = (
            variable_dropdown_props.copy() if variable_dropdown_props else {}
        )

        if "style" not in uhe_dropdown_props:
            uhe_dropdown_props["style"] = {"display": "none"}
        if "style" not in ute_dropdown_props:
            ute_dropdown_props["style"] = {"display": "none"}
        if "style" not in ree_dropdown_props:
            ree_dropdown_props["style"] = {"display": "none"}
        if "style" not in submercado_dropdown_props:
            submercado_dropdown_props["style"] = {"display": "none"}
        if "style" not in submercado_de_dropdown_props:
            submercado_de_dropdown_props["style"] = {"display": "none"}
        if "style" not in submercado_para_dropdown_props:
            submercado_para_dropdown_props["style"] = {"display": "none"}
        # if "style" not in patamar_dropdown_props:
        #     patamar_dropdown_props["style"] = {"display": "none"}
        if "style" not in estagio_dropdown_props:
            estagio_dropdown_props["style"] = {"display": "none"}
        if "style" not in resolution_dropdown_props:
            resolution_dropdown_props["style"] = {"display": "none"}
        # if "style" not in variable_dropdown_props:
        #     variable_dropdown_props["style"] = {"display": "none"}

        if "className" not in uhe_dropdown_props:
            uhe_dropdown_props["className"] = "dropdown-container"
        if "className" not in ute_dropdown_props:
            ute_dropdown_props["className"] = "dropdown-container"
        if "className" not in ree_dropdown_props:
            ree_dropdown_props["className"] = "dropdown-container"
        if "className" not in submercado_dropdown_props:
            submercado_dropdown_props["className"] = "dropdown-container"
        if "className" not in submercado_de_dropdown_props:
            submercado_de_dropdown_props["className"] = "dropdown-container"
        if "className" not in submercado_para_dropdown_props:
            submercado_para_dropdown_props["className"] = "dropdown-container"
        # if "className" not in patamar_dropdown_props:
        #     patamar_dropdown_props["className"] = "dropdown-container"
        if "className" not in estagio_dropdown_props:
            estagio_dropdown_props["className"] = "dropdown-container"
        if "className" not in resolution_dropdown_props:
            resolution_dropdown_props["className"] = "dropdown-container"
        if "className" not in variable_dropdown_props:
            variable_dropdown_props["className"] = "dropdown-container"

        if "children" not in uhe_dropdown_props:
            uhe_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.uhe_dropdown(aio_id),
                options=[],
                value=None,
                placeholder="Usina",
                className="variable-dropdown",
            )
        if "children" not in ute_dropdown_props:
            ute_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.ute_dropdown(aio_id),
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
                style={
                    "width": "150px",
                },
                value=None,
                placeholder="REE",
                className="variable-dropdown",
            )
        if "children" not in submercado_dropdown_props:
            submercado_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.submercado_dropdown(aio_id),
                options=[],
                style={
                    "width": "150px",
                },
                style={
                    "width": "150px",
                },
                value=None,
                placeholder="Submercado",
                className="variable-dropdown",
            )
        if "children" not in submercado_de_dropdown_props:
            submercado_de_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.submercado_de_dropdown(aio_id),
                options=[],
                style={
                    "width": "150px",
                },
                value=None,
                placeholder="Submercado De",
                className="variable-dropdown",
            )
        if "children" not in submercado_para_dropdown_props:
            submercado_para_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.submercado_para_dropdown(aio_id),
                options=[],
                style={
                    "width": "150px",
                },
                value=None,
                placeholder="Submercado Para",
                className="variable-dropdown",
            )
        # if "children" not in patamar_dropdown_props:
        #     patamar_dropdown_props["children"] = dcc.Dropdown(
        #         id=self.ids.patamar_dropdown(aio_id),
        #         options=[],
        #         value=None,
        #         placeholder="Patamar",
        #         className="variable-dropdown",
        #     )
        if "children" not in estagio_dropdown_props:
            estagio_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.estagio_dropdown(aio_id),
                options=[],
                style={
                    "width": "100px",
                },
                style={
                    "width": "100px",
                },
                value=None,
                placeholder="Estagio",
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
                    "width": "400px",
                },
                style={
                    "width": "400px",
                },
                value=None,
                placeholder="Variavel",
                className="variable-dropdown",
            )

        super().__init__(
            children=[
                html.Div(
                    id=self.ids.estagio_dropdown_container(aio_id),
                    **estagio_dropdown_props,
                ),
                html.Div(
                    id=self.ids.uhe_dropdown_container(aio_id),
                    **uhe_dropdown_props,
                ),
                html.Div(
                    id=self.ids.ute_dropdown_container(aio_id),
                    **ute_dropdown_props,
                ),
                html.Div(
                    id=self.ids.ree_dropdown_container(aio_id),
                    **ree_dropdown_props,
                ),
                html.Div(
                    id=self.ids.submercado_dropdown_container(aio_id),
                    **submercado_dropdown_props,
                ),
                html.Div(
                    id=self.ids.submercado_de_dropdown_container(aio_id),
                    **submercado_de_dropdown_props,
                ),
                html.Div(
                    id=self.ids.submercado_para_dropdown_container(aio_id),
                    **submercado_para_dropdown_props,
                ),
                # html.Div(
                #     id=self.ids.patamar_dropdown_container(aio_id),
                #     **patamar_dropdown_props,
                # ),
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
        Output(ids.uhe_dropdown_container(MATCH), "style"),
        Input(ids.resolution_dropdown(MATCH), "value"),
        prevent_initial_call=True,
    )
    def update_display_uhe_dropdown(resolution: str):
        return (
            {"display": "flex"}
            if resolution == "Usina Hidroelétrica"
            else {"display": "none"}
        )

    @callback(
        Output(ids.ute_dropdown_container(MATCH), "style"),
        Input(ids.resolution_dropdown(MATCH), "value"),
        prevent_initial_call=True,
    )
    def update_display_ute_dropdown(resolution: str):
        return (
            {"display": "flex"}
            if resolution == "Usina Termelétrica"
            else {"display": "none"}
        )

    @callback(
        Output(ids.ree_dropdown_container(MATCH), "style"),
        Input(ids.resolution_dropdown(MATCH), "value"),
        prevent_initial_call=True,
    )
    def update_display_ree_dropdown(resolution: str):
        return (
            {"display": "flex"}
            if resolution == "Reservatório Equivalente"
            else {"display": "none"}
        )

    @callback(
        Output(ids.submercado_dropdown_container(MATCH), "style"),
        Input(ids.resolution_dropdown(MATCH), "value"),
        prevent_initial_call=True,
    )
    def update_display_submercado_dropdown(resolution: str):
        return (
            {"display": "flex"}
            if resolution == "Submercado"
            else {"display": "none"}
        )

    @callback(
        Output(ids.submercado_de_dropdown_container(MATCH), "style"),
        Input(ids.resolution_dropdown(MATCH), "value"),
        prevent_initial_call=True,
    )
    def update_display_submercado_de_dropdown(resolution: str):
        return (
            {"display": "flex"}
            if resolution == "Par de Submercados"
            else {"display": "none"}
        )

    @callback(
        Output(ids.submercado_para_dropdown_container(MATCH), "style"),
        Input(ids.resolution_dropdown(MATCH), "value"),
        prevent_initial_call=True,
    )
    def update_display_submercado_para_dropdown(resolution: str):
        return (
            {"display": "flex"}
            if resolution == "Par de Submercados"
            else {"display": "none"}
        )

    # @callback(
    #     Output(ids.patamar_dropdown_container(MATCH), "style"),
    #     Input(ids.resolution_dropdown(MATCH), "value"),
    #     Input(ids.variable_dropdown(MATCH), "value"),
    #     prevent_initial_call=True,
    # )
    # def update_display_patamar_dropdown(agregacao: str, variavel: str):
    #     should_display = all([agregacao is not None, variavel is not None])
    #     return {"display": "flex"} if should_display else {"display": "none"}

    @callback(
        Output(ids.resolution_dropdown_container(MATCH), "style"),
        Input(ids.variable_dropdown(MATCH), "value"),
        prevent_initial_call=True,
    )
    def update_display_resolution_dropdown(variavel: str):
        return (
            {"display": "flex"} if variavel is not None else {"display": "none"}
        )

    @callback(
        Output(ids.filters(MATCH), "data"),
        Input(ids.uhe_dropdown(MATCH), "value"),
        Input(ids.ute_dropdown(MATCH), "value"),
        Input(ids.ree_dropdown(MATCH), "value"),
        Input(ids.submercado_dropdown(MATCH), "value"),
        Input(ids.submercado_de_dropdown(MATCH), "value"),
        Input(ids.submercado_para_dropdown(MATCH), "value"),
        # Input(ids.patamar_dropdown(MATCH), "value"),
        Input(ids.estagio_dropdown(MATCH), "value"),
        Input(ids.resolution_dropdown(MATCH), "value"),
    )
    def update_filters(
        uhe: int,
        ute: int,
        ree: int,
        submercado: int,
        submercado_de: int,
        submercado_para: int,
        # patamar: int,
        estagio: int,
        agregacao: str,
    ):
        filtros = {}
        if uhe:
            filtros["codigo_uhe"] = uhe
        if ute:
            filtros["codigo_ute"] = ute
        if ree:
            filtros["codigo_ree"] = ree
        if submercado:
            filtros["codigo_submercado"] = submercado
        if submercado_de:
            filtros["codigo_submercado_de"] = submercado_de
        if submercado_para:
            filtros["codigo_submercado_para"] = submercado_para
        # if patamar:
        #     filtros["patamar"] = patamar
        if estagio:
            filtros["estagio"] = estagio
        if agregacao:
            filtros["agregacao"] = agregacao
        return filtros

    @callback(
        Output(ids.estagio_dropdown(MATCH), "options"),
        Input(ids.studies(MATCH), "data"),
        prevent_initial_call=True,
    )
    def update_variables_estagio_dropdown_options(studies_data):
        return dropdowns.update_operation_dropdown_system_entity_options_casos(
            studies_data, "EST"
        )

    # @callback(
    #     Output(ids.patamar_dropdown(MATCH), "options"),
    #     Input(ids.studies(MATCH), "data"),
    #     prevent_initial_call=True,
    # )
    # def update_variables_patamar_dropdown_options(studies_data):
    #     return dropdowns.update_operation_dropdown_system_entity_options_casos(
    #         studies_data, "PAT"
    #     )

    @callback(
        Output(ids.submercado_dropdown(MATCH), "options"),
        Input(ids.studies(MATCH), "data"),
        prevent_initial_call=True,
    )
    def update_variables_submercado_dropdown_options(studies_data):
        return dropdowns.update_operation_dropdown_system_entity_options_casos(
            studies_data, "SBM"
        )

    @callback(
        Output(ids.submercado_de_dropdown(MATCH), "options"),
        Input(ids.studies(MATCH), "data"),
        prevent_initial_call=True,
    )
    def update_variables_submercado_de_dropdown_options(studies_data):
        return dropdowns.update_operation_dropdown_system_entity_options_casos(
            studies_data, "SBM"
        )

    @callback(
        Output(ids.submercado_para_dropdown(MATCH), "options"),
        Input(ids.studies(MATCH), "data"),
        prevent_initial_call=True,
    )
    def update_variables_submercado_para_dropdown_options(studies_data):
        return dropdowns.update_operation_dropdown_system_entity_options_casos(
            studies_data, "SBM"
        )

    @callback(
        Output(ids.ree_dropdown(MATCH), "options"),
        Input(ids.studies(MATCH), "data"),
        prevent_initial_call=True,
    )
    def update_variables_ree_dropdown_options(studies_data):
        return dropdowns.update_operation_dropdown_system_entity_options_casos(
            studies_data, "REE"
        )

    @callback(
        Output(ids.uhe_dropdown(MATCH), "options"),
        Input(ids.studies(MATCH), "data"),
        prevent_initial_call=True,
    )
    def update_variables_uhe_dropdown_options(studies_data):
        return dropdowns.update_operation_dropdown_system_entity_options_casos(
            studies_data, "UHE"
        )

    @callback(
        Output(ids.ute_dropdown(MATCH), "options"),
        Input(ids.studies(MATCH), "data"),
        prevent_initial_call=True,
    )
    def update_variables_ute_dropdown_options(studies_data):
        return dropdowns.update_operation_dropdown_system_entity_options_casos(
            studies_data, "UTE"
        )

    @callback(
        Output(ids.variable_dropdown(MATCH), "options"),
        Input(ids.studies(MATCH), "data"),
        prevent_initial_call=True,
    )
    def update_variable_dropdown_options(studies_data):
        return dropdowns.update_operation_variables_dropdown_options_casos(
            studies_data
        )

    @callback(
        Output(ids.resolution_dropdown(MATCH), "options"),
        Input(ids.studies(MATCH), "data"),
        Input(ids.variable_dropdown(MATCH), "value"),
        prevent_initial_call=True,
    )
    def update_resolution_dropdown_options(studies_data, variable: str):
        return dropdowns.update_operation_resolution_dropdown_options_casos(
            studies_data, variable
        )

    # @callback(
    #     Output(ids.options(MATCH), "data"),
    #     Input(ids.studies(MATCH), "data"),
    #     Input(ids.variable_dropdown(MATCH), "value"),
    # )
    # def update_options(studies, variable: str):
    #     return dropdowns.update_operation_options_encadeador(studies, variable)

    @callback(
        Output(ids.data(MATCH), "data"),
        Input(ids.studies(MATCH), "data"),
        Input(ids.filters(MATCH), "data"),
        Input(ids.variable_dropdown(MATCH), "value"),
    )
    def update_data(studies, filters: dict, variable: str):
        return data.update_operation_data_encadeador(
            studies, filters, variable, kind="STATISTICS"
        )

    @callback(
        Output(ids.download(MATCH), "data"),
        Input(ids.download_btn(MATCH), "n_clicks"),
        State(ids.data(MATCH), "data"),
        State(ids.variable_dropdown(MATCH), "value"),
        prevent_initial_call=True,
    )
    def generate_csv(n_clicks, operation_data, variable):
        if n_clicks is None:
            raise PreventUpdate
        if operation_data is not None:
            dados = pd.read_json(StringIO(operation_data), orient="split")
            dados[START_DATE_COLUMN] = pd.to_datetime(
                dados["data_inicio"], unit="ms"
            )
            dados[END_DATE_COLUMN] = pd.to_datetime(
                dados["data_fim"], unit="ms"
            )
            return dcc.send_data_frame(dados.to_csv, f"{variable}.csv")
