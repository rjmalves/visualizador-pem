from email.utils import parsedate_to_datetime
import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
from plotly import tools
from os.path import join, isfile
import pandas as pd
import socket
from dash.dependencies import Input, Output
from typing import List
from waitress import serve
import base62

from visualizador.modelos.log import Log
from visualizador.modelos.configuracoes import Configuracoes
from visualizador.utils.db import DB

CFG_FILENAME = "visualiza.cfg"


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
        self.__app.layout = html.Div(
            [
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H1(
                                    "Visualizador de Estudos Encadeados",
                                    className="app-header-title",
                                ),
                                html.H2(
                                    "Gerência de Metodologias e Modelos Energéticos - PEM",
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
                                            "DECOMP",
                                            className="app-frame-title",
                                        ),
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    children=[
                                                        dcc.Dropdown(
                                                            id="escolhe-variavel-decomps",
                                                            options=App.__opcoes_dropdown_decomp(),
                                                            value=App.__opcoes_dropdown_decomp()[
                                                                0
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
                                                    id="decomp-btn",
                                                    className="download-button",
                                                ),
                                            ],
                                            className="dropdown-button-container",
                                        ),
                                    ],
                                    className="graph-header",
                                ),
                                dcc.Graph(id="grafico-decomps"),
                            ],
                            className="twelve column graph-with-dropdown-container first",
                        ),
                        html.Div(
                            children=[
                                html.Div(
                                    [
                                        html.H3(
                                            "RESERVATORIOS",
                                            className="app-frame-title",
                                        ),
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    children=[
                                                        dcc.Dropdown(
                                                            id="escolhe-variavel-reservatorios",
                                                            options=App.__opcoes_dropdown_reservatorios(),
                                                            value=App.__opcoes_dropdown_reservatorios()[
                                                                0
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
                                                    id="reservatorios-btn",
                                                    className="download-button",
                                                ),
                                            ],
                                            className="dropdown-button-container",
                                        ),
                                    ],
                                    className="graph-header",
                                ),
                                dcc.Graph(id="grafico-reservatorios"),
                            ],
                            className="twelve column graph-with-dropdown-container first",
                        ),
                        html.Div(
                            children=[
                                html.Div(
                                    [
                                        html.H3(
                                            "DEFLUENCIAS",
                                            className="app-frame-title",
                                        ),
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    children=[
                                                        dcc.Dropdown(
                                                            id="escolhe-variavel-defluencias",
                                                            options=App.__opcoes_dropdown_defluencias(),
                                                            value=App.__opcoes_dropdown_defluencias()[
                                                                0
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
                                                    id="defluencias-btn",
                                                    className="download-button",
                                                ),
                                            ],
                                            className="dropdown-button-container",
                                        ),
                                    ],
                                    className="graph-header",
                                ),
                                dcc.Graph(id="grafico-defluencias"),
                            ],
                            className="twelve column graph-with-dropdown-container first",
                        ),
                        html.Div(
                            children=[
                                html.Div(
                                    [
                                        html.H4(
                                            "NEWAVE",
                                            className="app-frame-title",
                                        ),
                                        html.Div(
                                            children=[
                                                html.Div(
                                                    children=[
                                                        dcc.Dropdown(
                                                            id="escolhe-variavel-newaves",
                                                            options=App.__opcoes_dropdown_newave(),
                                                            value=App.__opcoes_dropdown_newave()[
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
                                                    id="newave-btn",
                                                    className="download-button",
                                                ),
                                            ],
                                            className="dropdown-button-container",
                                        ),
                                    ],
                                    className="graph-header",
                                ),
                                dcc.Graph(id="grafico-newaves"),
                            ],
                            className="twelve column graph-with-dropdown-container second",
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
                dcc.Store(id="dados-grafico-estudo-encadeado"),
                dcc.Store(id="dados-grafico-decomps"),
                dcc.Store(id="dados-grafico-reservatorios"),
                dcc.Store(id="dados-grafico-defluencias"),
                dcc.Store(id="dados-grafico-newaves"),
                dcc.Store(id="dados-grafico-inviabs"),
                dcc.Download(id="download-decomp"),
                dcc.Download(id="download-reservatorios"),
                dcc.Download(id="download-defluencias"),
                dcc.Download(id="download-newave"),
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
            Output("dados-grafico-decomps", "data"),
            Input("atualiza-dados-graficos", "n_intervals"),
            Input("dados-caminhos-casos", "data"),
        )
        def atualiza_dados_grafico_decomps(interval, data):
            return self.__db.le_resumo_decomps(data)

        @self.__app.callback(
            Output("dados-grafico-reservatorios", "data"),
            Input("atualiza-dados-graficos", "n_intervals"),
            Input("dados-caminhos-casos", "data"),
        )
        def atualiza_dados_grafico_reservatorios(interval, data):
            return self.__db.le_resumo_reservatorios(data)

        @self.__app.callback(
            Output("dados-grafico-defluencias", "data"),
            Input("atualiza-dados-graficos", "n_intervals"),
            Input("dados-caminhos-casos", "data"),
        )
        def atualiza_dados_grafico_defluencias(interval, data):
            return self.__db.le_resumo_defluencias(data)

        @self.__app.callback(
            Output("dados-grafico-newaves", "data"),
            Input("atualiza-dados-graficos", "n_intervals"),
            Input("dados-caminhos-casos", "data"),
        )
        def atualiza_dados_grafico_newaves(interval, data):
            return self.__db.le_resumo_newaves(data)

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
            Output("grafico-decomps", "figure"),
            Input("dados-grafico-decomps", "data"),
            Input("escolhe-variavel-decomps", "value"),
        )
        def gera_grafico_decomps(dados: str, variavel: str):
            if dados is None:
                Log.log().warning("Sem dados de DECOMP")
                return go.Figure()
            dados_locais: pd.DataFrame = pd.read_json(dados, orient="split")
            if dados_locais.empty:
                Log.log().warning("Sem dados de DECOMP")
                return go.Figure()

            if "EARM" not in variavel:
                casos_sem_inicial = list(dados_locais["Caso"].unique())
                casos_sem_inicial = casos_sem_inicial[1:]
                filtro = dados_locais["Caso"].isin(casos_sem_inicial)
                dados_locais = dados_locais.loc[filtro, :]

            def sortfun(col: pd.Series):
                col.loc[col == "Inicial"] = ""
                return col

            dados_locais.sort_values(
                ["Estudo", "Caso"], inplace=True, key=sortfun
            )
            fig = px.line(dados_locais, x="Caso", y=variavel, color="Estudo")
            return fig

        @self.__app.callback(
            Output("grafico-reservatorios", "figure"),
            Input("dados-grafico-reservatorios", "data"),
            Input("escolhe-variavel-reservatorios", "value"),
        )
        def gera_grafico_reservatorios(dados: str, variavel: str):
            if dados is None:
                Log.log().warning("Sem dados de reservatórios")
                return go.Figure()
            dados_locais: pd.DataFrame = pd.read_json(dados, orient="split")
            if dados_locais.empty:
                Log.log().warning("Sem dados de reservatórios")
                return go.Figure()
            dados_locais = dados_locais.loc[
                dados_locais["Estagio"] == "Estágio 1", :
            ]
            dados_locais.sort_values(["Estudo", "Caso"], inplace=True)
            fig = px.line(dados_locais, x="Caso", y=variavel, color="Estudo")
            return fig

        @self.__app.callback(
            Output("grafico-defluencias", "figure"),
            Input("dados-grafico-defluencias", "data"),
            Input("escolhe-variavel-defluencias", "value"),
        )
        def gera_grafico_defluencias(dados: str, variavel: str):
            if dados is None:
                Log.log().warning("Sem dados de defluências")
                return go.Figure()
            dados_locais: pd.DataFrame = pd.read_json(dados, orient="split")
            if dados_locais.empty:
                Log.log().warning("Sem dados de defluências")
                return go.Figure()
            dados_locais = dados_locais.loc[
                dados_locais["Estagio"] == "Estágio 1", :
            ]
            dados_locais.sort_values(["Estudo", "Caso"], inplace=True)
            fig = px.line(dados_locais, x="Caso", y=variavel, color="Estudo")
            return fig

        @self.__app.callback(
            Output("grafico-newaves", "figure"),
            Input("dados-grafico-newaves", "data"),
            Input("escolhe-variavel-newaves", "value"),
        )
        def gera_grafico_newaves(dados: str, variavel: str):
            if dados is None:
                Log.log().warning("Sem dados de NEWAVE")
                return go.Figure()
            dados_locais: pd.DataFrame = pd.read_json(dados, orient="split")
            if dados_locais.empty:
                Log.log().warning("Sem dados de NEWAVE")
                return go.Figure()
            dados_locais.sort_values(["Estudo", "Caso"], inplace=True)
            fig = px.line(dados_locais, x="Caso", y=variavel, color="Estudo")
            return fig

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
            Output("download-decomp", "data"),
            Input("decomp-btn", "n_clicks"),
            Input("dados-caminhos-casos", "data"),
        )
        def gera_csv_decomp(n_clicks, data):
            if n_clicks is None:
                return
            df = pd.read_json(
                self.__db.le_resumo_decomps(data), orient="split"
            )
            return dcc.send_data_frame(df.to_csv, "decomps.csv")

        @self.__app.callback(
            Output("download-reservatorios", "data"),
            Input("reservatorios-btn", "n_clicks"),
            Input("dados-caminhos-casos", "data"),
        )
        def gera_csv_reservatorios(n_clicks, data):
            if n_clicks is None:
                return
            df = pd.read_json(
                self.__db.le_resumo_reservatorios(data), orient="split"
            )
            return dcc.send_data_frame(df.to_csv, "reservatorios.csv")

        @self.__app.callback(
            Output("download-defluencias", "data"),
            Input("defluencias-btn", "n_clicks"),
            Input("dados-caminhos-casos", "data"),
        )
        def gera_csv_defluencias(n_clicks, data):
            if n_clicks is None:
                return
            df = pd.read_json(
                self.__db.le_resumo_defluencias(data), orient="split"
            )
            return dcc.send_data_frame(df.to_csv, "defluencias.csv")

        @self.__app.callback(
            Output("download-newave", "data"),
            Input("newave-btn", "n_clicks"),
            Input("dados-caminhos-casos", "data"),
        )
        def gera_csv_newave(n_clicks, data):
            if n_clicks is None:
                return
            df = pd.read_json(
                self.__db.le_resumo_newaves(data), orient="split"
            )
            return dcc.send_data_frame(df.to_csv, "newaves.csv")

        @self.__app.callback(
            Output("download-inviabs", "data"),
            Input("inviab-btn", "n_clicks"),
            Input("dados-caminhos-casos", "data"),
        )
        def gera_csv_inviabs(n_clicks, data):
            if n_clicks is None:
                return
            df = pd.read_json(
                self.__db.le_inviabilidades_decomps(data), orient="split"
            )
            return dcc.send_data_frame(df.to_csv, "inviabilidades.csv")

        @self.__app.callback(
            Output("download-tempo", "data"),
            Input("tempo-btn", "n_clicks"),
            Input("dados-caminhos-casos", "data"),
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
