from typing import Optional

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
