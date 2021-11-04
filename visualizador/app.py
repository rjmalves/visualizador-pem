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
        self.__app = dash.Dash(__name__)
        self.__inicializa()

    # @staticmethod
    # def __opcoes_dropdown() -> List[dict]:
    #     cfg = Configuracoes()
    #     pastas_casos = [normpath(c).split(sep)[-1]
    #                     for c in cfg.caminhos_casos]
    #     opcoes = [
    #         {"label": p, "value": p}
    #         for p in pastas_casos
    #     ]
    #     return opcoes

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

    def __inicializa(self):
        cfg = Configuracoes()
        self.__app.layout = html.Div([
            html.H1("Visualizador de Estudos Encadeados"),
            html.H2("Gerência de Metodologias e Modelos Energéticos - PEM"),
            html.Table(id="informacao-caso-atual"),
            html.H3("Resumo dos DECOMPs"),
            dcc.Dropdown(id="escolhe-variavel-decomps",
                         options=App.__opcoes_dropdown_decomp(),
                         value=App.__opcoes_dropdown_decomp()[0]["value"]),
            dcc.Graph(id="grafico-decomps"),
            html.H3("Resumo dos NEWAVEs"),
            dcc.Dropdown(id="escolhe-variavel-newaves",
                         options=App.__opcoes_dropdown_newave(),
                         value=App.__opcoes_dropdown_newave()[-1]["value"]),
            dcc.Graph(id="grafico-newaves"),
            dcc.Interval(id="atualiza-dados-graficos",
                         interval=int(cfg.periodo_atualizacao_graficos),
                         n_intervals=0),
            dcc.Interval(id="atualiza-dados-caso",
                         interval=int(cfg.periodo_atualizacao_caso_atual),
                         n_intervals=0),
            dcc.Store(id="dados-caso-atual"),
            dcc.Store(id="dados-estudo-encadeado"),
            dcc.Store(id="dados-grafico-decomps"),
            dcc.Store(id="dados-grafico-newaves")
        ])

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
            Output("dados-estudo-encadeado", "data"),
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
