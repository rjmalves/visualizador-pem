import pandas as pd
import pathlib
import os
import asyncio
from datetime import timedelta
from src.utils.api import API
from typing import List
from datetime import timedelta
import src.utils.validation as validation
from src.utils.settings import Settings
from dash import ctx


def edit_current_study_data(
    add_study_button_clicks,
    edit_study_button_clicks,
    remove_study_button_clicks,
    new_study_id,
    new_study_label,
    edit_study_id,
    edit_study_path,
    edit_study_name,
    selected_study,
    current_studies,
    add_trigger,
    edit_trigger,
    remove_trigger,
):
    if ctx.triggered_id == add_trigger:
        if add_study_button_clicks:
            if not new_study_id:
                return current_studies
            elif len(new_study_id) == 0:
                return current_studies
            current_data = pd.read_json(current_studies, orient="split")
            if new_study_id in current_data["CAMINHO"].tolist():
                return current_studies
            else:
                current_ids = current_data["id"].to_list()
                last_id = 0 if len(current_ids) == 0 else int(current_ids[-1])
                if new_study_label is None:
                    label = pathlib.Path(new_study_id).parts[-1]
                else:
                    label = new_study_label
                new_data = pd.DataFrame(
                    data={
                        "id": [str(last_id + 1)],
                        "CAMINHO": [new_study_id],
                        "NOME": [label],
                    }
                )
                return pd.concat(
                    [current_data, new_data], ignore_index=True
                ).to_json(orient="split")
        else:
            return current_studies
    elif ctx.triggered_id == edit_trigger:
        if edit_study_button_clicks:
            current_data = pd.read_json(current_studies, orient="split")
            current_data.loc[
                current_data["id"] == edit_study_id, "CAMINHO"
            ] = edit_study_path
            current_data.loc[
                current_data["id"] == edit_study_id, "NOME"
            ] = edit_study_name
            return current_data.to_json(orient="split")
    elif ctx.triggered_id == remove_trigger:
        if remove_study_button_clicks:
            current_data = pd.read_json(current_studies, orient="split")
            new_data = current_data.loc[
                ~current_data["id"].isin(selected_study)
            ]
            return new_data.to_json(orient="split")
        else:
            return current_studies
    else:
        return current_studies


def extract_selected_study_data(
    selected_study,
    current_studies,
) -> dict:
    current_data = pd.read_json(current_studies, orient="split")
    if selected_study is None:
        return None
    elif len(selected_study) == 0:
        return None
    else:
        study_id = selected_study[0]
        return {
            "id": study_id,
            "CAMINHO": current_data.loc[
                current_data["id"] == study_id, "CAMINHO"
            ].tolist()[0],
            "NOME": current_data.loc[
                current_data["id"] == study_id, "NOME"
            ].tolist()[0],
        }


def get_statistics_scenarios(all_scenarios: List[str]) -> List[str]:
    scenarios = [
        s for s in all_scenarios if s in ["min", "max", "median", "mean"]
    ]
    scenarios = [s for s in scenarios if "p" in s]
    return scenarios


def get_non_statistics_scenarios(all_scenarios: List[str]) -> List[str]:
    scenarios = [
        s for s in all_scenarios if s not in ["min", "max", "median", "mean"]
    ]
    scenarios = [s for s in scenarios if "p" not in s]
    return scenarios


def strfdelta(tdelta: timedelta) -> str:
    days = tdelta.days
    hours, rem = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return (
        f"{str(days).zfill(2)}:{str(hours).zfill(2)}"
        + f":{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"
    )


def update_status_data_encadeador(interval, studies):
    if not studies:
        return None

    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["CAMINHO"].tolist()
    labels = studies_df["NOME"].tolist()
    study_df = asyncio.run(
        API.fetch_result_list(
            paths,
            labels,
            "ESTUDO",
            {"preprocess": "FULL"},
        )
    )
    cases_df = asyncio.run(
        API.fetch_result_list(
            paths,
            labels,
            "CASOS",
            {"preprocess": "FULL"},
        )
    )
    runs_df = asyncio.run(
        API.fetch_result_list(
            paths,
            labels,
            "RODADAS",
            {"preprocess": "FULL"},
        )
    )
    names = []
    times = []
    progress = []
    current = []
    status = []
    for label in labels:
        names.append(label)
        study_cases = cases_df.loc[cases_df["estudo"] == label]
        total_seconds = study_cases["tempo_execucao"].sum()
        times.append(strfdelta(timedelta(seconds=total_seconds)))
        n_total = study_cases.shape[0]
        n_concluidos = study_cases.loc[
            study_cases["estado"] == "CONCLUIDO"
        ].shape[0]
        progress.append(int(n_concluidos * 100 / n_total))
        current_data = study_cases.loc[study_cases["estado"] != "CONCLUIDO"]
        if current_data.shape[0] == 0:
            current_name = "-"
            current_status = "CONCLUIDO"
        else:
            program = current_data["programa"].tolist()[0]
            year = current_data["ano"].tolist()[0]
            month = current_data["mes"].tolist()[0]
            rv = current_data["revisao"].tolist()[0]
            stat = current_data["estado"].tolist()[0]
            current_name = f"{program} - {year}_{str(month).zfill(2)}_rv{rv}"
            current_status = stat
        current.append(current_name)
        status.append(current_status)

    status_df = pd.DataFrame(
        data={
            "NOME": names,
            "TEMPO DE EXECUCAO": times,
            "PROGRESSO (%)": progress,
            "CASO ATUAL": current,
            "ESTADO": status,
        }
    )
    return status_df.to_json(orient="split")


def update_operation_data_encadeador(
    interval, studies, filters: dict, variable: str
):
    if not studies:
        return None
    if not variable:
        return None
    req_filters = validation.validate_required_filters(variable, filters)
    if req_filters is None:
        return None
    fetch_filters = {**req_filters, "estagio": 1}
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["CAMINHO"].tolist()
    labels = studies_df["NOME"].tolist()
    complete_df = pd.DataFrame()
    newave_df = asyncio.run(
        API.fetch_result_list(
            [
                os.path.join(p, Settings.synthesis_dir, Settings.newave_dir)
                for p in paths
            ],
            labels,
            variable,
            fetch_filters,
        )
    )
    decomp_df = asyncio.run(
        API.fetch_result_list(
            [
                os.path.join(p, Settings.synthesis_dir, Settings.decomp_dir)
                for p in paths
            ],
            labels,
            variable,
            fetch_filters,
        )
    )
    if newave_df is not None:
        cols_newave = newave_df.columns.to_list()
        newave_df["programa"] = "NEWAVE"
        complete_df = pd.concat(
            [complete_df, newave_df[["programa"] + cols_newave]],
            ignore_index=True,
        )
    if decomp_df is not None:
        cols_decomp = decomp_df.columns.to_list()
        decomp_df["programa"] = "DECOMP"
        complete_df = pd.concat(
            [
                complete_df,
                decomp_df[["programa"] + cols_decomp],
            ],
            ignore_index=True,
        )
    if complete_df.empty:
        return None
    else:
        return complete_df.to_json(orient="split")


def update_operation_data_casos(
    interval,
    studies,
    filters: dict,
    variable: str,
    preprocess: str = "STATISTICS",
    needs_stage: bool = False,
):
    if not studies:
        return None
    if not variable:
        return None
    req_filters = validation.validate_required_filters(
        variable, filters, ppq=needs_stage
    )
    if req_filters is None:
        return None
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["CAMINHO"].tolist()
    labels = studies_df["NOME"].tolist()
    df = asyncio.run(
        API.fetch_result_list(
            paths,
            labels,
            variable,
            {**req_filters, "preprocess": preprocess},
        )
    )

    if df is None:
        return None
    if df.empty:
        return None
    else:
        return df.to_json(orient="split")


def update_custos_tempo_data_encadeador(
    interval,
    studies,
    filters: dict,
    variable: str,
):
    if not studies:
        return None
    if not variable:
        return None
    programa = filters.get("programa")
    if programa is None:
        return None
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["CAMINHO"].tolist()
    labels = studies_df["NOME"].tolist()
    dir = {"NEWAVE": Settings.newave_dir, "DECOMP": Settings.decomp_dir}.get(
        programa
    )
    df = asyncio.run(
        API.fetch_result_list(
            [os.path.join(p, Settings.synthesis_dir, dir) for p in paths],
            labels,
            variable,
            {},
        )
    )
    if df.empty:
        return None
    else:
        return df.to_json(orient="split")


def update_violation_data_encadeador(
    interval,
    studies,
    filters: dict,
    violation: str,
):
    if not studies:
        return None
    if not violation:
        return None
    programa = filters.get("programa")
    if programa is None:
        return None
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["CAMINHO"].tolist()
    labels = studies_df["NOME"].tolist()
    dir = {"NEWAVE": Settings.newave_dir, "DECOMP": Settings.decomp_dir}.get(
        programa
    )

    df = asyncio.run(
        API.fetch_result_list(
            [os.path.join(p, Settings.synthesis_dir, dir) for p in paths],
            labels,
            "INVIABILIDADES",
            {"iteracao": -1, "tipo": f"'{violation}'", "preprocess": "FULL"},
        )
    )
    if df is None:
        return None
    if df.empty:
        return None
    else:
        df = df[["estudo", "caso", "unidade", "violacao"]]
        return df.to_json(orient="split")


def update_custos_tempo_data_casos(
    interval,
    studies,
    variable: str,
):
    if not studies:
        return None
    if not variable:
        return None
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["CAMINHO"].tolist()
    labels = studies_df["NOME"].tolist()
    df = asyncio.run(
        API.fetch_result_list(
            paths,
            labels,
            variable,
            {},
        )
    )
    if df is None:
        return None
    if df.empty:
        return None
    else:
        return df.to_json(orient="split")


def update_runtime_data_casos(
    interval,
    studies,
):
    if not studies:
        return None
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["CAMINHO"].tolist()
    labels = studies_df["NOME"].tolist()
    df = asyncio.run(
        API.fetch_result_list(
            paths,
            labels,
            "TEMPO",
            {},
        )
    )
    if df is None:
        return None
    if df.empty:
        return None
    else:
        return df.to_json(orient="split")


def update_convergence_data_casos(
    interval,
    studies,
):
    if not studies:
        return None
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["CAMINHO"].tolist()
    labels = studies_df["NOME"].tolist()
    df = asyncio.run(
        API.fetch_result_list(
            paths,
            labels,
            "CONVERGENCIA",
            {},
        )
    )
    if df is None:
        return None
    if df.empty:
        return None
    else:
        return df.to_json(orient="split")


def update_job_resources_data_casos(
    interval,
    studies,
):
    if not studies:
        return None
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["CAMINHO"].tolist()
    labels = studies_df["NOME"].tolist()
    df_cluster = asyncio.run(
        API.fetch_result_list(
            paths,
            labels,
            "RECURSOS_JOB",
            {},
        )
    )
    if df_cluster is None:
        return None
    if df_cluster.empty:
        return None

    else:
        return df_cluster.to_json(orient="split")


def update_cluster_resources_data_casos(
    interval,
    studies,
):
    if not studies:
        return None
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["CAMINHO"].tolist()
    labels = studies_df["NOME"].tolist()
    df_job = asyncio.run(
        API.fetch_result_list(
            paths,
            labels,
            "RECURSOS_CLUSTER",
            {},
        )
    )
    if df_job is None:
        return None
    if df_job.empty:
        return None
    else:
        return df_job.to_json(orient="split")


def update_operation_data_ppq(interval, studies, filters: dict, variable: str):
    if not studies:
        return None
    if not variable:
        return None
    req_filters = validation.validate_required_filters(
        variable, filters, ppq=True
    )
    if req_filters is None:
        return None
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["CAMINHO"].tolist()
    labels = studies_df["NOME"].tolist()
    df = asyncio.run(
        API.fetch_result_list(
            paths,
            labels,
            variable,
            {**req_filters, "preprocess": "STATISTICS"},
        )
    )
    if df is None:
        return None
    if df.empty:
        return None
    else:
        return df.to_json(orient="split")
