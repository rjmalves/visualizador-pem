import pandas as pd
import os
import asyncio
from src.utils.api import API
from typing import List
from datetime import timedelta
import src.utils.validation as validation
from dash import ctx


def edit_current_study_data(
    add_study_button_clicks,
    remove_study_button_clicks,
    new_study_id,
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
                new_data = pd.DataFrame(
                    data={
                        "id": [str(last_id + 1)],
                        "CAMINHO": [new_study_id],
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
    complete_df = pd.DataFrame()
    newave_df = asyncio.run(
        API.fetch_result_list(
            [os.path.join(p, "NEWAVE") for p in paths],
            variable,
            fetch_filters,
            path_part_to_name_study=-2,
        )
    )
    decomp_df = asyncio.run(
        API.fetch_result_list(
            [os.path.join(p, "DECOMP") for p in paths],
            variable,
            fetch_filters,
            path_part_to_name_study=-2,
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
    df = asyncio.run(
        API.fetch_result_list(
            paths,
            variable,
            {**req_filters, "preprocess": preprocess},
            path_part_to_name_study=-1,
        )
    )

    if df is None:
        return None
    if df.empty:
        return None
    else:
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
    df = asyncio.run(
        API.fetch_result_list(
            paths,
            variable,
            {},
            path_part_to_name_study=-1,
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
    df = asyncio.run(
        API.fetch_result_list(
            paths,
            "TEMPO",
            {},
            path_part_to_name_study=-1,
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
    df = asyncio.run(
        API.fetch_result_list(
            paths,
            "CONVERGENCIA",
            {},
            path_part_to_name_study=-1,
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
    df_cluster = asyncio.run(
        API.fetch_result_list(
            paths,
            "RECURSOS_JOB",
            {},
            path_part_to_name_study=-1,
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
    df_job = asyncio.run(
        API.fetch_result_list(
            paths,
            "RECURSOS_CLUSTER",
            {},
            path_part_to_name_study=-1,
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
    df = asyncio.run(
        API.fetch_result_list(
            paths,
            variable,
            {**req_filters, "preprocess": "STATISTICS"},
            path_part_to_name_study=-1,
        )
    )
    if df is None:
        return None
    if df.empty:
        return None
    else:
        return df.to_json(orient="split")
