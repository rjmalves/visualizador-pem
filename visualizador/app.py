import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import socket
from dash.dependencies import Input, Output
from typing import List
from waitress import serve

from visualizador.modelos.log import Log
from visualizador.modelos.configuracoes import Configuracoes
from visualizador.utils.db import DB


class App:
    
    def __init__(self) -> None:
        self.__app = dash.Dash(__name__,
                               title="Encadeador",
                               update_title="Carregando...")
        self.__inicializa()

    @staticmethod
    def __opcoes_dropdown_decomp() -> List[dict]:
        variaveis = ["CMO SE",
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
                     "GH SIN",
                     "GH SE",
                     "GH S",
                     "GH NE",
                     "GH N",
                     "Mercado SIN",
                     "Mercado SE",
                     "Mercado S",
                     "Mercado NE",
                     "Mercado N",]
        opcoes = [
            {"label": p, "value": p}
            for p in variaveis
        ]
        return opcoes

    @staticmethod
    def __opcoes_dropdown_newave() -> List[dict]:
        variaveis = ["GERACAO TERMICA",
                     "DEFICIT",
                     "VERTIMENTO",
                     "EXCESSO ENERGIA",
                     "VIOLACAO CAR",
                     "VIOLACAO SAR",
                     "VIOL. OUTROS USOS",
                     "VIOLACAO VZMIN",
                     "INTERCAMBIO",
                     "VERT. FIO N. TURB",
                     "VIOLACAO GHMIN",
                     "TOTAL"]
        opcoes = [
            {"label": p, "value": p}
            for p in variaveis
        ]
        return opcoes

    @staticmethod
    def __opcoes_dropdown_inviab() -> List[dict]:
        variaveis = ["RE",
                     "RHQ",
                     "TI",
                     "RHV",
                     "RHE",
                     "EV",
                     "DEFMIN",
                     "FP",
                     "DEFICIT",
                     "OUTRO",
                     "TOTAL"]
        opcoes = [
            {"label": p, "value": p}
            for p in variaveis
        ]
        return opcoes

    @staticmethod
    def __opcoes_dropdown_tempo() -> List[dict]:
        variaveis = ["NEWAVE",
                     "DECOMP",
                     "TOTAL"]
        opcoes = [
            {"label": p, "value": p}
            for p in variaveis
        ]
        return opcoes

    def __inicializa(self):
        cfg = Configuracoes()
        self.__app.layout = html.Div([
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.H1("Visualizador de Estudos Encadeados",
                                    className="app-header-title"),
                            html.H2("Gerência de Metodologias e Modelos Energéticos - PEM",
                                    className="app-header-subtitle")
                        ],
                        className="app-header-titles"
                    ),
                    html.Div(
                        children=[

                        ],
                        className="app-header-logo"
                    )
                ],
                className="app-header"
            ),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(children=[
                                html.H4("CASOS ATUAIS",
                                        className="app-table-frame-title"),
                                ],
                                className="table-header"
                            ),
                            html.Table(id="informacao-caso-atual",
                                       className="app-table")
                        ],
                        className="twelve column current-case-table-container"
                    ),
                    html.Div(
                        children=[
                            html.Div([
                                html.H3("DECOMP",
                                        className="app-frame-title"),
                                html.Div(children=[
                                    html.Div(children=[
                                        dcc.Dropdown(id="escolhe-variavel-decomps",
                                                     options=App.__opcoes_dropdown_decomp(),
                                                     value=App.__opcoes_dropdown_decomp()[0]["value"],
                                                     className="variable-dropdown")
                                        ],
                                        className="dropdown-container"
                                    ),
                                    html.Button("CSV",
                                                id="decomp-btn",
                                                className="download-button"),
                                    ],
                                    className="dropdown-button-container"
                                ),
                                ],
                                className="graph-header"
                            ),
                            dcc.Graph(id="grafico-decomps")
                        ],
                        className="twelve column graph-with-dropdown-container first"
                    ),
                    html.Div(
                        children=[
                            html.Div([
                                html.H4("NEWAVE",
                                        className="app-frame-title"),
                                html.Div(children=[
                                    html.Div(children=[
                                        dcc.Dropdown(id="escolhe-variavel-newaves",
                                                     options=App.__opcoes_dropdown_newave(),
                                                     value=App.__opcoes_dropdown_newave()[-1]["value"],
                                                     className="variable-dropdown")
                                        ],
                                        className="dropdown-container"
                                    ),
                                    html.Button("CSV",
                                                 id="newave-btn",
                                                 className="download-button"),
                                    ],
                                    className="dropdown-button-container"
                                ),
                                ],
                                className="graph-header"
                            ),
                            dcc.Graph(id="grafico-newaves")
                        ],
                        className="twelve column graph-with-dropdown-container second"
                    ),
                    html.Div(
                        children=[
                            html.Div([
                                html.H3("INVIABILIDADES",
                                        className="app-frame-title"),
                                html.Div(children=[
                                    html.Div(children=[
                                        dcc.Dropdown(id="escolhe-variavel-inviab",
                                                     options=App.__opcoes_dropdown_inviab(),
                                                     value=App.__opcoes_dropdown_inviab()[-1]["value"],
                                                     className="variable-dropdown")
                                        ],
                                        className="dropdown-container"
                                    ),
                                    html.Button("CSV",
                                                id="inviab-btn",
                                                className="download-button"),
                                    ],
                                    className="dropdown-button-container"
                                ),
                                ],
                                className="graph-header"
                            ),
                            dcc.Graph(id="grafico-inviabs")
                        ],
                        className="twelve column graph-with-dropdown-container second"
                    ),
                    html.Div(
                        children=[
                            html.Div([
                                html.H3("TEMPO EXECUCAO",
                                        className="app-frame-title"),
                                html.Div(children=[
                                    html.Div(children=[
                                        dcc.Dropdown(id="escolhe-variavel-tempo",
                                                     options=App.__opcoes_dropdown_tempo(),
                                                     value=App.__opcoes_dropdown_tempo()[-1]["value"],
                                                     className="variable-dropdown")
                                        ],
                                        className="dropdown-container"
                                    ),
                                    html.Button("CSV",
                                                id="tempo-btn",
                                                className="download-button"),
                                    ],
                                    className="dropdown-button-container"
                                ),
                                ],
                                className="graph-header"
                            ),
                            dcc.Graph(id="grafico-tempo")
                        ],
                        className="twelve column graph-with-dropdown-container second"
                    ),
                ],
                className="app-content"
            ),
            dcc.Interval(id="atualiza-dados-graficos",
                         interval=int(cfg.periodo_atualizacao_graficos),
                         n_intervals=0),
            dcc.Interval(id="atualiza-dados-caso",
                         interval=int(cfg.periodo_atualizacao_caso_atual),
                         n_intervals=0),
            dcc.Interval(id="resume-inviabilidades-decomp",
                         interval=int(cfg.periodo_atualizacao_graficos),
                         n_intervals=0),
            dcc.Store(id="dados-caso-atual"),
            dcc.Store(id="dados-grafico-estudo-encadeado"),
            dcc.Store(id="dados-grafico-decomps"),
            dcc.Store(id="dados-grafico-newaves"),
            dcc.Store(id="dados-grafico-inviabs"),
            dcc.Download(id="download-decomp"),
            dcc.Download(id="download-newave"),
            dcc.Download(id="download-inviabs"),
            dcc.Download(id="download-tempo"),
            html.Div(id="hidden-div", style={"display":"none"}, )
        ],
        className="app-container"
        )

        @self.__app.callback(
            Output("dados-grafico-decomps", "data"),
            Input("atualiza-dados-graficos", "n_intervals")
        )
        def atualiza_dados_grafico_decomps(interval):
            return DB.le_resumo_decomps()

        @self.__app.callback(
            Output("dados-grafico-newaves", "data"),
            Input("atualiza-dados-graficos", "n_intervals")
        )
        def atualiza_dados_grafico_newaves(interval):
            return DB.le_resumo_newaves()

        @self.__app.callback(
            Output("dados-grafico-estudo-encadeado", "data"),
            Input("atualiza-dados-graficos", "n_intervals")
        )
        def atualiza_dados_estudo(interval):
            return DB.le_resumo_estudo_encadeado()

        @self.__app.callback(
            Output("dados-caso-atual", "data"),
            Input("atualiza-dados-caso", "n_intervals")
        )
        def atualiza_dados_caso(interval):
            return DB.le_informacoes_proximo_caso()

        @self.__app.callback(
            Output("dados-grafico-inviabs", "data"),
            Input("atualiza-dados-graficos", "n_intervals")
        )
        def atualiza_dados_grafico_inviabs(interval):
            return DB.le_inviabilidades_decomps()

        @self.__app.callback(
            Output("hidden-div", "n_clicks"),
            Input("atualiza-dados-graficos", "n_intervals")
        )
        def resume_dados_inviabs_decomp(n_clicks):
            return DB.resume_inviabilidades_decomps()

        @self.__app.callback(
            Output("informacao-caso-atual", "children"),
            Input("dados-caso-atual", "data")
        )
        def gera_tabela(dados: pd.DataFrame):
            dados_locais: pd.DataFrame = pd.read_json(dados,
                                                      orient="split")
            return App.gera_tabela(dados_locais)

        @self.__app.callback(
            Output("grafico-decomps", "figure"),
            Input("dados-grafico-decomps", "data"),
            Input("escolhe-variavel-decomps", "value")
        )
        def gera_grafico_decomps(dados: str, variavel: str):
            dados_locais: pd.DataFrame = pd.read_json(dados,
                                                      orient="split")
            if "EARM" not in variavel:
                casos_sem_inicial = list(dados_locais["Caso"].unique())
                casos_sem_inicial = casos_sem_inicial[1:]
                filtro = dados_locais["Caso"].isin(casos_sem_inicial)
                dados_locais = dados_locais.loc[filtro, :]
            fig = px.line(dados_locais,
                          x="Caso",
                          y=variavel,
                          color="Estudo")
            return fig

        @self.__app.callback(
            Output("grafico-newaves", "figure"),
            Input("dados-grafico-newaves", "data"),
            Input("escolhe-variavel-newaves", "value")
        )
        def gera_grafico_newaves(dados: str, variavel: str):
            dados_locais: pd.DataFrame = pd.read_json(dados,
                                                      orient="split")
            fig = px.line(dados_locais,
                          x="Caso",
                          y=variavel,
                          color="Estudo")
            return fig

        @self.__app.callback(
            Output("grafico-inviabs", "figure"),
            Input("dados-grafico-inviabs", "data"),
            Input("escolhe-variavel-inviab", "value")
        )
        def gera_grafico_inviab(dados: str, variavel: str):
            dados_locais: pd.DataFrame = pd.read_json(dados,
                                                      orient="split")
            if variavel != "TOTAL":
                dados_inv = dados_locais["Tipo"] == variavel
                dados_locais = dados_locais.loc[dados_inv, :]

            print(dados_locais)
            fig = px.bar(dados_locais,
                         x="Caso",
                         y="Num. Violacoes",
                         color="Estudo",
                         hover_data=["Tipo"])
            return fig

        @self.__app.callback(
            Output("grafico-tempo", "figure"),
            Input("dados-grafico-estudo-encadeado", "data"),
            Input("escolhe-variavel-tempo", "value")
        )
        def gera_grafico_tempo(dados: str, variavel: str):
            dados_locais: pd.DataFrame = pd.read_json(dados,
                                                      orient="split")
            if variavel != "TOTAL":
                dados_prog = dados_locais["Programa"] == variavel
                dados_locais = dados_locais.loc[dados_prog, :]

            dados_locais = dados_locais.groupby(["Estudo", "Caso"]).sum().reset_index()
            fig = px.bar(dados_locais,
                         x="Caso",
                         y="Tempo Execucao (min)",
                         color="Estudo")
            return fig

        @self.__app.callback(
            Output("download-decomp", "data"),
            Input("decomp-btn", "n_clicks")
        )
        def gera_csv_decomp(n_clicks):
            if n_clicks is None:
                return
            df = pd.read_json(DB.le_resumo_decomps(),
                              orient="split")
            return dcc.send_data_frame(df.to_csv, "decomps.csv")

        @self.__app.callback(
            Output("download-newave", "data"),
            Input("newave-btn", "n_clicks")
        )
        def gera_csv_newave(n_clicks):
            if n_clicks is None:
                return
            df = pd.read_json(DB.le_resumo_newaves(),
                              orient="split")
            return dcc.send_data_frame(df.to_csv, "newaves.csv")

        @self.__app.callback(
            Output("download-inviabs", "data"),
            Input("inviab-btn", "n_clicks")
        )
        def gera_csv_inviabs(n_clicks):
            if n_clicks is None:
                return
            df = pd.read_json(DB.le_inviabilidades_decomps(),
                              orient="split")
            return dcc.send_data_frame(df.to_csv, "inviabilidades.csv")

        @self.__app.callback(
            Output("download-tempo", "data"),
            Input("tempo-btn", "n_clicks")
        )
        def gera_csv_tempo(n_clicks):
            if n_clicks is None:
                return
            df = pd.read_json(DB.le_resumo_estudo_encadeado(),
                              orient="split")
            return dcc.send_data_frame(df.to_csv, "tempo_execucao.csv")

    @staticmethod
    def gera_tabela(df: pd.DataFrame):
        return html.Table([
            html.Thead(
                html.Tr([html.Th(col) for col in df.columns])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(df.iloc[i][col]) for col in df.columns
                ])
                for i in range(min(len(df), 20))
            ])
        ])

    def serve(self):
        log = Log.log()
        cfg = Configuracoes()
        ip_servidor = socket.gethostbyname(socket.gethostname())
        log.info(f"Visualizador: {ip_servidor}:{cfg.porta_servidor}")
        if cfg.modo == "DEV":
            self.__app.run_server(host="0.0.0.0",
                                  port=str(cfg.porta_servidor),
                                  debug=True)
        elif cfg.modo == "PROD":
            serve(self.__app.server,
                  host="0.0.0.0",
                  port=str(cfg.porta_servidor))
