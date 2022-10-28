from dash import Output, Input, State, html, dcc, callback, MATCH
import plotly.graph_objects as go
import src.utils.validation as validation
from src.utils.settings import Settings
from src.utils.api import API
import pandas as pd
import uuid
import os


DISCRETE_COLOR_PALLETE = [
    "rgba(249, 65, 68, 1)",
    "rgba(39, 125, 161, 1)",
    "rgba(144, 190, 109, 1)",
    "rgba(243, 114, 44, 1)",
    "rgba(87, 117, 144, 1)",
    "rgba(249, 199, 79, 1)",
    "rgba(248, 150, 30, 1)",
    "rgba(77, 144, 142, 1)",
    "rgba(249, 132, 74, 1)",
    "rgba(67, 170, 139, 1)",
]

DISCRETE_COLOR_PALLETE_BACKGROUND = [
    "rgba(249, 65, 68, 0.3)",
    "rgba(39, 125, 161, 0.3)",
    "rgba(144, 190, 109, 0.3)",
    "rgba(243, 114, 44, 0.3)",
    "rgba(87, 117, 144, 0.3)",
    "rgba(249, 199, 79, 0.3)",
    "rgba(248, 150, 30, 0.3)",
    "rgba(77, 144, 142, 0.3)",
    "rgba(249, 132, 74, 0.3)",
    "rgba(67, 170, 139, 0.3)",
]

VARIABLE_LEGENDS = {
    "COP": "R$",
    "CFU": "R$",
    "CMO": "R$ / MWh",
    "CTER": "R$",
    "DEF": "MWmed",
    "EARMI": "MWmed",
    "EARPI": "%",
    "EARMF": "MWmed",
    "EARPF": "%",
    "ENAA": "MWmed",
    "ENAM": "%",
    "EVERNT": "MWmed",
    "EVERT": "MWmed",
    "GHID": "MWmed",
    "GTER": "MWmed",
    "INT": "MWmed",
    "MER": "MWmed",
    "QAFL": "m3/s",
    "QDEF": "m3/s",
    "VAGUA": "R$ / hm3",
    "VARMI": "hm3",
    "VARMF": "hm3",
    "VARPI": "%",
    "VARPF": "%",
}

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

# All-in-One Components should be suffixed with 'AIO'
class OperationGraphAIO(html.Div):

    # A set of functions that create pattern-matching callbacks of the subcomponents
    class ids:
        data = lambda aio_id: {
            "component": "OperationGraphAIO",
            "subcomponent": "data",
            "aio_id": aio_id,
        }
        options = lambda aio_id: {
            "component": "OperationGraphAIO",
            "subcomponent": "options",
            "aio_id": aio_id,
        }
        filters = lambda aio_id: {
            "component": "OperationGraphAIO",
            "subcomponent": "filters",
            "aio_id": aio_id,
        }
        usina_dropdown = lambda aio_id: {
            "component": "OperationGraphAIO",
            "subcomponent": "usina_dropdown",
            "aio_id": aio_id,
        }
        usina_dropdown_container = lambda aio_id: {
            "component": "OperationGraphAIO",
            "subcomponent": "usina_dropdown_container",
            "aio_id": aio_id,
        }
        ree_dropdown = lambda aio_id: {
            "component": "OperationGraphAIO",
            "subcomponent": "ree_dropdown",
            "aio_id": aio_id,
        }
        ree_dropdown_container = lambda aio_id: {
            "component": "OperationGraphAIO",
            "subcomponent": "ree_dropdown_container",
            "aio_id": aio_id,
        }
        submercado_dropdown = lambda aio_id: {
            "component": "OperationGraphAIO",
            "subcomponent": "submercado_dropdown",
            "aio_id": aio_id,
        }
        submercado_dropdown_container = lambda aio_id: {
            "component": "OperationGraphAIO",
            "subcomponent": "submercado_dropdown_container",
            "aio_id": aio_id,
        }
        submercadoDe_dropdown = lambda aio_id: {
            "component": "OperationGraphAIO",
            "subcomponent": "submercadoDe_dropdown",
            "aio_id": aio_id,
        }
        submercadoDe_dropdown_container = lambda aio_id: {
            "component": "OperationGraphAIO",
            "subcomponent": "submercadoDe_dropdown_container",
            "aio_id": aio_id,
        }
        submercadoPara_dropdown = lambda aio_id: {
            "component": "OperationGraphAIO",
            "subcomponent": "submercadoPara_dropdown",
            "aio_id": aio_id,
        }
        submercadoPara_dropdown_container = lambda aio_id: {
            "component": "OperationGraphAIO",
            "subcomponent": "submercadoPara_dropdown_container",
            "aio_id": aio_id,
        }
        patamar_dropdown = lambda aio_id: {
            "component": "OperationGraphAIO",
            "subcomponent": "patamar_dropdown",
            "aio_id": aio_id,
        }
        patamar_dropdown_container = lambda aio_id: {
            "component": "OperationGraphAIO",
            "subcomponent": "patamar_dropdown_container",
            "aio_id": aio_id,
        }
        variable_dropdown = lambda aio_id: {
            "component": "OperationGraphAIO",
            "subcomponent": "variable_dropdown",
            "aio_id": aio_id,
        }
        download = lambda aio_id: {
            "component": "OperationGraphAIO",
            "subcomponent": "download",
            "aio_id": aio_id,
        }
        download_btn = lambda aio_id: {
            "component": "OperationGraphAIO",
            "subcomponent": "download_btn",
            "aio_id": aio_id,
        }
        graph = lambda aio_id: {
            "component": "OperationGraphAIO",
            "subcomponent": "graph",
            "aio_id": aio_id,
        }
        updater = lambda aio_id: {
            "component": "OperationGraphAIO",
            "subcomponent": "updater",
            "aio_id": aio_id,
        }

    # Make the ids class a public class
    ids = ids

    # Define the arguments of the All-in-One component
    def __init__(
        self,
        aio_id=None,
    ):

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        # Define the component's layout
        super().__init__(
            [
                html.Div(
                    [
                        html.H4(
                            "VARIÁVEIS DA OPERAÇÂO",
                            className="card-title",
                        ),
                        html.Div(
                            [
                                html.Div(
                                    children=[
                                        html.Div(
                                            children=[
                                                dcc.Dropdown(
                                                    id=self.ids.usina_dropdown(
                                                        aio_id
                                                    ),
                                                    options=[],
                                                    value=None,
                                                    placeholder="Usina",
                                                    className="variable-dropdown",
                                                )
                                            ],
                                            style={"display": "none"},
                                            id=self.ids.usina_dropdown_container(
                                                aio_id
                                            ),
                                            className="dropdown-container",
                                        ),
                                        html.Div(
                                            children=[
                                                dcc.Dropdown(
                                                    id=self.ids.ree_dropdown(
                                                        aio_id
                                                    ),
                                                    options=[],
                                                    value=None,
                                                    placeholder="REE",
                                                    className="variable-dropdown",
                                                )
                                            ],
                                            style={"display": "none"},
                                            id=self.ids.ree_dropdown_container(
                                                aio_id
                                            ),
                                            className="dropdown-container",
                                        ),
                                        html.Div(
                                            children=[
                                                dcc.Dropdown(
                                                    id=self.ids.submercado_dropdown(
                                                        aio_id
                                                    ),
                                                    options=[],
                                                    value=None,
                                                    placeholder="Submercado",
                                                    className="variable-dropdown",
                                                )
                                            ],
                                            style={"display": "none"},
                                            id=self.ids.submercado_dropdown_container(
                                                aio_id
                                            ),
                                            className="dropdown-container",
                                        ),
                                        html.Div(
                                            children=[
                                                dcc.Dropdown(
                                                    id=self.ids.submercadoDe_dropdown(
                                                        aio_id
                                                    ),
                                                    options=[],
                                                    value=None,
                                                    placeholder="Submercado De",
                                                    className="variable-dropdown",
                                                )
                                            ],
                                            style={"display": "none"},
                                            id=self.ids.submercadoDe_dropdown_container(
                                                aio_id
                                            ),
                                            className="dropdown-container",
                                        ),
                                        html.Div(
                                            children=[
                                                dcc.Dropdown(
                                                    id=self.ids.submercadoPara_dropdown(
                                                        aio_id
                                                    ),
                                                    options=[],
                                                    value=None,
                                                    placeholder="Submercado Para",
                                                    className="variable-dropdown",
                                                )
                                            ],
                                            style={"display": "none"},
                                            id=self.ids.submercadoPara_dropdown_container(
                                                aio_id
                                            ),
                                            className="dropdown-container",
                                        ),
                                        html.Div(
                                            children=[
                                                dcc.Dropdown(
                                                    id=self.ids.patamar_dropdown(
                                                        aio_id
                                                    ),
                                                    options=[],
                                                    value=None,
                                                    placeholder="Patamar",
                                                    className="variable-dropdown",
                                                )
                                            ],
                                            style={"display": "none"},
                                            id=self.ids.patamar_dropdown_container(
                                                aio_id
                                            ),
                                            className="dropdown-container",
                                        ),
                                        html.Div(
                                            children=[
                                                dcc.Dropdown(
                                                    id=self.ids.variable_dropdown(
                                                        aio_id
                                                    ),
                                                    options=[],
                                                    value=None,
                                                    placeholder="Variavel",
                                                    className="variable-dropdown",
                                                )
                                            ],
                                            className="dropdown-container",
                                        ),
                                        html.Button(
                                            "CSV",
                                            id=self.ids.download_btn(aio_id),
                                        ),
                                    ],
                                    className="card-menu-row",
                                ),
                            ],
                            className="card-menu",
                        ),
                    ],
                    className="card-header",
                ),
                html.Div(
                    dcc.Graph(id=self.ids.graph(aio_id)),
                    className="card-content",
                ),
                dcc.Interval(
                    id=self.ids.updater(aio_id),
                    interval=int(Settings.graphs_update_period),
                    n_intervals=0,
                ),
                dcc.Store(
                    id=self.ids.data(aio_id),
                    storage_type=Settings.storage,
                ),
                dcc.Store(
                    id=self.ids.options(aio_id),
                    storage_type=Settings.storage,
                ),
                dcc.Store(
                    id=self.ids.filters(aio_id),
                    storage_type=Settings.storage,
                ),
                dcc.Download(id=self.ids.download(aio_id)),
            ],
            className="card",
        )

    @callback(
        Output(ids.usina_dropdown_container(MATCH), "style"),
        Input(ids.variable_dropdown(MATCH), "value"),
    )
    def update_display_usina_dropdown(variavel: str):
        agregacao_espacial = variavel.split("_")[1] if variavel else ""
        return (
            {"display": "flex"}
            if agregacao_espacial in ["UHE", "UTE", "UEE"]
            else {"display": "none"}
        )

    @callback(
        Output(ids.ree_dropdown_container(MATCH), "style"),
        Input(ids.variable_dropdown(MATCH), "value"),
    )
    def update_display_ree_dropdown(variavel: str):
        agregacao_espacial = variavel.split("_")[1] if variavel else ""
        return (
            {"display": "flex"}
            if agregacao_espacial == "REE"
            else {"display": "none"}
        )

    @callback(
        Output(ids.submercado_dropdown_container(MATCH), "style"),
        Input(ids.variable_dropdown(MATCH), "value"),
    )
    def update_display_submercado_dropdown(variavel: str):
        agregacao_espacial = variavel.split("_")[1] if variavel else ""
        return (
            {"display": "flex"}
            if agregacao_espacial == "SBM"
            else {"display": "none"}
        )

    @callback(
        Output(ids.submercadoDe_dropdown_container(MATCH), "style"),
        Input(ids.variable_dropdown(MATCH), "value"),
    )
    def update_display_submercadoDe_dropdown(variavel: str):
        agregacao_espacial = variavel.split("_")[1] if variavel else ""
        return (
            {"display": "flex"}
            if agregacao_espacial == "SBP"
            else {"display": "none"}
        )

    @callback(
        Output(ids.submercadoPara_dropdown_container(MATCH), "style"),
        Input(ids.variable_dropdown(MATCH), "value"),
    )
    def update_display_submercadoPara_dropdown(variavel: str):
        agregacao_espacial = variavel.split("_")[1] if variavel else ""
        return (
            {"display": "flex"}
            if agregacao_espacial == "SBP"
            else {"display": "none"}
        )

    @callback(
        Output(ids.patamar_dropdown_container(MATCH), "style"),
        Input(ids.variable_dropdown(MATCH), "value"),
    )
    def update_display_patamar_dropdown(variavel: str):
        agregacao_temporal = variavel.split("_")[2] if variavel else ""
        return (
            {"display": "flex"}
            if agregacao_temporal == "PAT"
            else {"display": "none"}
        )

    @callback(
        Output(ids.usina_dropdown(MATCH), "options"),
        Input(ids.updater(MATCH), "n_intervals"),
        Input(ids.options(MATCH), "data"),
    )
    def update_usina_options(interval, options):
        if options:
            if "usina" in options.keys():
                return sorted(list(set(options["usina"])))
        return []

    @callback(
        Output(ids.ree_dropdown(MATCH), "options"),
        Input(ids.updater(MATCH), "n_intervals"),
        Input(ids.options(MATCH), "data"),
    )
    def update_ree_options(interval, options):
        if options:
            if "ree" in options.keys():
                return sorted(list(set(options["ree"])))
        return []

    @callback(
        Output(ids.submercado_dropdown(MATCH), "options"),
        Input(ids.updater(MATCH), "n_intervals"),
        Input(ids.options(MATCH), "data"),
    )
    def update_submercado_options(interval, options):
        if options:
            if "submercado" in options.keys():
                subs = list(set(options["submercado"]))
                return sorted(
                    list(set([GRUPOS_SUBMERCADOS.get(s, s) for s in subs]))
                )
        return []

    @callback(
        Output(ids.submercadoDe_dropdown(MATCH), "options"),
        Input(ids.updater(MATCH), "n_intervals"),
        Input(ids.options(MATCH), "data"),
    )
    def update_submercadoDe_options(interval, options):
        if options:
            if "submercadoDe" in options.keys():
                subs = list(set(options["submercadoDe"]))
                return sorted(
                    list(set([GRUPOS_SUBMERCADOS.get(s, s) for s in subs]))
                )
        return []

    @callback(
        Output(ids.submercadoPara_dropdown(MATCH), "options"),
        Input(ids.updater(MATCH), "n_intervals"),
        Input(ids.options(MATCH), "data"),
    )
    def update_submercadoPara_options(interval, options):
        if options:
            if "submercadoPara" in options.keys():
                subs = list(set(options["submercadoPara"]))
                return sorted(
                    list(set([GRUPOS_SUBMERCADOS.get(s, s) for s in subs]))
                )
        return []

    @callback(
        Output(ids.patamar_dropdown(MATCH), "options"),
        Input(ids.updater(MATCH), "n_intervals"),
        Input(ids.options(MATCH), "data"),
    )
    def update_patamar_options(interval, options):
        if options:
            if "patamar" in options.keys():
                return sorted(list(set(options["patamar"])))
        return []

    @callback(
        Output(ids.filters(MATCH), "data"),
        Input(ids.usina_dropdown(MATCH), "value"),
        Input(ids.ree_dropdown(MATCH), "value"),
        Input(ids.submercado_dropdown(MATCH), "value"),
        Input(ids.submercadoDe_dropdown(MATCH), "value"),
        Input(ids.submercadoPara_dropdown(MATCH), "value"),
        Input(ids.patamar_dropdown(MATCH), "value"),
    )
    def update_filters(
        usina: str,
        ree: str,
        submercado: str,
        submercado_de: str,
        submercado_para: str,
        patamar: str,
    ):
        filtros = {}
        if usina:
            filtros["usina"] = f"'{usina}'"
        if ree:
            filtros["ree"] = f"'{ree}'"
        if submercado:
            filtros["submercado"] = NOMES_SUBMERCADOS.get(submercado)
        if submercado_de:
            filtros["submercadoDe"] = NOMES_SUBMERCADOS.get(submercado_de)
        if submercado_de:
            filtros["submercadoPara"] = NOMES_SUBMERCADOS.get(submercado_para)
        if patamar:
            filtros["patamar"] = f"'{patamar}'"
        return filtros

    @callback(
        Output(ids.download(MATCH), "data"),
        Input(ids.download_btn(MATCH), "n_clicks"),
        State(ids.data(MATCH), "data"),
    )
    def generate_csv(n_clicks, operation_data):
        if n_clicks is None:
            return
        if operation_data is not None:
            dados = pd.read_json(operation_data, orient="split")
            dados["dataInicio"] = pd.to_datetime(
                dados["dataInicio"], unit="ms"
            )
            dados["dataFim"] = pd.to_datetime(dados["dataFim"], unit="ms")
            return dcc.send_data_frame(dados.to_csv, "operacao.csv")
