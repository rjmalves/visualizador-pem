import os
from io import StringIO

import pandas as pd

from src.utils.api import API
from src.utils.settings import Settings

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


def update_operation_variables_dropdown_options_encadeador(studies_data):
    if studies_data is None:
        return []
    studies = pd.read_json(StringIO(studies_data), orient="split")
    if studies.empty:
        return []
    options_df = pd.concat(
        [
            pd.read_json(StringIO(opt["operacao"]), orient="split")
            for opt in studies["options"]
        ],
        ignore_index=True,
    )
    if options_df.empty:
        return []
    else:
        return options_df["nome_longo_variavel"].unique().tolist()


def update_operation_variables_dropdown_options_casos(studies_data):
    if studies_data is None:
        return []
    studies = pd.read_json(StringIO(studies_data), orient="split")
    if studies.empty:
        return []
    options_df = pd.concat(
        [
            pd.read_json(StringIO(opt["operacao"]), orient="split")
            for opt in studies["options"]
        ],
        ignore_index=True,
    )
    if options_df.empty:
        return []
    else:
        return options_df["nome_longo_variavel"].unique().tolist()


def update_operation_resolution_dropdown_options_casos(studies_data, variable):
    if studies_data is None:
        return []
    studies = pd.read_json(StringIO(studies_data), orient="split")
    if studies.empty:
        return []
    options_df = pd.concat(
        [
            pd.read_json(StringIO(opt["operacao"]), orient="split")
            for opt in studies["options"]
        ],
        ignore_index=True,
    )
    if options_df.empty:
        return []
    else:
        return (
            options_df.loc[
                options_df["nome_longo_variavel"] == variable,
                "nome_longo_agregacao",
            ]
            .unique()
            .tolist()
        )


def update_scenario_variables_dropdown_options_casos(studies_data):
    if studies_data is None:
        return []
    studies = pd.read_json(StringIO(studies_data), orient="split")
    if studies.empty:
        return []
    options_df = pd.concat(
        [
            pd.read_json(StringIO(opt["cenarios"]), orient="split")
            for opt in studies["options"]
        ],
        ignore_index=True,
    )
    if options_df.empty:
        return []
    return options_df["nome_longo_variavel"].unique().tolist()


def update_scenarios_resolution_dropdown_options_casos(studies_data, variable):
    if studies_data is None:
        return []
    studies = pd.read_json(StringIO(studies_data), orient="split")
    if studies.empty:
        return []
    options_df = pd.concat(
        [
            pd.read_json(StringIO(opt["cenarios"]), orient="split")
            for opt in studies["options"]
        ],
        ignore_index=True,
    )
    if options_df.empty:
        return []
    else:
        return (
            options_df.loc[
                options_df["nome_longo_variavel"] == variable,
                "nome_longo_agregacao",
            ]
            .unique()
            .tolist()
        )


def update_scenarios_etapa_dropdown_options_casos(
    studies_data, variable, resolution
):
    if studies_data is None:
        return []
    studies = pd.read_json(StringIO(studies_data), orient="split")
    if studies.empty:
        return []
    options_df = pd.concat(
        [
            pd.read_json(StringIO(opt["cenarios"]), orient="split")
            for opt in studies["options"]
        ],
        ignore_index=True,
    )
    if options_df.empty:
        return []
    else:
        return (
            options_df.loc[
                (options_df["nome_longo_variavel"] == variable)
                & (options_df["nome_longo_agregacao"] == resolution),
                "nome_longo_etapa",
            ]
            .unique()
            .tolist()
        )


def update_costs_time_variables_dropdown_options_encadeador(studies_data):
    if studies_data is None:
        return []
    studies = pd.read_json(StringIO(studies_data), orient="split")
    if studies.empty:
        return []
    options_df = pd.concat(
        [
            pd.read_json(StringIO(opt["execucao"]), orient="split")
            for opt in studies["options"]
        ],
        ignore_index=True,
    )
    if options_df.empty:
        return []
    else:
        return [
            o
            for o in options_df["chave"].unique().tolist()
            if o in ["TEMPO", "CUSTOS"]
        ]


def update_costs_time_variables_dropdown_options_casos(studies_data):
    if studies_data is None:
        return []
    studies = pd.read_json(StringIO(studies_data), orient="split")
    if studies.empty:
        return []
    options_df = pd.concat(
        [
            pd.read_json(StringIO(opt["execucao"]), orient="split")
            for opt in studies["options"]
        ],
        ignore_index=True,
    )
    if options_df.empty:
        return []
    else:
        return [
            o
            for o in options_df["chave"].unique().tolist()
            if o in ["TEMPO", "CUSTOS"]
        ]


def update_studies_names_dropdown_options_encadeador(studies_data):
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


def update_operation_options_encadeador(studies, variable: str):
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

    dessem_options = API.fetch_result_options_list(
        [
            os.path.join(p, Settings.synthesis_dir, Settings.dessem_dir)
            for p in paths
        ],
        variable,
    )

    if newave_options is not None:
        complete_options = {**complete_options, **newave_options}
    if decomp_options is not None:
        complete_options = {**complete_options, **decomp_options}
    if dessem_options is not None:
        complete_options = {**complete_options, **dessem_options}
    if len(complete_options) == 0:
        return None
    else:
        return complete_options


def update_operation_dropdown_system_entity_options_casos(studies, entity: str):
    def __postproc_entity_df(
        entity_df: pd.DataFrame, entity: str
    ) -> pd.DataFrame:
        if entity == "EST":
            return {
                v: k for k, v in zip(entity_df["estagio"], entity_df["estagio"])
            }
        elif entity == "PAT":
            return {
                v: k for k, v in zip(entity_df["patamar"], entity_df["patamar"])
            }
        elif entity == "SBM":
            return {
                v: k
                for k, v in zip(
                    entity_df["submercado"], entity_df["codigo_submercado"]
                )
            }
        elif entity == "REE":
            return {
                v: k for k, v in zip(entity_df["ree"], entity_df["codigo_ree"])
            }
        elif entity == "UHE":
            return {
                v: k
                for k, v in zip(entity_df["usina"], entity_df["codigo_usina"])
            }
        elif entity == "UTE":
            return {
                v: k
                for k, v in zip(entity_df["usina"], entity_df["codigo_usina"])
            }
        elif entity == "SIN":
            return {}

    if not studies:
        return []
    if not entity:
        return []
    studies_df = pd.read_json(StringIO(studies), orient="split")
    if studies_df.empty:
        return []
    options = pd.concat(
        [
            pd.read_json(StringIO(opt[entity]), orient="split")
            for opt in studies_df["system"]
        ],
        ignore_index=True,
    )
    options = __postproc_entity_df(options, entity)
    if len(options) == 0:
        return []
    else:
        return options


def update_aggregation_options_casos(studies, variable: str):
    if not studies:
        return None
    if not variable:
        return None
    studies_df = pd.read_json(StringIO(studies), orient="split")
    options = pd.concat(
        [
            pd.read_json(StringIO(opt["operacao"]), orient="split")
            for opt in studies_df["options"]
        ],
        ignore_index=True,
    )
    options = {}
    if len(options) == 0:
        return None
    else:
        return options


def update_operation_options_casos(studies, variable: str):
    if not studies:
        return None
    if not variable:
        return None
    studies_df = pd.read_json(StringIO(studies), orient="split")
    options = pd.concat(
        [
            pd.read_json(StringIO(opt["operacao"]), orient="split")
            for opt in studies_df["options"]
        ],
        ignore_index=True,
    )
    options = {}
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
