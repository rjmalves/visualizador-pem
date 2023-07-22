from dash import html, dcc, callback, Input, State, Output, MATCH
from dash.exceptions import PreventUpdate
import uuid
import pandas as pd

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


class SpatialViewFilters(html.Div):
    class ids:
        studies = lambda aio_id: {
            "component": "SpatialViewFilters",
            "subcomponent": "studies",
            "aio_id": aio_id,
        }
        data = lambda aio_id: {
            "component": "SpatialViewFilters",
            "subcomponent": "data",
            "aio_id": aio_id,
        }
        options = lambda aio_id: {
            "component": "SpatialViewFilters",
            "subcomponent": "options",
            "aio_id": aio_id,
        }
        filters = lambda aio_id: {
            "component": "SpatialViewFilters",
            "subcomponent": "filters",
            "aio_id": aio_id,
        }
        cenario_dropdown = lambda aio_id: {
            "component": "SpatialViewFilters",
            "subcomponent": "cenario_dropdown",
            "aio_id": aio_id,
        }
        cenario_dropdown_container = lambda aio_id: {
            "component": "SpatialViewFilters",
            "subcomponent": "cenario_dropdown_container",
            "aio_id": aio_id,
        }
        estagio_dropdown = lambda aio_id: {
            "component": "SpatialViewFilters",
            "subcomponent": "estagio_dropdown",
            "aio_id": aio_id,
        }
        estagio_dropdown_container = lambda aio_id: {
            "component": "SpatialViewFilters",
            "subcomponent": "estagio_dropdown_container",
            "aio_id": aio_id,
        }
        study_dropdown = lambda aio_id: {
            "component": "SpatialViewFilters",
            "subcomponent": "study_dropdown",
            "aio_id": aio_id,
        }
        download = lambda aio_id: {
            "component": "SpatialViewFilters",
            "subcomponent": "download",
            "aio_id": aio_id,
        }
        download_btn = lambda aio_id: {
            "component": "SpatialViewFilters",
            "subcomponent": "download_btn",
            "aio_id": aio_id,
        }
        updater = lambda aio_id: {
            "component": "SpatialViewFilters",
            "subcomponent": "updater",
            "aio_id": aio_id,
        }

    ids = ids

    def __init__(
        self,
        aio_id=None,
        estagio_dropdown_props=None,
        cenario_dropdown_props=None,
        study_dropdown_props=None,
    ):
        if aio_id is None:
            aio_id = str(uuid.uuid4())
        pass

        estagio_dropdown_props = (
            estagio_dropdown_props.copy() if estagio_dropdown_props else {}
        )
        cenario_dropdown_props = (
            cenario_dropdown_props.copy() if cenario_dropdown_props else {}
        )
        study_dropdown_props = (
            study_dropdown_props.copy() if study_dropdown_props else {}
        )
        if "className" not in estagio_dropdown_props:
            estagio_dropdown_props["className"] = "dropdown-container"
        if "className" not in cenario_dropdown_props:
            cenario_dropdown_props["className"] = "dropdown-container"
        if "className" not in study_dropdown_props:
            study_dropdown_props["className"] = "dropdown-container"

        if "children" not in estagio_dropdown_props:
            estagio_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.estagio_dropdown(aio_id),
                options=[],
                value=None,
                placeholder="Estágio",
                className="variable-dropdown",
            )

        if "children" not in cenario_dropdown_props:
            cenario_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.cenario_dropdown(aio_id),
                options=[],
                value=None,
                placeholder="Cenário",
                className="variable-dropdown",
            )

        if "children" not in study_dropdown_props:
            study_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.study_dropdown(aio_id),
                options=[],
                value=None,
                placeholder="Estudo",
                className="variable-dropdown",
            )

        super().__init__(
            children=[
                html.Div(
                    id=self.ids.estagio_dropdown_container(aio_id),
                    **estagio_dropdown_props,
                ),
                html.Div(
                    id=self.ids.cenario_dropdown_container(aio_id),
                    **cenario_dropdown_props,
                ),
                html.Div(
                    **study_dropdown_props,
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
        Output(ids.options(MATCH), "data"),
        Input(ids.studies(MATCH), "data"),
        Input(ids.study_dropdown(MATCH), "value"),
    )
    def update_options(studies, study: str):
        return dropdowns.update_spatial_options_casos(studies, study)

    @callback(
        Output(ids.estagio_dropdown(MATCH), "options"),
        Input(ids.options(MATCH), "data"),
    )
    def update_estagio_options(options):
        if options:
            if "estagio" in options.keys():
                return sorted(list(set(options["estagio"])))
        raise PreventUpdate

    @callback(
        Output(ids.cenario_dropdown(MATCH), "options"),
        Input(ids.options(MATCH), "data"),
    )
    def update_cenario_options(options):
        if options:
            if "cenario" in options.keys():
                return sorted(list(set(options["cenario"])))
        raise PreventUpdate

    @callback(
        Output(ids.study_dropdown(MATCH), "options"),
        Input(ids.studies(MATCH), "data"),
    )
    def update_study_dropdown_options(studies_data):
        return dropdowns.update_studies_names_dropdown_options_casos(
            studies_data
        )

    @callback(
        Output(ids.filters(MATCH), "data"),
        Input(ids.estagio_dropdown(MATCH), "value"),
        Input(ids.cenario_dropdown(MATCH), "value"),
    )
    def update_filters(estagio: str, cenario: str):
        filtros = {}
        if estagio:
            filtros["estagio"] = f"{estagio}"
        if cenario:
            filtros["cenario"] = f"'{cenario}'"
        return filtros

    @callback(
        Output(ids.data(MATCH), "data"),
        Input(ids.studies(MATCH), "data"),
        Input(ids.study_dropdown(MATCH), "value"),
        Input(ids.filters(MATCH), "data"),
        prevent_initial_call=True,
    )
    def update_data(studies, study, filters):
        return {
            "SBM": data.update_spatial_SBM_data_casos(studies, study, filters),
            "INT": data.update_spatial_INT_data_casos(studies, study, filters),
        }

    @callback(
        Output(ids.download(MATCH), "data"),
        Input(ids.download_btn(MATCH), "n_clicks"),
        State(ids.data(MATCH), "data"),
        prevent_initial_call=True,
    )
    def generate_csv(n_clicks, operation_data):
        if n_clicks is None:
            raise PreventUpdate
        if operation_data is not None:
            dados = pd.read_json(operation_data, orient="split")
            return dcc.send_data_frame(dados.to_csv, "recursos.csv")
