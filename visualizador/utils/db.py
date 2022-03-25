import pandas as pd
import numpy as np
import time
import json
from datetime import datetime, timedelta
import calendar as cal
from os import sep, stat
from os.path import join, normpath

from visualizador.modelos.configuracoes import Configuracoes
from visualizador.modelos.log import Log

ARQUIVO_RESUMO_PROXIMO_CASO = "proximo_caso.json"
ARQUIVO_RESUMO_ESTUDO_ENCADEADO = "estudo_encadeado.json"
ARQUIVO_RESUMO_NEWAVES = "newaves_encadeados.csv"
ARQUIVO_RESUMO_DECOMPS = "decomps_encadeados.csv"
ARQUIVO_RESUMO_RESERVATORIOS = "reservatorios_encadeados.csv"
ARQUIVO_CONVERGENCIA_NEWAVES = "convergencia_newaves.csv"
ARQUIVO_CONVERGENCIA_DECOMPS = "convergencia_decomps.csv"
ARQUIVO_INVIABS_DECOMPS = "inviabilidades_decomps.csv"
ARQUIVO_INVIABS_DECOMPS_RESUMIDAS = "inviabilidades_decomps_resumidas.csv"

MAX_RETRY = 5
INTERVALO_RETRY = 0.1


class DB:
    def __init__(self) -> None:
        pass

    @staticmethod
    def le_json_com_retry(arq: str) -> dict:
        num_retry = 0
        while num_retry < MAX_RETRY:
            try:
                with open(arq, "r") as f:
                    dados = json.load(f)
                return dados
            except OSError:
                num_retry += 1
                time.sleep(INTERVALO_RETRY)
                continue
            except BlockingIOError:
                num_retry += 1
                time.sleep(INTERVALO_RETRY)
                continue
        return {}

    @staticmethod
    def le_com_retry(arq: str) -> pd.DataFrame:
        num_retry = 0
        while num_retry < MAX_RETRY:
            try:
                df = pd.read_csv(arq, index_col=0)
                return df
            except OSError:
                num_retry += 1
                time.sleep(INTERVALO_RETRY)
                continue
            except BlockingIOError:
                num_retry += 1
                time.sleep(INTERVALO_RETRY)
                continue
        return pd.DataFrame()

    @staticmethod
    def escreve_com_retry(df: pd.DataFrame, arq: str):
        num_retry = 0
        while num_retry < MAX_RETRY:
            try:
                df = df.to_csv(arq)
                return
            except OSError:
                num_retry += 1
                time.sleep(INTERVALO_RETRY)
                continue
            except BlockingIOError:
                num_retry += 1
                time.sleep(INTERVALO_RETRY)
                continue

    @staticmethod
    def le_informacoes_proximo_caso() -> pd.DataFrame:
        def f(x: timedelta):
            if not isinstance(x, timedelta):
                return ""
            ts = x.total_seconds()
            days, remainder = divmod(ts, 24 * 3600)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{int(hours)}:{int(minutes):02d}:{int(seconds):02d}"

        def resume_flexibilizacoes(df: pd.DataFrame) -> pd.DataFrame:
            esp = df["Estado"] == "ESPERANDO"
            exe = df["Estado"] == "EXECUTANDO"
            err = df["Estado"] == "ERRO"
            con = df["Estado"] == "CONCLUIDO"
            df.loc[esp, "Tempo Fila"] = (
                time.time() - df.loc[esp, "Entrada Fila"]
            )
            df.loc[exe, "Tempo Fila"] = (
                df.loc[exe, "Inicio Execucao"] - df.loc[exe, "Entrada Fila"]
            )
            df.loc[con, "Tempo Fila"] = (
                df.loc[con, "Inicio Execucao"] - df.loc[con, "Entrada Fila"]
            )
            df.loc[err, "Tempo Fila"] = np.nan
            df.loc[esp, "Tempo Execucao"] = np.nan
            df.loc[exe, "Tempo Execucao"] = (
                time.time() - df.loc[exe, "Inicio Execucao"]
            )
            df.loc[con, "Tempo Execucao"] = (
                df.loc[con, "Fim Execucao"] - df.loc[con, "Inicio Execucao"]
            )
            df.loc[err, "Tempo Execucao"] = np.nan
            indices = list(df.index)
            indices.pop()
            dfr = df.drop(index=indices)
            colunas_a_remover = [
                "Caminho",
                "Nome",
                "Tentativas",
                "Processadores",
                "Entrada Fila",
                "Inicio Execucao",
                "Fim Execucao",
            ]
            dfr = dfr.drop(columns=colunas_a_remover)
            num_flex = df.shape[0] - 1
            dfr["Numero Flexibilizacoes"] = num_flex
            dfr["Tempo Fila"] = pd.to_timedelta(dfr["Tempo Fila"], unit="sec")
            dfr["Tempo Execucao"] = pd.to_timedelta(
                dfr["Tempo Execucao"], unit="sec"
            )
            dfr["Tempo Fila"] = dfr["Tempo Fila"].apply(f)
            dfr["Tempo Execucao"] = dfr["Tempo Execucao"].apply(f)
            return dfr

        cfg = Configuracoes()
        log = Log().log()
        # Descobre o caminho dos próximos casos
        arqs_proximos = [
            join(c, ARQUIVO_RESUMO_PROXIMO_CASO) for c in cfg.caminhos_casos
        ]
        df_casos = pd.DataFrame()
        log.info("Lendo informações dos casos atuais")
        for a in arqs_proximos:
            # Lê o caminho
            caminho = DB.le_json_com_retry(a)["Caminho"]
            # Lê o resumo do caso
            dados_caso = DB.le_json_com_retry(caminho)
            n_jobs = len(dados_caso["_jobs"])
            df_caso = pd.DataFrame(
                data={
                    "Programa": [dados_caso["_dados"]["_programa"]] * n_jobs,
                    "Caminho": [dados_caso["_dados"]["_caminho"]] * n_jobs,
                    "Nome": [dados_caso["_dados"]["_nome"]] * n_jobs,
                    "Ano": [dados_caso["_dados"]["_ano"]] * n_jobs,
                    "Mes": [dados_caso["_dados"]["_mes"]] * n_jobs,
                    "Revisao": [dados_caso["_dados"]["_revisao"]] * n_jobs,
                    "Estado": [d["_estado"] for d in dados_caso["_jobs"]],
                    "Tentativas": list(range(n_jobs)),
                    "Processadores": [
                        d["_dados"]["_numero_processadores"]
                        for d in dados_caso["_jobs"]
                    ],
                    "Entrada Fila": [
                        d["_dados"]["_instante_entrada_fila"]
                        for d in dados_caso["_jobs"]
                    ],
                    "Inicio Execucao": [
                        d["_dados"]["_instante_inicio_execucao"]
                        for d in dados_caso["_jobs"]
                    ],
                    "Fim Execucao": [
                        d["_dados"]["_instante_saida_fila"]
                        for d in dados_caso["_jobs"]
                    ],
                }
            )
            # Gera um identificador para o caso
            identificador_caso = normpath(a).split(sep)[-2]
            colunas_atuais = list(df_caso.columns)
            df_caso["Estudo"] = identificador_caso
            df_caso = df_caso[["Estudo"] + colunas_atuais]
            df_caso = resume_flexibilizacoes(df_caso)
            if df_casos.empty:
                df_casos = df_caso
            else:
                df_casos = pd.concat([df_casos, df_caso], ignore_index=True)
        return df_casos.to_json(orient="split")

    @staticmethod
    def le_resumo_estudo_encadeado() -> pd.DataFrame:
        def f_caso(caminho: str):
            return caminho.split(sep)[-2]

        def formata_tempos(df: pd.DataFrame) -> pd.DataFrame:
            # Converte para minutos
            df["Tempo Fila (min)"] = df["Tempo Fila (min)"] / 60
            df["Tempo Execucao (min)"] = df["Tempo Execucao (min)"] / 60
            return df

        cfg = Configuracoes()
        log = Log().log()
        # Descobre o caminho dos arquivos de estudo
        arqs_resumo = [
            join(c, ARQUIVO_RESUMO_ESTUDO_ENCADEADO)
            for c in cfg.caminhos_casos
        ]
        df_resumos = pd.DataFrame()
        log.info("Lendo informações do estudo encadeado")
        for a in arqs_resumo:
            # Lê o resumo do estudo
            dados_estudo = DB.le_json_com_retry(a)
            diretorios_casos = [
                normpath(p)
                for p in dados_estudo["_dados"]["_diretorios_casos"]
            ]
            pastas_casos = [f_caso(c) for c in diretorios_casos]
            df = pd.DataFrame(
                data={
                    "Programa": [
                        d.split(sep)[-1].upper() for d in diretorios_casos
                    ],
                    "Caminho": diretorios_casos,
                    "Nome": dados_estudo["_dados"]["_nomes_casos"],
                    "Ano": [int(p.split("_")[0]) for p in pastas_casos],
                    "Mes": [int(p.split("_")[1]) for p in pastas_casos],
                    "Revisao": [
                        int(p.split("_")[2].split("rv")[1])
                        for p in pastas_casos
                    ],
                    "Sucesso": [
                        e == "CONCLUIDO"
                        for e in dados_estudo["_dados"]["_estados_casos"]
                    ],
                    "Estado": dados_estudo["_dados"]["_estados_casos"],
                    "Tempo Fila (min)": dados_estudo["_dados"]["_tempos_fila_casos"],
                    "Tempo Execucao (min)": dados_estudo["_dados"][
                        "_tempos_execucao_casos"
                    ],
                }
            )
            df = formata_tempos(df)
            identificador_caso = normpath(a).split(sep)[-2]
            casos = df["Caminho"].apply(f_caso)
            colunas_a_remover = ["Caminho", "Nome"]
            df = df.drop(columns=colunas_a_remover)
            colunas_atuais = list(df.columns)
            df["Caso"] = casos
            df["Estudo"] = identificador_caso
            df = df[["Estudo", "Caso"] + colunas_atuais]
            if df_resumos.empty:
                df_resumos = df
            else:
                df_resumos = pd.concat([df_resumos, df], ignore_index=True)
        return df_resumos.to_json(orient="split")

    @staticmethod
    def le_resumo_newaves() -> pd.DataFrame:
        cfg = Configuracoes()
        log = Log().log()
        # Descobre o caminho dos arquivos de estudo
        arqs_resumo = [
            join(c, ARQUIVO_RESUMO_NEWAVES) for c in cfg.caminhos_casos
        ]
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
                df_resumos = pd.concat([df_resumos, df], ignore_index=True)
        df_resumos["TOTAL"] = df_resumos.sum(axis=1, numeric_only=True)
        return df_resumos.to_json(orient="split")

    @staticmethod
    def le_resumo_decomps() -> pd.DataFrame:
        cfg = Configuracoes()
        log = Log().log()
        # Descobre o caminho dos arquivos de estudo
        arqs_resumo = [
            join(c, ARQUIVO_RESUMO_DECOMPS) for c in cfg.caminhos_casos
        ]
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
                df_resumos = pd.concat([df_resumos, df], ignore_index=True)
        return df_resumos.to_json(orient="split")

    @staticmethod
    def le_resumo_reservatorios() -> pd.DataFrame:
        cfg = Configuracoes()
        log = Log().log()

        def extrai_semana_operativa(linha):
            ano = int(linha["Ano"])
            mes = int(linha["Mes"])
            rv = linha["Revisao"]
            estagio = linha["Estagio"]
            if estagio == "Inicial":
                delta_estagio = 0
            else:
                delta_estagio = int(estagio.split(" ")[1])
            n_rv = int(rv.split("rv")[1])
            mes_anterior = 12 if mes == 1 else mes - 1
            ano_anterior = ano - 1 if mes_anterior == 12 else ano
            cal_mes_anterior = cal.monthcalendar(ano_anterior, mes_anterior)
            ultimo_sabado_mes_anterior = 0
            for i in range(len(cal_mes_anterior) - 1, -1, -1):
                sabado = cal_mes_anterior[i][5]
                if sabado != 0:
                    ultimo_sabado_mes_anterior = sabado
                    break
            inic_ult_semana_operativa_mes_anterior = datetime(
                year=ano_anterior,
                month=mes_anterior,
                day=ultimo_sabado_mes_anterior,
            )
            fim_ult_semana_operativa_mes_anterior = (
                inic_ult_semana_operativa_mes_anterior + timedelta(days=6)
            )
            defasagem = timedelta(days=0)
            if fim_ult_semana_operativa_mes_anterior.month == mes:
                defasagem = timedelta(weeks=1)
            # Se, no mês passado, a última semana operativa tinha
            # dias do mês vigente, aplica uma defasagem de 1 semana,
            # pois a rv0 começa a contar a partir da "última semana civil"
            # do mês anterior.
            data = (
                fim_ult_semana_operativa_mes_anterior
                + timedelta(days=1)
                + timedelta(weeks=n_rv)
                - defasagem
            )
            return data + timedelta(weeks=delta_estagio)

        # Descobre o caminho dos arquivos de estudo
        arqs_resumo = [
            join(c, ARQUIVO_RESUMO_RESERVATORIOS) for c in cfg.caminhos_casos
        ]
        df_resumos = pd.DataFrame()
        log.info("Lendo informações dos Reservatórios")
        for a in arqs_resumo:
            # Lê o resumo do estudo
            df = DB.le_com_retry(a)
            colunas_atuais = [c for c in list(df.columns) if c != "Caso"]
            df[["Ano", "Mes", "Revisao"]] = df["Caso"].str.split(
                "_", expand=True
            )
            df["Data"] = df.apply(extrai_semana_operativa, axis=1)
            identificador_caso = normpath(a).split(sep)[-2]
            df["Estudo"] = identificador_caso
            df = df[
                ["Estudo", "Caso", "Ano", "Mes", "Revisao", "Data"]
                + colunas_atuais
            ]
            if df_resumos.empty:
                df_resumos = df
            else:
                df_resumos = pd.concat([df_resumos, df], ignore_index=True)
        df_resumos["Data"] = df_resumos["Data"].dt.strftime("%Y-%m-%d")
        return df_resumos.to_json(orient="split")

    @staticmethod
    def le_inviabilidades_decomps() -> pd.DataFrame:
        cfg = Configuracoes()
        log = Log().log()
        # Descobre o caminho dos arquivos de estudo
        arqs_resumo = [
            join(c, ARQUIVO_INVIABS_DECOMPS_RESUMIDAS)
            for c in cfg.caminhos_casos
        ]
        df_resumos = pd.DataFrame()
        log.info("Lendo informações de inviabilidades do DECOMP")
        for a in arqs_resumo:
            # Lê o resumo do estudo
            df = DB.le_com_retry(a)
            if df_resumos.empty:
                df_resumos = df
            else:
                df_resumos = pd.concat([df_resumos, df], ignore_index=True)

        return df_resumos.to_json(orient="split")

    @staticmethod
    def resume_inviabilidades_decomps() -> pd.DataFrame:
        def f(x: str) -> str:
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

        cfg = Configuracoes()
        log = Log().log()
        # Descobre o caminho dos arquivos de estudo
        arqs_resumo = [
            join(c, ARQUIVO_INVIABS_DECOMPS) for c in cfg.caminhos_casos
        ]
        arqs_inviabs_resumidas = [
            join(c, ARQUIVO_INVIABS_DECOMPS_RESUMIDAS)
            for c in cfg.caminhos_casos
        ]
        log.info("Resumindo informações de inviabilidades do DECOMP")
        for a, ar in zip(arqs_resumo, arqs_inviabs_resumidas):
            log.info(f"Resumindo inviabilidades do caso em {a}")
            # Lê o resumo do estudo
            df = DB.le_com_retry(a)
            identificador_caso = normpath(a).split(sep)[-2]
            colunas_atuais = list(df.columns)
            df["Estudo"] = identificador_caso
            df = df[["Estudo"] + colunas_atuais]
            df["Tipo"] = df["Restricao"].apply(f)
            df = df.groupby(["Estudo", "Caso", "Tipo"]).count().reset_index()
            df = df.rename(columns={"Violacao": "Num. Violacoes"})
            DB.escreve_com_retry(df, ar)
        log.info("Fim do resumo das inviabilidades do DECOMP")
