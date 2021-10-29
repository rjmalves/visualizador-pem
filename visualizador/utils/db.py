import pandas as pd
from os import sep
from os.path import join, normpath

from visualizador.modelos.configuracoes import Configuracoes
from visualizador.modelos.log import Log

ARQUIVO_RESUMO_PROXIMO_CASO = "proximo_caso.csv"
ARQUIVO_RESUMO_ESTUDO_ENCADEADO = "estudo_encadeado.csv"
ARQUIVO_RESUMO_NEWAVES = "newaves_encadeados.csv"
ARQUIVO_RESUMO_DECOMPS = "decomps_encadeados.csv"


class DB:

    def __init__(self) -> None:
        pass

    @staticmethod
    def le_informacoes_proximo_caso() -> pd.DataFrame:
        cfg = Configuracoes()
        # Descobre o caminho dos próximos casos
        arqs_proximos = [join(c, ARQUIVO_RESUMO_PROXIMO_CASO)
                         for c in cfg.caminhos_casos]
        df_casos = pd.DataFrame()
        for a in arqs_proximos:
            # Lê o caminho
            df = pd.read_csv(a, index_col=0)
            caminho = df["Caminho"].tolist()[0]
            # Lê o resumo do caso
            df_caso = pd.read_csv(caminho, index_col=0)
            # Gera um identificador para o caso
            identificador_caso = normpath(a).split(sep)[-2]
            colunas_atuais = list(df_caso.columns)
            df_caso["Estudo"] = identificador_caso
            df_caso = df_caso[["Estudo"] + colunas_atuais]
            if df_casos.empty:
                df_casos = df_caso
            else:
                df_casos = pd.concat([df_casos, df_caso],
                                     ignore_index=True)
        return df_casos

    @staticmethod
    def le_resumo_estudo_encadeado() -> pd.DataFrame:
        cfg = Configuracoes()
        # Descobre o caminho dos arquivos de estudo
        arqs_resumo = [join(c, ARQUIVO_RESUMO_ESTUDO_ENCADEADO)
                       for c in cfg.caminhos_casos]
        df_resumos = pd.DataFrame()
        for a in arqs_resumo:
            # Lê o resumo do estudo
            df = pd.read_csv(a, index_col=0)
            identificador_caso = normpath(a).split(sep)[-2]
            colunas_atuais = list(df.columns)
            df["Estudo"] = identificador_caso
            df = df[["Estudo"] + colunas_atuais]
            if df_resumos.empty:
                df_resumos = df
            else:
                df_resumos = pd.concat([df_resumos, df],
                                       ignore_index=True)
        return df_resumos

    @staticmethod
    def le_resumo_newaves() -> pd.DataFrame:
        cfg = Configuracoes()
        # Descobre o caminho dos arquivos de estudo
        arqs_resumo = [join(c, ARQUIVO_RESUMO_NEWAVES)
                       for c in cfg.caminhos_casos]
        df_resumos = pd.DataFrame()
        for a in arqs_resumo:
            # Lê o resumo do estudo
            df = pd.read_csv(a, index_col=0)
            identificador_caso = normpath(a).split(sep)[-2]
            colunas_atuais = list(df.columns)
            df["Estudo"] = identificador_caso
            df = df[["Estudo"] + colunas_atuais]
            if df_resumos.empty:
                df_resumos = df
            else:
                df_resumos = pd.concat([df_resumos, df],
                                       ignore_index=True)
        return df_resumos

    @staticmethod
    def le_resumo_decomps() -> pd.DataFrame:
        cfg = Configuracoes()
        # Descobre o caminho dos arquivos de estudo
        arqs_resumo = [join(c, ARQUIVO_RESUMO_DECOMPS)
                       for c in cfg.caminhos_casos]
        df_resumos = pd.DataFrame()
        for a in arqs_resumo:
            # Lê o resumo do estudo
            df = pd.read_csv(a, index_col=0)
            identificador_caso = normpath(a).split(sep)[-2]
            colunas_atuais = list(df.columns)
            df["Estudo"] = identificador_caso
            df = df[["Estudo"] + colunas_atuais]
            if df_resumos.empty:
                df_resumos = df
            else:
                df_resumos = pd.concat([df_resumos, df],
                                       ignore_index=True)
        return df_resumos
