import pandas as pd
import os
import plotly.graph_objects as go
from src.utils.settings import Settings
from dash import html, callback, Output, Input, State, dcc
from src.utils.api import API

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
    "SUDESTE": ("SUDESTE", "SE"),
    "SUL": ("SUL", "S"),
    "NORDESTE": ("NORDESTE", "NE"),
    "NORTE": ("NORTE", "N"),
    "FC": ("FC",),
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
    Input("current_studies", "data"),
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
    Input("operation-data", "data"),
)
def atualiza_dados_dropdown_usina(interval, dados_operacao):
    if dados_operacao:
        dados = pd.read_json(dados_operacao, orient="split")
        if "Usina" in dados.columns:
            return dados["Usina"].unique().tolist()
    return []


@callback(
    Output("choose-operation-ree", "options"),
    Input("update-graph-data", "n_intervals"),
    Input("operation-data", "data"),
)
def atualiza_dados_dropdown_ree(interval, dados_operacao):
    if dados_operacao:
        dados = pd.read_json(dados_operacao, orient="split")
        if "REE" in dados.columns:
            return dados["REE"].unique().tolist()
    return []


@callback(
    Output("choose-operation-submercado", "options"),
    Input("update-graph-data", "n_intervals"),
    Input("operation-data", "data"),
)
def atualiza_dados_dropdown_submercado(interval, dados_operacao):
    if dados_operacao:
        dados = pd.read_json(dados_operacao, orient="split")
        if "Submercado" in dados.columns:
            submercados_programas = dados["Submercado"].unique().tolist()
            return list(
                set(
                    [
                        GRUPOS_SUBMERCADOS.get(s, s)
                        for s in submercados_programas
                    ]
                )
            )
    return []


@callback(
    Output("choose-operation-submercado-de", "options"),
    Input("update-graph-data", "n_intervals"),
    Input("operation-data", "data"),
)
def atualiza_dados_dropdown_submercado_de(interval, dados_operacao):
    if dados_operacao:
        dados = pd.read_json(dados_operacao, orient="split")
        if "Submercado De" in dados.columns:
            submercados_programas = dados["Submercado De"].unique().tolist()
            return list(
                set(
                    [
                        GRUPOS_SUBMERCADOS.get(s, s)
                        for s in submercados_programas
                    ]
                )
            )
    return []


@callback(
    Output("choose-operation-submercado-para", "options"),
    Input("update-graph-data", "n_intervals"),
    Input("operation-data", "data"),
)
def atualiza_dados_dropdown_submercado_para(interval, dados_operacao):
    if dados_operacao:
        dados = pd.read_json(dados_operacao, orient="split")
        if "Submercado Para" in dados.columns:
            submercados_programas = dados["Submercado Para"].unique().tolist()
            return list(
                set(
                    [
                        GRUPOS_SUBMERCADOS.get(s, s)
                        for s in submercados_programas
                    ]
                )
            )
    return []


@callback(
    Output("choose-operation-patamar", "options"),
    Input("update-graph-data", "n_intervals"),
    Input("operation-data", "data"),
)
def atualiza_dados_dropdown_patamar(interval, dados_operacao):
    if dados_operacao:
        dados = pd.read_json(dados_operacao, orient="split")
        if "Patamar" in dados.columns:
            return dados["Patamar"].unique().tolist()
    return []


@callback(
    Output("operation-data", "data"),
    Input("update-graph-data", "n_intervals"),
    Input("current_studies", "data"),
    Input("choose-operation-variable", "value"),
)
def atualiza_dados_variaveis_operacao(interval, studies, variable: str):
    if not studies:
        return None
    if not variable:
        return None
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["CAMINHO"].tolist()
    complete_df = pd.DataFrame()
    newave_df = API.fetch_result_list(
        [os.path.join(p, "NEWAVE") for p in paths], variable
    )
    decomp_df = API.fetch_result_list(
        [os.path.join(p, "DECOMP") for p in paths], variable
    )
    if newave_df is not None:
        cols_newave = newave_df.columns.to_list()
        newave_df["Programa"] = "NEWAVE"
        complete_df = pd.concat(
            [complete_df, newave_df[["Programa"] + cols_newave]],
            ignore_index=True,
        )
    if decomp_df is not None:
        cols_decomp = decomp_df.columns.to_list()
        decomp_df["Programa"] = "DECOMP"
        complete_df = pd.concat(
            [
                complete_df,
                decomp_df[["Programa"] + cols_decomp],
            ],
            ignore_index=True,
        )
    if complete_df.empty:
        return None
    else:
        return complete_df.loc[complete_df["Estagio"] == 1].to_json(
            orient="split"
        )


@callback(
    Output("operation-filters", "data"),
    Input("choose-operation-usina", "value"),
    Input("choose-operation-ree", "value"),
    Input("choose-operation-submercado", "value"),
    Input("choose-operation-submercado-de", "value"),
    Input("choose-operation-submercado-para", "value"),
    Input("choose-operation-patamar", "value"),
)
def atualiza_filtros_variaveis_operacao(
    usina: str,
    ree: str,
    submercado: str,
    submercado_de: str,
    submercado_para: str,
    patamar: str,
):
    filtros = {}
    if usina:
        filtros["Usina"] = usina
    if ree:
        filtros["REE"] = ree
    if submercado:
        filtros["Submercado"] = submercado
    if submercado_de:
        filtros["Submercado De"] = submercado_de
    if submercado_de:
        filtros["Submercado Para"] = submercado_para
    if patamar:
        filtros["Patamar"] = patamar
    return filtros


@callback(
    Output("operation-graph", "figure"),
    Input("operation-data", "data"),
    Input("choose-operation-variable", "value"),
    Input("operation-filters", "data"),
)
def gera_grafico_operacao(dados_operacao, variavel, filtros: dict):
    graph_layout = go.Layout(
        plot_bgcolor="rgba(158, 149, 128, 0.2)",
        paper_bgcolor="rgba(255,255,255,1)",
    )
    fig = go.Figure()
    fig.update_layout(graph_layout)
    if dados_operacao is None:
        return fig
    dados = pd.read_json(dados_operacao, orient="split")
    dados["Data Inicio"] = pd.to_datetime(dados["Data Inicio"], unit="ms")
    dados["Data Fim"] = pd.to_datetime(dados["Data Fim"], unit="ms")
    estudos = dados["Estudo"].unique().tolist()

    variaveis = list(dados.columns)
    queries_variaveis = []
    for k, v in filtros.items():
        if k in variaveis:
            if "Submercado" in k:
                queries_variaveis.append(
                    f"`{k}` in {str(NOMES_SUBMERCADOS.get(v, '()'))}"
                )
            elif "Patamar" in k:
                queries_variaveis.append(f"`{k}` == {v}")
            else:
                queries_variaveis.append(f"`{k}` == '{v}'")
    query_final = " and ".join(queries_variaveis)
    if len(query_final) > 0:
        dados = dados.query(query_final)
    filtro_newave = dados["Programa"] == "NEWAVE"
    filtro_decomp = dados["Programa"] == "DECOMP"
    df_newave = dados.loc[filtro_newave]
    df_decomp = dados.loc[filtro_decomp]

    visibilidade_newave = "legendonly" if len(estudos) > 2 else None
    for i, estudo in enumerate(estudos):
        if df_decomp is not None:
            estudo_decomp = df_decomp.loc[df_decomp["Estudo"] == estudo]
            if not estudo_decomp.empty:
                fig.add_trace(
                    go.Scatter(
                        x=estudo_decomp["Data Inicio"],
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
            estudo_newave = df_newave.loc[df_newave["Estudo"] == estudo]
            if not estudo_newave.empty:
                fig.add_trace(
                    go.Scatter(
                        x=estudo_newave["Data Inicio"],
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
                        x=estudo_newave["Data Inicio"],
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
                        x=estudo_newave["Data Inicio"],
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

    fig.update_layout(graph_layout)
    if variavel is not None:
        fig.update_layout(
            xaxis_title="Data Inicio",
            yaxis_title=VARIABLE_LEGENDS.get(variavel.split("_")[0], ""),
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
        dados["Data Inicio"] = pd.to_datetime(dados["Data Inicio"], unit="ms")
        dados["Data Fim"] = pd.to_datetime(dados["Data Fim"], unit="ms")
        return dcc.send_data_frame(dados.to_csv, "operacao.csv")
