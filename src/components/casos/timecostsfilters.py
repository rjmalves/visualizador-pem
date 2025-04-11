import uuid
from io import StringIO

import pandas as pd
from dash import MATCH, Input, Output, State, callback, dcc, html

import src.utils.data as data
import src.utils.dropdowns as dropdowns

NOMES_SUBMERCADOS = {
    "SUDESTE": "'SUDESTE'|'SE'",
    "SUL": "'SUL'|'S'",
    "NORDESTE": "'NORDESTE'|'NE'",
    "NORTE": "'NORTE'|'N'",
    "FC": "'FC'",
    "IV": "'IV'",
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


class TimeCostsFilters(html.Div):
    class ids:
        studies = lambda aio_id: {
            "component": "TimeCostsFilters",
            "subcomponent": "studies",
            "aio_id": aio_id,
        }
        data = lambda aio_id: {
            "component": "TimeCostsFilters",
            "subcomponent": "data",
            "aio_id": aio_id,
        }
        variable_dropdown = lambda aio_id: {
            "component": "TimeCostsFilters",
            "subcomponent": "variable_dropdown",
            "aio_id": aio_id,
        }
        download = lambda aio_id: {
            "component": "TimeCostsFilters",
            "subcomponent": "download",
            "aio_id": aio_id,
        }
        download_btn = lambda aio_id: {
            "component": "TimeCostsFilters",
            "subcomponent": "download_btn",
            "aio_id": aio_id,
        }
        updater = lambda aio_id: {
            "component": "TimeCostsFilters",
            "subcomponent": "updater",
            "aio_id": aio_id,
        }

    ids = ids

    def __init__(
        self,
        aio_id=None,
        variable_dropdown_props=None,
    ):
        if aio_id is None:
            aio_id = str(uuid.uuid4())
        pass

        variable_dropdown_props = (
            variable_dropdown_props.copy() if variable_dropdown_props else {}
        )
        if "className" not in variable_dropdown_props:
            variable_dropdown_props["className"] = "dropdown-container"

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
                dcc.Download(id=self.ids.download(aio_id)),
                html.Button(
                    "CSV",
                    id=self.ids.download_btn(aio_id),
                ),
            ],
            className="card-menu-row",
        )

    @callback(
        Output(ids.variable_dropdown(MATCH), "options"),
        Input(ids.studies(MATCH), "data"),
    )
    def update_variables_dropdown_options(studies_data):
        return dropdowns.update_costs_time_variables_dropdown_options_casos(
            studies_data
        )

    @callback(
        Output(ids.data(MATCH), "data"),
        Input(ids.studies(MATCH), "data"),
        Input(ids.variable_dropdown(MATCH), "value"),
    )
    def update_data(studies, variable: str):
        return data.update_custos_tempo_data_casos(
            studies,
            variable,
        )

    @callback(
        Output(ids.download(MATCH), "data"),
        Input(ids.download_btn(MATCH), "n_clicks"),
        State(ids.data(MATCH), "data"),
        State(ids.variable_dropdown(MATCH), "value"),
    )
    def generate_csv(n_clicks, operation_data, variable):
        if n_clicks is None:
            return
        if operation_data is not None:
            dados = pd.read_json(StringIO(operation_data), orient="split")
            return dcc.send_data_frame(dados.to_csv, f"{variable}.csv")
