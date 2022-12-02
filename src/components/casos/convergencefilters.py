from dash import html, dcc, callback, Input, State, Output, MATCH
import uuid
import pandas as pd

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


class ConvergenceFilters(html.Div):
    class ids:
        studies = lambda aio_id: {
            "component": "ConvergenceFilters",
            "subcomponent": "studies",
            "aio_id": aio_id,
        }
        data = lambda aio_id: {
            "component": "ConvergenceFilters",
            "subcomponent": "data",
            "aio_id": aio_id,
        }
        variables_dropdown = lambda aio_id: {
            "component": "ConvergenceFilters",
            "subcomponent": "variables_dropdown",
            "aio_id": aio_id,
        }
        download = lambda aio_id: {
            "component": "ConvergenceFilters",
            "subcomponent": "download",
            "aio_id": aio_id,
        }
        download_btn = lambda aio_id: {
            "component": "ConvergenceFilters",
            "subcomponent": "download_btn",
            "aio_id": aio_id,
        }
        updater = lambda aio_id: {
            "component": "ConvergenceFilters",
            "subcomponent": "updater",
            "aio_id": aio_id,
        }

    ids = ids

    def __init__(
        self,
        aio_id=None,
        variables_dropdown_props=None,
    ):
        if aio_id is None:
            aio_id = str(uuid.uuid4())
        pass

        variables_dropdown_props = (
            variables_dropdown_props.copy() if variables_dropdown_props else {}
        )
        if "className" not in variables_dropdown_props:
            variables_dropdown_props["className"] = "dropdown-container"

        if "children" not in variables_dropdown_props:
            variables_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.variables_dropdown(aio_id),
                options=[],
                value=None,
                placeholder="Variavel",
                className="variable-dropdown",
            )

        super().__init__(
            children=[
                html.Div(
                    **variables_dropdown_props,
                ),
                dcc.Store(
                    id=self.ids.studies(aio_id),
                    storage_type=Settings.storage,
                ),
                dcc.Store(
                    id=self.ids.data(aio_id),
                    storage_type=Settings.storage,
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
        Output(ids.variables_dropdown(MATCH), "options"),
        Input(ids.updater(MATCH), "n_intervals"),
        Input(ids.studies(MATCH), "data"),
    )
    def update_variables_dropdown_options(interval, studies_data):
        return ["zsup", "zinf", "dZinf", "tempo"]

    @callback(
        Output(ids.data(MATCH), "data"),
        Input(ids.updater(MATCH), "n_intervals"),
        Input(ids.studies(MATCH), "data"),
    )
    def update_data(interval, studies):
        return data.update_convergence_data_casos(
            interval,
            studies,
        )

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
            return dcc.send_data_frame(dados.to_csv, "convergencia.csv")
