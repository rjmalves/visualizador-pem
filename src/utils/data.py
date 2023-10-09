import pandas as pd
import pathlib
import os
from datetime import timedelta
from src.utils.api import API
from typing import List, Optional
from datetime import timedelta
import src.utils.validation as validation
from src.utils.settings import Settings
from dash import ctx
from src.utils.log import Log
import src.utils.db as db
from datetime import datetime

DISCRETE_COLOR_PALLETE = [
    "#f94144",
    "#277da1",
    "#90be6d",
    "#f3722c",
    "#577590",
    "#f9c74f",
    "#f8961e",
    "#4d908e",
    "#f9844a",
    "#43aa8b",
]

ENCADEADOR_TABLES = ["ESTUDO", "CASOS", "RODADAS"]


def update_variables_options_casos(paths):
    unique_variables = API.fetch_available_results_list(paths)
    return sorted(unique_variables)


def update_variables_options_encadeador(paths):
    all_variables = set()
    newaves_paths = []
    decomps_paths = []
    for path in paths:
        newave_path = os.path.join(
            path, Settings.synthesis_dir, Settings.newave_dir
        )
        decomp_path = os.path.join(
            path, Settings.synthesis_dir, Settings.decomp_dir
        )
        newaves_paths.append(newave_path)
        decomps_paths.append(decomp_path)
    newave_variables = API.fetch_available_results_list(newaves_paths)
    decomp_variables = API.fetch_available_results_list(decomps_paths)

    all_variables = all_variables.union(set(newave_variables))
    all_variables = all_variables.union(set(decomp_variables))
    all_variables = [a for a in all_variables if a not in ENCADEADOR_TABLES]
    return sorted(list(all_variables))


def edit_current_study_data(
    add_study_button_clicks,
    edit_study_button_clicks,
    remove_study_button_clicks,
    new_study_id,
    new_study_label,
    new_study_color,
    edit_study_id,
    edit_study_path,
    edit_study_name,
    edit_study_color,
    selected_study,
    current_studies,
    add_trigger,
    edit_trigger,
    remove_trigger,
    screen,
    screen_type_str,
):
    if ctx.triggered_id == add_trigger:
        if add_study_button_clicks:
            if not new_study_id:
                return current_studies
            elif len(new_study_id) == 0:
                return current_studies
            current_data = pd.read_json(current_studies, orient="split")
            if new_study_id in current_data["path"].tolist():
                return current_studies
            else:
                current_ids = current_data["table_id"].to_list()
                last_id = 0 if len(current_ids) == 0 else int(current_ids[-1])
                if new_study_label is None:
                    label = pathlib.Path(new_study_id).parts[-1]
                else:
                    label = new_study_label
                if new_study_color == "#ffffff":
                    color = DISCRETE_COLOR_PALLETE[
                        last_id % len(DISCRETE_COLOR_PALLETE)
                    ]
                else:
                    color = new_study_color
                casos_options = update_variables_options_casos([new_study_id])
                encadeador_options = update_variables_options_encadeador(
                    [new_study_id]
                )
                options = list(set(casos_options).union(encadeador_options))
                new_data = pd.DataFrame(
                    data={
                        "study_id": [None],
                        "table_id": [str(last_id + 1)],
                        "path": [new_study_id],
                        "name": [label],
                        "color": [color],
                        "created_date": [datetime.now()],
                        "options": [",".join(options)],
                        "program": [_get_programa(new_study_id)],
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
                current_data["table_id"] == edit_study_id, "path"
            ] = edit_study_path
            current_data.loc[
                current_data["table_id"] == edit_study_id, "name"
            ] = edit_study_name
            current_data.loc[
                current_data["table_id"] == edit_study_id, "color"
            ] = edit_study_color
            casos_options = update_variables_options_casos([edit_study_path])
            encadeador_options = update_variables_options_encadeador(
                [edit_study_path]
            )
            options = list(set(casos_options).union(encadeador_options))
            current_data.loc[
                current_data["table_id"] == edit_study_id, "options"
            ] = ",".join(options)
            current_data.loc[
                current_data["table_id"] == edit_study_id, "program"
            ] = _get_programa(edit_study_path)
            return current_data.to_json(orient="split")
    elif ctx.triggered_id == remove_trigger:
        if remove_study_button_clicks:
            current_data = pd.read_json(current_studies, orient="split")
            new_data = current_data.loc[
                ~current_data["table_id"].isin(selected_study)
            ]
            return new_data.to_json(orient="split")
        else:
            return current_studies
    elif screen is not None:
        screen_df = db.load_screen(screen, screen_type_str)
        if screen_df is not None:
            screen_df["options"] = screen_df.apply(
                lambda linha: ",".join(
                    list(
                        set(
                            update_variables_options_casos([linha["path"]])
                        ).union(
                            set(
                                update_variables_options_encadeador(
                                    [linha["path"]]
                                )
                            )
                        )
                    )
                ),
                axis=1,
            )
            screen_df["program"] = screen_df.apply(
                lambda linha: _get_programa(linha["path"]), axis=1
            )
            return screen_df.to_json(orient="split")
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
        table_id = selected_study[0]
        return {
            "table_id": table_id,
            "path": current_data.loc[
                current_data["table_id"] == table_id, "path"
            ].tolist()[0],
            "name": current_data.loc[
                current_data["table_id"] == table_id, "name"
            ].tolist()[0],
            "color": current_data.loc[
                current_data["table_id"] == table_id, "color"
            ].tolist()[0],
        }


def get_statistics_scenarios(all_scenarios: List[str]) -> List[str]:
    scenarios = [
        s
        for s in all_scenarios
        if s in ["min", "max", "median", "mean", "std"]
    ]
    scenarios = [s for s in scenarios if "p" in s]
    return scenarios


def get_non_statistics_scenarios(all_scenarios: List[str]) -> List[str]:
    scenarios = [
        s
        for s in all_scenarios
        if s not in ["min", "max", "median", "mean", "std"]
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
    paths = studies_df["path"].tolist()
    labels = studies_df["name"].tolist()
    study_df = API.fetch_result_list(
        paths,
        labels,
        "ESTUDO",
        {"preprocess": "FULL"},
    )

    cases_df = API.fetch_result_list(
        paths,
        labels,
        "CASOS",
        {"preprocess": "FULL"},
    )

    runs_df = API.fetch_result_list(
        paths,
        labels,
        "RODADAS",
        {"preprocess": "FULL"},
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
    Log.log().info(f"Obtendo dados - ENCADEADOR ({variable}, {filters})")
    fetch_filters = {**req_filters, "estagio": 1, "preprocess": "STATISTICS"}
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["path"].tolist()
    labels = studies_df["name"].tolist()
    complete_df = pd.DataFrame()
    newave_df = API.fetch_result_list(
        [
            os.path.join(p, Settings.synthesis_dir, Settings.newave_dir)
            for p in paths
        ],
        labels,
        variable,
        fetch_filters,
    )
    decomp_df = API.fetch_result_list(
        [
            os.path.join(p, Settings.synthesis_dir, Settings.decomp_dir)
            for p in paths
        ],
        labels,
        variable,
        fetch_filters,
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
    Log.log().info(f"Dados obtidos - ENCADEADOR ({variable}, {filters})")
    if complete_df.empty:
        return None
    else:
        return complete_df.to_json(orient="split")


def _get_programa(
    path: str,
) -> Optional[str]:
    df = API.fetch_result(
        path,
        "PROGRAMA",
        {"preprocess": "FULL"},
    )
    if df is None:
        return None
    if df.empty:
        return None
    else:
        return df["programa"].iloc[0]


def update_spatial_programa(
    studies,
    study: str,
    filters: dict,
):
    if not studies:
        return None
    if not study:
        return None
    if not all(["estagio" in filters and "cenario" in filters]):
        return None

    studies_df = pd.read_json(studies, orient="split")
    return studies_df.loc[studies_df["name"] == study, "program"].iloc[0]


def update_spatial_SBM_data_casos(
    studies,
    study: str,
    filters: dict,
    programa: str,
    preprocess: str = "FULL",
):
    if not studies:
        return None
    if not study:
        return None
    if not programa:
        return None
    if not filters:
        return None
    if not all(["estagio" in filters and "cenario" in filters]):
        return None
    req_filters = {
        "programa": programa,
        "estagio": filters["estagio"],
        "cenario": filters["cenario"],
    }
    studies_df = pd.read_json(studies, orient="split")
    path = studies_df.loc[studies_df["name"] == study, "path"].iloc[0]
    df = API.fetch_study_SBM_spatial_variable_list(
        path,
        [
            "EARPF_SBM_EST",
            "GHID_SBM_EST",
            "GTER_SBM_EST",
            "EVER_SBM_EST",
            "CMO_SBM_EST",
            "MERL_SBM_EST",
        ],
        {**req_filters, "preprocess": preprocess},
    )

    if df is None:
        return None
    if df.empty:
        return None
    else:
        return df.to_json(orient="split")


def update_spatial_INT_data_casos(
    studies,
    study: str,
    filters: dict,
    programa: str,
    preprocess: str = "FULL",
):
    if not studies:
        return None
    if not study:
        return None
    if not programa:
        return None
    if not filters:
        return None
    if not all(["estagio" in filters and "cenario" in filters]):
        return None
    req_filters = {
        "programa": programa,
        "estagio": filters["estagio"],
        "cenario": filters["cenario"],
    }
    studies_df = pd.read_json(studies, orient="split")
    path = studies_df.loc[studies_df["name"] == study, "path"].iloc[0]
    df = API.fetch_study_INT_spatial_variable_list(
        path,
        {**req_filters, "preprocess": preprocess},
    )

    if df is None:
        return None
    if df.empty:
        return None
    else:
        return df.to_json(orient="split")


def update_operation_data_casos(
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
    paths = studies_df["path"].tolist()
    labels = studies_df["name"].tolist()
    df = API.fetch_result_list(
        paths,
        labels,
        variable,
        {**req_filters, "preprocess": preprocess},
    )

    if df is None:
        return None
    if df.empty:
        return None
    else:
        return df.to_json(orient="split")


def update_scenario_data_casos(
    studies,
    filters: dict,
    variable: str,
    preprocess: str = "FULL",
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
    paths = studies_df["path"].tolist()
    labels = studies_df["name"].tolist()
    df = API.fetch_result_list(
        paths,
        labels,
        variable,
        {**req_filters, "preprocess": preprocess},
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
    Log.log().info(f"Obtendo dados - ENCADEADOR ({variable}, {filters})")
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["path"].tolist()
    labels = studies_df["name"].tolist()
    dir = {"NEWAVE": Settings.newave_dir, "DECOMP": Settings.decomp_dir}.get(
        programa
    )
    df = API.fetch_result_list(
        [os.path.join(p, Settings.synthesis_dir, dir) for p in paths],
        labels,
        variable,
        {},
    )
    Log.log().info(f"Dados obtidos - ENCADEADOR ({variable}, {filters})")
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
    Log.log().info(f"Obtendo dados - ENCADEADOR ({violation}, {filters})")
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["path"].tolist()
    labels = studies_df["name"].tolist()
    dir = {"NEWAVE": Settings.newave_dir, "DECOMP": Settings.decomp_dir}.get(
        programa
    )

    df = API.fetch_result_list(
        [os.path.join(p, Settings.synthesis_dir, dir) for p in paths],
        labels,
        "INVIABILIDADES",
        {"iteracao": -1, "tipo": f"'{violation}'", "preprocess": "FULL"},
    )

    Log.log().info(f"Dados obtidos - ENCADEADOR ({violation}, {filters})")
    if df is None:
        return None
    if df.empty:
        return None
    else:
        df = df[["estudo", "caso", "unidade", "violacao"]]
        return df.to_json(orient="split")


def update_custos_tempo_data_casos(
    studies,
    variable: str,
):
    if not studies:
        return None
    if not variable:
        return None
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["path"].tolist()
    labels = studies_df["name"].tolist()
    df = API.fetch_result_list(
        paths,
        labels,
        variable,
        {},
    )

    if df is None:
        return None
    if df.empty:
        return None
    else:
        return df.to_json(orient="split")


def update_runtime_data_casos(
    studies,
):
    if not studies:
        return None
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["path"].tolist()
    labels = studies_df["name"].tolist()
    df = API.fetch_result_list(
        paths,
        labels,
        "TEMPO",
        {},
    )
    if df is None:
        return None
    if df.empty:
        return None
    else:
        return df.to_json(orient="split")


def update_convergence_data_casos(
    studies,
):
    if not studies:
        return None
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["path"].tolist()
    labels = studies_df["name"].tolist()
    df = API.fetch_result_list(
        paths,
        labels,
        "CONVERGENCIA",
        {},
    )

    if df is None:
        return None
    if df.empty:
        return None
    else:
        return df.to_json(orient="split")


def update_job_resources_data_casos(
    studies,
):
    if not studies:
        return None
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["path"].tolist()
    labels = studies_df["name"].tolist()
    df_cluster = API.fetch_result_list(
        paths,
        labels,
        "RECURSOS_JOB",
        {},
    )
    if df_cluster is None:
        return None
    if df_cluster.empty:
        return None

    else:
        return df_cluster.to_json(orient="split")


def update_cluster_resources_data_casos(
    studies,
):
    if not studies:
        return None
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["path"].tolist()
    labels = studies_df["name"].tolist()
    df_job = API.fetch_result_list(
        paths,
        labels,
        "RECURSOS_CLUSTER",
        {},
    )
    if df_job is None:
        return None
    if df_job.empty:
        return None
    else:
        return df_job.to_json(orient="split")


def update_distribution_data_ppq(studies, filters: dict, variable: str):
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
    paths = studies_df["path"].tolist()
    labels = studies_df["name"].tolist()
    df = API.fetch_result_list(
        paths,
        labels,
        variable,
        {**req_filters, "preprocess": "FULL"},
    )

    if df is None:
        return None
    if df.empty:
        return None
    else:
        return df.to_json(orient="split")


def update_operation_data_ppq(
    studies, filters: dict, variable: str, study: str
):
    if not studies:
        return None
    if not variable:
        return None
    if not study:
        return None
    req_filters = validation.validate_required_filters(variable, filters)
    if req_filters is None:
        return None
    studies_df = pd.read_json(studies, orient="split")
    paths = studies_df["path"].tolist()
    labels = studies_df["name"].tolist()
    df = API.fetch_result_list(
        paths,
        labels,
        variable,
        {**req_filters, "preprocess": "STATISTICS"},
    )

    if df is None:
        return None
    if df.empty:
        return None
    else:
        return df.to_json(orient="split")
