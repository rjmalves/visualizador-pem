import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import List

DISCRETE_COLOR_PALLETE = [
    "rgba(249, 65, 68, 1)",
    "rgba(39, 125, 161, 1)",
    "rgba(144, 190, 109, 1)",
    "rgba(243, 114, 44, 1)",
    "rgba(87, 117, 144, 1)",
    "rgba(249, 199, 79, 1)",
    "rgba(248, 150, 30, 1)",
    "rgba(77, 144, 142, 1)",
    "rgba(249, 132, 74, 1)",
    "rgba(67, 170, 139, 1)",
]

DISCRETE_COLOR_PALLETE_BACKGROUND = [
    "rgba(249, 65, 68, 0.3)",
    "rgba(39, 125, 161, 0.3)",
    "rgba(144, 190, 109, 0.3)",
    "rgba(243, 114, 44, 0.3)",
    "rgba(87, 117, 144, 0.3)",
    "rgba(249, 199, 79, 0.3)",
    "rgba(248, 150, 30, 0.3)",
    "rgba(77, 144, 142, 0.3)",
    "rgba(249, 132, 74, 0.3)",
    "rgba(67, 170, 139, 0.3)",
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
    "EVERNT": "Energia Vertida Não-Turbinável",
    "EVERT": "Energia Vertida Turbinável",
    "GHID": "Geração Hidráulica",
    "GTER": "Geração Térmica",
    "GEOL": "Geração Eólica",
    "INT": "Intercâmbio",
    "MER": "Mercado",
    "QAFL": "Vazão Afluente",
    "QDEF": "Vazão Defluente",
    "QINC": "Vazão Afluente Incremental",
    "QTUR": "Vazão Turbinada",
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
    "UHE": "UHE",
    "UTE": "UTE",
    "UEE": "UEE",
}

SPATIAL_RES_FILTER_NAMES = {
    "SIN": "SIN",
    "SBM": "submercado",
    "REE": "ree",
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
    "EVERNT": "MWmed",
    "EVERT": "MWmed",
    "GHID": "MWmed",
    "GTER": "MWmed",
    "GEOL": "MWmed",
    "INT": "MWmed",
    "MER": "MWmed",
    "QAFL": "m3/s",
    "QDEF": "m3/s",
    "QINC": "m3/s",
    "QTUR": "m3/s",
    "VAGUA": "R$ / hm3",
    "VARMI": "hm3",
    "VARMF": "hm3",
    "VARPI": "%",
    "VARPF": "%",
    "VTUR": "hm3",
    "VVER": "hm3",
    "VENTO": "m/s",
}


def generate_operation_graph_casos(operation_data, variable, filters):
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
    estudos = dados["estudo"].unique().tolist()
    line_shape = "hv"

    visibilidade_p = __background_area_visibility(estudos)
    for i, estudo in enumerate(estudos):
        if dados is not None:
            dados_estudo = dados.loc[dados["estudo"] == estudo]
            if not dados_estudo.empty:
                dados_estudo = __add_final_date_line_to_df(dados_estudo)
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo["dataInicio"],
                        y=dados_estudo["mean"],
                        line={
                            "color": DISCRETE_COLOR_PALLETE[i],
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
                        y=dados_estudo["median"],
                        line={
                            "color": DISCRETE_COLOR_PALLETE[i],
                            "width": 3,
                            "dash": "dot",
                            "shape": line_shape,
                        },
                        name=estudo,
                        legendgroup="median",
                        legendgrouptitle_text="median",
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo["dataInicio"],
                        y=dados_estudo["p10"],
                        line_color=DISCRETE_COLOR_PALLETE_BACKGROUND[i],
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
                        line_color=DISCRETE_COLOR_PALLETE_BACKGROUND[i],
                        fillcolor=DISCRETE_COLOR_PALLETE_BACKGROUND[i],
                        line_shape=line_shape,
                        fill="tonexty",
                        legendgroup="p90",
                        legendgrouptitle_text="p90",
                        name=estudo,
                        visible=visibilidade_p,
                    )
                )
                if filters.get("cenario"):
                    cen = filters.get("cenario")
                    fig.add_trace(
                        go.Scatter(
                            x=dados_estudo["dataInicio"],
                            y=dados_estudo["cenario"],
                            line={
                                "color": DISCRETE_COLOR_PALLETE[i],
                                "width": 2,
                                "shape": line_shape,
                                "dash": "dash",
                            },
                            legendgroup=f"cenario {cen}",
                            legendgrouptitle_text=f"cenario {cen}",
                            name=estudo,
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
            operation_data, variable, filters
        )
    elif operation_data is None and operation_data_twinx is not None:
        return generate_operation_graph_casos(
            operation_data_twinx, variable_twinx, filters_twinx
        )

    dados = pd.read_json(operation_data, orient="split")
    dados["dataInicio"] = pd.to_datetime(dados["dataInicio"], unit="ms")
    dados["dataFim"] = pd.to_datetime(dados["dataFim"], unit="ms")
    estudos = dados["estudo"].unique().tolist()
    dados_twinx = pd.read_json(operation_data_twinx, orient="split")
    dados_twinx["dataInicio"] = pd.to_datetime(
        dados_twinx["dataInicio"], unit="ms"
    )
    dados_twinx["dataFim"] = pd.to_datetime(dados_twinx["dataFim"], unit="ms")
    estudos_twinx = dados_twinx["estudo"].unique().tolist()
    estudos_completos = list(set(estudos).union(set(estudos_twinx)))

    line_shape = "hv"
    next_color = 0
    visibilidade_p = __background_area_visibility(estudos)
    for i, estudo in enumerate(estudos_completos):
        dados_estudo = dados.loc[dados["estudo"] == estudo]
        dados_legend = __make_operation_plot_legend_name(
            estudos_completos, estudo, variable, filters
        )
        dados_twinx_legend = __make_operation_plot_legend_name(
            estudos_completos, estudo, variable_twinx, filters_twinx
        )
        if not dados_estudo.empty:
            dados_estudo = __add_final_date_line_to_df(dados_estudo)
            fig.add_trace(
                go.Scatter(
                    x=dados_estudo["dataInicio"],
                    y=dados_estudo["mean"],
                    line={
                        "color": DISCRETE_COLOR_PALLETE[next_color],
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
                    y=dados_estudo["median"],
                    line={
                        "color": DISCRETE_COLOR_PALLETE[next_color],
                        "width": 3,
                        "dash": "dot",
                        "shape": line_shape,
                    },
                    name="median",
                    legendgroup=dados_legend,
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=dados_estudo["dataInicio"],
                    y=dados_estudo["p10"],
                    line_color=DISCRETE_COLOR_PALLETE_BACKGROUND[next_color],
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
                    line_color=DISCRETE_COLOR_PALLETE_BACKGROUND[next_color],
                    fillcolor=DISCRETE_COLOR_PALLETE_BACKGROUND[next_color],
                    line_shape=line_shape,
                    fill="tonexty",
                    name="p90",
                    legendgroup=dados_legend,
                    visible=visibilidade_p,
                )
            )
            if filters.get("cenario"):
                cen = filters.get("cenario")
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo["dataInicio"],
                        y=dados_estudo["cenario"],
                        line={
                            "color": DISCRETE_COLOR_PALLETE[i],
                            "width": 2,
                            "shape": line_shape,
                            "dash": "dash",
                        },
                        legendgroup=f"cenario {cen}",
                        legendgrouptitle_text=f"cenario {cen}",
                        name=estudo,
                    )
                )
            next_color += 1

        dados_estudo = dados_twinx.loc[dados_twinx["estudo"] == estudo]
        if not dados_estudo.empty:
            dados_estudo = __add_final_date_line_to_df(dados_estudo)
            fig.add_trace(
                go.Scatter(
                    x=dados_estudo["dataInicio"],
                    y=dados_estudo["mean"],
                    line={
                        "color": DISCRETE_COLOR_PALLETE[next_color],
                        "width": 3,
                        "shape": line_shape,
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
                    y=dados_estudo["median"],
                    line={
                        "color": DISCRETE_COLOR_PALLETE[next_color],
                        "width": 3,
                        "dash": "dot",
                        "shape": line_shape,
                    },
                    name="median",
                    legendgroup=dados_twinx_legend,
                ),
                secondary_y=True,
            )
            fig.add_trace(
                go.Scatter(
                    x=dados_estudo["dataInicio"],
                    y=dados_estudo["p10"],
                    line_color=DISCRETE_COLOR_PALLETE_BACKGROUND[next_color],
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
                    line_color=DISCRETE_COLOR_PALLETE_BACKGROUND[next_color],
                    fillcolor=DISCRETE_COLOR_PALLETE_BACKGROUND[next_color],
                    line_shape=line_shape,
                    fill="tonexty",
                    name="p90",
                    legendgroup=dados_twinx_legend,
                    visible=visibilidade_p,
                ),
                secondary_y=True,
            )
            if filters.get("cenario"):
                cen = filters.get("cenario")
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo["dataInicio"],
                        y=dados_estudo["cenario"],
                        line={
                            "color": DISCRETE_COLOR_PALLETE[i],
                            "width": 2,
                            "shape": line_shape,
                            "dash": "dash",
                        },
                        legendgroup=f"cenario {cen}",
                        legendgrouptitle_text=f"cenario {cen}",
                        name=estudo,
                    ),
                    secondary_y=True,
                )
            next_color += 1

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
    operation_data, variable: str, filters
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
    estudos = dados["estudo"].unique().tolist()

    filtro_newave = dados["programa"] == "NEWAVE"
    filtro_decomp = dados["programa"] == "DECOMP"
    df_newave = dados.loc[filtro_newave]
    df_decomp = dados.loc[filtro_decomp]

    visibilidade_newave = __background_area_visibility(estudos)
    for i, estudo in enumerate(estudos):
        if df_decomp is not None:
            estudo_decomp = df_decomp.loc[df_decomp["estudo"] == estudo]
            if not estudo_decomp.empty:
                fig.add_trace(
                    go.Scatter(
                        x=estudo_decomp["dataInicio"],
                        y=estudo_decomp["mean"],
                        line={
                            "color": DISCRETE_COLOR_PALLETE[i],
                            "width": 3,
                        },
                        name=estudo,
                        legendgroup="DECOMP",
                        legendgrouptitle_text="DECOMP",
                    )
                )
        if df_newave is not None:
            estudo_newave = df_newave.loc[df_newave["estudo"] == estudo]
            if not estudo_newave.empty:
                fig.add_trace(
                    go.Scatter(
                        x=estudo_newave["dataInicio"],
                        y=estudo_newave["mean"],
                        line={
                            "color": DISCRETE_COLOR_PALLETE[i],
                            "dash": "dot",
                            "width": 2,
                        },
                        name=estudo,
                        legendgroup="NEWAVEm",
                        legendgrouptitle_text="NEWAVEm",
                        visible=visibilidade_newave,
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=estudo_newave["dataInicio"],
                        y=estudo_newave["p10"],
                        line_color=DISCRETE_COLOR_PALLETE_BACKGROUND[i],
                        legendgroup="NEWAVEp10",
                        legendgrouptitle_text="NEWAVEp10",
                        name=estudo,
                        visible=visibilidade_newave,
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=estudo_newave["dataInicio"],
                        y=estudo_newave["p90"],
                        line_color=DISCRETE_COLOR_PALLETE_BACKGROUND[i],
                        fillcolor=DISCRETE_COLOR_PALLETE_BACKGROUND[i],
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
    return fig


def generate_operation_graph_ppq(operation_data, variable, filters):
    graph_layout = go.Layout(
        plot_bgcolor="rgba(158, 149, 128, 0.2)",
        paper_bgcolor="rgba(255,255,255,1)",
    )
    fig = go.Figure()
    fig.update_layout(graph_layout)
    if operation_data is None:
        return fig
    dados = pd.read_json(operation_data, orient="split")
    estudos = dados["estudo"].unique().tolist()

    for i, estudo in enumerate(estudos):
        if dados is not None:
            dados_estudo = dados.loc[dados["estudo"] == estudo]
            if not dados_estudo.empty:
                dados_estudo = dados_estudo.sort_values("iteracao")
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo["iteracao"],
                        y=dados_estudo["mean"],
                        line={
                            "color": DISCRETE_COLOR_PALLETE[i],
                            "dash": "dot",
                            "width": 2,
                        },
                        name="mean",
                        legendgroup=estudo,
                        legendgrouptitle_text=estudo,
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo["iteracao"],
                        y=dados_estudo["mean"] - dados_estudo["std"],
                        line_color=DISCRETE_COLOR_PALLETE_BACKGROUND[i],
                        fillcolor=DISCRETE_COLOR_PALLETE_BACKGROUND[i],
                        legendgroup=estudo,
                        name="lower bound",
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo["iteracao"],
                        y=dados_estudo["mean"] + dados_estudo["std"],
                        line_color=DISCRETE_COLOR_PALLETE_BACKGROUND[i],
                        fill="tonexty",
                        legendgroup=estudo,
                        legendgrouptitle_text=estudo,
                        name="upper bound",
                    )
                )
                if filters.get("cenario"):
                    cen = filters.get("cenario")
                    fig.add_trace(
                        go.Scatter(
                            x=dados_estudo["iteracao"],
                            y=dados_estudo["cenario"],
                            line={
                                "color": DISCRETE_COLOR_PALLETE[i],
                                "width": 2,
                                "dash": "dash",
                            },
                            legendgroup=f"cenario {cen}",
                            legendgrouptitle_text=f"cenario {cen}",
                            name=estudo,
                        )
                    )

    if variable is not None:
        fig.update_layout(
            title=__make_operation_plot_title(variable, filters),
            xaxis_title="Iteracao",
            yaxis_title=VARIABLE_UNITS.get(variable.split("_")[0], ""),
            hovermode="x unified",
            legend=dict(groupclick="toggleitem"),
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
