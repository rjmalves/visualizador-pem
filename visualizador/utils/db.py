import pandas as pd
import numpy as np
import time
from os import sep, stat
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

MAX_RETRY = 3
INTERVALO_RETRY = 0.1


class DB:

    def __init__(self) -> None:
        pass

    @staticmethod
    def le_com_retry(arq: str) -> pd.DataFrame:
        num_retry = 0
        while num_retry < MAX_RETRY:
            try:
                df = pd.read_csv(arq,
                                 index_col = 0)
                return df
            except OSError:
                num_retry += 1
                time.sleep(INTERVALO_RETRY)
                continue
            except BlockingIOError:
                num_retry += 1
                time.sleep(INTERVALO_RETRY)
                continue
        raise RuntimeError(f"Erro na leitura do arquivo: {arq}")

    @staticmethod
    def le_informacoes_proximo_caso() -> pd.DataFrame:

        def f(x: timedelta):
            ts = x.total_seconds()
            days, remainder = divmod(ts, 24 * 3600)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f'{int(hours)}:{int(minutes):02d}:{int(seconds):02d}'

        def resume_flexibilizacoes(df: pd.DataFrame) -> pd.DataFrame:
            esp = df["Estado"] == "ESPERANDO"
            exe = df["Estado"] == "EXECUTANDO"
            err = df["Estado"] == "ERRO"
            con = df["Estado"] == "CONCLUIDO"
            df.loc[esp, "Tempo Fila"] = (time.time() -
                                               df.loc[esp, "Entrada Fila"])
            df.loc[exe, "Tempo Fila"] = (df.loc[exe, "Inicio Execucao"] -
                                               df.loc[exe, "Entrada Fila"])
            df.loc[con, "Tempo Fila"] = (df.loc[con, "Inicio Execucao"] -
                                               df.loc[con, "Entrada Fila"])
            df.loc[err, "Tempo Fila"] = np.nan
            df.loc[esp, "Tempo Execucao"] = np.nan
            df.loc[exe, "Tempo Execucao"] = (time.time() -
                                                   df.loc[exe, "Inicio Execucao"])
            df.loc[con, "Tempo Execucao"] = (df.loc[con, "Fim Execucao"] -
                                                   df.loc[con, "Inicio Execucao"])
            df.loc[err, "Tempo Execucao"] = np.nan
            indices = list(df.index)
            indices.pop()
            dfr = df.drop(index=indices)
            colunas_a_remover = ["Caminho",
                                 "Nome",
                                 "Tentativas",
                                 "Processadores",
                                 "Entrada Fila",
                                 "Inicio Execucao",
                                 "Fim Execucao"]
            dfr = dfr.drop(columns=colunas_a_remover)
            num_flex = df.shape[0] - 1
            dfr["Numero Flexibilizacoes"] = num_flex
            dfr["Tempo Fila"] = pd.to_timedelta(dfr["Tempo Fila"],
                                                unit="sec")
            dfr["Tempo Execucao"] = pd.to_timedelta(dfr["Tempo Execucao"],
                                                    unit="sec")
            dfr["Tempo Fila"] = dfr["Tempo Fila"].apply(f)
            dfr["Tempo Execucao"] = dfr["Tempo Execucao"].apply(f)
            return dfr


        cfg = Configuracoes()
        log = Log().log()
        # Descobre o caminho dos próximos casos
        arqs_proximos = [join(c, ARQUIVO_RESUMO_PROXIMO_CASO)
                         for c in cfg.caminhos_casos]
        df_casos = pd.DataFrame()
        log.info("Lendo informações dos casos atuais")
        for a in arqs_proximos:
            # Lê o caminho
            df = DB.le_com_retry(a)
            caminho = df["Caminho"].tolist()[0]
            # Lê o resumo do caso
            df_caso = DB.le_com_retry(caminho)
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

        def f_caso(caminho: str):
            return caminho.split("/")[-2]

        def formata_tempos(df: pd.DataFrame) -> pd.DataFrame:
            esp = df["Estado"] == "ESPERANDO"
            exe = df["Estado"] == "EXECUTANDO"
            err = df["Estado"] == "ERRO"
            con = df["Estado"] == "CONCLUIDO"
            df.loc[esp, "Tempo Fila (min)"] = (time.time() -
                                               df.loc[esp, "Entrada Fila"])
            df.loc[exe, "Tempo Fila (min)"] = (df.loc[exe, "Inicio Execucao"] -
                                               df.loc[exe, "Entrada Fila"])
            df.loc[con, "Tempo Fila (min)"] = (df.loc[con, "Inicio Execucao"] -
                                               df.loc[con, "Entrada Fila"])
            df.loc[err, "Tempo Fila (min)"] = np.nan
            df.loc[esp, "Tempo Execucao (min)"] = np.nan
            df.loc[exe, "Tempo Execucao (min)"] = (time.time() -
                                                   df.loc[exe, "Inicio Execucao"])
            df.loc[con, "Tempo Execucao (min)"] = (df.loc[con, "Fim Execucao"] -
                                                   df.loc[con, "Inicio Execucao"])
            df.loc[err, "Tempo Execucao (min)"] = np.nan
            # Converte para minutos
            df["Tempo Fila (min)"] = df["Tempo Fila (min)"] / 60
            df["Tempo Execucao (min)"] = df["Tempo Execucao (min)"] / 60
            return df

        cfg = Configuracoes()
        log = Log().log()
        # Descobre o caminho dos arquivos de estudo
        arqs_resumo = [join(c, ARQUIVO_RESUMO_ESTUDO_ENCADEADO)
                       for c in cfg.caminhos_casos]
        df_resumos = pd.DataFrame()
        log.info("Lendo informações do estudo encadeado")
        for a in arqs_resumo:
            # Lê o resumo do estudo
            df = DB.le_com_retry(a)
            df = formata_tempos(df)
            identificador_caso = normpath(a).split(sep)[-2]
            casos = df["Caminho"].apply(f_caso)
            colunas_a_remover = ["Caminho",
                                 "Nome",
                                 "Tentativas",
                                 "Processadores",
                                 "Entrada Fila",
                                 "Inicio Execucao",
                                 "Fim Execucao"]
            df = df.drop(columns=colunas_a_remover)
            colunas_atuais = list(df.columns)
            df["Caso"] = casos
            df["Estudo"] = identificador_caso
            df = df[["Estudo", "Caso"] + colunas_atuais]
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
            df = DB.le_com_retry(a)
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
            df = DB.le_com_retry(a)
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
    def le_inviabilidades_decomps() -> pd.DataFrame:
        cfg = Configuracoes()
        log = Log().log()
        # Descobre o caminho dos arquivos de estudo
        arqs_resumo = [join(c, ARQUIVO_INVIABS_DECOMPS)
                       for c in cfg.caminhos_casos]
        df_resumos = pd.DataFrame()
        log.info("Lendo informações de inviabilidades do DECOMP")
        for a in arqs_resumo:
            # Lê o resumo do estudo
            df = DB.le_com_retry(a)
            identificador_caso = normpath(a).split(sep)[-2]
            colunas_atuais = list(df.columns)
            df["Estudo"] = identificador_caso
            df = df[["Estudo"] + colunas_atuais]
            if df_resumos.empty:
                df_resumos = df
            else:
                df_resumos = pd.concat([df_resumos, df],
                                       ignore_index=True)

        def f(x: str):
            if "RESTRICAO ELETRICA" in x:
                return "RE"
            elif "RHQ" in x:
                return "RHQ"
            elif "IRRIGACAO" in x:
                return "TI"
            elif "RHV" in x:
                return "RHV"
            elif "RHE" in x:
                return "RHE"
            elif "EVAPORACAO" in x:
                return "EV"
            elif "DEF. MINIMA" in x:
                return "DEFMIN"
            elif "FUNCAO DE PRODUCAO" in x:
                return "FP"
            elif "DEFICIT" in x:
                return "DEFICIT"
            else:
                return "OUTRO"
    
        df_resumos["Tipo"] = df_resumos["Restricao"].apply(f)
        return df_resumos.to_json(orient="split")
