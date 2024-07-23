from typing import Optional

REQUIRED_OPERATION_FILTERS = {
    "Sistema Interligado": ["patamar"],
    "Submercado": ["patamar", "codigo_submercado"],
    "Par de Submercados": [
        "patamar",
        "codigo_submercado_de",
        "codigo_submercado_para",
    ],
    "Reservatório Equivalente": ["patamar", "codigo_ree"],
    "Usina Hidroelétrica": ["patamar", "codigo_uhe"],
    "Usina Termelétrica": ["patamar", "codigo_ute"],
}

REQUIRED_SCENARIO_FILTERS = {
    "Sistema Interligado": [],
    "Submercado": ["codigo_submercado"],
    "Reservatório Equivalente": ["codigo_ree"],
    "Usina Hidroelétrica": ["codigo_usina"],
}

REQUIRED_FILTERS = {
    "SIN": [],
    "SBM": ["submercado"],
    "SBP": ["submercadoDe", "submercadoPara"],
    "REE": ["ree"],
    "PEE": ["pee"],
    "UHE": ["usina"],
    "UTE": ["usina"],
    "UEE": ["usina"],
    "PAT": ["patamar"],
    "EST": [],
    "FOR": ["iteracao"],
    "BKW": ["iteracao"],
    "SF": [],
}


def validate_required_filters_operation(
    variable: str, filters: dict, needs_stage: bool
) -> Optional[dict]:
    if not variable:
        return None
    if "agregacao" not in filters:
        return None
    required_filters = REQUIRED_OPERATION_FILTERS.copy()
    if needs_stage:
        required_filters = {
            k: v + ["estagio"] for k, v in required_filters.items()
        }
    agregacao = filters["agregacao"]
    valid = all([filters.get(k) for k in required_filters[agregacao]])
    if valid:
        req_filters = {k: int(filters[k]) for k in required_filters[agregacao]}
        req_filters["agregacao"] = agregacao
        return req_filters
    return None


def validate_required_filters_scenarios(
    variable: str, filters: dict, needs_iteration: bool
) -> Optional[dict]:
    if not variable:
        return None
    if "agregacao" not in filters:
        return None
    if "etapa" not in filters:
        return None
    required_filters = REQUIRED_SCENARIO_FILTERS.copy()
    if needs_iteration:
        required_filters = {
            k: v + ["iteracao"] for k, v in required_filters.items()
        }
    agregacao = filters["agregacao"]
    etapa = filters["etapa"]
    valid = all([filters.get(k) for k in required_filters[agregacao]])
    if valid:
        req_filters = {k: int(filters[k]) for k in required_filters[agregacao]}
        req_filters["agregacao"] = agregacao
        req_filters["etapa"] = etapa
        return req_filters
    return None


def validate_required_filters(
    variable: str, filters: dict, ppq: bool = False
) -> Optional[dict]:
    if not variable:
        return False
    variable_data = variable.split("_")
    if len(variable_data) != 3:
        return False
    spatial_res = variable_data[1]
    temporal_res = variable_data[2]
    valid_spatial = all(
        [filters.get(k) for k in REQUIRED_FILTERS.get(spatial_res, [])]
    )
    valid_temporal = all(
        [filters.get(k) for k in REQUIRED_FILTERS.get(temporal_res, [])]
    )
    valid_ppq = any([filters.get("estagio"), not ppq])
    if valid_spatial and valid_temporal and valid_ppq:
        filters_spatial = {
            k: filters[k] for k in REQUIRED_FILTERS.get(spatial_res)
        }
        filters_temporal = {
            k: filters[k] for k in REQUIRED_FILTERS.get(temporal_res)
        }
        filters_ppq = {"estagio": filters.get("estagio")} if ppq else {}
        return {
            **filters_spatial,
            **filters_temporal,
            **filters_ppq,
        }
    else:
        return None
