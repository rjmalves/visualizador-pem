import pandas as pd

VARIABLE_UNITS = {
    "EARPF": "%",
    "GHID": "MWmed",
    "GTER": "MWmed",
    "MERL": "MWmed",
    "EVER": "MWmed",
    "INT": "MWmed",
    "CMO": "R$/MWh",
}

VARIABLE_NAMES = {
    "EARPF": "Energia Armazenada",
    "GHID": "Ger. Hidráulica",
    "GTER": "Ger. Térmica",
    "MERL": "Mercado Líq.",
    "EVER": "Energia Vert.",
    "INT": "Intercâmbio",
    "CMO": "CMO",
}

MAPA_NOMES_SUBMERCADOS = {
    "SE": "SE/CO",
    "NE": "NE",
    "S": "S",
    "N": "N",
    "FC": "NOFICT",
    "IV": "IV",
    "SUDESTE": "SE/CO",
    "NORDESTE": "NE",
    "SUL": "S",
    "NORTE": "N",
    "NOFICT1": "NOFICT",
}

SUBMERCADOS_NEWAVE = pd.DataFrame(
    data={
        "submercado": [1, 2, 3, 4, 11],
        "nome": ["SE/CO", "S", "NE", "N", "NOFICT"],
    }
)

INTERCAMBIOS_SUBMERCADOS_NEWAVE = pd.DataFrame(
    data={
        "source": ["S", "N", "NE", "NOFICT", "N", "NE"],
        "target": [
            "SE/CO",
            "SE/CO",
            "SE/CO",
            "SE/CO",
            "NOFICT",
            "NOFICT",
        ],
        "label": [
            "S_SE/CO",
            "N_SE/CO",
            "NE_SE/CO",
            "NOFICT_SE/CO",
            "N_NOFICT",
            "NE_NOFICT",
        ],
    }
)


NOS_SUBMERCADOS_NEWAVE = {
    "SE/CO": {
        "pos": [-48, -20],
        "color": "white",
        "size": 35,
        "textposition": [-38, -23],
        "textframe": [13, 6],
        "fict": False,
    },
    "S": {
        "pos": [-52, -28],
        "color": "white",
        "size": 35,
        "textposition": [-42, -31],
        "textframe": [13, 6],
        "fict": False,
    },
    "NE": {
        "pos": [-39, -8],
        "color": "white",
        "size": 35,
        "textposition": [-29, -8],
        "textframe": [13, 6],
        "fict": False,
    },
    "N": {
        "pos": [-64, -5],
        "color": "white",
        "size": 35,
        "textposition": [-74, -4],
        "textframe": [13, 6],
        "fict": False,
    },
    "NOFICT": {
        "pos": [-48, -10],
        "color": "black",
        "size": 10,
        "textposition": [-46, -5],
        "textframe": [13, 6],
        "fict": True,
    },
}


ARESTAS_INTERCAMBIOS_NEWAVE = {
    ("S", "SE/CO"): {
        "color": "white",
        "textposition": [-55, -24],
        "textframe": [7.5, 2],
    },
    ("NE", "SE/CO"): {
        "color": "white",
        "textposition": [-39, -15],
        "textframe": [7.5, 2],
    },
    ("N", "SE/CO"): {
        "color": "white",
        "textposition": [-60, -14],
        "textframe": [7.5, 2],
    },
    ("NOFICT", "SE/CO"): {
        "color": "white",
        "textposition": [-52, -12],
        "textframe": [7.5, 2],
    },
    ("N", "NOFICT"): {
        "color": "white",
        "textposition": [-54, -5.5],
        "textframe": [7.5, 2],
    },
    ("NE", "NOFICT"): {
        "color": "black",
        "textposition": [-45, -7],
        "textframe": [7.5, 2],
    },
}


SUBMERCADOS_DECOMP = pd.DataFrame(
    data={
        "submercado": [1, 2, 3, 4, 11, 0],
        "nome": ["SE/CO", "S", "NE", "N", "NOFICT", "IV"],
    }
)


INTERCAMBIOS_SUBMERCADOS_DECOMP = pd.DataFrame(
    data={
        "source": ["S", "IV", "NOFICT", "NE", "N", "N", "NE"],
        "target": [
            "IV",
            "SE/CO",
            "SE/CO",
            "SE/CO",
            "SE/CO",
            "NOFICT",
            "NOFICT",
        ],
        "label": [
            "S_IV",
            "IV_SE/CO",
            "NOFICT_SE/CO",
            "NE_SE/CO",
            "N_SE/CO",
            "N_NOFICT",
            "NE_NOFICT",
        ],
    }
)


NOS_SUBMERCADOS_DECOMP = {
    "SE/CO": {
        "pos": [-48, -20],
        "color": "white",
        "size": 35,
        "textposition": [-38, -23],
        "textframe": [13, 6],
        "fict": False,
    },
    "S": {
        "pos": [-53, -29],
        "color": "white",
        "size": 30,
        "textposition": [-42, -31],
        "textframe": [13, 6],
        "fict": False,
    },
    "NE": {
        "pos": [-39, -8],
        "color": "white",
        "size": 35,
        "textposition": [-29, -8],
        "textframe": [13, 6],
        "fict": False,
    },
    "N": {
        "pos": [-64, -5],
        "color": "white",
        "size": 35,
        "textposition": [-74, -4],
        "textframe": [13, 6],
        "fict": False,
    },
    "NOFICT": {
        "pos": [-48, -10],
        "color": "black",
        "size": 10,
        "textposition": [-46, -5],
        "textframe": [13, 6],
        "fict": True,
    },
    "IV": {
        "pos": [-51, -24],
        "color": "black",
        "size": 10,
        "textposition": [-48, -5],
        "textframe": [11, 6],
        "fict": True,
    },
}

ARESTAS_INTERCAMBIOS_DECOMP = {
    ("S", "IV"): {
        "color": "white",
        "textposition": [-56.5, -25],
        "textframe": [7.5, 2],
    },
    ("IV", "SE/CO"): {
        "color": "white",
        "textposition": [-54, -21],
        "textframe": [7.5, 2],
    },
    ("NE", "SE/CO"): {
        "color": "white",
        "textposition": [-39, -15],
        "textframe": [7.5, 2],
    },
    ("N", "SE/CO"): {
        "color": "white",
        "textposition": [-60, -14],
        "textframe": [7.5, 2],
    },
    ("NOFICT", "SE/CO"): {
        "color": "white",
        "textposition": [-52, -12],
        "textframe": [7.5, 2],
    },
    ("N", "NOFICT"): {
        "color": "white",
        "textposition": [-54, -5.5],
        "textframe": [7.5, 2],
    },
    ("NE", "NOFICT"): {
        "color": "black",
        "textposition": [-45, -7],
        "textframe": [7.5, 2],
    },
}
