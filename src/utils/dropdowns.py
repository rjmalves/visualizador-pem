import pandas as pd
import os
from src.utils.api import API


def update_operation_variables_dropdown_options_encadeador(
    interval, studies_data
):
    studies = pd.read_json(studies_data, orient="split")
    all_variables = set()
    for _, line in studies.iterrows():
        newave_path = os.path.join(line["CAMINHO"], "NEWAVE")
        decomp_path = os.path.join(line["CAMINHO"], "DECOMP")
        unique_variables = API.fetch_available_results_list(
            [newave_path, decomp_path]
        )
        all_variables = all_variables.union(set(unique_variables))
    return sorted(list(all_variables))


def update_operation_variables_dropdown_options_casos(interval, studies_data):
    studies = pd.read_json(studies_data, orient="split")
    paths = studies["CAMINHO"].tolist()
    unique_variables = API.fetch_available_results_list(paths)
    return sorted(unique_variables)


def update_operation_options_encadeador(interval, studies, variable: str):
    if not studies:
        return None
    if not variable:
        return None
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["CAMINHO"].tolist()
    complete_options = {}
    newave_options = API.fetch_result_options_list(
        [os.path.join(p, "NEWAVE") for p in paths], variable
    )
    decomp_options = API.fetch_result_options_list(
        [os.path.join(p, "DECOMP") for p in paths], variable
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
    options = API.fetch_result_options_list(paths, variable)
    if len(options) == 0:
        return None
    else:
        return options
