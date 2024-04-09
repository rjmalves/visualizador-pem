import pandas as pd
import os
import itertools
from io import StringIO
from src.utils.settings import Settings
from src.utils.api import API

SYSTEM_FILES = ["PAT", "EST", "SIN", "SBM", "REE", "UHE", "UTE", "PEE", "UEE"]

COSTS_TIME_FILES = [
    "CUSTOS",
    "TEMPO",
]

POLICY_FILES = (
    ["CORTES"]
    + [f"CORTES{i}" for i in range(1, 61)]
    + ["ESTADOS"]
    + [f"ESTADOS{i}" for i in range(1, 61)]
)

NOT_OPERATION_FILES = (
    [
        "CUSTOS",
        "TEMPO",
        "CONVERGENCIA",
        "PROBABILIDADES",
        "INVIABILIDADES",
        "RECURSOS_CLUSTER",
        "RECURSOS_JOB",
        "PROGRAMA",
        "CASOS",
        "RODADAS",
        "ESTUDO",
    ]
    + SYSTEM_FILES
    + POLICY_FILES
)

SCENARIO_FILE_PATTERNS = ["_FOR", "_BKW", "_SF"]


def update_operation_variables_dropdown_options_encadeador(
    interval, studies_data
):
    if studies_data is None:
        return []
    studies = pd.read_json(StringIO(studies_data), orient="split")
    options = studies["options"].tolist()
    unique_variables = [o.split(",") for o in options]
    unique_variables = list(
        set(list(itertools.chain.from_iterable(unique_variables)))
    )
    unique_variables = [
        a for a in unique_variables if a not in NOT_OPERATION_FILES
    ]
    unique_variables = [
        a
        for a in unique_variables
        if not any([p in a for p in SCENARIO_FILE_PATTERNS])
    ]
    return sorted(unique_variables)


def update_operation_variables_dropdown_options_casos(studies_data):
    if studies_data is None:
        return []
    studies = pd.read_json(StringIO(studies_data), orient="split")
    options = studies["options"].tolist()
    unique_variables = [o.split(",") for o in options]
    unique_variables = list(
        set(list(itertools.chain.from_iterable(unique_variables)))
    )
    unique_variables = [
        a for a in unique_variables if a not in NOT_OPERATION_FILES
    ]
    unique_variables = [
        a
        for a in unique_variables
        if not any([p in a for p in SCENARIO_FILE_PATTERNS])
    ]
    return sorted(unique_variables)


def update_scenario_variables_dropdown_options_casos(studies_data):
    if studies_data is None:
        return []
    studies = pd.read_json(StringIO(studies_data), orient="split")
    options = studies["options"].tolist()
    unique_variables = [o.split(",") for o in options]
    unique_variables = list(
        set(list(itertools.chain.from_iterable(unique_variables)))
    )
    unique_variables = [
        a
        for a in unique_variables
        if any([s in a for s in SCENARIO_FILE_PATTERNS])
    ]
    return sorted(unique_variables)


def update_costs_time_variables_dropdown_options_encadeador(
    interval, studies_data
):
    if studies_data is None:
        return []
    studies = pd.read_json(StringIO(studies_data), orient="split")
    options = studies["options"].tolist()
    unique_variables = [o.split(",") for o in options]
    unique_variables = list(
        set(list(itertools.chain.from_iterable(unique_variables)))
    )
    unique_variables = [a for a in unique_variables if a in COSTS_TIME_FILES]
    return sorted(unique_variables)


def update_costs_time_variables_dropdown_options_casos(studies_data):
    if studies_data is None:
        return []
    studies = pd.read_json(StringIO(studies_data), orient="split")
    options = studies["options"].tolist()
    unique_variables = [o.split(",") for o in options]
    unique_variables = list(
        set(list(itertools.chain.from_iterable(unique_variables)))
    )
    unique_variables = [a for a in unique_variables if a in COSTS_TIME_FILES]
    return sorted(unique_variables)


def update_studies_names_dropdown_options_encadeador(interval, studies_data):
    if studies_data is None:
        return []
    studies = pd.read_json(StringIO(studies_data), orient="split")
    labels = studies["name"].tolist()
    return labels


def update_studies_names_dropdown_options_casos(studies_data):
    if studies_data is None:
        return []
    studies = pd.read_json(StringIO(studies_data), orient="split")
    labels = studies["name"].tolist()
    return labels


def update_operation_options_encadeador(interval, studies, variable: str):
    if not studies:
        return None
    if not variable:
        return None
    studies_df = pd.read_json(StringIO(studies), orient="split")
    paths = studies_df["path"].tolist()
    complete_options = {}
    newave_options = API.fetch_result_options_list(
        [
            os.path.join(p, Settings.synthesis_dir, Settings.newave_dir)
            for p in paths
        ],
        variable,
    )

    decomp_options = API.fetch_result_options_list(
        [
            os.path.join(p, Settings.synthesis_dir, Settings.decomp_dir)
            for p in paths
        ],
        variable,
    )

    if newave_options is not None:
        complete_options = {**complete_options, **newave_options}
    if decomp_options is not None:
        complete_options = {**complete_options, **decomp_options}
    if len(complete_options) == 0:
        return None
    else:
        return complete_options


def update_operation_options_casos(studies, variable: str):
    if not studies:
        return None
    if not variable:
        return None
    studies_df = pd.read_json(StringIO(studies), orient="split")
    paths = studies_df["path"].tolist()
    options = API.fetch_result_options_list(paths, variable)
    if len(options) == 0:
        return None
    else:
        return options


def update_scenario_options_casos(studies, variable: str):
    if not studies:
        return None
    if not variable:
        return None
    studies_df = pd.read_json(StringIO(studies), orient="split")
    paths = studies_df["path"].tolist()
    options = API.fetch_result_options_list(paths, variable)
    if len(options) == 0:
        return None
    else:
        return options


def update_spatial_options_casos(studies, study: str):
    if not studies:
        return None
    if not study:
        return None
    studies_df = pd.read_json(StringIO(studies), orient="split")
    path = studies_df.loc[studies_df["name"] == study, "path"].iloc[0]
    options = API.fetch_spatial_options_list(path)
    if len(options) == 0:
        return None
    else:
        return options
