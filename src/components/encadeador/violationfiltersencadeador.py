from dash import html, dcc, callback, Input, State, Output, MATCH
import uuid
import pandas as pd

from src.utils.settings import Settings
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


class ViolationFilters(html.Div):
    class ids:
        studies = lambda aio_id: {
            "component": "ViolationFilters",
            "subcomponent": "studies",
            "aio_id": aio_id,
        }
        data = lambda aio_id: {
            "component": "ViolationFilters",
            "subcomponent": "data",
            "aio_id": aio_id,
        }
        options = lambda aio_id: {
            "component": "ViolationFilters",
            "subcomponent": "options",
            "aio_id": aio_id,
        }
        filters = lambda aio_id: {
            "component": "ViolationFilters",
            "subcomponent": "filters",
            "aio_id": aio_id,
        }
        programa_dropdown = lambda aio_id: {
            "component": "ViolationFilters",
            "subcomponent": "programa_dropdown",
            "aio_id": aio_id,
        }
        programa_dropdown_container = lambda aio_id: {
            "component": "ViolationFilters",
            "subcomponent": "programa_dropdown_container",
            "aio_id": aio_id,
        }
        violation_dropdown = lambda aio_id: {
            "component": "ViolationFilters",
            "subcomponent": "violation_dropdown",
            "aio_id": aio_id,
        }
        download = lambda aio_id: {
            "component": "ViolationFilters",
            "subcomponent": "download",
            "aio_id": aio_id,
        }
        download_btn = lambda aio_id: {
            "component": "ViolationFilters",
            "subcomponent": "download_btn",
            "aio_id": aio_id,
        }
        updater = lambda aio_id: {
            "component": "ViolationFilters",
            "subcomponent": "updater",
            "aio_id": aio_id,
        }

    ids = ids

    def __init__(
        self,
        aio_id=None,
        programa_dropdown_props=None,
        violation_dropdown_props=None,
    ):
        if aio_id is None:
            aio_id = str(uuid.uuid4())
        pass

        programa_dropdown_props = (
            programa_dropdown_props.copy() if programa_dropdown_props else {}
        )

        violation_dropdown_props = (
            violation_dropdown_props.copy() if violation_dropdown_props else {}
        )
        if "className" not in programa_dropdown_props:
            programa_dropdown_props["className"] = "dropdown-container"

        if "className" not in violation_dropdown_props:
            violation_dropdown_props["className"] = "dropdown-container"

        if "children" not in programa_dropdown_props:
            programa_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.programa_dropdown(aio_id),
                options=["DECOMP"],
                value="DECOMP",
                placeholder="Programa",
                className="variable-dropdown",
            )

        if "children" not in violation_dropdown_props:
            violation_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.violation_dropdown(aio_id),
                options=[
                    "RHQ",
                    "RE",
                    "RHE",
                    "RHV",
                    "TI",
                    "EV",
                    "DEFICIT",
                    "DEFMIN",
                    "RHA",
                ],
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
                    **violation_dropdown_props,
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
        Output(ids.data(MATCH), "data"),
        Input(ids.updater(MATCH), "n_intervals"),
        Input(ids.studies(MATCH), "data"),
        Input(ids.filters(MATCH), "data"),
        Input(ids.violation_dropdown(MATCH), "value"),
    )
    def update_data(interval, studies, filters, violation: str):
        return data.update_violation_data_encadeador(
            interval,
            studies,
            filters,
            violation,
        )

    @callback(
        Output(ids.download(MATCH), "data"),
        Input(ids.download_btn(MATCH), "n_clicks"),
        State(ids.data(MATCH), "data"),
        State(ids.violation_dropdown(MATCH), "value"),
    )
    def generate_csv(n_clicks, operation_data, violation):
        if n_clicks is None:
            return
        if operation_data is not None:
            dados = pd.read_json(operation_data, orient="split")
            return dcc.send_data_frame(dados.to_csv, f"{violation}.csv")
