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


class ResourcesFilters(html.Div):
    class ids:
        studies = lambda aio_id: {
            "component": "ResourcesFilters",
            "subcomponent": "studies",
            "aio_id": aio_id,
        }
        jobData = lambda aio_id: {
            "component": "ResourcesFilters",
            "subcomponent": "jobData",
            "aio_id": aio_id,
        }
        clusterData = lambda aio_id: {
            "component": "ResourcesFilters",
            "subcomponent": "clusterData",
            "aio_id": aio_id,
        }
        timeData = lambda aio_id: {
            "component": "ResourcesFilters",
            "subcomponent": "timeData",
            "aio_id": aio_id,
        }
        convergenceData = lambda aio_id: {
            "component": "ResourcesFilters",
            "subcomponent": "convergenceData",
            "aio_id": aio_id,
        }
        studies_dropdown = lambda aio_id: {
            "component": "ResourcesFilters",
            "subcomponent": "studies_dropdown",
            "aio_id": aio_id,
        }
        download = lambda aio_id: {
            "component": "ResourcesFilters",
            "subcomponent": "download",
            "aio_id": aio_id,
        }
        download_btn = lambda aio_id: {
            "component": "ResourcesFilters",
            "subcomponent": "download_btn",
            "aio_id": aio_id,
        }
        updater = lambda aio_id: {
            "component": "ResourcesFilters",
            "subcomponent": "updater",
            "aio_id": aio_id,
        }

    ids = ids

    def __init__(
        self,
        aio_id=None,
        studies_dropdown_props=None,
    ):
        if aio_id is None:
            aio_id = str(uuid.uuid4())
        pass

        studies_dropdown_props = (
            studies_dropdown_props.copy() if studies_dropdown_props else {}
        )
        if "className" not in studies_dropdown_props:
            studies_dropdown_props["className"] = "dropdown-container"

        if "children" not in studies_dropdown_props:
            studies_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.studies_dropdown(aio_id),
                options=[],
                value=None,
                placeholder="Estudo",
                className="variable-dropdown",
            )

        super().__init__(
            children=[
                html.Div(
                    **studies_dropdown_props,
                ),
                dcc.Store(
                    id=self.ids.studies(aio_id),
                    storage_type="memory",
                ),
                dcc.Store(
                    id=self.ids.clusterData(aio_id),
                    storage_type="memory",
                ),
                dcc.Store(
                    id=self.ids.jobData(aio_id),
                    storage_type="memory",
                ),
                dcc.Store(
                    id=self.ids.convergenceData(aio_id),
                    storage_type="memory",
                ),
                dcc.Store(
                    id=self.ids.timeData(aio_id),
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
        Output(ids.studies_dropdown(MATCH), "options"),
        Input(ids.studies(MATCH), "data"),
        prevent_initial_call=True,
    )
    def update_studies_dropdown_options(studies_data):
        return dropdowns.update_studies_names_dropdown_options_casos(
            studies_data
        )

    @callback(
        Output(ids.jobData(MATCH), "data"),
        Input(ids.studies(MATCH), "data"),
        prevent_initial_call=True,
    )
    def update_data(studies):
        return data.update_job_resources_data_casos(
            studies,
        )

    @callback(
        Output(ids.clusterData(MATCH), "data"),
        Input(ids.studies(MATCH), "data"),
        prevent_initial_call=True,
    )
    def update_data(studies):
        return data.update_cluster_resources_data_casos(
            studies,
        )

    @callback(
        Output(ids.timeData(MATCH), "data"),
        Input(ids.studies(MATCH), "data"),
        prevent_initial_call=True,
    )
    def update_data(studies):
        return data.update_runtime_data_casos(
            studies,
        )

    @callback(
        Output(ids.convergenceData(MATCH), "data"),
        Input(ids.studies(MATCH), "data"),
        prevent_initial_call=True,
    )
    def update_data(studies):
        return data.update_convergence_data_casos(
            studies,
        )

    @callback(
        Output(ids.download(MATCH), "data"),
        Input(ids.download_btn(MATCH), "n_clicks"),
        State(ids.jobData(MATCH), "data"),
        prevent_initial_call=True,
    )
    def generate_csv(n_clicks, operation_data):
        if n_clicks is None:
            raise PreventUpdate
        if operation_data is not None:
            dados = pd.read_json(StringIO(operation_data), orient="split")
            return dcc.send_data_frame(dados.to_csv, "recursos.csv")
