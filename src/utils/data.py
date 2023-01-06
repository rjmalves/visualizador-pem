import pandas as pd
import pathlib
import os
import asyncio
from src.utils.api import API
from typing import List
from datetime import timedelta
import src.utils.validation as validation
from src.utils.settings import Settings
from dash import ctx


def edit_current_study_data(
    add_study_button_clicks,
    remove_study_button_clicks,
    new_study_id,
    new_study_label,
    selected_study,
    current_studies,
    add_trigger,
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
