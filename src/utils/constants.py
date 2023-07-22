import pandas as pd

VARIABLE_UNITS = {
    "EARPF": "%",
    "GHID": "MWmed",
    "GTER": "MWmed",
    "INT": "MWmed",
    "CMO": "R$/MWh",
    "MER": "MWmed",
}

INTERCAMBIOS_SUBMERCADOS_NEWAVE = pd.DataFrame(
    data={
        "source": ["S", "NE", "NOFICT", "N", "NE"],
        "target": [
            "SE/CO",
            "SE/CO",
            "SE/CO",
            "NOFICT",
            "NOFICT",
        ],
        "label": [
            "S_SE/CO",
            "NE_SE/CO",
            "NOFICT_SE/CO",
            "N_NOFICT",
            "NE_NOFICT",
        ],
    }
)


ARESTAS_INTERCAMBIOS_NEWAVE = {
    ("S", "SE/CO"): {
        "color": "white",
        "textposition": [-55, -24],
        "textframe": [6, 2],
    },
    ("NE", "SE/CO"): {
        "color": "white",
        "textposition": [-40, -15],
        "textframe": [6, 2],
    },
    ("NOFICT", "SE/CO"): {
        "color": "white",
        "textposition": [-52, -15],
        "textframe": [6, 2],
    },
    ("N", "NOFICT"): {
        "color": "white",
        "textposition": [-58, -8],
        "textframe": [6, 2],
    },
    ("NE", "NOFICT"): {
        "color": "black",
        "textposition": [-45, -7],
        "textframe": [6, 2],
    },
}

SUBMERCADOS_NEWAVE = pd.DataFrame(
    data={
        "submercado": [1, 2, 3, 4, 11],
        "nome": ["SE/CO", "S", "NE", "N", "NOFICT"],
    }
)


NOS_SUBMERCADOS_NEWAVE = {
    "SE/CO": {
        "pos": [-48, -20],
        "color": "white",
        "size": 35,
        "textposition": [-42, -23],
        "textframe": [8, 4],
        "fict": False,
    },
    "S": {
        "pos": [-52, -28],
        "color": "white",
        "size": 35,
        "textposition": [-46, -31],
        "textframe": [8, 4],
        "fict": False,
    },
    "NE": {
        "pos": [-39, -8],
        "color": "white",
        "size": 35,
        "textposition": [-33, -8],
        "textframe": [8, 4],
        "fict": False,
    },
    "N": {
        "pos": [-60, -3],
        "color": "white",
        "size": 35,
        "textposition": [-67, -4],
        "textframe": [8, 4],
        "fict": False,
    },
    "NOFICT": {
        "pos": [-48, -10],
        "color": "black",
        "size": 10,
        "textposition": [-48, -5],
        "textframe": [8, 4],
        "fict": True,
    },
}

# SUBMERCADOS_NEWAVE = pd.DataFrame(
#     data={
#         "submercado": [0, 1, 2, 3, 4, 11],
#         "nome": ["EXPORTACAO", "SE/CO", "S", "NE", "N", "NOFICT"],
#     }
# )


# INTERCAMBIOS_SUBMERCADOS_NEWAVE = pd.DataFrame(
#     data={
#         "source": ["S", "S", "NE", "NOFICT", "N", "NE"],
#         "target": [
#             "EXPORTACAO",
#             "SE/CO",
#             "SE/CO",
#             "SE/CO",
#             "NOFICT",
#             "NOFICT",
#         ],
#         "label": [
#             "S_EXPORTACAO",
#             "S_SE/CO",
#             "NE_SE/CO",
#             "NOFICT_SE/CO",
#             "N_NOFICT",
#             "NE_NOFICT",
#         ],
#     }
# )


# NOS_SUBMERCADOS_NEWAVE = {
#     "EXPORTACAO": {
#         "pos": [-59, -29],
#         "color": "black",
#         "size": 10,
#         "textposition": [-64, -29],
#         "textframe": [8, 4],
#         "fict": True,
#     },
#     "SE/CO": {
#         "pos": [-48, -20],
#         "color": "white",
#         "size": 35,
#         "textposition": [-42, -23],
#         "textframe": [8, 4],
#         "fict": False,
#     },
#     "S": {
#         "pos": [-52, -28],
#         "color": "white",
#         "size": 35,
#         "textposition": [-46, -31],
#         "textframe": [8, 4],
#         "fict": False,
#     },
#     "NE": {
#         "pos": [-39, -8],
#         "color": "white",
#         "size": 35,
#         "textposition": [-33, -8],
#         "textframe": [8, 4],
#         "fict": False,
#     },
#     "N": {
#         "pos": [-60, -3],
#         "color": "white",
#         "size": 35,
#         "textposition": [-67, -4],
#         "textframe": [8, 4],
#         "fict": False,
#     },
#     "NOFICT": {
#         "pos": [-48, -10],
#         "color": "black",
#         "size": 10,
#         "textposition": [-48, -5],
#         "textframe": [8, 4],
#         "fict": True,
#     },
# }

MAPA_NOMES_SUBMERCADOS = {
    "SE": "SE/CO",
    "NE": "NE",
    "S": "S",
    "N": "N",
    "FC": "NOFICT",
    "SUDESTE": "SE/CO",
    "NORDESTE": "NE",
    "SUL": "S",
    "NORTE": "N",
    "NOFICT1": "NOFICT",
}
