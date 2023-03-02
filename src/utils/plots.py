import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import List
from datetime import timedelta
from src.utils.log import Log
from src.utils.data import DISCRETE_COLOR_PALLETE

DISCRETE_COLOR_PALLETE_COSTS = [
    "rgba(249, 65, 68, 1)",
    "rgba(144, 190, 109, 1)",
    "rgba(243, 114, 44, 1)",
    "rgba(249, 199, 79, 1)",
    "rgba(249, 132, 74, 1)",
    "rgba(39, 125, 161, 1)",
    "rgba(67, 170, 139, 1)",
    "rgba(248, 150, 30, 1)",
    "rgba(77, 144, 142, 1)",
    "rgba(87, 117, 144, 1)",
]


VARIABLE_NAMES = {
    "COP": "Custo de Operação",
    "CFU": "Custo Futuro",
    "CMO": "Custo Marginal de Operação",
    "CTER": "Custo de Geração Térmica",
    "DEF": "Déficit",
    "EARMI": "Energia Armazenada Inicial",
    "EARPI": "Energia Armazenada Inicial",
    "EARMF": "Energia Armazenada Final",
    "EARPF": "Energia Armazenada Final",
    "ENAA": "Energia Natural Afluente",
    "ENAM": "Energia Natural Afluente",
    "EVER": "Energia Vertida",
    "EVERNT": "Energia Vertida Não-Turbinável",
    "EVERT": "Energia Vertida Turbinável",
    "EVERR": "Energia Vertida em Reservatórios",
    "EVERF": "Energia Vertida Fio d'Água",
    "EVERRT": "Energia Vertida em Reservatórios Turbinável",
    "EVERRNT": "Energia Vertida em Reservatórios Não-Turbinável",
    "EVERFT": "Energia Vertida Fio d'Água Turbinável",
    "EVERFNT": "Energia Vertida Fio d'Água Não-Turbinável",
    "GHID": "Geração Hidráulica",
    "GTER": "Geração Térmica",
    "GEOL": "Geração Eólica",
    "INT": "Intercâmbio",
    "MER": "Mercado",
    "QAFL": "Vazão Afluente",
    "QDEF": "Vazão Defluente",
    "QINC": "Vazão Afluente Incremental",
    "QTUR": "Vazão Turbinada",
    "QVER": "Vazão Vertida",
    "VAGUA": "Valor da Água",
    "VARMI": "Volume Armazenado Inicial",
    "VARMF": "Volume Armazenado Final",
    "VARPI": "Volume Armazenado Inicial",
    "VARPF": "Volume Armazenado Final",
    "VTUR": "Volume Turbinado",
    "VVER": "Volume Vertido",
    "VENTO": "Velocidade do Vento",
}

SPATIAL_RES_NAMES = {
    "SIN": "SIN",
    "SBM": "Submercado",
    "SBP": "Submercados",
    "REE": "REE",
    "PEE": "PEE",
    "UHE": "UHE",
    "UTE": "UTE",
    "UEE": "UEE",
}

SPATIAL_RES_FILTER_NAMES = {
    "SIN": "SIN",
    "SBM": "submercado",
    "REE": "ree",
    "PEE": "pee",
    "UHE": "usina",
    "UTE": "usina",
    "UEE": "usina",
}

TEMPORAL_RES_NAMES = {"PAT": "Patamar"}

TEMPORAL_RES_FILTER_NAMES = {"PAT": "patamar"}

VARIABLE_UNITS = {
    "COP": "R$",
    "CFU": "R$",
    "CMO": "R$ / MWh",
    "CTER": "R$",
    "DEF": "MWmed",
    "EARMI": "MWmed",
    "EARPI": "%",
    "EARMF": "MWmed",
    "EARPF": "%",
    "ENAA": "MWmed",
    "ENAM": "%",
    "EVER": "MWmed",
    "EVERT": "MWmed",
    "EVERNT": "MWmed",
    "EVERR": "MWmed",
    "EVERRT": "MWmed",
    "EVERRNT": "MWmed",
    "EVERF": "MWmed",
    "EVERFT": "MWmed",
    "EVERFNT": "MWmed",
    "GHID": "MWmed",
    "GTER": "MWmed",
    "GEOL": "MWmed",
    "INT": "MWmed",
    "MER": "MWmed",
    "QAFL": "m3/s",
    "QDEF": "m3/s",
    "QINC": "m3/s",
    "QTUR": "m3/s",
    "QVER": "m3/s",
    "VAGUA": "R$ / hm3",
    "VARMI": "hm3",
    "VARMF": "hm3",
    "VARPI": "%",
    "VARPF": "%",
    "VTUR": "hm3",
    "VVER": "hm3",
    "VENTO": "m/s",
}

NOT_SCENARIO_COLUMNS = [
    "iteracao",
    "estudo",
    "caso",
    "estagio",
    "submercado",
    "submercadoDe",
    "submercadoPara",
    "ree",
    "pee",
    "usina",
    "patamar",
    "dataInicio",
    "dataFim",
]


def pivot_df_for_plot(df: pd.DataFrame) -> pd.DataFrame:
    index_cols = [c for c in df.columns if c in NOT_SCENARIO_COLUMNS]
    df_plot = df.pivot(index=index_cols, columns="cenario", values="valor")
    return df_plot.reset_index()


def hex_to_rgb(value):
    value = value.lstrip("#")
    lv = len(value)
    return tuple(
        int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3)
    )


def generate_operation_graph_casos(
    operation_data, variable, filters, studies_data
):
    graph_layout = go.Layout(
        plot_bgcolor="rgba(158, 149, 128, 0.2)",
        paper_bgcolor="rgba(255,255,255,1)",
    )
    fig = go.Figure()
    fig.update_layout(graph_layout)
    if operation_data is None:
        return fig
    dados = pd.read_json(operation_data, orient="split")
    dados["dataInicio"] = pd.to_datetime(dados["dataInicio"], unit="ms")
    dados["dataFim"] = pd.to_datetime(dados["dataFim"], unit="ms")
    df_estudos = pd.read_json(studies_data, orient="split")

    line_shape = "hv"

    visibilidade_p = __background_area_visibility(df_estudos["name"])
    for _, linha_df in df_estudos.iterrows():
        estudo = linha_df["name"]
        rgb = hex_to_rgb(linha_df["color"])
        cor = f"rgba({rgb[0]},{rgb[1]},{rgb[2]}, 1.0)"
        cor_fundo = f"rgba({rgb[0]},{rgb[1]},{rgb[2]}, 0.3)"
        if dados is not None:
            dados_estudo = pivot_df_for_plot(
                dados.loc[dados["estudo"] == estudo]
            )
            if not dados_estudo.empty:
                dados_estudo = __add_final_date_line_to_df(dados_estudo)
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo["dataInicio"],
                        y=dados_estudo["mean"],
                        line={
                            "color": cor,
                            "width": 3,
                            "shape": line_shape,
                        },
                        name=estudo,
                        legendgroup="mean",
                        legendgrouptitle_text="mean",
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo["dataInicio"],
                        y=dados_estudo["p10"],
                        line_color=cor_fundo,
                        line_shape=line_shape,
                        legendgroup="p10",
                        legendgrouptitle_text="p10",
                        name=estudo,
                        visible=visibilidade_p,
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo["dataInicio"],
                        y=dados_estudo["p90"],
                        line_color=cor_fundo,
                        fillcolor=cor_fundo,
                        line_shape=line_shape,
                        fill="tonexty",
                        legendgroup="p90",
                        legendgrouptitle_text="p90",
                        name=estudo,
                        visible=visibilidade_p,
                    )
                )

    if variable is not None:
        fig.update_layout(
            title=__make_operation_plot_title(variable, filters),
            xaxis_title="Data",
            yaxis_title=VARIABLE_UNITS.get(variable.split("_")[0], ""),
            hovermode="x unified",
            legend=dict(groupclick="toggleitem"),
        )
    return fig


def generate_operation_graph_casos_twinx(
    operation_data,
    variable,
    filters,
    operation_data_twinx,
    variable_twinx,
    filters_twinx,
    studies_data,
):

    graph_layout = go.Layout(
        plot_bgcolor="rgba(158, 149, 128, 0.2)",
        paper_bgcolor="rgba(255,255,255,1)",
    )
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.update_layout(graph_layout)
    if operation_data is None and operation_data_twinx is None:
        return fig
    if operation_data is not None and operation_data_twinx is None:
        return generate_operation_graph_casos(
            operation_data, variable, filters, studies_data
        )
    elif operation_data is None and operation_data_twinx is not None:
        return generate_operation_graph_casos(
            operation_data_twinx, variable_twinx, filters_twinx, studies_data
        )

    dados = pd.read_json(operation_data, orient="split")
    dados["dataInicio"] = pd.to_datetime(dados["dataInicio"], unit="ms")
    dados["dataFim"] = pd.to_datetime(dados["dataFim"], unit="ms")
    dados_twinx = pd.read_json(operation_data_twinx, orient="split")
    dados_twinx["dataInicio"] = pd.to_datetime(
        dados_twinx["dataInicio"], unit="ms"
    )
    dados_twinx["dataFim"] = pd.to_datetime(dados_twinx["dataFim"], unit="ms")
    df_estudos = pd.read_json(studies_data, orient="split")

    line_shape = "hv"
    visibilidade_p = __background_area_visibility(df_estudos["name"])
    for _, linha_df in df_estudos.iterrows():
        estudo = linha_df["name"]
        rgb = hex_to_rgb(linha_df["color"])
        cor = f"rgba({rgb[0]},{rgb[1]},{rgb[2]}, 1.0)"
        cor_fundo = f"rgba({rgb[0]},{rgb[1]},{rgb[2]}, 0.3)"
        dados_estudo = pivot_df_for_plot(dados.loc[dados["estudo"] == estudo])
        dados_legend = __make_operation_plot_legend_name(
            df_estudos["name"].tolist(), estudo, variable, filters
        )
        dados_twinx_legend = __make_operation_plot_legend_name(
            df_estudos["name"].tolist(), estudo, variable_twinx, filters_twinx
        )
        if not dados_estudo.empty:
            dados_estudo = __add_final_date_line_to_df(dados_estudo)

            fig.add_trace(
                go.Scatter(
                    x=dados_estudo["dataInicio"],
                    y=dados_estudo["mean"],
                    line={
                        "color": cor,
                        "width": 3,
                        "shape": line_shape,
                    },
                    name="mean",
                    legendgroup=dados_legend,
                    legendgrouptitle_text=dados_legend,
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=dados_estudo["dataInicio"],
                    y=dados_estudo["p10"],
                    line_color=cor_fundo,
                    line_shape=line_shape,
                    name="p10",
                    legendgroup=dados_legend,
                    visible=visibilidade_p,
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=dados_estudo["dataInicio"],
                    y=dados_estudo["p90"],
                    line_color=cor_fundo,
                    fillcolor=cor_fundo,
                    line_shape=line_shape,
                    fill="tonexty",
                    name="p90",
                    legendgroup=dados_legend,
                    visible=visibilidade_p,
                )
            )

        dados_estudo = pivot_df_for_plot(
            dados_twinx.loc[dados_twinx["estudo"] == estudo]
        )
        if not dados_estudo.empty:
            dados_estudo = __add_final_date_line_to_df(dados_estudo)
            fig.add_trace(
                go.Scatter(
                    x=dados_estudo["dataInicio"],
                    y=dados_estudo["mean"],
                    line={
                        "color": cor,
                        "width": 3,
                        "shape": line_shape,
                        "dash": "dash",
                    },
                    name="mean",
                    legendgroup=dados_twinx_legend,
                    legendgrouptitle_text=dados_twinx_legend,
                ),
                secondary_y=True,
            )
            fig.add_trace(
                go.Scatter(
                    x=dados_estudo["dataInicio"],
                    y=dados_estudo["p10"],
                    line_color=cor_fundo,
                    line_shape=line_shape,
                    name="p10",
                    legendgroup=dados_twinx_legend,
                    visible=visibilidade_p,
                ),
                secondary_y=True,
            )
            fig.add_trace(
                go.Scatter(
                    x=dados_estudo["dataInicio"],
                    y=dados_estudo["p90"],
                    line_color=cor_fundo,
                    fillcolor=cor_fundo,
                    line_shape=line_shape,
                    fill="tonexty",
                    fillpattern=go.scatter.Fillpattern(
                        bgcolor=cor_fundo, shape="."
                    ),
                    name="p90",
                    legendgroup=dados_twinx_legend,
                    visible=visibilidade_p,
                ),
                secondary_y=True,
            )

    full_title = (
        f"{__make_operation_plot_title(variable, filters)}"
        + f" | {__make_operation_plot_title(variable_twinx, filters_twinx)}"
    )
    fig.update_layout(
        title=full_title,
        xaxis_title="Data",
        yaxis_title=VARIABLE_UNITS.get(variable.split("_")[0], ""),
        hovermode="x unified",
        legend=dict(groupclick="toggleitem"),
    )
    fig.update_yaxes(
        title_text=VARIABLE_UNITS.get(variable_twinx.split("_")[0], ""),
        secondary_y=True,
    )

    return fig


def generate_operation_graph_encadeador(
    operation_data, variable: str, filters: dict, studies_data
):
    graph_layout = go.Layout(
        plot_bgcolor="rgba(158, 149, 128, 0.2)",
        paper_bgcolor="rgba(255, 255, 255, 1)",
    )
    fig = go.Figure()
    fig.update_layout(graph_layout)
    if operation_data is None:
        return fig
    Log.log().info(f"Plotando gráfico - ENCADEADOR ({variable}, {filters})")
    dados = pd.read_json(operation_data, orient="split")
    dados["dataInicio"] = pd.to_datetime(dados["dataInicio"], unit="ms")
    dados["dataFim"] = pd.to_datetime(dados["dataFim"], unit="ms")
    df_estudos = pd.read_json(studies_data, orient="split")

    filtro_newave = dados["programa"] == "NEWAVE"
    filtro_decomp = dados["programa"] == "DECOMP"
    df_newave = dados.loc[filtro_newave]
    df_decomp = dados.loc[filtro_decomp]

    visibilidade_newave = __background_area_visibility(df_estudos["name"])
    for _, linha_df in df_estudos.iterrows():
        estudo = linha_df["name"]
        rgb = hex_to_rgb(linha_df["color"])
        cor = f"rgba({rgb[0]},{rgb[1]},{rgb[2]}, 1.0)"
        cor_fundo = f"rgba({rgb[0]},{rgb[1]},{rgb[2]}, 0.3)"
        if df_decomp is not None:
            estudo_decomp = pivot_df_for_plot(
                df_decomp.loc[df_decomp["estudo"] == estudo]
            )
            if not estudo_decomp.empty:
                fig.add_trace(
                    go.Scatter(
                        x=estudo_decomp["dataFim"],
                        y=estudo_decomp["mean"],
                        line={
                            "color": cor,
                            "width": 3,
                        },
                        name=estudo,
                        legendgroup="DECOMP",
                        legendgrouptitle_text="DECOMP",
                    )
                )
        if df_newave is not None:
            estudo_newave = pivot_df_for_plot(
                df_newave.loc[df_newave["estudo"] == estudo]
            )
            if not estudo_newave.empty:
                fig.add_trace(
                    go.Scatter(
                        x=estudo_newave["dataFim"],
                        y=estudo_newave["mean"],
                        line={
                            "color": cor,
                            "dash": "dot",
                            "width": 2,
                        },
                        mode="lines",
                        name=estudo,
                        legendgroup="NEWAVEm",
                        legendgrouptitle_text="NEWAVEm",
                        visible=visibilidade_newave,
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=estudo_newave["dataFim"],
                        y=estudo_newave["p10"],
                        line_color=cor_fundo,
                        mode="lines",
                        legendgroup="NEWAVEp10",
                        legendgrouptitle_text="NEWAVEp10",
                        name=estudo,
                        visible=visibilidade_newave,
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=estudo_newave["dataFim"],
                        y=estudo_newave["p90"],
                        line_color=cor_fundo,
                        fillcolor=cor_fundo,
                        mode="lines",
                        fill="tonexty",
                        legendgroup="NEWAVEp90",
                        legendgrouptitle_text="NEWAVEp90",
                        name=estudo,
                        visible=visibilidade_newave,
                    )
                )
    if variable is not None:
        fig.update_layout(
            title=__make_operation_plot_title(variable, filters),
            xaxis_title="Data",
            yaxis_title=VARIABLE_UNITS.get(variable.split("_")[0], ""),
            hovermode="x unified",
            legend=dict(groupclick="toggleitem"),
        )
    Log.log().info(f"Gráfico plotado - ENCADEADOR ({variable}, {filters})")
    return fig


def generate_operation_graph_ppq(
    operation_data, variable, filters, studies_data
):
    graph_layout = go.Layout(
        plot_bgcolor="rgba(158, 149, 128, 0.2)",
        paper_bgcolor="rgba(255,255,255,1)",
    )
    fig = go.Figure()
    fig.update_layout(graph_layout)
    if operation_data is None:
        return fig
    dados = pd.read_json(operation_data, orient="split")
    dados["dataInicio"] = pd.to_datetime(dados["dataInicio"], unit="ms")
    dados["dataFim"] = pd.to_datetime(dados["dataFim"], unit="ms")

    line_shape = "linear"

    dados = dados.loc[dados["estudo"] == filters["estudo"]]

    if dados is not None:
        iteracoes = sorted(dados["iteracao"].unique().tolist())
        visibilidade_p = "legendonly" if len(iteracoes) > 2 else None
        for i, iteracao in enumerate(iteracoes):
            rgb = hex_to_rgb(
                DISCRETE_COLOR_PALLETE[i % len(DISCRETE_COLOR_PALLETE)]
            )
            cor = f"rgba({rgb[0]},{rgb[1]},{rgb[2]}, 1.0)"
            cor_fundo = f"rgba({rgb[0]},{rgb[1]},{rgb[2]}, 0.3)"
            dados_estudo = pivot_df_for_plot(
                dados.loc[dados["iteracao"] == iteracao]
            )
            nome = f"it {iteracao}"
            if not dados_estudo.empty:
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo["dataInicio"],
                        y=dados_estudo["mean"],
                        line={
                            "color": cor,
                            "width": 3,
                            "shape": line_shape,
                        },
                        name=nome,
                        legendgroup="mean",
                        legendgrouptitle_text="mean",
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo["dataInicio"],
                        y=dados_estudo["p10"],
                        line_color=cor_fundo,
                        line_shape=line_shape,
                        legendgroup="p10",
                        legendgrouptitle_text="p10",
                        name=nome,
                        visible=visibilidade_p,
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo["dataInicio"],
                        y=dados_estudo["p90"],
                        line_color=cor_fundo,
                        fillcolor=cor_fundo,
                        line_shape=line_shape,
                        fill="tonexty",
                        legendgroup="p90",
                        legendgrouptitle_text="p90",
                        name=nome,
                        visible=visibilidade_p,
                    )
                )

    if variable is not None:
        fig.update_layout(
            title=__make_operation_plot_title(variable, filters),
            xaxis_title="Data",
            yaxis_title=VARIABLE_UNITS.get(variable.split("_")[0], ""),
            hovermode="x unified",
            legend=dict(groupclick="toggleitem"),
        )
    return fig


def generate_distribution_graph_ppq(
    operation_data, variable, filters, studies_data
):
    graph_layout = go.Layout(
        plot_bgcolor="rgba(158, 149, 128, 0.2)",
        paper_bgcolor="rgba(255,255,255,1)",
    )
    fig = go.Figure()
    fig.update_layout(graph_layout)
    if operation_data is None:
        return fig
    dados = pd.read_json(operation_data, orient="split")
    df_estudos = pd.read_json(studies_data, orient="split")
    mapa_cor = {
        linha["name"]: linha["color"] for _, linha in df_estudos.iterrows()
    }
    ordem_estudos = dados["estudo"].unique().tolist()
    fig = px.box(
        dados,
        x="iteracao",
        y="valor",
        color="estudo",
        color_discrete_map=mapa_cor,
        category_orders={"estudo": ordem_estudos},
    )
    fig.update_layout(graph_layout)
    fig.update_layout(
        title=__make_operation_plot_title(variable, filters),
        xaxis_title="Iteracao",
        yaxis_title=VARIABLE_UNITS.get(variable.split("_")[0], ""),
        hovermode="x unified",
        legend=dict(groupclick="toggleitem"),
    )

    return fig


def __process_acumprob(operation_data: pd.DataFrame) -> pd.DataFrame:
    cols_scenarios = [
        c for c in operation_data.columns if c not in NOT_SCENARIO_COLUMNS
    ]
    all_scenarios = operation_data["cenario"].unique().tolist()
    stats_scenarios = ["mean", "min", "max", "median"] + [
        c for c in all_scenarios if "p" in str(c)
    ]
    vals = (
        operation_data.loc[
            ~operation_data["cenario"].isin(stats_scenarios), cols_scenarios
        ]
        .to_numpy()
        .flatten()
    )
    df = pd.DataFrame(data={"values": vals})
    df["cdf"] = df.rank(method="average", pct=True)
    return df.sort_values("values")


def generate_acumprob_graph_casos(
    operation_data, variable, filters, studies_data
):
    graph_layout = go.Layout(
        plot_bgcolor="rgba(158, 149, 128, 0.2)",
        paper_bgcolor="rgba(255,255,255,1)",
    )
    fig = go.Figure()
    fig.update_layout(graph_layout)
    if operation_data is None:
        return fig
    dados = pd.read_json(operation_data, orient="split")
    df_estudos = pd.read_json(studies_data, orient="split")
    line_shape = "hv"
    for _, linha_df in df_estudos.iterrows():
        estudo = linha_df["name"]
        rgb = hex_to_rgb(linha_df["color"])
        cor = f"rgba({rgb[0]},{rgb[1]},{rgb[2]}, 1.0)"
        if dados is not None:
            dados_estudo = dados.loc[dados["estudo"] == estudo]
            if not dados_estudo.empty:
                dados_estudo = __process_acumprob(dados_estudo)
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo["cdf"] * 100,
                        y=dados_estudo["values"],
                        line_color=cor,
                        line_shape=line_shape,
                        name=estudo,
                    )
                )

    if variable is not None:
        fig.update_layout(
            title=__make_operation_plot_title(variable, filters),
            xaxis_title="%",
            yaxis_title=VARIABLE_UNITS.get(variable.split("_")[0], ""),
            hovermode="x unified",
            legend=dict(groupclick="toggleitem"),
        )
    return fig


def generate_timecosts_graph_encadeador(time_costs, variable, studies_data):
    graph_layout = go.Layout(
        plot_bgcolor="rgba(158, 149, 128, 0.2)",
        paper_bgcolor="rgba(255,255,255,1)",
    )
    fig = go.Figure()
    fig.update_layout(graph_layout)
    if time_costs is None:
        return fig
    Log.log().info(f"Plotando gráfico - ENCADEADOR ({variable})")
    dados = pd.read_json(time_costs, orient="split")
    ordem_estudos = dados["estudo"].unique().tolist()
    df_estudos = pd.read_json(studies_data, orient="split")
    mapa_cor = {
        linha["name"]: linha["color"] for _, linha in df_estudos.iterrows()
    }
    if "etapa" in dados.columns:
        dados = dados.loc[dados["etapa"] == "Tempo Total", :]
        dados = (
            dados.groupby(["estudo", "caso"])
            .sum(numeric_only=True)
            .reset_index()
        )
        dados["tempo"] = pd.to_timedelta(dados["tempo"], unit="s") / timedelta(
            hours=1
        )
        dados["label"] = [
            str(timedelta(hours=d)) for d in dados["tempo"].tolist()
        ]
        y_col = "tempo"
        title = "Tempo de Execução"
        unit = "Tempo (horas)"
        error_y = None
    else:
        n_parcelas = len(dados["parcela"].unique().tolist())
        df_plot = pd.DataFrame()
        for estudo in ordem_estudos:
            df_estudo = dados.loc[dados["estudo"] == estudo]
            casos = df_estudo["caso"].unique().tolist()
            for c in casos:
                df_caso = df_estudo.loc[df_estudo["caso"] == c]
                n_linhas_caso = df_caso.shape[0]
                n_exec_caso = int(n_linhas_caso / n_parcelas)
                indice_inicial_caso = (n_exec_caso - 1) * n_parcelas
                indice_final = n_exec_caso * n_parcelas + 1
                df_plot = pd.concat(
                    [
                        df_plot,
                        df_caso.iloc[indice_inicial_caso:indice_final, :],
                    ],
                    ignore_index=True,
                )

        dados = df_plot
        dados = dados.loc[dados["mean"] > 0, :]
        dados = (
            dados.groupby(["estudo", "caso"])
            .sum(numeric_only=True)
            .reset_index()
        )
        dados["label"] = dados["mean"].round(2)
        y_col = "mean"
        title = "Custos de Operação"
        unit = "Custo ($)"
        error_y = "std"

    fig = px.bar(
        dados,
        x="caso",
        y=y_col,
        error_y=error_y,
        color="estudo",
        color_discrete_map=mapa_cor,
        text="label",
        category_orders={"estudo": ordem_estudos},
    )
    fig.update_layout(graph_layout)
    if variable is not None:
        fig.update_traces(textposition="inside")
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode="hide")
        fig.update_layout(
            title=title,
            yaxis_title=unit,
        )
    Log.log().info(f"Gráfico plotado - ENCADEADOR ({variable})")
    return fig


def generate_timecosts_graph_casos(time_costs, variable, studies_data):
    graph_layout = go.Layout(
        plot_bgcolor="rgba(158, 149, 128, 0.2)",
        paper_bgcolor="rgba(255,255,255,1)",
    )
    fig = go.Figure()
    fig.update_layout(graph_layout)
    if time_costs is None:
        return fig
    Log.log().info(f"Plotando gráfico - ENCADEADOR ({variable})")
    dados = pd.read_json(time_costs, orient="split")
    df_estudos = pd.read_json(studies_data, orient="split")
    mapa_cor = {
        linha["name"]: linha["color"] for _, linha in df_estudos.iterrows()
    }
    if "etapa" in dados.columns:
        dados = dados.loc[dados["etapa"] != "Tempo Total", :]
        dados["tempo"] = pd.to_timedelta(dados["tempo"], unit="s") / timedelta(
            hours=1
        )
        dados["label"] = [
            str(timedelta(hours=d)) for d in dados["tempo"].tolist()
        ]
        y_col = "tempo"
        color_col = "etapa"
        title = "Tempo de Execução"
        unit = "Tempo (horas)"
        error_y = None
    else:
        dados = dados.loc[dados["mean"] > 0, :]
        dados["label"] = dados["mean"]
        y_col = "mean"
        color_col = "parcela"
        title = "Custos de Operação"
        unit = "Custo ($)"
        error_y = "std"

    fig = px.bar(
        dados,
        x="estudo",
        y=y_col,
        error_y=error_y,
        color=color_col,
        color_discrete_map=mapa_cor,
        text="label",
    )
    fig.update_layout(graph_layout)
    if variable is not None:
        fig.update_traces(textposition="inside")
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode="hide")
        fig.update_layout(
            title=title,
            yaxis_title=unit,
        )
    Log.log().info(f"Gráfico plotado - ENCADEADOR ({variable})")
    return fig


def generate_violation_graph_encadeador(
    violation_data, violation, studies_data
):
    graph_layout = go.Layout(
        plot_bgcolor="rgba(158, 149, 128, 0.2)",
        paper_bgcolor="rgba(255,255,255,1)",
    )
    fig = go.Figure()
    fig.update_layout(graph_layout)
    if violation_data is None:
        return fig

    Log.log().info(f"Plotando gráfico - ENCADEADOR ({violation})")
    dados = pd.read_json(violation_data, orient="split")

    df_estudos = pd.read_json(studies_data, orient="split")
    mapa_cor = {
        linha["name"]: linha["color"] for _, linha in df_estudos.iterrows()
    }

    ordem_estudos = dados["estudo"].unique().tolist()
    if violation in ["TI", "RHQ", "RE", "RHE", "RHV"]:
        unit = str(dados["unidade"].tolist()[0])
        error_y = None
        # Grafico com montantes
        dados = (
            dados.groupby(["estudo", "caso"])
            .sum(numeric_only=True)
            .reset_index()
        )
        y_col = "violacao"
        title = f"Montante de Violação - {violation}"
    else:
        # Grafico com contagens
        unit = "Núm. Inviabilidades"
        error_y = None
        # Grafico com montantes
        dados = dados.groupby(["estudo", "caso"]).count().reset_index()
        y_col = "violacao"
        title = f"Número de Violações - {violation}"

    fig = px.bar(
        dados,
        x="caso",
        y=y_col,
        error_y=error_y,
        color="estudo",
        color_discrete_sequence=mapa_cor,
        category_orders={"estudo": ordem_estudos},
    )
    fig.update_layout(graph_layout)
    if violation is not None:
        fig.update_traces(textposition="inside")
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode="hide")
        fig.update_layout(
            title=title,
            yaxis_title=unit,
        )
    Log.log().info(f"Gráfico plotado - ENCADEADOR ({violation})")
    return fig


def generate_convergence_graph_casos(convergence_data, variable, studies_data):
    graph_layout = go.Layout(
        plot_bgcolor="rgba(158, 149, 128, 0.2)",
        paper_bgcolor="rgba(255,255,255,1)",
    )
    fig = go.Figure()
    fig.update_layout(graph_layout)
    if convergence_data is None or variable is None:
        return fig
    dados = pd.read_json(convergence_data, orient="split")
    if dados.empty:
        return fig
    dados["tempo"] = pd.to_timedelta(dados["tempo"], unit="s")
    dados["tempo"] /= timedelta(minutes=1)
    x_col = "iter"
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(x=dados[x_col], y=dados["tempo"], name="tempo"),
        secondary_y=True,
    )
    df_estudos = pd.read_json(studies_data, orient="split")
    mapa_cor = {
        linha["name"]: linha["color"] for _, linha in df_estudos.iterrows()
    }
    fig.update_layout(graph_layout)
    if variable is not None:
        if variable == "tempo":
            fig = px.bar(
                dados,
                x=x_col,
                y=variable,
                color="estudo",
                color_discrete_map=mapa_cor,
                barmode="group",
            )
            unit = "Tempo (minutos)"
        else:
            fig = px.line(
                dados,
                x=x_col,
                y=variable,
                color="estudo",
                color_discrete_map=mapa_cor,
            )
            unit = "" if variable != "dZinf" else "(%)"
        fig.update_layout(
            title=f"Convergência - {variable}",
            xaxis_title="iteração",
            hovermode="x unified",
        )
        fig.update_layout(graph_layout)
        fig.update_yaxes(
            title_text=unit,
        )
    return fig


def generate_resources_graph_casos(
    cluster_data, job_data, time_data, convergence_data, study
):
    graph_layout = go.Layout(
        plot_bgcolor="rgba(158, 149, 128, 0.2)",
        paper_bgcolor="rgba(255,255,255,1)",
    )
    fig = go.Figure()
    fig.update_layout(graph_layout)
    if cluster_data is None:
        return fig
    if job_data is None:
        return fig
    if time_data is None:
        return fig
    if convergence_data is None:
        return fig
    master = pd.read_json(cluster_data, orient="split")
    master = master.loc[master["estudo"] == study, :]
    job = pd.read_json(job_data, orient="split")
    job = job.loc[job["estudo"] == study, :]
    tim = pd.read_json(time_data, orient="split")
    tim = tim.loc[tim["estudo"] == study, :]
    conv = pd.read_json(convergence_data, orient="split")
    conv = conv.loc[conv["estudo"] == study, :]
    if master.empty:
        return fig
    if job.empty:
        return fig
    if tim.empty:
        return fig
    if conv.empty:
        return fig
    tim["tempo"] = pd.to_timedelta(tim["tempo"], unit="s")
    conv["tempo"] = pd.to_timedelta(conv["tempo"], unit="s")
    master["timeInstant"] = pd.to_datetime(master["timeInstant"], unit="ms")
    job["timeInstant"] = pd.to_datetime(job["timeInstant"])

    # Regra: se tem múltiplos jobs pro caso, pega o último
    if "jobId" in job.columns:
        jobIds = job["jobId"]
        if len(jobIds.dropna()) > 0:
            job = job.loc[
                job["jobId"] == job.at[job["timeInstant"].idxmax(), "jobId"]
            ]

    COLS_CALCULOS_INICIAIS = [
        "Leitura de Dados",
        "Calculos Iniciais",
    ]

    tempo_total_job = tim.loc[tim["etapa"] == "Tempo Total", "tempo"].tolist()[
        0
    ]
    tempo_antes_politica = tim.loc[
        tim["etapa"].isin(COLS_CALCULOS_INICIAIS), "tempo"
    ].sum()
    instante_inicial = job["timeInstant"].tolist()[0]
    instante_inicial_politica = instante_inicial + tempo_antes_politica
    instante_final = instante_inicial + tempo_total_job

    job = job.drop(job.loc[job["timeInstant"] < instante_inicial].index)
    master = master.drop(
        master.loc[master["timeInstant"] < instante_inicial].index
    )
    job = job.drop(job.loc[job["timeInstant"] > instante_final].index)
    master = master.drop(
        master.loc[master["timeInstant"] > instante_final].index
    )

    tempos_iteracoes = conv.loc[:, ["iter", "tempo"]]
    tempos_iteracoes["paridade"] = tempos_iteracoes["iter"] % 2
    instante_final_politica = (
        instante_inicial_politica + tempos_iteracoes["tempo"].sum()
    )
    tempos_iteracoes.loc[:, "timeInstant"] = tempos_iteracoes["tempo"].cumsum()

    tempos_iteracoes["timeInstant"] += instante_inicial_politica
    tempos_iteracoes_com_inicial = [
        instante_inicial_politica
    ] + tempos_iteracoes["timeInstant"].to_list()

    job["cpuDiff"] = [0.0] + list(
        job["cpuSeconds"].to_numpy()[1:] - job["cpuSeconds"].to_numpy()[:-1]
    )
    job["memDiff"] = [0.0] + list(
        job["memoryCpuSeconds"].to_numpy()[1:]
        - job["memoryCpuSeconds"].to_numpy()[:-1]
    )
    job["memoryPerCore"] = job["memDiff"] / job["cpuDiff"]

    max_y = 1.1 * master["totalMem"].max()

    area_calculos_iniciais_x = np.array(
        [instante_inicial, instante_inicial_politica]
    )
    area_calculos_iniciais_y = np.ones_like(area_calculos_iniciais_x) * max_y
    area_sf_x = np.array([instante_final_politica, instante_final])
    area_sf_y = np.ones_like(area_sf_x) * max_y

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.update_layout(graph_layout)
    fig.add_trace(
        go.Scatter(
            x=master["timeInstant"],
            y=master["totalMem"],
            name="totalMem",
            line={"color": "rgb(38, 70, 83)", "width": 2, "dash": "dash"},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=master["timeInstant"],
            y=master["cachedMem"],
            name="cachedMem",
            line={"color": "rgb(38, 70, 83)", "width": 2, "dash": "dot"},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=master["timeInstant"],
            y=master["freeMem"],
            name="freeMem",
            line={"color": "rgb(38, 70, 83)", "width": 2},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=job["timeInstant"],
            y=job["memoryPerCore"],
            name="memoryPerCore",
            line={"color": "rgb(231, 111, 81)", "width": 3},
        ),
        secondary_y=True,
    )

    fig.add_trace(
        go.Scatter(
            x=area_calculos_iniciais_x,
            y=area_calculos_iniciais_y,
            fill="tozeroy",
            line_color="rgba(42, 157, 143, 0.5)",
            fillcolor="rgba(42, 157, 143, 0.5)",
            name="CI",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=area_sf_x,
            y=area_sf_y,
            fill="tozeroy",
            line_color="rgba(42, 157, 143, 0.5)",
            fillcolor="rgba(42, 157, 143, 0.5)",
            name="SF",
        )
    )

    for i in range(1, len(tempos_iteracoes_com_inicial), 2):
        area_x = np.array(
            [
                tempos_iteracoes_com_inicial[i - 1],
                tempos_iteracoes_com_inicial[i],
            ]
        )
        area_y = np.ones_like(area_x) * max_y
        fig.add_trace(
            go.Scatter(
                x=area_x,
                y=area_y,
                fill="tozeroy",
                line_color="rgba(233, 197, 106, 0.5)",
                fillcolor="rgba(233, 197, 106, 0.5)",
                showlegend=i == 1,
                name="oddIterations",
                legendgroup="iterations",
            )
        )

    for i in range(2, len(tempos_iteracoes_com_inicial), 2):
        area_x = np.array(
            [
                tempos_iteracoes_com_inicial[i - 1],
                tempos_iteracoes_com_inicial[i],
            ]
        )
        area_y = np.ones_like(area_x) * max_y
        fig.add_trace(
            go.Scatter(
                x=area_x,
                y=area_y,
                fill="tozeroy",
                line_color="rgba(231, 111, 81, 0.5)",
                fillcolor="rgba(231, 111, 81, 0.5)",
                showlegend=i == 2,
                name="evenIterations",
                legendgroup="iterations",
            )
        )

    fig.update_yaxes(
        title_text="Memória - Master Node (GB)",
        range=[0, 1.1 * master["totalMem"].max()],
        secondary_y=False,
    )
    fig.update_yaxes(
        title_text="Memória por Processo (GB)",
        range=[0, 1.1 * job["memoryPerCore"].max()],
        secondary_y=True,
    )
    fig.update_layout(
        title=f"Uso de Recursos - {study}", hovermode="x unified"
    )
    return fig


def __make_operation_plot_title(variable: str, filters: dict) -> str:

    variable_data = variable.split("_")
    name = variable_data[0]
    spatial_res = variable_data[1]
    temporal_res = variable_data[2]

    full_name = VARIABLE_NAMES.get(name)
    full_spatial_res = SPATIAL_RES_NAMES.get(spatial_res)
    full_temporal_res = TEMPORAL_RES_NAMES.get(temporal_res)
    title = ""
    if full_name:
        title += full_name

    if spatial_res == "SIN":
        title += " - SIN"
    elif spatial_res == "SBP":
        sbm_de = filters["submercadoDe"].split("|")[0].strip("'")
        sbm_para = filters["submercadoPara"].split("|")[0].strip("'")
        title += f" - {full_spatial_res} {sbm_de} -> {sbm_para}"
    elif spatial_res == "SBM":
        sbm = filters["submercado"].split("|")[0].strip("'")
        title += f" - {full_spatial_res} {sbm}"
    elif full_spatial_res:
        title += f" - {full_spatial_res} {filters[SPATIAL_RES_FILTER_NAMES[spatial_res]]}"

    if temporal_res == "EST":
        pass
    elif full_temporal_res:
        title += f" - {full_temporal_res} {filters[TEMPORAL_RES_FILTER_NAMES[temporal_res]]}"

    if "estagio" in filters:
        title += f" - Estagio {filters['estagio']}"

    return title


def __background_area_visibility(estudos: list) -> str:
    return "legendonly" if len(estudos) > 2 else None


def __add_final_date_line_to_df(df: pd.DataFrame) -> pd.DataFrame:
    new_df = df.copy()
    last_index = df.index.tolist()[-1]
    new_df.loc[last_index + 1, :] = df.loc[last_index, :]
    new_df.loc[last_index + 1, "dataInicio"] = df.loc[last_index, "dataFim"]
    return new_df


def __make_operation_plot_legend_name(
    estudos: List[str], estudo: str, variable: str, filters: dict
) -> str:

    variable_data = variable.split("_")
    name = variable_data[0]
    spatial_res = variable_data[1]
    temporal_res = variable_data[2]

    legend = f"{estudo} - {name}" if len(estudos) > 1 else f"{name}"

    if spatial_res == "SIN":
        legend += " - SIN"
    elif spatial_res == "SBP":
        sbm_de = filters["submercadoDe"].split("|")[0].strip("'")
        sbm_para = filters["submercadoPara"].split("|")[0].strip("'")
        legend += f" - {spatial_res} {sbm_de} -> {sbm_para}"
    elif spatial_res == "SBM":
        sbm = filters["submercado"].split("|")[0].strip("'")
        legend += f" - SBM {sbm}"
    else:
        legend += f" - {spatial_res} {filters[SPATIAL_RES_FILTER_NAMES[spatial_res]]}"

    if temporal_res == "EST":
        pass
    else:
        legend += f" - {temporal_res} {filters[TEMPORAL_RES_FILTER_NAMES[temporal_res]]}"

    return legend
