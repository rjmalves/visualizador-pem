import pandas as pd
import os
import asyncio
import pathlib
from src.utils.settings import Settings
from src.utils.api import API


COSTS_TIME_FILES = [
    "CUSTOS",
    "TEMPO",
]

NOT_OPERATION_FILES = [
    "CUSTOS",
    "TEMPO",
    "CONVERGENCIA",
    "PROBABILIDADES",
    "INVIABILIDADES",
    "RECURSOS_CLUSTER",
    "RECURSOS_JOB",
    "PROGRAMA",
]


def update_operation_variables_dropdown_options_encadeador(
    interval, studies_data
):
    studies = pd.read_json(studies_data, orient="split")
    all_variables = set()
    newaves_paths = []
    decomps_paths = []
    for _, line in studies.iterrows():
        newave_path = os.path.join(
            line["CAMINHO"], Settings.synthesis_dir, Settings.newave_dir
        )
        decomp_path = os.path.join(
            line["CAMINHO"], Settings.synthesis_dir, Settings.decomp_dir
        )
        newaves_paths.append(newave_path)
        decomps_paths.append(decomp_path)
    newave_variables = asyncio.run(
        API.fetch_available_results_list(newaves_paths)
    )
    decomp_variables = asyncio.run(
        API.fetch_available_results_list(decomps_paths)
    )

    all_variables = all_variables.union(set(newave_variables))
    all_variables = all_variables.union(set(decomp_variables))
    all_variables = [a for a in all_variables if a not in NOT_OPERATION_FILES]
    return sorted(list(all_variables))


def update_operation_variables_dropdown_options_casos(interval, studies_data):
    studies = pd.read_json(studies_data, orient="split")
    paths = studies["CAMINHO"].tolist()
    unique_variables = asyncio.run(API.fetch_available_results_list(paths))
    unique_variables = [
        a for a in unique_variables if a not in NOT_OPERATION_FILES
    ]
    return sorted(unique_variables)


def update_costs_time_variables_dropdown_options_encadeador(
    interval, studies_data
):
    studies = pd.read_json(studies_data, orient="split")
    all_variables = set()
    newaves_paths = []
    decomps_paths = []
    for _, line in studies.iterrows():
        newave_path = os.path.join(
            line["CAMINHO"], Settings.synthesis_dir, Settings.newave_dir
        )
        decomp_path = os.path.join(
            line["CAMINHO"], Settings.synthesis_dir, Settings.decomp_dir
        )
        newaves_paths.append(newave_path)
        decomps_paths.append(decomp_path)
    newave_variables = asyncio.run(
        API.fetch_available_results_list(newaves_paths)
    )
    decomp_variables = asyncio.run(
        API.fetch_available_results_list(decomps_paths)
    )

    all_variables = all_variables.union(set(newave_variables))
    all_variables = all_variables.union(set(decomp_variables))
    all_variables = [a for a in all_variables if a in COSTS_TIME_FILES]
    return sorted(list(all_variables))


def update_costs_time_variables_dropdown_options_casos(interval, studies_data):
    studies = pd.read_json(studies_data, orient="split")
    paths = studies["CAMINHO"].tolist()
    unique_variables = asyncio.run(API.fetch_available_results_list(paths))
    unique_variables = [a for a in unique_variables if a in COSTS_TIME_FILES]
    return sorted(unique_variables)


def update_studies_names_dropdown_options_encadeador(interval, studies_data):
    studies = pd.read_json(studies_data, orient="split")
    paths = studies["CAMINHO"].tolist()
    return [pathlib.Path(p).parts[-1] for p in paths]


def update_studies_names_dropdown_options_casos(interval, studies_data):
    studies = pd.read_json(studies_data, orient="split")
    paths = studies["CAMINHO"].tolist()
    return [pathlib.Path(p).parts[-1] for p in paths]


def update_operation_options_encadeador(interval, studies, variable: str):
    print(studies)
    if not studies:
        return None
    if not variable:
        return None
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["CAMINHO"].tolist()
    complete_options = {}
    newave_options = asyncio.run(
        API.fetch_result_options_list(
            [
                os.path.join(p, Settings.synthesis_dir, Settings.newave_dir)
                for p in paths
            ],
            variable,
        )
    )
    decomp_options = asyncio.run(
        API.fetch_result_options_list(
            [
                os.path.join(p, Settings.synthesis_dir, Settings.decomp_dir)
                for p in paths
            ],
            variable,
        )
    )
    if newave_options is not None:
        complete_options = {**complete_options, **newave_options}
    if decomp_options is not None:
        complete_options = {**complete_options, **decomp_options}
    if len(complete_options) == 0:
        return None
    else:
        return complete_options


def update_operation_options_casos(interval, studies, variable: str):
    if not studies:
        return None
    if not variable:
        return None
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["CAMINHO"].tolist()
    options = asyncio.run(API.fetch_result_options_list(paths, variable))
    if len(options) == 0:
        return None
    else:
        return options
