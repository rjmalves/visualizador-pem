from dash import html, dcc, callback, Input, State, Output, MATCH
from dash.exceptions import PreventUpdate
import uuid
import pandas as pd
from io import StringIO
from src.utils.settings import Settings
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


class TimeCostsFiltersEncadeador(html.Div):
    class ids:
        studies = lambda aio_id: {
            "component": "TimeCostsFiltersEncadeador",
            "subcomponent": "studies",
            "aio_id": aio_id,
        }
        data = lambda aio_id: {
            "component": "TimeCostsFiltersEncadeador",
            "subcomponent": "data",
            "aio_id": aio_id,
        }
        options = lambda aio_id: {
            "component": "TimeCostsFiltersEncadeador",
            "subcomponent": "options",
            "aio_id": aio_id,
        }
        filters = lambda aio_id: {
            "component": "TimeCostsFiltersEncadeador",
            "subcomponent": "filters",
            "aio_id": aio_id,
        }
        programa_dropdown = lambda aio_id: {
            "component": "TimeCostsFiltersEncadeador",
            "subcomponent": "programa_dropdown",
            "aio_id": aio_id,
        }
        programa_dropdown_container = lambda aio_id: {
            "component": "TimeCostsFiltersEncadeador",
            "subcomponent": "programa_dropdown_container",
            "aio_id": aio_id,
        }
        variable_dropdown = lambda aio_id: {
            "component": "TimeCostsFiltersEncadeador",
            "subcomponent": "variable_dropdown",
            "aio_id": aio_id,
        }
        download = lambda aio_id: {
            "component": "TimeCostsFiltersEncadeador",
            "subcomponent": "download",
            "aio_id": aio_id,
        }
        download_btn = lambda aio_id: {
            "component": "TimeCostsFiltersEncadeador",
            "subcomponent": "download_btn",
            "aio_id": aio_id,
        }
        updater = lambda aio_id: {
            "component": "TimeCostsFiltersEncadeador",
            "subcomponent": "updater",
            "aio_id": aio_id,
        }

    ids = ids

    def __init__(
        self,
        aio_id=None,
        programa_dropdown_props=None,
        variable_dropdown_props=None,
    ):
        if aio_id is None:
            aio_id = str(uuid.uuid4())
        pass

        programa_dropdown_props = (
            programa_dropdown_props.copy() if programa_dropdown_props else {}
        )

        variable_dropdown_props = (
            variable_dropdown_props.copy() if variable_dropdown_props else {}
        )
        if "className" not in programa_dropdown_props:
            programa_dropdown_props["className"] = "dropdown-container"

        if "className" not in variable_dropdown_props:
            variable_dropdown_props["className"] = "dropdown-container"

        if "children" not in programa_dropdown_props:
            programa_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.programa_dropdown(aio_id),
                options=["NEWAVE", "DECOMP"],
                value=None,
                placeholder="Programa",
                className="variable-dropdown",
            )

        if "children" not in variable_dropdown_props:
            variable_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.variable_dropdown(aio_id),
                options=[],
                value=None,
                placeholder="Variavel",
                className="variable-dropdown",
            )

        super().__init__(
            children=[
                html.Div(
                    id=self.ids.programa_dropdown_container(aio_id),
                    **programa_dropdown_props,
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
                    id=self.ids.filters(aio_id),
                    storage_type="memory",
                ),
                dcc.Interval(
                    id=self.ids.updater(aio_id),
                    interval=int(Settings.graphs_update_period),
                    n_intervals=0,
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
        Output(ids.filters(MATCH), "data"),
        Input(ids.programa_dropdown(MATCH), "value"),
    )
    def update_filters(
        programa: str,
    ):
        filtros = {}
        if programa:
            filtros["programa"] = f"{programa}"
        return filtros

    @callback(
        Output(ids.variable_dropdown(MATCH), "options"),
        Input(ids.updater(MATCH), "n_intervals"),
        Input(ids.studies(MATCH), "data"),
    )
    def update_variables_dropdown_options(interval, studies_data):
        return (
            dropdowns.update_costs_time_variables_dropdown_options_encadeador(
                interval, studies_data
            )
        )

    @callback(
        Output(ids.data(MATCH), "data"),
        Input(ids.updater(MATCH), "n_intervals"),
        Input(ids.studies(MATCH), "data"),
        Input(ids.filters(MATCH), "data"),
        Input(ids.variable_dropdown(MATCH), "value"),
    )
    def update_data(interval, studies, filters, variable: str):
        return data.update_custos_tempo_data_encadeador(
            interval,
            studies,
            filters,
            variable,
        )

    @callback(
        Output(ids.download(MATCH), "data"),
        Input(ids.download_btn(MATCH), "n_clicks"),
        State(ids.data(MATCH), "data"),
        State(ids.variable_dropdown(MATCH), "value"),
    )
    def generate_csv(n_clicks, operation_data, variavel):
        if n_clicks is None:
            raise PreventUpdate
        if operation_data is not None:
            dados = pd.read_json(StringIO(operation_data), orient="split")
            return dcc.send_data_frame(dados.to_csv, f"{variavel}.csv")
