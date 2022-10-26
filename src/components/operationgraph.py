import pandas as pd
import os
import plotly.graph_objects as go
from src.utils.settings import Settings
from dash import html, callback, Output, Input, State, dcc
from src.utils.api import API
import src.utils.validation as validation

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

graph_updater = dcc.Interval(
    id="update-graph-data",
    interval=int(Settings.graphs_update_period),
    n_intervals=0,
)

operation_variables_data = dcc.Store(id="operation-data")
operation_variables_options = dcc.Store(id="operation-data-options")
operation_variables_filter = dcc.Store(id="operation-filters")
operation_data_download = dcc.Download(id="operation-download")

graph = html.Div(
    children=[
        html.Div(
            [
                html.H3(
                    "VARIÁVEIS DA OPERAÇÂO",
                    className="table__header__title",
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                dcc.Dropdown(
                                    id="choose-operation-usina",
                                    options=[],
                                    value=None,
                                    placeholder="Usina",
                                    className="variable-dropdown",
                                )
                            ],
                            style={"display": "none"},
                            id="operation-usina-dropdown",
                            className="dropdown-container",
                        ),
                        html.Div(
                            children=[
                                dcc.Dropdown(
                                    id="choose-operation-ree",
                                    options=[],
                                    value=None,
                                    placeholder="REE",
                                    className="variable-dropdown",
                                )
                            ],
                            style={"display": "none"},
                            id="operation-ree-dropdown",
                            className="dropdown-container",
                        ),
                        html.Div(
                            children=[
                                dcc.Dropdown(
                                    id="choose-operation-submercado",
                                    options=[],
                                    value=None,
                                    placeholder="Submercado",
                                    className="variable-dropdown",
                                )
                            ],
                            style={"display": "none"},
                            id="operation-submercado-dropdown",
                            className="dropdown-container",
                        ),
                        html.Div(
                            children=[
                                dcc.Dropdown(
                                    id="choose-operation-submercado-de",
                                    options=[],
                                    value=None,
                                    placeholder="Submercado De",
                                    className="variable-dropdown",
                                )
                            ],
                            style={"display": "none"},
                            id="operation-submercado-de-dropdown",
                            className="dropdown-container",
                        ),
                        html.Div(
                            children=[
                                dcc.Dropdown(
                                    id="choose-operation-submercado-para",
                                    options=[],
                                    value=None,
                                    placeholder="Submercado Para",
                                    className="variable-dropdown",
                                )
                            ],
                            style={"display": "none"},
                            id="operation-submercado-para-dropdown",
                            className="dropdown-container",
                        ),
                        html.Div(
                            children=[
                                dcc.Dropdown(
                                    id="choose-operation-patamar",
                                    options=[],
                                    value=None,
                                    placeholder="Patamar",
                                    className="variable-dropdown",
                                )
                            ],
                            style={"display": "none"},
                            id="operation-patamar-dropdown",
                            className="dropdown-container",
                        ),
                        html.Div(
                            children=[
                                dcc.Dropdown(
                                    id="choose-operation-variable",
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
                            id="operation-download-btn",
                            className="download-button",
                        ),
                    ],
                    className="dropdown-button-container",
                ),
            ],
            className="table__header",
        ),
        html.Div(dcc.Graph(id="operation-graph")),
    ],
    className="card",
)


@callback(
    Output("choose-operation-variable", "options"),
    Input("update-graph-data", "n_intervals"),
    Input("current-studies", "data"),
)
def update_operation_variables_dropdown_options(interval, studies_data):
    studies = pd.read_json(studies_data, orient="split")
    all_variables = set()
    for _, line in studies.iterrows():
        newave_path = os.path.join(line["CAMINHO"], "NEWAVE")
        decomp_path = os.path.join(line["CAMINHO"], "DECOMP")
        unique_variables = API.fetch_available_results_list(
            [newave_path, decomp_path]
        )
        all_variables = all_variables.union(set(unique_variables))
    return sorted(list(all_variables))


@callback(
    Output("operation-usina-dropdown", "style"),
    Input("choose-operation-variable", "value"),
)
def atualiza_exibe_dropdown_usinas_operacao(variavel: str):
    agregacao_espacial = variavel.split("_")[1] if variavel else ""
    return (
        {"display": "flex"}
        if agregacao_espacial in ["UHE", "UTE", "UEE"]
        else {"display": "none"}
    )


@callback(
    Output("operation-ree-dropdown", "style"),
    Input("choose-operation-variable", "value"),
)
def atualiza_exibe_dropdown_ree_operacao(variavel: str):
    agregacao_espacial = variavel.split("_")[1] if variavel else ""
    return (
        {"display": "flex"}
        if agregacao_espacial == "REE"
        else {"display": "none"}
    )


@callback(
    Output("operation-submercado-dropdown", "style"),
    Input("choose-operation-variable", "value"),
)
def atualiza_exibe_dropdown_submercado_operacao(variavel: str):
    agregacao_espacial = variavel.split("_")[1] if variavel else ""
    return (
        {"display": "flex"}
        if agregacao_espacial == "SBM"
        else {"display": "none"}
    )


@callback(
    Output("operation-submercado-de-dropdown", "style"),
    Input("choose-operation-variable", "value"),
)
def atualiza_exibe_dropdown_submercado_de_operacao(variavel: str):
    agregacao_espacial = variavel.split("_")[1] if variavel else ""
    return (
        {"display": "flex"}
        if agregacao_espacial == "SBP"
        else {"display": "none"}
    )


@callback(
    Output("operation-submercado-para-dropdown", "style"),
    Input("choose-operation-variable", "value"),
)
def atualiza_exibe_dropdown_submercado_para_operacao(variavel: str):
    agregacao_espacial = variavel.split("_")[1] if variavel else ""
    return (
        {"display": "flex"}
        if agregacao_espacial == "SBP"
        else {"display": "none"}
    )


@callback(
    Output("operation-patamar-dropdown", "style"),
    Input("choose-operation-variable", "value"),
)
def atualiza_exibe_dropdown_patamar_operacao(variavel: str):
    agregacao_temporal = variavel.split("_")[2] if variavel else ""
    return (
        {"display": "flex"}
        if agregacao_temporal == "PAT"
        else {"display": "none"}
    )


@callback(
    Output("choose-operation-usina", "options"),
    Input("update-graph-data", "n_intervals"),
    Input("operation-data-options", "data"),
)
def update_dropdown_options_usina(interval, options):
    if options:
        if "patamar" in options.keys():
            return sorted(list(set(options["patamar"])))
    return []


@callback(
    Output("choose-operation-ree", "options"),
    Input("update-graph-data", "n_intervals"),
    Input("operation-data-options", "data"),
)
def update_dropdown_options_ree(interval, options):
    if options:
        if "ree" in options.keys():
            return sorted(list(set(options["ree"])))
    return []


@callback(
    Output("choose-operation-submercado", "options"),
    Input("update-graph-data", "n_intervals"),
    Input("operation-data-options", "data"),
)
def update_dropdown_options_submercado(interval, options):
    if options:
        if "submercado" in options.keys():
            subs = list(set(options["submercado"]))
            return sorted(
                list(set([GRUPOS_SUBMERCADOS.get(s, s) for s in subs]))
            )
    return []


@callback(
    Output("choose-operation-submercado-de", "options"),
    Input("update-graph-data", "n_intervals"),
    Input("operation-data-options", "data"),
)
def update_dropdown_options_submercado_de(interval, options):
    if options:
        if "submercadoDe" in options.keys():
            subs = list(set(options["submercadoDe"]))
            return sorted(
                list(set([GRUPOS_SUBMERCADOS.get(s, s) for s in subs]))
            )
    return []


@callback(
    Output("choose-operation-submercado-para", "options"),
    Input("update-graph-data", "n_intervals"),
    Input("operation-data-options", "data"),
)
def update_dropdown_options_submercado_para(interval, options):
    if options:
        if "submercadoPara" in options.keys():
            subs = list(set(options["submercadoPara"]))
            return sorted(
                list(set([GRUPOS_SUBMERCADOS.get(s, s) for s in subs]))
            )
    return []


@callback(
    Output("choose-operation-patamar", "options"),
    Input("update-graph-data", "n_intervals"),
    Input("operation-data-options", "data"),
)
def update_dropdown_options_patamar(interval, options):
    if options:
        if "patamar" in options.keys():
            return sorted(list(set(options["patamar"])))
    return []


@callback(
    Output("operation-data", "data"),
    Input("update-graph-data", "n_intervals"),
    Input("current-studies", "data"),
    Input("operation-filters", "data"),
    Input("choose-operation-variable", "value"),
)
def update_operation_variables_data(
    interval, studies, filters: dict, variable: str
):
    if not studies:
        return None
    if not variable:
        return None
    req_filters = validation.validate_required_filters(variable, filters)
    if req_filters is None:
        return None
    fetch_filters = {**req_filters, "estagio": 1}
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["CAMINHO"].tolist()
    complete_df = pd.DataFrame()
    newave_df = API.fetch_result_list(
        [os.path.join(p, "NEWAVE") for p in paths], variable, fetch_filters
    )
    decomp_df = API.fetch_result_list(
        [os.path.join(p, "DECOMP") for p in paths], variable, fetch_filters
    )
    if newave_df is not None:
        cols_newave = newave_df.columns.to_list()
        newave_df["programa"] = "NEWAVE"
        complete_df = pd.concat(
            [complete_df, newave_df[["programa"] + cols_newave]],
            ignore_index=True,
        )
    if decomp_df is not None:
        cols_decomp = decomp_df.columns.to_list()
        decomp_df["programa"] = "DECOMP"
        complete_df = pd.concat(
            [
                complete_df,
                decomp_df[["programa"] + cols_decomp],
            ],
            ignore_index=True,
        )
    if complete_df.empty:
        return None
    else:
        return complete_df.to_json(orient="split")


@callback(
    Output("operation-data-options", "data"),
    Input("update-graph-data", "n_intervals"),
    Input("current-studies", "data"),
    Input("choose-operation-variable", "value"),
)
def update_operation_data_options(interval, studies, variable: str):
    if not studies:
        return None
    if not variable:
        return None
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["CAMINHO"].tolist()
    complete_options = {}
    newave_options = API.fetch_result_options_list(
        [os.path.join(p, "NEWAVE") for p in paths], variable
    )
    decomp_options = API.fetch_result_options_list(
        [os.path.join(p, "DECOMP") for p in paths], variable
    )
    if newave_options is not None:
        complete_options = {**complete_options, **newave_options}
    if decomp_options is not None:
        complete_options = {**complete_options, **decomp_options}
    if len(complete_options) == 0:
        return None
    else:
        return complete_options


@callback(
    Output("operation-filters", "data"),
    Input("choose-operation-usina", "value"),
    Input("choose-operation-ree", "value"),
    Input("choose-operation-submercado", "value"),
    Input("choose-operation-submercado-de", "value"),
    Input("choose-operation-submercado-para", "value"),
    Input("choose-operation-patamar", "value"),
)
def update_operation_variables_filters(
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
        filtros["patamar"] = f"{patamar}"
    return filtros


@callback(
    Output("operation-graph", "figure"),
    Input("operation-data", "data"),
    State("choose-operation-variable", "value"),
)
def generate_operation_graph(operation_data, variable):
    graph_layout = go.Layout(
        plot_bgcolor="rgba(158, 149, 128, 0.2)",
        paper_bgcolor="rgba(255,255,255,1)",
    )
    fig = go.Figure()
    fig.update_layout(graph_layout)
    if operation_data is None:
        return fig
    dados = pd.read_json(operation_data, orient="split")
    dados["dataInicio"] = pd.to_datetime(dados["dataInicio"], unit="ms")
    dados["dataFim"] = pd.to_datetime(dados["dataFim"], unit="ms")
    estudos = dados["estudo"].unique().tolist()

    filtro_newave = dados["programa"] == "NEWAVE"
    filtro_decomp = dados["programa"] == "DECOMP"
    df_newave = dados.loc[filtro_newave]
    df_decomp = dados.loc[filtro_decomp]

    visibilidade_newave = "legendonly" if len(estudos) > 2 else None
    for i, estudo in enumerate(estudos):
        if df_decomp is not None:
            estudo_decomp = df_decomp.loc[df_decomp["estudo"] == estudo]
            if not estudo_decomp.empty:
                fig.add_trace(
                    go.Scatter(
                        x=estudo_decomp["dataInicio"],
                        y=estudo_decomp["mean"],
                        line={
                            "color": DISCRETE_COLOR_PALLETE[i],
                            "width": 3,
                        },
                        name=estudo,
                        legendgroup="DECOMP",
                        legendgrouptitle_text="DECOMP",
                    )
                )
        if df_newave is not None:
            estudo_newave = df_newave.loc[df_newave["estudo"] == estudo]
            if not estudo_newave.empty:
                fig.add_trace(
                    go.Scatter(
                        x=estudo_newave["dataInicio"],
                        y=estudo_newave["mean"],
                        line={
                            "color": DISCRETE_COLOR_PALLETE[i],
                            "dash": "dot",
                            "width": 2,
                        },
                        name=estudo,
                        legendgroup="NEWAVEm",
                        legendgrouptitle_text="NEWAVEm",
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=estudo_newave["dataInicio"],
                        y=estudo_newave["p10"],
                        line_color=DISCRETE_COLOR_PALLETE_BACKGROUND[i],
                        legendgroup="NEWAVEp10",
                        legendgrouptitle_text="NEWAVEp10",
                        name=estudo,
                        visible=visibilidade_newave,
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=estudo_newave["dataInicio"],
                        y=estudo_newave["p90"],
                        line_color=DISCRETE_COLOR_PALLETE_BACKGROUND[i],
                        fillcolor=DISCRETE_COLOR_PALLETE_BACKGROUND[i],
                        fill="tonexty",
                        legendgroup="NEWAVEp90",
                        legendgrouptitle_text="NEWAVEp90",
                        name=estudo,
                        visible=visibilidade_newave,
                    )
                )

    if variable is not None:
        fig.update_layout(
            xaxis_title="Data",
            yaxis_title=VARIABLE_LEGENDS.get(variable.split("_")[0], ""),
            hovermode="x unified",
            legend=dict(groupclick="toggleitem"),
        )
    return fig


@callback(
    Output("operation-download", "data"),
    Input("operation-download-btn", "n_clicks"),
    State("operation-data", "data"),
)
def gera_csv_operacao(n_clicks, dados_operacao):
    if n_clicks is None:
        return
    if dados_operacao is not None:
        dados = pd.read_json(dados_operacao, orient="split")
        dados["dataInicio"] = pd.to_datetime(dados["dataInicio"], unit="ms")
        dados["dataFim"] = pd.to_datetime(dados["dataFim"], unit="ms")
        return dcc.send_data_frame(dados.to_csv, "operacao.csv")
