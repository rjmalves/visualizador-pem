import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
from os.path import join, isfile
import pandas as pd
import socket
from dash.dependencies import Input, Output, State
from typing import List
from waitress import serve
import base62

from visualizador.modelos.log import Log
from visualizador.modelos.configuracoes import Configuracoes
from visualizador.utils.db import DB

CFG_FILENAME = "visualiza.cfg"

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
    "rgba(249, 65, 68, 0.08)",
    "rgba(39, 125, 161, 0.08)",
    "rgba(144, 190, 109, 0.08)",
    "rgba(243, 114, 44, 0.08)",
    "rgba(87, 117, 144, 0.08)",
    "rgba(249, 199, 79, 0.08)",
    "rgba(248, 150, 30, 0.08)",
    "rgba(77, 144, 142, 0.08)",
    "rgba(249, 132, 74, 0.08)",
    "rgba(67, 170, 139, 0.08)",
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


class App:
    def __init__(self) -> None:
        self.__app = dash.Dash(
            __name__,
            title="Encadeador",
            update_title="Carregando...",
            url_base_pathname=Configuracoes().prefixo_url,
        )
        self.__inicializa()

    def __inicializa(self):
        cfg = Configuracoes()
        self.__db = DB()
        self.__graph_layout = go.Layout(
            plot_bgcolor="rgba(158, 149, 128, 0.2)",
            paper_bgcolor="rgba(255,255,255,1)",
        )
        self.__default_fig = go.Figure(layout=self.__graph_layout)
        self.__app.layout = html.Div(
            [
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H1(
                                    "VISUALIZADOR DE ESTUDOS ENCADEADOS",
                                    className="app-header-title",
                                ),
                                html.H2(
                                    "GERÊNCIA DE METODOLOGIAS E MODELOS ENERGÉTICOS - PEM",
                                    className="app-header-subtitle",
                                ),
                            ],
                            className="app-header-titles",
                        ),
                        html.Div(children=[], className="app-header-logo"),
                    ],
                    className="app-header",
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        html.H4(
                                            "CASOS ATUAIS",
                                            className="app-table-frame-title",
                                        ),
                                    ],
                                    className="table-header",
                                ),
                                html.Table(
                                    id="informacao-caso-atual",
                                    className="app-table",
                                ),
                            ],
                            className="twelve column current-case-table-container",
                        ),
                        html.Div(
                            children=[
                                html.Div(
                                    [
                                        html.H3(
                                            "VARIÁVEIS DA OPERAÇÂO",
                                            className="app-frame-title",
                                        ),
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    children=[
                                                        dcc.Dropdown(
                                                            id="escolhe-usina-operacao",
                                                            options=[],
                                                            value=None,
                                                            placeholder="Usina",
                                                            className="variable-dropdown",
                                                        )
                                                    ],
                                                    style={"display": "none"},
                                                    id="dropdown-usina-operacao",
                                                    className="dropdown-container",
                                                ),
                                                html.Div(
                                                    children=[
                                                        dcc.Dropdown(
                                                            id="escolhe-ree-operacao",
                                                            options=[],
                                                            value=None,
                                                            placeholder="REE",
                                                            className="variable-dropdown",
                                                        )
                                                    ],
                                                    style={"display": "none"},
                                                    id="dropdown-ree-operacao",
                                                    className="dropdown-container",
                                                ),
                                                html.Div(
                                                    children=[
                                                        dcc.Dropdown(
                                                            id="escolhe-submercado-operacao",
                                                            options=[],
                                                            value=None,
                                                            placeholder="Submercado",
                                                            className="variable-dropdown",
                                                        )
                                                    ],
                                                    style={"display": "none"},
                                                    id="dropdown-submercado-operacao",
                                                    className="dropdown-container",
                                                ),
                                                html.Div(
                                                    children=[
                                                        dcc.Dropdown(
                                                            id="escolhe-submercado-de-operacao",
                                                            options=[],
                                                            value=None,
                                                            placeholder="Submercado De",
                                                            className="variable-dropdown",
                                                        )
                                                    ],
                                                    style={"display": "none"},
                                                    id="dropdown-submercado-de-operacao",
                                                    className="dropdown-container",
                                                ),
                                                html.Div(
                                                    children=[
                                                        dcc.Dropdown(
                                                            id="escolhe-submercado-para-operacao",
                                                            options=[],
                                                            value=None,
                                                            placeholder="Submercado Para",
                                                            className="variable-dropdown",
                                                        )
                                                    ],
                                                    style={"display": "none"},
                                                    id="dropdown-submercado-para-operacao",
                                                    className="dropdown-container",
                                                ),
                                                html.Div(
                                                    children=[
                                                        dcc.Dropdown(
                                                            id="escolhe-patamar-operacao",
                                                            options=[],
                                                            value=None,
                                                            placeholder="Patamar",
                                                            className="variable-dropdown",
                                                        )
                                                    ],
                                                    style={"display": "none"},
                                                    id="dropdown-patamar-operacao",
                                                    className="dropdown-container",
                                                ),
                                                html.Div(
                                                    children=[
                                                        dcc.Dropdown(
                                                            id="escolhe-variavel-operacao",
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
                                                    id="operacao-btn",
                                                    className="download-button",
                                                ),
                                            ],
                                            className="dropdown-button-container",
                                        ),
                                    ],
                                    className="graph-header",
                                ),
                                html.Div(dcc.Graph(id="grafico-operacao")),
                            ],
                            className="twelve column graph-with-dropdown-container first",
                        ),
                    ],
                    className="app-content",
                ),
                dcc.Interval(
                    id="atualiza-dados-graficos",
                    interval=int(cfg.periodo_atualizacao_graficos),
                    n_intervals=0,
                ),
                dcc.Interval(
                    id="atualiza-dados-caso",
                    interval=int(cfg.periodo_atualizacao_caso_atual),
                    n_intervals=0,
                ),
                dcc.Store(id="dados-caso-atual"),
                dcc.Store(id="dados-variaveis-operacao"),
                dcc.Store(id="filtros-variaveis-operacao"),
                dcc.Download(id="download-operacao"),
                html.Div(
                    id="hidden-div",
                    style={"display": "none"},
                ),
                dcc.Store(id="dados-caminhos-casos"),
                dcc.Location(id="url"),
            ],
            className="app-container",
        )

        @self.__app.callback(
            Output("dados-caso-atual", "data"),
            Input("atualiza-dados-caso", "n_intervals"),
            Input("dados-caminhos-casos", "data"),
        )
        def atualiza_dados_caso(interval, data):
            return self.__db.le_informacoes_proximo_caso(data)

        @self.__app.callback(
            Output("escolhe-variavel-operacao", "options"),
            Input("atualiza-dados-graficos", "n_intervals"),
            Input("dados-caminhos-casos", "data"),
        )
        def atualiza_dados_dropdown_operacao(interval, data):
            variaveis_newave = self.__db.le_sinteses_disponiveis_newave(data)
            variaveis_decomp = self.__db.le_sinteses_disponiveis_decomp(data)
            variaveis_unicas = list(
                set(variaveis_newave).union(set(variaveis_decomp))
            )
            return sorted(variaveis_unicas)

        @self.__app.callback(
            Output("informacao-caso-atual", "children"),
            Input("dados-caso-atual", "data"),
        )
        def gera_tabela(dados: pd.DataFrame):
            if dados is None:
                Log.log().warning("Sem dados de ESTUDO")
                return html.Table([])
            dados_locais: pd.DataFrame = pd.read_json(dados, orient="split")
            if dados_locais.empty:
                Log.log().warning("Sem dados de ESTUDO")
                return html.Table([])
            if not dados_locais.empty:
                dados_locais.sort_values("Estudo", inplace=True)
            return App.gera_tabela(dados_locais)

        @self.__app.callback(
            Output("grafico-operacao", "figure"),
            Input("dados-variaveis-operacao", "data"),
            Input("escolhe-variavel-operacao", "value"),
            Input("filtros-variaveis-operacao", "data"),
        )
        def gera_grafico_operacao(dados_operacao, variavel, filtros):
            if dados_operacao is None:
                return self.__default_fig
            dados = pd.read_json(dados_operacao, orient="split")
            dados["Data Inicio"] = pd.to_datetime(
                dados["Data Inicio"], unit="ms"
            )
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
            Log.log().info("QUERY:" + query_final)
            if len(query_final) > 0:
                dados = dados.query(query_final)
            filtro_newave = dados["Programa"] == "NEWAVE"
            filtro_decomp = dados["Programa"] == "DECOMP"
            df_newave = dados.loc[filtro_newave]
            df_decomp = dados.loc[filtro_decomp]

            fig = go.Figure()
            for i, estudo in enumerate(estudos):
                if df_newave is not None:
                    estudo_newave = df_newave.loc[
                        df_newave["Estudo"] == estudo
                    ]
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
                                legendgroup="NEWAVE",
                                legendgrouptitle_text="NEWAVE",
                            )
                        )
                        fig.add_trace(
                            go.Scatter(
                                x=estudo_newave["Data Inicio"],
                                y=estudo_newave["p10"],
                                line_color=DISCRETE_COLOR_PALLETE_BACKGROUND[
                                    i
                                ],
                                legendgroup="NEWAVE",
                                name="p10",
                                showlegend=False,
                            )
                        )
                        fig.add_trace(
                            go.Scatter(
                                x=estudo_newave["Data Inicio"],
                                y=estudo_newave["p90"],
                                line_color=DISCRETE_COLOR_PALLETE_BACKGROUND[
                                    i
                                ],
                                fill="tonexty",
                                legendgroup="NEWAVE",
                                name="p90",
                                showlegend=False,
                            )
                        )
                if df_decomp is not None:
                    estudo_decomp = df_decomp.loc[
                        df_decomp["Estudo"] == estudo
                    ]
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

            fig.update_layout(self.__graph_layout)
            if variavel is not None:
                fig.update_layout(
                    xaxis_title="Data Inicio",
                    yaxis_title=VARIABLE_LEGENDS.get(
                        variavel.split("_")[0], ""
                    ),
                    hovermode="x unified",
                )
            return fig

        @self.__app.callback(
            Output("dropdown-usina-operacao", "style"),
            Input("escolhe-variavel-operacao", "value"),
        )
        def atualiza_exibe_dropdown_usinas_operacao(variavel: str):
            agregacao_espacial = variavel.split("_")[1] if variavel else ""
            return (
                {"display": "flex"}
                if agregacao_espacial in ["UHE", "UTE", "UEE"]
                else {"display": "none"}
            )

        @self.__app.callback(
            Output("dropdown-ree-operacao", "style"),
            Input("escolhe-variavel-operacao", "value"),
        )
        def atualiza_exibe_dropdown_ree_operacao(variavel: str):
            agregacao_espacial = variavel.split("_")[1] if variavel else ""
            return (
                {"display": "flex"}
                if agregacao_espacial == "REE"
                else {"display": "none"}
            )

        @self.__app.callback(
            Output("dropdown-submercado-operacao", "style"),
            Input("escolhe-variavel-operacao", "value"),
        )
        def atualiza_exibe_dropdown_submercado_operacao(variavel: str):
            agregacao_espacial = variavel.split("_")[1] if variavel else ""
            return (
                {"display": "flex"}
                if agregacao_espacial == "SBM"
                else {"display": "none"}
            )

        @self.__app.callback(
            Output("dropdown-submercado-de-operacao", "style"),
            Input("escolhe-variavel-operacao", "value"),
        )
        def atualiza_exibe_dropdown_submercado_de_operacao(variavel: str):
            agregacao_espacial = variavel.split("_")[1] if variavel else ""
            return (
                {"display": "flex"}
                if agregacao_espacial == "SBP"
                else {"display": "none"}
            )

        @self.__app.callback(
            Output("dropdown-submercado-para-operacao", "style"),
            Input("escolhe-variavel-operacao", "value"),
        )
        def atualiza_exibe_dropdown_submercado_para_operacao(variavel: str):
            agregacao_espacial = variavel.split("_")[1] if variavel else ""
            return (
                {"display": "flex"}
                if agregacao_espacial == "SBP"
                else {"display": "none"}
            )

        @self.__app.callback(
            Output("dropdown-patamar-operacao", "style"),
            Input("escolhe-variavel-operacao", "value"),
        )
        def atualiza_exibe_dropdown_patamar_operacao(variavel: str):
            agregacao_temporal = variavel.split("_")[2] if variavel else ""
            return (
                {"display": "flex"}
                if agregacao_temporal == "PAT"
                else {"display": "none"}
            )

        @self.__app.callback(
            Output("escolhe-usina-operacao", "options"),
            Input("atualiza-dados-graficos", "n_intervals"),
            Input("dados-variaveis-operacao", "data"),
        )
        def atualiza_dados_dropdown_usina(interval, dados_operacao):
            if dados_operacao:
                dados = pd.read_json(dados_operacao, orient="split")
                if "Usina" in dados.columns:
                    return dados["Usina"].unique().tolist()
            return []

        @self.__app.callback(
            Output("escolhe-ree-operacao", "options"),
            Input("atualiza-dados-graficos", "n_intervals"),
            Input("dados-variaveis-operacao", "data"),
        )
        def atualiza_dados_dropdown_ree(interval, dados_operacao):
            if dados_operacao:
                dados = pd.read_json(dados_operacao, orient="split")
                if "REE" in dados.columns:
                    return dados["REE"].unique().tolist()
            return []

        @self.__app.callback(
            Output("escolhe-submercado-operacao", "options"),
            Input("atualiza-dados-graficos", "n_intervals"),
            Input("dados-variaveis-operacao", "data"),
        )
        def atualiza_dados_dropdown_submercado(interval, dados_operacao):
            if dados_operacao:
                dados = pd.read_json(dados_operacao, orient="split")
                if "Submercado" in dados.columns:
                    submercados_programas = (
                        dados["Submercado"].unique().tolist()
                    )
                    return list(
                        set(
                            [
                                GRUPOS_SUBMERCADOS.get(s, s)
                                for s in submercados_programas
                            ]
                        )
                    )
            return []

        @self.__app.callback(
            Output("escolhe-submercado-de-operacao", "options"),
            Input("atualiza-dados-graficos", "n_intervals"),
            Input("dados-variaveis-operacao", "data"),
        )
        def atualiza_dados_dropdown_submercado_de(interval, dados_operacao):
            if dados_operacao:
                dados = pd.read_json(dados_operacao, orient="split")
                if "Submercado De" in dados.columns:
                    submercados_programas = (
                        dados["Submercado De"].unique().tolist()
                    )
                    return list(
                        set(
                            [
                                GRUPOS_SUBMERCADOS.get(s, s)
                                for s in submercados_programas
                            ]
                        )
                    )
            return []

        @self.__app.callback(
            Output("escolhe-submercado-para-operacao", "options"),
            Input("atualiza-dados-graficos", "n_intervals"),
            Input("dados-variaveis-operacao", "data"),
        )
        def atualiza_dados_dropdown_submercado_para(interval, dados_operacao):
            if dados_operacao:
                dados = pd.read_json(dados_operacao, orient="split")
                if "Submercado Para" in dados.columns:
                    submercados_programas = (
                        dados["Submercado Para"].unique().tolist()
                    )
                    return list(
                        set(
                            [
                                GRUPOS_SUBMERCADOS.get(s, s)
                                for s in submercados_programas
                            ]
                        )
                    )
            return []

        @self.__app.callback(
            Output("escolhe-patamar-operacao", "options"),
            Input("atualiza-dados-graficos", "n_intervals"),
            Input("dados-variaveis-operacao", "data"),
        )
        def atualiza_dados_dropdown_patamar(interval, dados_operacao):
            if dados_operacao:
                dados = pd.read_json(dados_operacao, orient="split")
                if "Patamar" in dados.columns:
                    return dados["Patamar"].unique().tolist()
            return []

        @self.__app.callback(
            Output("dados-variaveis-operacao", "data"),
            Input("atualiza-dados-graficos", "n_intervals"),
            Input("dados-caminhos-casos", "data"),
            Input("escolhe-variavel-operacao", "value"),
        )
        def atualiza_dados_variaveis_operacao(
            interval, casos: str, variavel: str
        ):
            df_newave = self.__db.le_dados_sintese_newave(casos, variavel)
            df_completo = pd.DataFrame()
            if df_newave is not None:
                cols_newave = df_newave.columns.to_list()
                df_newave["Programa"] = "NEWAVE"
                df_completo = pd.concat(
                    [df_completo, df_newave[["Programa"] + cols_newave]],
                    ignore_index=True,
                )
            df_decomp = self.__db.le_dados_sintese_decomp(casos, variavel)
            if df_decomp is not None:
                cols_decomp = df_decomp.columns.to_list()
                df_decomp["Programa"] = "DECOMP"
                df_completo = pd.concat(
                    [
                        df_completo,
                        df_decomp[["Programa"] + cols_decomp],
                    ],
                    ignore_index=True,
                )
            if df_completo.empty:
                return None
            else:
                return df_completo.loc[df_completo["Estagio"] == 1].to_json(
                    orient="split"
                )

        @self.__app.callback(
            Output("filtros-variaveis-operacao", "data"),
            Input("escolhe-usina-operacao", "value"),
            Input("escolhe-ree-operacao", "value"),
            Input("escolhe-submercado-operacao", "value"),
            Input("escolhe-submercado-de-operacao", "value"),
            Input("escolhe-submercado-para-operacao", "value"),
            Input("escolhe-patamar-operacao", "value"),
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

        @self.__app.callback(
            Output("download-operacao", "data"),
            Input("operacao-btn", "n_clicks"),
            State("dados-variaveis-operacao", "data"),
        )
        def gera_csv_operacao(n_clicks, dados_operacao):
            if n_clicks is None:
                return
            if dados_operacao is not None:
                dados = pd.read_json(dados_operacao, orient="split")
                dados["Data Inicio"] = pd.to_datetime(
                    dados["Data Inicio"], unit="ms"
                )
                dados["Data Fim"] = pd.to_datetime(
                    dados["Data Fim"], unit="ms"
                )
                return dcc.send_data_frame(dados.to_csv, "operacao.csv")

        @self.__app.callback(
            Output("dados-caminhos-casos", "data"),
            Input("url", "pathname"),
        )
        def le_url(pathname):
            # Processa o pathname
            PATTERN = Configuracoes().prefixo_url
            Log.log().info(f"URL: {pathname}")
            if PATTERN not in pathname:
                Log.log().error("Caminho não indica um caso encadeado")
                return []
            # Decodifica o base62
            try:
                caminho = base62.decodebytes(
                    pathname.split(PATTERN)[1]
                ).decode("utf-8")
                caminho = join(caminho, CFG_FILENAME)
                Log.log().info(f"Caminho: {caminho}")
                # Confere se existe um arquivo encadeia.cfg e lê
                if isfile(caminho):
                    with open(caminho, "r") as arq:
                        return [p.strip() for p in arq.readlines()]
            except Exception as e:
                Log.log().exception(f"Erro no processamento da URL: {e}")
            return []

    @staticmethod
    def gera_tabela(df: pd.DataFrame):
        return html.Table(
            [
                html.Thead(html.Tr([html.Th(col) for col in df.columns])),
                html.Tbody(
                    [
                        html.Tr(
                            [html.Td(df.iloc[i][col]) for col in df.columns]
                        )
                        for i in range(min(len(df), 20))
                    ]
                ),
            ]
        )

    def serve(self):
        log = Log.log()
        cfg = Configuracoes()
        ip_servidor = socket.gethostbyname(socket.gethostname())
        log.info(f"Visualizador: {ip_servidor}:{cfg.porta_servidor}")
        if cfg.modo == "DEV":
            self.__app.run(
                host="0.0.0.0", port=str(cfg.porta_servidor), debug=True
            )
        elif cfg.modo == "PROD":
            serve(
                self.__app.server, host="0.0.0.0", port=str(cfg.porta_servidor)
            )
