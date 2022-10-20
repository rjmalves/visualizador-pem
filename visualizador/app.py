from email.utils import parsedate_to_datetime
import os
import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
from plotly import tools
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
    "rgba(249, 65, 68, 0.1)",
    "rgba(39, 125, 161, 0.1)",
    "rgba(144, 190, 109, 0.1)",
    "rgba(243, 114, 44, 0.1)",
    "rgba(87, 117, 144, 0.1)",
    "rgba(249, 199, 79, 0.1)",
    "rgba(248, 150, 30, 0.1)",
    "rgba(77, 144, 142, 0.1)",
    "rgba(249, 132, 74, 0.1)",
    "rgba(67, 170, 139, 0.1)",
]

VARIABLE_LEGENDS = {
    "COP": "R$",
    "CFU": "R$",
    "CMO": "R$ / MWh",
    "CTER": "R$",
    "DEF": "MWmed",
    "EARMI": "%",
    "EARPI": "%",
    "EARMF": "%",
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
    "VARPI": "hm3",
    "VARPF": "hm3",
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

    @staticmethod
    def __opcoes_dropdown_decomp() -> List[dict]:
        variaveis = [
            "CMO SE",
            "CMO S",
            "CMO NE",
            "CMO N",
            "EARM SIN",
            "EARM SE",
            "EARM S",
            "EARM NE",
            "EARM N",
            "GT SIN",
            "GT SE",
            "GT S",
            "GT NE",
            "GT N",
            "GT SIN (% MAX)",
            "GT SE (% MAX)",
            "GT S (% MAX)",
            "GT NE (% MAX)",
            "GT N (% MAX)",
            "GT SIN (% FLEX)",
            "GT SE (% FLEX)",
            "GT S (% FLEX)",
            "GT NE (% FLEX)",
            "GT N (% FLEX)",
            "GH SIN",
            "GH SE",
            "GH S",
            "GH NE",
            "GH N",
            "Mercado SIN",
            "Mercado SE",
            "Mercado S",
            "Mercado NE",
            "Mercado N",
            "Déficit SIN",
            "Déficit SE",
            "Déficit S",
            "Déficit NE",
            "Déficit N",
        ]
        opcoes = [{"label": p, "value": p} for p in variaveis]
        return opcoes

    @staticmethod
    def __opcoes_dropdown_reservatorios() -> List[dict]:
        variaveis = [
            "CAMARGOS",
            "FURNAS",
            "M. DE MORAES",
            "CACONDE",
            "MARIMBONDO",
            "A. VERMELHA",
            "BATALHA",
            "SERRA FACAO",
            "EMBORCACAO",
            "NOVA PONTE",
            "MIRANDA",
            "CAPIM BRANC1",
            "CORUMBA IV",
            "CORUMBA III",
            "CORUMBA I",
            "ITUMBIARA",
            "SAO SIMAO",
            "ESPORA",
            "CACU",
            "I. SOLTEIRA",
            "BILLINGS",
            "GUARAPIRANGA",
            "BARRA BONITA",
            "PROMISSAO",
            "TRES IRMAOS",
            "A.A. LAYDNER",
            "CHAVANTES",
            "MAUA",
            "CAPIVARA",
            "ITAIPU",
            "JAGUARI",
            "PARAIBUNA",
            "SANTA BRANCA",
            "FUNIL",
            "LAJES",
            "P. ESTRELA",
            "MANSO",
            "RONDON II",
            "SAMUEL",
            "SINOP",
            "STA CLARA PR",
            "JORDAO",
            "G.B. MUNHOZ",
            "SEGREDO",
            "SLT.SANTIAGO",
            "BARRA GRANDE",
            "GARIBALDI",
            "CAMPOS NOVOS",
            "MACHADINHO",
            "PASSO FUNDO",
            "QUEBRA QUEIX",
            "ERNESTINA",
            "PASSO REAL",
            "G.P. SOUZA",
            "IRAPE",
            "RETIRO BAIXO",
            "TRES MARIAS",
            "QUEIMADO",
            "SOBRADINHO",
            "ITAPARICA",
            "P. CAVALO",
            "B. ESPERANCA",
            "SERRA MESA",
            "PEIXE ANGIC",
            "CURUA-UNA",
            "TUCURUI",
            "BALBINA",
        ]
        variaveis.sort()
        opcoes = [{"label": p, "value": p} for p in variaveis]
        return opcoes

    @staticmethod
    def __opcoes_dropdown_defluencias() -> List[dict]:
        variaveis = [
            "CAMARGOS",
            "ITUTINGA",
            "FUNIL-GRANDE",
            "FURNAS",
            "M. DE MORAES",
            "ESTREITO",
            "JAGUARA",
            "IGARAPAVA",
            "VOLTA GRANDE",
            "P. COLOMBIA",
            "CACONDE",
            "E. DA CUNHA",
            "A.S.OLIVEIRA",
            "MARIMBONDO",
            "A. VERMELHA",
            "BATALHA",
            "SERRA FACAO",
            "EMBORCACAO",
            "NOVA PONTE",
            "MIRANDA",
            "CAPIM BRANC1",
            "CAPIM BRANC2",
            "CORUMBA IV",
            "CORUMBA III",
            "CORUMBA I",
            "ITUMBIARA",
            "CACH.DOURADA",
            "SAO SIMAO",
            "SALTO",
            "SLT VERDINHO",
            "ESPORA",
            "CACU",
            "B. COQUEIROS",
            "FOZ R. CLARO",
            "I. SOLTEIRA",
            "BILLINGS",
            "HENRY BORDEN",
            "GUARAPIRANGA",
            "EDGARD SOUZA",
            "BARRA BONITA",
            "A.S. LIMA",
            "IBITINGA",
            "PROMISSAO",
            "NAVANHANDAVA",
            "TRES IRMAOS",
            "JUPIA",
            "SAO DOMINGOS",
            "P. PRIMAVERA",
            "A.A. LAYDNER",
            "PIRAJU",
            "CHAVANTES",
            "OURINHOS",
            "L.N. GARCEZ",
            "CANOAS II",
            "CANOAS I",
            "MAUA",
            "CAPIVARA",
            "TAQUARUCU",
            "ROSANA",
            "ITAIPU",
            "JAGUARI",
            "PARAIBUNA",
            "SANTA BRANCA",
            "FUNIL",
            "PICADA",
            "SOBRAGI",
            "TOCOS",
            "SANTANA",
            "SIMPLICIO",
            "ILHA POMBOS",
            "NILO PECANHA",
            "LAJES",
            "FONTES A",
            "FONTES BC",
            "P. PASSOS",
            "SALTO GRANDE",
            "P. ESTRELA",
            "CANDONGA",
            "GUILMAN-AMOR",
            "SA CARVALHO",
            "BAGUARI",
            "AIMORES",
            "MASCARENHAS",
            "JAURU",
            "ROSAL",
            "MANSO",
            "PONTE PEDRA",
            "STA CLARA MG",
            "ITIQUIRA I",
            "ITIQUIRA II",
            "GUAPORE",
            "JIRAU",
            "STO ANTONIO",
            "RONDON II",
            "SAMUEL",
            "DARDANELOS",
            "SINOP",
            "COLIDER",
            "TELES PIRES",
            "SAO MANOEL",
            "STA CLARA PR",
            "FUNDAO",
            "JORDAO",
            "G.B. MUNHOZ",
            "SEGREDO",
            "SLT.SANTIAGO",
            "SALTO OSORIO",
            "SALTO CAXIAS",
            "BAIXO IGUACU",
            "BARRA GRANDE",
            "GARIBALDI",
            "CAMPOS NOVOS",
            "MACHADINHO",
            "ITA",
            "PASSO FUNDO",
            "MONJOLINHO",
            "QUEBRA QUEIX",
            "CASTRO ALVES",
            "MONTE CLARO",
            "14 DE JULHO",
            "SAO JOSE",
            "PASSO S JOAO",
            "FOZ CHAPECO",
            "ERNESTINA",
            "PASSO REAL",
            "JACUI",
            "ITAUBA",
            "D. FRANCISCA",
            "G.P. SOUZA",
            "IRAPE",
            "ITAPEBI",
            "RETIRO BAIXO",
            "TRES MARIAS",
            "QUEIMADO",
            "SOBRADINHO",
            "ITAPARICA",
            "MOXOTO",
            "P.AFONSO 123",
            "P.AFONSO 4",
            "XINGO",
            "P. CAVALO",
            "B. ESPERANCA",
            "CACH.CALDEIR",
            "SALTO PILAO",
            "SERRA MESA",
            "CANA BRAVA",
            "SAO SALVADOR",
            "PEIXE ANGIC",
            "LAJEADO",
            "ESTREITO TOC",
            "CURUA-UNA",
            "TUCURUI",
            "BALBINA",
            "COARACY NUNE",
            "FERREIRA GOM",
            "STO ANT JARI",
            "BELO MONTE",
            "PIMENTAL",
        ]
        variaveis.sort()
        opcoes = [{"label": p, "value": p} for p in variaveis]
        return opcoes

    @staticmethod
    def __opcoes_dropdown_newave() -> List[dict]:
        variaveis = [
            "GERACAO TERMICA",
            "DEFICIT",
            "VERTIMENTO",
            "EXCESSO ENERGIA",
            "VIOLACAO CAR",
            "VIOLACAO SAR",
            "VIOL. OUTROS USOS",
            "VIOLACAO VZMIN",
            "INTERCAMBIO",
            "VERT. FIO N. TURB.",
            "VIOLACAO GHMIN",
            "TOTAL",
        ]
        opcoes = [{"label": p, "value": p} for p in variaveis]
        return opcoes

    @staticmethod
    def __opcoes_dropdown_inviab() -> List[dict]:
        variaveis = [
            "RE",
            "RHQ",
            "TI",
            "RHV",
            "RHE",
            "EV",
            "DEFMIN",
            "FP",
            "DEFICIT",
            "OUTRO",
            "TOTAL",
        ]
        opcoes = [{"label": p, "value": p} for p in variaveis]
        return opcoes

    @staticmethod
    def __opcoes_dropdown_tempo() -> List[dict]:
        variaveis = ["NEWAVE", "DECOMP", "TOTAL"]
        opcoes = [{"label": p, "value": p} for p in variaveis]
        return opcoes

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
                                                            id="escolhe-variavel-operacao",
                                                            options=[],
                                                            value=None,
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
                        html.Div(
                            children=[
                                html.Div(
                                    [
                                        html.H3(
                                            "INVIABILIDADES",
                                            className="app-frame-title",
                                        ),
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    children=[
                                                        dcc.Dropdown(
                                                            id="escolhe-variavel-inviab",
                                                            options=App.__opcoes_dropdown_inviab(),
                                                            value=App.__opcoes_dropdown_inviab()[
                                                                -1
                                                            ][
                                                                "value"
                                                            ],
                                                            className="variable-dropdown",
                                                        )
                                                    ],
                                                    className="dropdown-container",
                                                ),
                                                html.Button(
                                                    "CSV",
                                                    id="inviab-btn",
                                                    className="download-button",
                                                ),
                                            ],
                                            className="dropdown-button-container",
                                        ),
                                    ],
                                    className="graph-header",
                                ),
                                dcc.Graph(id="grafico-inviabs"),
                            ],
                            className="twelve column graph-with-dropdown-container second",
                        ),
                        html.Div(
                            children=[
                                html.Div(
                                    [
                                        html.H3(
                                            "TEMPO EXECUCAO",
                                            className="app-frame-title",
                                        ),
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    children=[
                                                        dcc.Dropdown(
                                                            id="escolhe-variavel-tempo",
                                                            options=App.__opcoes_dropdown_tempo(),
                                                            value=App.__opcoes_dropdown_tempo()[
                                                                -1
                                                            ][
                                                                "value"
                                                            ],
                                                            className="variable-dropdown",
                                                        )
                                                    ],
                                                    className="dropdown-container",
                                                ),
                                                html.Button(
                                                    "CSV",
                                                    id="tempo-btn",
                                                    className="download-button",
                                                ),
                                            ],
                                            className="dropdown-button-container",
                                        ),
                                    ],
                                    className="graph-header",
                                ),
                                dcc.Graph(id="grafico-tempo"),
                            ],
                            className="twelve column graph-with-dropdown-container second",
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
                dcc.Interval(
                    id="resume-inviabilidades-decomp",
                    interval=int(cfg.periodo_atualizacao_graficos),
                    n_intervals=0,
                ),
                dcc.Store(id="dados-caso-atual"),
                dcc.Store(id="dados-variaveis-operacao"),
                dcc.Store(id="dados-grafico-estudo-encadeado"),
                dcc.Store(id="dados-grafico-inviabs"),
                dcc.Download(id="download-operacao"),
                dcc.Download(id="download-inviabs"),
                dcc.Download(id="download-tempo"),
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
            Output("dados-grafico-estudo-encadeado", "data"),
            Input("atualiza-dados-graficos", "n_intervals"),
            Input("dados-caminhos-casos", "data"),
        )
        def atualiza_dados_estudo(interval, data):
            return self.__db.le_resumo_estudo_encadeado(data)

        @self.__app.callback(
            Output("dados-caso-atual", "data"),
            Input("atualiza-dados-caso", "n_intervals"),
            Input("dados-caminhos-casos", "data"),
        )
        def atualiza_dados_caso(interval, data):
            return self.__db.le_informacoes_proximo_caso(data)

        @self.__app.callback(
            Output("dados-grafico-inviabs", "data"),
            Input("atualiza-dados-graficos", "n_intervals"),
            Input("dados-caminhos-casos", "data"),
        )
        def atualiza_dados_grafico_inviabs(interval, data):
            return self.__db.le_inviabilidades_decomps(data)

        @self.__app.callback(
            Output("hidden-div", "n_clicks"),
            Input("atualiza-dados-graficos", "n_intervals"),
            Input("dados-caminhos-casos", "data"),
        )
        def resume_dados_inviabs_decomp(n_clicks, data):
            return self.__db.resume_inviabilidades_decomps(data)

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
        )
        def gera_grafico_operacao(dados_operacao, variavel):
            if dados_operacao is None:
                return self.__default_fig
            dados = pd.read_json(dados_operacao, orient="split")
            dados["Data Inicio"] = pd.to_datetime(
                dados["Data Inicio"], unit="ms"
            )
            dados["Data Fim"] = pd.to_datetime(dados["Data Fim"], unit="ms")
            estudos = dados["Estudo"].unique().tolist()
            estagio = 1
            filtro_newave = (dados["Programa"] == "NEWAVE") & (
                dados["Estagio"] == estagio
            )
            filtro_decomp = (dados["Programa"] == "DECOMP") & (
                dados["Estagio"] == estagio
            )
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
                return df_completo.to_json(orient="split")

        @self.__app.callback(
            Output("grafico-inviabs", "figure"),
            Input("dados-grafico-inviabs", "data"),
            Input("escolhe-variavel-inviab", "value"),
        )
        def gera_grafico_inviab(dados: str, variavel: str):
            if dados is None:
                Log.log().warning("Sem dados de inviabilidades")
                return go.Figure()
            dados_locais: pd.DataFrame = pd.read_json(dados, orient="split")
            if dados_locais.empty:
                Log.log().warning("Sem dados de inviabilidades")
                return go.Figure()
            if variavel != "TOTAL":
                dados_inv = dados_locais["Tipo"] == variavel
                dados_locais = dados_locais.loc[dados_inv, :]
            dados_locais.sort_values(["Estudo", "Caso"], inplace=True)
            fig = px.bar(
                dados_locais,
                x="Caso",
                y="Num. Violacoes",
                color="Estudo",
                hover_data=["Tipo"],
            )
            return fig

        @self.__app.callback(
            Output("grafico-tempo", "figure"),
            Input("dados-grafico-estudo-encadeado", "data"),
            Input("escolhe-variavel-tempo", "value"),
        )
        def gera_grafico_tempo(dados: str, variavel: str):
            if dados is None:
                Log.log().warning("Sem dados de TEMPO")
                return go.Figure()
            dados_locais: pd.DataFrame = pd.read_json(dados, orient="split")
            if dados_locais.empty:
                Log.log().warning("Sem dados de TEMPO")
                return go.Figure()
            if variavel != "TOTAL":
                dados_prog = dados_locais["Programa"] == variavel
                dados_locais = dados_locais.loc[dados_prog, :]

            dados_locais = (
                dados_locais.groupby(["Estudo", "Caso"]).sum().reset_index()
            )
            dados_locais.sort_values(["Estudo", "Caso"], inplace=True)
            fig = px.bar(
                dados_locais.loc[dados_locais["Sucesso"] > 0, :],
                x="Caso",
                y="Tempo Execucao (min)",
                color="Estudo",
            )
            return fig

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
            Output("download-tempo", "data"),
            Input("tempo-btn", "n_clicks"),
            State("dados-caminhos-casos", "data"),
        )
        def gera_csv_tempo(n_clicks, data):
            if n_clicks is None:
                return
            df = pd.read_json(
                self.__db.le_resumo_estudo_encadeado(data), orient="split"
            )
            return dcc.send_data_frame(df.to_csv, "tempo_execucao.csv")

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
