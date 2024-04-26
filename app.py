import panel as pn
from hvplot import hvPlot
import pandas as pd
import numpy as np
import param
from typing import Optional

pn.extension(design="material", template="fast")

data_file_sin = "/home/rogerio/git/visualizador-pem/data/newave/sintese/ESTATISTICAS_OPERACAO_SIN.parquet"
data_sin = pd.read_parquet(data_file_sin)

MAPA_NOMES = {
    "estagio": "Estágio",
    "data_inicio": "Data Início",
    "valor": "VARM (hm3)",
}


def view_timeseries(
    data: pd.DataFrame, x_axis: str, y_axis: str, color: Optional[str] = None
):
    return hvPlot(data).line(
        x=x_axis,
        y=y_axis,
        by=color,
        title="Evolução do VARM SIN",
        xlabel=MAPA_NOMES[x_axis],
        ylabel=MAPA_NOMES[y_axis],
        legend="bottom_right",
        width=800,
        height=400,
        persist=True,
    )


def plot_sin_distribution(
    data: pd.DataFrame,
    variable="data_inicio",
    lower_perc=10,
    upper_perc=90,
    view_fn=view_timeseries,
):
    special_names = {
        0: "min",
        50: "median",
        100: "max",
    }
    lower_col = (
        f"p{lower_perc}"
        if lower_perc not in [0, 50, 100]
        else special_names[lower_perc]
    )
    upper_col = (
        f"p{upper_perc}"
        if upper_perc not in [0, 50, 100]
        else special_names[upper_perc]
    )
    mean_data = data.loc[
        data["cenario"].isin([lower_col, "mean", upper_col])
        & (data["variavel"] == "VARMF")
    ]
    return view_fn(mean_data, variable, "valor", color="cenario")


class TimeseriesEvolution(param.Parameterized):
    variable = param.Selector(
        default="data_inicio", objects=list(data_sin.columns)
    )
    lower_percentile = param.Integer(default=10, bounds=(0, 100), step=5)
    upper_percentile = param.Integer(default=90, bounds=(0, 100), step=5)

    def view(self):
        return plot_sin_distribution(
            data_sin,
            self.variable,
            self.lower_percentile,
            self.upper_percentile,
            view_fn=view_timeseries,
        )


obj_sin = TimeseriesEvolution()
obj_sin2 = TimeseriesEvolution()

pn.Column(
    pn.Row(obj_sin.param, obj_sin.view),
    pn.Row(obj_sin2.param, obj_sin2.view),
).servable()
