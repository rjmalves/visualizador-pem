import panel as pn
from hvplot import hvPlot
import pandas as pd
import numpy as np
import param
from typing import Optional

pn.extension(design="material", template="fast")

data_file_sin = (
    "/home/rogerio/git/visualizador-pem/data/newave/EARPF_SIN_EST.parquet.gzip"
)
data_sin = pd.read_parquet(data_file_sin)

data_file_sbm = (
    "/home/rogerio/git/visualizador-pem/data/newave/CMO_SBM_EST.parquet.gzip"
)
data_sbm = pd.read_parquet(data_file_sbm)

MAPA_NOMES = {
    "estagio": "Estágio",
    "dataInicio": "Data Início",
    "valor": "EARM (%)",
}


def view_timeseries(
    data: pd.DataFrame, x_axis: str, y_axis: str, color: Optional[str] = None
):
    return hvPlot(data).line(
        x=x_axis,
        y=y_axis,
        by=color,
        title="Evolução do EARM SIN",
        xlabel=MAPA_NOMES[x_axis],
        ylabel=MAPA_NOMES[y_axis],
        legend="bottom_right",
        width=800,
        height=400,
        persist=True,
    )


def plot_sin_distribution(
    data: pd.DataFrame,
    variable="dataInicio",
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
    mean_data = data.loc[data["cenario"].isin([lower_col, "mean", upper_col])]
    return view_fn(mean_data, variable, "valor", color="cenario")


def plot_sbm_mean(
    data: pd.DataFrame,
    variable="dataInicio",
    view_fn=view_timeseries,
):
    mean_data = data.loc[data["cenario"].isin(["mean"])]
    return view_fn(mean_data, variable, "valor", color="submercado")


class TimeseriesEvolution(param.Parameterized):
    variable = param.Selector(
        default="dataInicio", objects=list(data_sin.columns)
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


class TimeseriesEvolutionSBM(param.Parameterized):
    variable = param.Selector(
        default="dataInicio", objects=list(data_sbm.columns)
    )
    lower_percentile = param.Integer(default=10, bounds=(0, 100), step=5)
    upper_percentile = param.Integer(default=90, bounds=(0, 100), step=5)

    def view(self):
        return plot_sbm_mean(
            data_sbm,
            self.variable,
            view_fn=view_timeseries,
        )


obj_sin = TimeseriesEvolution()
obj_sbm = TimeseriesEvolutionSBM()

pn.Column(
    pn.Row(obj_sin.param, obj_sin.view),
    pn.Row(obj_sbm.param, obj_sbm.view),
).servable()
