from dash import html, dcc, callback, Input, State, Output, MATCH
import uuid

from src.utils.settings import Settings


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


class OperationFiltersAIO(html.Div):
    class ids:
        options = lambda aio_id: {
            "component": "OperationFiltersAIO",
            "subcomponent": "options",
            "aio_id": aio_id,
        }
        filters = lambda aio_id: {
            "component": "OperationFiltersAIO",
            "subcomponent": "filters",
            "aio_id": aio_id,
        }
        usina_dropdown = lambda aio_id: {
            "component": "OperationFiltersAIO",
            "subcomponent": "usina_dropdown",
            "aio_id": aio_id,
        }
        usina_dropdown_container = lambda aio_id: {
            "component": "OperationFiltersAIO",
            "subcomponent": "usina_dropdown_container",
            "aio_id": aio_id,
        }
        ree_dropdown = lambda aio_id: {
            "component": "OperationFiltersAIO",
            "subcomponent": "ree_dropdown",
            "aio_id": aio_id,
        }
        ree_dropdown_container = lambda aio_id: {
            "component": "OperationFiltersAIO",
            "subcomponent": "ree_dropdown_container",
            "aio_id": aio_id,
        }
        submercado_dropdown = lambda aio_id: {
            "component": "OperationFiltersAIO",
            "subcomponent": "submercado_dropdown",
            "aio_id": aio_id,
        }
        submercado_dropdown_container = lambda aio_id: {
            "component": "OperationFiltersAIO",
            "subcomponent": "submercado_dropdown_container",
            "aio_id": aio_id,
        }
        submercadoDe_dropdown = lambda aio_id: {
            "component": "OperationFiltersAIO",
            "subcomponent": "submercadoDe_dropdown",
            "aio_id": aio_id,
        }
        submercadoDe_dropdown_container = lambda aio_id: {
            "component": "OperationFiltersAIO",
            "subcomponent": "submercadoDe_dropdown_container",
            "aio_id": aio_id,
        }
        submercadoPara_dropdown = lambda aio_id: {
            "component": "OperationFiltersAIO",
            "subcomponent": "submercadoPara_dropdown",
            "aio_id": aio_id,
        }
        submercadoPara_dropdown_container = lambda aio_id: {
            "component": "OperationFiltersAIO",
            "subcomponent": "submercadoPara_dropdown_container",
            "aio_id": aio_id,
        }
        patamar_dropdown = lambda aio_id: {
            "component": "OperationFiltersAIO",
            "subcomponent": "patamar_dropdown",
            "aio_id": aio_id,
        }
        patamar_dropdown_container = lambda aio_id: {
            "component": "OperationFiltersAIO",
            "subcomponent": "patamar_dropdown_container",
            "aio_id": aio_id,
        }
        estagio_dropdown = lambda aio_id: {
            "component": "OperationFiltersAIO",
            "subcomponent": "estagio_dropdown",
            "aio_id": aio_id,
        }
        estagio_dropdown_container = lambda aio_id: {
            "component": "OperationFiltersAIO",
            "subcomponent": "estagio_dropdown_container",
            "aio_id": aio_id,
        }
        cenario_dropdown = lambda aio_id: {
            "component": "OperationFiltersAIO",
            "subcomponent": "cenario_dropdown",
            "aio_id": aio_id,
        }
        cenario_dropdown_container = lambda aio_id: {
            "component": "OperationFiltersAIO",
            "subcomponent": "cenario_dropdown_container",
            "aio_id": aio_id,
        }
        variable_dropdown = lambda aio_id: {
            "component": "OperationFiltersAIO",
            "subcomponent": "variable_dropdown",
            "aio_id": aio_id,
        }
        download = lambda aio_id: {
            "component": "OperationFiltersAIO",
            "subcomponent": "download",
            "aio_id": aio_id,
        }
        download_btn = lambda aio_id: {
            "component": "OperationFiltersAIO",
            "subcomponent": "download_btn",
            "aio_id": aio_id,
        }

    ids = ids

    def __init__(
        self,
        updater_id,
        aio_id=None,
        usina_dropdown_props=None,
        ree_dropdown_props=None,
        submercado_dropdown_props=None,
        submercadoDe_dropdown_props=None,
        submercadoPara_dropdown_props=None,
        patamar_dropdown_props=None,
        estagio_dropdown_props=None,
        cenario_dropdown_props=None,
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
        submercado_dropdown_props = (
            submercado_dropdown_props.copy()
            if submercado_dropdown_props
            else {}
        )
        submercadoDe_dropdown_props = (
            submercadoDe_dropdown_props.copy()
            if submercadoDe_dropdown_props
            else {}
        )
        submercadoPara_dropdown_props = (
            submercadoPara_dropdown_props.copy()
            if submercadoPara_dropdown_props
            else {}
        )
        patamar_dropdown_props = (
            patamar_dropdown_props.copy() if patamar_dropdown_props else {}
        )
        estagio_dropdown_props = (
            estagio_dropdown_props.copy() if estagio_dropdown_props else {}
        )
        cenario_dropdown_props = (
            cenario_dropdown_props.copy() if cenario_dropdown_props else {}
        )
        variable_dropdown_props = (
            variable_dropdown_props.copy() if variable_dropdown_props else {}
        )

        if "style" not in usina_dropdown_props:
            usina_dropdown_props["style"] = {"display": "none"}
        if "style" not in ree_dropdown_props:
            ree_dropdown_props["style"] = {"display": "none"}
        if "style" not in submercado_dropdown_props:
            submercado_dropdown_props["style"] = {"display": "none"}
        if "style" not in submercadoDe_dropdown_props:
            submercadoDe_dropdown_props["style"] = {"display": "none"}
        if "style" not in submercadoPara_dropdown_props:
            submercadoPara_dropdown_props["style"] = {"display": "none"}
        if "style" not in patamar_dropdown_props:
            patamar_dropdown_props["style"] = {"display": "none"}
        if "style" not in estagio_dropdown_props:
            estagio_dropdown_props["style"] = {"display": "none"}
        if "style" not in cenario_dropdown_props:
            cenario_dropdown_props["style"] = {"display": "none"}
        if "style" not in cenario_dropdown_props:
            cenario_dropdown_props["style"] = {"display": "none"}
        if "style" not in variable_dropdown_props:
            variable_dropdown_props["style"] = {"display": "none"}

        if "className" not in usina_dropdown_props:
            usina_dropdown_props["className"] = "dropdown-container"
        if "className" not in ree_dropdown_props:
            ree_dropdown_props["className"] = "dropdown-container"
        if "className" not in submercado_dropdown_props:
            submercado_dropdown_props["className"] = "dropdown-container"
        if "className" not in submercadoDe_dropdown_props:
            submercadoDe_dropdown_props["className"] = "dropdown-container"
        if "className" not in submercadoPara_dropdown_props:
            submercadoPara_dropdown_props["className"] = "dropdown-container"
        if "className" not in patamar_dropdown_props:
            patamar_dropdown_props["className"] = "dropdown-container"
        if "className" not in estagio_dropdown_props:
            estagio_dropdown_props["className"] = "dropdown-container"
        if "className" not in cenario_dropdown_props:
            cenario_dropdown_props["className"] = "dropdown-container"
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
                value=None,
                placeholder="REE",
                className="variable-dropdown",
            )
        if "children" not in submercado_dropdown_props:
            submercado_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.submercado_dropdown(aio_id),
                options=[],
                value=None,
                placeholder="Submercado",
                className="variable-dropdown",
            )
        if "children" not in submercadoDe_dropdown_props:
            submercadoDe_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.submercadoDe_dropdown(aio_id),
                options=[],
                value=None,
                placeholder="Submercado De",
                className="variable-dropdown",
            )
        if "children" not in submercadoPara_dropdown_props:
            submercadoPara_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.submercadoPara_dropdown(aio_id),
                options=[],
                value=None,
                placeholder="Submercado De",
                className="variable-dropdown",
            )
        if "children" not in patamar_dropdown_props:
            patamar_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.patamar_dropdown(aio_id),
                options=[],
                value=None,
                placeholder="Patamar",
                className="variable-dropdown",
            )
        if "children" not in estagio_dropdown_props:
            estagio_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.estagio_dropdown(aio_id),
                options=[],
                value=None,
                placeholder="Estagio",
                className="variable-dropdown",
            )
        if "children" not in cenario_dropdown_props:
            cenario_dropdown_props["children"] = dcc.Dropdown(
                id=self.ids.cenario_dropdown(aio_id),
                options=[],
                value=None,
                placeholder="Cenario",
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
                    id=self.ids.usina_dropdown_container(aio_id),
                    **usina_dropdown_props,
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
                    id=self.ids.submercadoDe_dropdown_container(aio_id),
                    **submercadoDe_dropdown_props,
                ),
                html.Div(
                    id=self.ids.submercadoPara_dropdown_container(aio_id),
                    **submercadoPara_dropdown_props,
                ),
                html.Div(
                    id=self.ids.patamar_dropdown_container(aio_id),
                    **patamar_dropdown_props,
                ),
                html.Div(
                    id=self.ids.estagio_dropdown_container(aio_id),
                    **estagio_dropdown_props,
                ),
                html.Div(
                    id=self.ids.cenario_dropdown_container(aio_id),
                    **cenario_dropdown_props,
                ),
                html.Div(
                    **variable_dropdown_props,
                ),
                html.Button(
                    "CSV",
                    id=self.ids.download_btn(aio_id),
                ),
                dcc.Store(
                    id=self.ids.options(aio_id),
                    storage_type=Settings.storage,
                ),
                dcc.Store(
                    id=self.ids.filters(aio_id),
                    storage_type=Settings.storage,
                ),
            ],
            className="card-menu-row",
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
        Output(ids.estagio_dropdown(MATCH), "options"),
        Input(ids.updater(MATCH), "n_intervals"),
        Input(ids.options(MATCH), "data"),
    )
    def update_estagio_options(interval, options):
        if options:
            if "estagio" in options.keys():
                return sorted(list(set(options["estagio"])))
        return []

    @callback(
        Output(ids.filters(MATCH), "data"),
        Input(ids.usina_dropdown(MATCH), "value"),
        Input(ids.ree_dropdown(MATCH), "value"),
        Input(ids.submercado_dropdown(MATCH), "value"),
        Input(ids.submercadoDe_dropdown(MATCH), "value"),
        Input(ids.submercadoPara_dropdown(MATCH), "value"),
        Input(ids.patamar_dropdown(MATCH), "value"),
        Input(ids.estagio_dropdown(MATCH), "value"),
    )
    def update_filters(
        usina: str,
        ree: str,
        submercado: str,
        submercado_de: str,
        submercado_para: str,
        patamar: str,
        estagio: str,
        cenario: str,
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
        if estagio:
            filtros["estagio"] = f"{estagio}"
        if cenario:
            filtros["cenario"] = f"{cenario}"
        return filtros
