import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from os import sep
from os.path import normpath
from typing import List

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
    def __opcoes_dropdown() -> List[dict]:
        cfg = Configuracoes()
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

    def __inicializa(self):
        cfg = Configuracoes()
        self.__app.layout = html.Div([
            html.H1("Visualizador de Estudos Encadeados"),
            html.H2("Gerência de Metodologias e Modelos Energéticos - PEM"),
            dcc.Dropdown(id="escolhe-variavel",
                         options=App.__opcoes_dropdown,
                         value=App.__opcoes_dropdown[0]["value"]),
            html.Table(id="informacao-caso-atual"),
            dcc.Graph(id="grafico"),
            dcc.Interval(id="atualiza-dados-graficos",
                         interval=int(cfg.periodo_atualizacao_graficos),
                         n_intervals=0),
            dcc.Interval(id="atualiza-dados-caso",
                         interval=int(cfg.periodo_atualizacao_caso_atual),
                         n_intervals=0),
            dcc.Store(id="dados-caso-atual"),
            dcc.Store(id="dados-estudo-encadeado"),
            dcc.Store(id="dados-graficos")
        ])

        @self.__app.callback(
            Input("atualiza-dados-graficos", "n_intervals"),
            Output("dados-graficos", "data")
        )
        def atualiza_dados_graficos(interval):
            return DB.le_resumo_decomps()

        @self.__app.callback(
            Input("atualiza-dados-graficos", "n_intervals"),
            Output("dados-estudo-encadeado", "data")
        )
        def atualiza_dados_estudo(interval):
            return DB.le_resumo_estudo_encadeado()

        @self.__app.callback(
            Input("atualiza-dados-caso", "n_intervals"),
            Output("dados-caso-atual", "data")
        )
        def atualiza_dados_caso(interval):
            return DB.le_informacoes_proximo_caso()

        @self.__app.callback(
            Input("dados-caso-atual", "data"),
            Output("informacao-caso-atual", "children")
        )
        def gera_tabela(dados: pd.DataFrame):
            return App.gera_tabela(dados)

        @self.__app.callback(
            Input("dados-graficos", "data"),
            Input("escolhe-variavel", "value"),
            Output("grafico", "figure")
        )
        def gera_graficos(dados: pd.DataFrame, variavel: str):
            dados_locais = dados.copy()
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
        cfg = Configuracoes()
        self.__app.run_server(host="0.0.0.0",
                              port=str(cfg.porta_servidor),
                              debug=True)
