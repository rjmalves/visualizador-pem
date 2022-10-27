import plotly.graph_objects as go
import pandas as pd

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

VARIABLE_LEGENDS = {
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
    "INT": "MWmed",
    "MER": "MWmed",
    "QAFL": "m3/s",
    "QDEF": "m3/s",
    "VAGUA": "R$ / hm3",
    "VARMI": "hm3",
    "VARMF": "hm3",
    "VARPI": "%",
    "VARPF": "%",
}


def generate_operation_graph_encadeador(operation_data, variable: str):
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

    visibilidade_newave = "legendonly" if len(estudos) > 2 else None
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
            xaxis_title="Data",
            yaxis_title=VARIABLE_LEGENDS.get(variable.split("_")[0], ""),
            hovermode="x unified",
            legend=dict(groupclick="toggleitem"),
        )
    return fig


def generate_operation_graph_casos(operation_data, variable):
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

    for i, estudo in enumerate(estudos):
        if dados is not None:
            dados_estudo = dados.loc[dados["estudo"] == estudo]
            if not dados_estudo.empty:
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo["dataInicio"],
                        y=dados_estudo["mean"],
                        line={
                            "color": DISCRETE_COLOR_PALLETE[i],
                            "width": 3,
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
                        legendgroup="p10",
                        legendgrouptitle_text="p10",
                        name=estudo,
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=dados_estudo["dataInicio"],
                        y=dados_estudo["p90"],
                        line_color=DISCRETE_COLOR_PALLETE_BACKGROUND[i],
                        fillcolor=DISCRETE_COLOR_PALLETE_BACKGROUND[i],
                        fill="tonexty",
                        legendgroup="p90",
                        legendgrouptitle_text="p90",
                        name=estudo,
                    )
                )

    if variable is not None:
        fig.update_layout(
            xaxis_title="Data",
            yaxis_title=VARIABLE_LEGENDS.get(variable.split("_")[0], ""),
            hovermode="x unified",
            legend=dict(groupclick="toggleitem"),
        )
    return fig
