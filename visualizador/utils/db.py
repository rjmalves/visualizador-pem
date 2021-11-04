import pandas as pd
import numpy as np
from os import sep
from os.path import join, normpath
from datetime import timedelta

from visualizador.modelos.configuracoes import Configuracoes
from visualizador.modelos.log import Log

ARQUIVO_RESUMO_PROXIMO_CASO = "proximo_caso.csv"
ARQUIVO_RESUMO_ESTUDO_ENCADEADO = "estudo_encadeado.csv"
ARQUIVO_RESUMO_NEWAVES = "newaves_encadeados.csv"
ARQUIVO_RESUMO_DECOMPS = "decomps_encadeados.csv"
ARQUIVO_CONVERGENCIA_NEWAVES = "convergencia_newaves.csv"
ARQUIVO_CONVERGENCIA_DECOMPS = "convergencia_decomps.csv"
ARQUIVO_INVIABS_DECOMPS = "inviabilidades_decomps.csv"


class DB:

    def __init__(self) -> None:
        pass

    @staticmethod
    def le_informacoes_proximo_caso() -> pd.DataFrame:

        def resume_flexibilizacoes(df: pd.DataFrame) -> pd.DataFrame:
            tempos_fila = df["Inicio Execucao"] - df["Entrada Fila"]
            tempo_total_fila = str(timedelta(seconds=np.sum(tempos_fila.to_numpy())))
            tempos_execucao = df["Fim Execucao"] - df["Inicio Execucao"]
            tempos_execucao = np.clip(tempos_execucao, 0, 1e12)
            tempo_total_exec = str(timedelta(seconds=np.sum(tempos_execucao)))
            num_flex = df.shape[0] - 1
            indices = list(df.index)
            indices.pop()
            df_resumido = df.drop(index=indices)
            colunas_a_remover = ["Tentativas",
                                 "Processadores",
                                 "Entrada Fila",
                                 "Inicio Execucao",
                                 "Fim Execucao"]
            df_resumido = df_resumido.drop(columns=colunas_a_remover)
            df_resumido["Tempo Total Fila"] = tempo_total_fila
            df_resumido["Tempo Total Execucao"] = tempo_total_exec
            df_resumido["Numero Flexibilizacoes"] = num_flex
            return df_resumido


        cfg = Configuracoes()
        log = Log().log()
        # Descobre o caminho dos próximos casos
        arqs_proximos = [join(c, ARQUIVO_RESUMO_PROXIMO_CASO)
                         for c in cfg.caminhos_casos]
        df_casos = pd.DataFrame()
        log.info("Lendo informações dos casos atuais")
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
            df_caso = resume_flexibilizacoes(df_caso)
            if df_casos.empty:
                df_casos = df_caso
            else:
                df_casos = pd.concat([df_casos, df_caso],
                                     ignore_index=True)
        return df_casos.to_json(orient="split")

    @staticmethod
    def le_resumo_estudo_encadeado() -> pd.DataFrame:
        cfg = Configuracoes()
        log = Log().log()
        # Descobre o caminho dos arquivos de estudo
        arqs_resumo = [join(c, ARQUIVO_RESUMO_ESTUDO_ENCADEADO)
                       for c in cfg.caminhos_casos]
        df_resumos = pd.DataFrame()
        log.info("Lendo informações do estudo encadeado")
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
        return df_resumos.to_json(orient="split")

    @staticmethod
    def le_resumo_newaves() -> pd.DataFrame:
        cfg = Configuracoes()
        log = Log().log()
        # Descobre o caminho dos arquivos de estudo
        arqs_resumo = [join(c, ARQUIVO_RESUMO_NEWAVES)
                       for c in cfg.caminhos_casos]
        df_resumos = pd.DataFrame()
        log.info("Lendo informações dos NEWAVEs")
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
        df_resumos["TOTAL"] = df_resumos.sum(axis=1,
                                             numeric_only=True)
        return df_resumos.to_json(orient="split")

    @staticmethod
    def le_resumo_decomps() -> pd.DataFrame:
        cfg = Configuracoes()
        log = Log().log()
        # Descobre o caminho dos arquivos de estudo
        arqs_resumo = [join(c, ARQUIVO_RESUMO_DECOMPS)
                       for c in cfg.caminhos_casos]
        df_resumos = pd.DataFrame()
        log.info("Lendo informações dos DECOMPs")
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
        return df_resumos.to_json(orient="split")
