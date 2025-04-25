import os
import pathlib
from datetime import datetime, timedelta
from io import StringIO
from typing import List, Optional

import pandas as pd
from dash import ctx

import src.utils.db as db
import src.utils.validation as validation
from src.utils.api import API
from src.utils.constants import SYNTHESIS_METADATA_NAMES
from src.utils.log import Log
from src.utils.settings import Settings

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
    Log.log().info(f"Obtendo variaveis - CASOS ({paths})")
    return unique_variables


def update_variables_options_encadeador(paths):
    all_variables = {}
    newaves_paths = []
    decomps_paths = []
    dessems_paths = []
    for path in paths:
        newave_path = os.path.join(
            path, Settings.synthesis_dir, Settings.newave_dir
        )
        decomp_path = os.path.join(
            path, Settings.synthesis_dir, Settings.decomp_dir
        )
        dessem_path = os.path.join(
            path, Settings.synthesis_dir, Settings.dessem_dir
        )
        newaves_paths.append(newave_path)
        decomps_paths.append(decomp_path)
        dessems_paths.append(dessem_path)
    newave_variables = API.fetch_available_results_list(newaves_paths)
    decomp_variables = API.fetch_available_results_list(decomps_paths)
    dessem_variables = API.fetch_available_results_list(dessems_paths)

    for k in SYNTHESIS_METADATA_NAMES.keys():
        df_newave = pd.read_json(StringIO(newave_variables[k]), orient="split")
        df_decomp = pd.read_json(StringIO(decomp_variables[k]), orient="split")
        df_dessem = pd.read_json(StringIO(dessem_variables[k]), orient="split")
        all_variables[k] = pd.concat(
            [df_newave, df_decomp, df_dessem], ignore_index=True
        ).to_json(orient="split")
    # TODO - talvez tenha que dar drop_duplicates

    return all_variables


def update_system_entities_casos(path, options):
    system_metadata = pd.read_json(StringIO(options["sistema"]), orient="split")
    if "chave" in system_metadata:
        system_entities = {
            e: API.fetch_result(path, e, {"preprocess": "FULL"})
            for e in system_metadata["chave"].tolist()
        }
    else:
        system_entities = {}
    return {
        e: df.to_json(orient="split")
        for e, df in system_entities.items()
        if isinstance(df, pd.DataFrame)
    }


def update_system_entities_encadeador(path, options):
    system_metadata = pd.read_json(StringIO(options["sistema"]), orient="split")
    if "chave" in system_metadata:
        newave_path = os.path.join(
            path, Settings.synthesis_dir, Settings.newave_dir
        )
        decomp_path = os.path.join(
            path, Settings.synthesis_dir, Settings.decomp_dir
        )
        dessem_path = os.path.join(
            path, Settings.synthesis_dir, Settings.dessem_dir
        )
        newave_system_entities = {
            e: API.fetch_result(newave_path, e, {"preprocess": "FULL"})
            for e in system_metadata["chave"].tolist()
        }
        decomp_system_entities = {
            e: API.fetch_result(decomp_path, e, {"preprocess": "FULL"})
            for e in system_metadata["chave"].tolist()
        }
        dessem_system_entities = {
            e: API.fetch_result(dessem_path, e, {"preprocess": "FULL"})
            for e in system_metadata["chave"].tolist()
        }
        system_entities = {
            e: pd.concat(
                [
                    newave_system_entities[e],
                    decomp_system_entities[e],
                    dessem_system_entities[e],
                ],
                ignore_index=True,
            )
            for e in system_metadata["chave"].tolist()
        }
    else:
        system_entities = {}
    return {
        e: df.to_json(orient="split")
        for e, df in system_entities.items()
        if isinstance(df, pd.DataFrame)
    }


def __merge_casos_encadeador_options(
    casos_options: dict, encadeador_options: dict
) -> dict:
    casos_keys = list(casos_options.keys())
    encadeador_keys = list(encadeador_options.keys())
    all_keys = list(set(casos_keys + encadeador_keys))
    options = {k: pd.DataFrame().to_json(orient="split") for k in all_keys}
    for k in all_keys:
        if k in casos_options and k in encadeador_options:
            options[k] = pd.concat(
                [
                    pd.read_json(StringIO(casos_options[k]), orient="split"),
                    pd.read_json(
                        StringIO(encadeador_options[k]), orient="split"
                    ),
                ],
                ignore_index=True,
            ).to_json(orient="split")
        elif k in casos_options:
            options[k] = casos_options[k]
        elif k in encadeador_options:
            options[k] = encadeador_options[k]
    return options


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
            current_data = pd.read_json(
                StringIO(current_studies), orient="split"
            )
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
                Log.log().info(
                    f"Adicionando estudo - CASOS ({new_study_id}, {label}, {color})"
                )
                casos_options = update_variables_options_casos([new_study_id])
                encadeador_options = update_variables_options_encadeador([
                    new_study_id
                ])
                options = __merge_casos_encadeador_options(
                    casos_options, encadeador_options
                )
                Log.log().info("Adicionando estudo - CASOS - Opcoes")
                casos_system = update_system_entities_casos(
                    new_study_id, casos_options
                )
                encadeador_system = update_system_entities_encadeador(
                    new_study_id, encadeador_options
                )
                system = __merge_casos_encadeador_options(
                    casos_system, encadeador_system
                )
                Log.log().info("Adicionando estudo - CASOS - Sistema")
                new_data = pd.DataFrame(
                    data={
                        "study_id": [None],
                        "table_id": [str(last_id + 1)],
                        "path": [new_study_id],
                        "name": [label],
                        "color": [color],
                        "created_date": [datetime.now()],
                        "options": [options],
                        "system": [system],
                        "program": [_get_programa(new_study_id)],
                    }
                )
                dfs_to_concat = (
                    [current_data, new_data]
                    if not current_data.empty
                    else [new_data]
                )
                return pd.concat(dfs_to_concat, ignore_index=True).to_json(
                    orient="split"
                )
        else:
            return current_studies
    elif ctx.triggered_id == edit_trigger:
        if edit_study_button_clicks:
            current_data = pd.read_json(
                StringIO(current_studies), orient="split"
            )
            old_study_path = current_data.loc[
                current_data["table_id"] == edit_study_id, "path"
            ].iloc[0]
            current_data.loc[
                current_data["table_id"] == edit_study_id, "path"
            ] = edit_study_path
            current_data.loc[
                current_data["table_id"] == edit_study_id, "name"
            ] = edit_study_name
            current_data.loc[
                current_data["table_id"] == edit_study_id, "color"
            ] = edit_study_color
            # Retorno rapido se mudou só "estética"
            if edit_study_path == old_study_path:
                return current_data.to_json(orient="split")

            casos_options = update_variables_options_casos([edit_study_path])
            encadeador_options = update_variables_options_encadeador([
                edit_study_path
            ])
            options = __merge_casos_encadeador_options(
                casos_options, encadeador_options
            )
            casos_system = update_system_entities_casos(
                edit_study_path, casos_options
            )
            encadeador_system = update_system_entities_encadeador(
                edit_study_path, encadeador_options
            )
            system = __merge_casos_encadeador_options(
                casos_system, encadeador_system
            )
            current_data.loc[
                current_data["table_id"] == edit_study_id, "options"
            ] = [options]
            current_data.loc[
                current_data["table_id"] == edit_study_id, "system"
            ] = [system]
            current_data.loc[
                current_data["table_id"] == edit_study_id, "program"
            ] = _get_programa(edit_study_path)
            return current_data.to_json(orient="split")
    elif ctx.triggered_id == remove_trigger:
        if remove_study_button_clicks:
            current_data = pd.read_json(
                StringIO(current_studies), orient="split"
            )
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
                lambda linha: __merge_casos_encadeador_options(
                    update_variables_options_casos([linha["path"]]),
                    update_variables_options_encadeador([linha["path"]]),
                ),
                axis=1,
            )
            screen_df["system"] = screen_df.apply(
                lambda linha: __merge_casos_encadeador_options(
                    update_system_entities_casos(
                        linha["path"], linha["options"]
                    ),
                    update_system_entities_encadeador(
                        linha["path"], linha["options"]
                    ),
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
    current_data = pd.read_json(StringIO(current_studies), orient="split")
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
        s for s in all_scenarios if s in ["min", "max", "median", "mean", "std"]
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

    studies_df = pd.read_json(StringIO(studies), orient="split")
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
    if cases_df is None:
        return pd.DataFrame(
            columns=[
                "NOME",
                "TEMPO DE EXECUCAO",
                "PROGRESSO (%)",
                "CASO ATUAL",
                "ESTADO",
            ]
        ).to_json(orient="split")

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
    if cases_df is not None:
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
                current_name = (
                    f"{program} - {year}_{str(month).zfill(2)}_rv{rv}"
                )
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
    studies,
    filters: dict,
    variable: str,
    kind: str = "STATISTICS",
    needs_stage: bool = False,
):
    if not studies:
        return None
    if not variable:
        return None
    req_filters = validation.validate_required_filters_operation(
        variable, filters, needs_stage=needs_stage
    )
    if req_filters is None:
        return None
    studies_df = pd.read_json(StringIO(studies), orient="split")
    paths = studies_df["path"].tolist()
    labels = studies_df["name"].tolist()
    aggregation = req_filters.pop("agregacao")
    data_filename, unit, data_filters = _get_operation_data_filename(
        studies_df, kind, variable, aggregation, req_filters
    )
    data_filters_nw_dc = {**data_filters, "estagio": 1, "preprocess": kind}
    data_filters_ds = {**data_filters, "preprocess": kind}
    if aggregation == "Usina Hidroelétrica":
        data_filters_nw_dc["codigo_usina"] = data_filters_nw_dc["codigo_uhe"]
        data_filters_ds["codigo_usina"] = data_filters_ds["codigo_uhe"]
    elif aggregation == "Usina Termelétrica":
        data_filters_nw_dc["codigo_usina"] = data_filters_nw_dc["codigo_ute"]
        data_filters_ds["codigo_usina"] = data_filters_ds["codigo_ute"]
    complete_df = pd.DataFrame()
    Log.log().info(f"Obtendo dados - ENCADEADOR ({variable})")
    newave_df = API.fetch_result_list(
        [
            os.path.join(p, Settings.synthesis_dir, Settings.newave_dir)
            for p in paths
        ],
        labels,
        data_filename,
        data_filters_nw_dc,
    )
    decomp_df = API.fetch_result_list(
        [
            os.path.join(p, Settings.synthesis_dir, Settings.decomp_dir)
            for p in paths
        ],
        labels,
        data_filename,
        data_filters_nw_dc,
    )
    dessem_df = API.fetch_result_list(
        [
            os.path.join(p, Settings.synthesis_dir, Settings.dessem_dir)
            for p in paths
        ],
        labels,
        data_filename,
        data_filters_ds,
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
    if dessem_df is not None:
        cols_dessem = dessem_df.columns.to_list()
        dessem_df["programa"] = "DESSEM"

        # TODO - melhorar filtro D1 DESSEM
        dessem_df = dessem_df.loc[dessem_df["estagio"] <= 48]

        complete_df = pd.concat(
            [
                complete_df,
                dessem_df[["programa"] + cols_dessem],
            ],
            ignore_index=True,
        )
    Log.log().info(f"Dados obtidos - ENCADEADOR ({variable})")
    if complete_df.empty:
        return None
    else:
        complete_df["unidade"] = unit
        return complete_df.to_json(orient="split")
        # for col in ["dataInicio", "dataFim"]:
        #     if col in complete_df.columns:
        #         complete_df[col] = complete_df[col].astype("datetime64[ns]")
        # return complete_df.to_json(
        #     orient="split", date_format="epoch", date_unit="ms"
        # )


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

    studies_df = pd.read_json(StringIO(studies), orient="split")
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
    studies_df = pd.read_json(StringIO(studies), orient="split")
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
    studies_df = pd.read_json(StringIO(studies), orient="split")
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


def _get_operation_data_filename(
    studies_df: pd.DataFrame,
    kind: str,
    variable: str,
    aggregation: str,
    filters: dict,
) -> tuple[str, str, dict]:
    options_df = pd.concat(
        [
            pd.read_json(StringIO(opt["operacao"]), orient="split")
            for opt in studies_df["options"]
        ],
        ignore_index=True,
    )
    metadata_line = options_df.loc[
        (options_df["nome_longo_variavel"] == variable)
        & (options_df["nome_longo_agregacao"] == aggregation)
    ]
    if metadata_line.empty:
        return "", "", {}
    unit = metadata_line["unidade"].iloc[0]
    chave = metadata_line["chave"].iloc[0]
    if kind == "STATISTICS":
        return (
            "ESTATISTICAS_OPERACAO_" + chave.split("_")[1],
            unit,
            {**filters, "variavel": chave.split("_")[0]},
        )
    elif kind == "SCENARIOS":
        return chave, unit, filters
    else:
        return "", "", {}


def _get_scenario_data_filename(
    studies_df: pd.DataFrame,
    kind: str,
    variable: str,
    aggregation: str,
    step: str,
    filters: dict,
) -> tuple[str, str, dict]:
    options_df = pd.concat(
        [
            pd.read_json(StringIO(opt["cenarios"]), orient="split")
            for opt in studies_df["options"]
        ],
        ignore_index=True,
    )
    metadata_line = options_df.loc[
        (options_df["nome_longo_variavel"] == variable)
        & (options_df["nome_longo_agregacao"] == aggregation)
        & (options_df["nome_longo_etapa"] == step)
    ]
    if metadata_line.empty:
        return "", "", {}
    unit = metadata_line["unidade"].iloc[0]
    chave = metadata_line["chave"].iloc[0]
    if kind == "STATISTICS":
        return (
            "ESTATISTICAS_CENARIOS_" + chave.split("_")[1],
            unit,
            {**filters, "variavel": chave.split("_")[0]},
        )
    elif kind == "SCENARIOS":
        return chave, unit, filters
    else:
        return "", "", {}


def update_operation_data_casos(
    studies,
    filters: dict,
    variable: str,
    kind: str = "STATISTICS",
    needs_stage: bool = False,
):
    if not studies:
        return None
    if not variable:
        return None
    req_filters = validation.validate_required_filters_operation(
        variable, filters, needs_stage=needs_stage
    )
    if req_filters is None:
        return None
    studies_df = pd.read_json(StringIO(studies), orient="split")
    paths = studies_df["path"].tolist()
    labels = studies_df["name"].tolist()
    aggregation = req_filters.pop("agregacao")
    data_filename, unit, data_filters = _get_operation_data_filename(
        studies_df, kind, variable, aggregation, req_filters
    )
    if aggregation == "Usina Hidroelétrica":
        data_filters["codigo_usina"] = data_filters["codigo_uhe"]
    elif aggregation == "Usina Termelétrica":
        data_filters["codigo_usina"] = data_filters["codigo_ute"]
    Log.log().info(f"Obtendo dados - CASOS ({variable})")
    df = API.fetch_result_list(
        paths,
        labels,
        data_filename,
        data_filters,
    )
    if df is None:
        return None
    if df.empty:
        return None
    else:
        df["unidade"] = unit
        return df.to_json(orient="split")


def update_scenario_data_casos(
    studies,
    filters: dict,
    variable: str,
    kind: str = "SCENARIOS",
):
    if not studies:
        return None
    if not variable:
        return None
    needs_iteration = (
        filters["etapa"] in ["Forward", "Backward"]
        if "etapa" in filters
        else False
    )
    req_filters = validation.validate_required_filters_scenarios(
        variable, filters, needs_iteration=needs_iteration
    )
    if req_filters is None:
        return None
    studies_df = pd.read_json(StringIO(studies), orient="split")
    paths = studies_df["path"].tolist()
    labels = studies_df["name"].tolist()
    aggregation = req_filters.pop("agregacao")
    step = req_filters.pop("etapa")
    data_filename, unit, data_filters = _get_scenario_data_filename(
        studies_df, kind, variable, aggregation, step, req_filters
    )
    Log.log().info(f"Obtendo dados - CASOS ({variable})")
    df = API.fetch_result_list(
        paths,
        labels,
        data_filename,
        data_filters,
    )

    if df is None:
        return None
    if df.empty:
        return None
    else:
        df["unidade"] = unit
        return df.to_json(orient="split")


def update_custos_tempo_data_encadeador(
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
    Log.log().info(f"Obtendo dados - ENCADEADOR ({variable})")
    studies_df = pd.read_json(StringIO(studies), orient="split")
    paths = studies_df["path"].tolist()
    labels = studies_df["name"].tolist()
    dir = {
        "NEWAVE": Settings.newave_dir,
        "DECOMP": Settings.decomp_dir,
        "DESSEM": Settings.dessem_dir,
    }.get(programa)
    df = API.fetch_result_list(
        [os.path.join(p, Settings.synthesis_dir, dir) for p in paths],
        labels,
        variable,
        {},
    )
    Log.log().info(f"Dados obtidos - ENCADEADOR ({variable})")
    if df.empty:
        return None
    else:
        return df.to_json(orient="split")


def update_violation_data_encadeador(
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
    Log.log().info(f"Obtendo dados - ENCADEADOR ({violation})")
    studies_df = pd.read_json(StringIO(studies), orient="split")
    paths = studies_df["path"].tolist()
    labels = studies_df["name"].tolist()
    dir = {
        "NEWAVE": Settings.newave_dir,
        "DECOMP": Settings.decomp_dir,
        "DESSEM": Settings.dessem_dir,
    }.get(programa)

    df = API.fetch_result_list(
        [os.path.join(p, Settings.synthesis_dir, dir) for p in paths],
        labels,
        "INVIABILIDADES",
        {"iteracao": -1, "tipo": f"'{violation}'", "preprocess": "FULL"},
    )

    Log.log().info(f"Dados obtidos - ENCADEADOR ({violation})")
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
    studies_df = pd.read_json(StringIO(studies), orient="split")
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
    studies_df = pd.read_json(StringIO(studies), orient="split")
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
    studies_df = pd.read_json(StringIO(studies), orient="split")
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
    studies_df = pd.read_json(StringIO(studies), orient="split")
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
    studies_df = pd.read_json(StringIO(studies), orient="split")
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
    studies_df = pd.read_json(StringIO(studies), orient="split")
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
    studies_df = pd.read_json(StringIO(studies), orient="split")
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
